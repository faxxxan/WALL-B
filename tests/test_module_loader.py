
import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import os
# Mock pubsub before importing module_loader
import types
sys.modules['pubsub'] = types.ModuleType('pubsub')
sys.modules['pubsub'].pub = MagicMock()
from module_loader import ModuleLoader

# Add parent directory to path to import module_loader
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))




class TestModuleLoader(unittest.TestCase):
    """Test cases for ModuleLoader class"""

    def setUp(self):
        self.patcher_os_walk = patch('os.walk')
        self.patcher_open = patch('builtins.open', create=True)
        self.patcher_yaml = patch('yaml.safe_load')
        self.patcher_importlib_spec = patch('importlib.util.spec_from_file_location')
        self.patcher_importlib_mod = patch('importlib.util.module_from_spec')
        self.mock_walk = self.patcher_os_walk.start()
        self.mock_open = self.patcher_open.start()
        self.mock_yaml = self.patcher_yaml.start()
        self.mock_spec = self.patcher_importlib_spec.start()
        self.mock_mod = self.patcher_importlib_mod.start()

    def tearDown(self):
        patch.stopall()

    def _setup_module_config(self, enabled=True, env=None, name='TestModule', path='modules.test.TestModule', config=None, instances=None):
        module_config = {
            'enabled': enabled,
            'path': path,
            'config': config or {'name': name},
        }
        if env is not None:
            module_config['environment'] = env
        if instances is not None:
            module_config['instances'] = instances
        return {'test_module': module_config}

    def test_initialization_default_env(self):
        # Should default to 'robot' environment
        self.mock_walk.return_value = []
        from module_loader import ModuleLoader
        loader = ModuleLoader(config_folder='config')
        self.assertEqual(loader.environment, 'robot')

    def test_load_yaml_files_enabled_and_env_string(self):
        # Only enabled modules with matching env are loaded
        self.mock_walk.return_value = [('modules/test', [], ['config.yml'])]
        mock_file = MagicMock()
        self.mock_open.return_value.__enter__.return_value = mock_file
        self.mock_yaml.return_value = self._setup_module_config(enabled=True, env='robot')
        from module_loader import ModuleLoader
        loader = ModuleLoader(config_folder='modules', environment='robot')
        modules = loader.load_yaml_files()
        self.assertEqual(len(modules), 1)
        # Should skip if env does not match
        self.mock_yaml.return_value = self._setup_module_config(enabled=True, env='dev')
        loader = ModuleLoader(config_folder='modules', environment='robot')
        modules = loader.load_yaml_files()
        self.assertEqual(len(modules), 0)

    def test_load_yaml_files_env_list(self):
        self.mock_walk.return_value = [('modules/test', [], ['config.yml'])]
        mock_file = MagicMock()
        self.mock_open.return_value.__enter__.return_value = mock_file
        self.mock_yaml.return_value = self._setup_module_config(enabled=True, env=['robot', 'dev'])
        from module_loader import ModuleLoader
        loader = ModuleLoader(config_folder='modules', environment='robot')
        modules = loader.load_yaml_files()
        self.assertEqual(len(modules), 1)
        loader = ModuleLoader(config_folder='modules', environment='other')
        modules = loader.load_yaml_files()
        self.assertEqual(len(modules), 0)

    def test_load_yaml_files_disabled(self):
        self.mock_walk.return_value = [('modules/test', [], ['config.yml'])]
        mock_file = MagicMock()
        self.mock_open.return_value.__enter__.return_value = mock_file
        self.mock_yaml.return_value = self._setup_module_config(enabled=False)
        from module_loader import ModuleLoader
        loader = ModuleLoader(config_folder='modules', environment='robot')
        modules = loader.load_yaml_files()
        self.assertEqual(len(modules), 0)

    def test_load_yaml_files_yaml_error(self):
        import yaml
        self.mock_walk.return_value = [('modules/test', [], ['config.yml'])]
        mock_file = MagicMock()
        self.mock_open.return_value.__enter__.return_value = mock_file
        self.mock_yaml.side_effect = yaml.YAMLError('YAML error')
        from module_loader import ModuleLoader
        loader = ModuleLoader(config_folder='modules', environment='robot')
        # Should not raise, just print error
        modules = loader.load_yaml_files()
        self.assertEqual(modules, [])
        self.mock_yaml.side_effect = None

    def test_load_modules_success_and_instance_naming(self):
        # Setup for dynamic loading
        self.mock_walk.return_value = [('modules/test', [], ['config.yml'])]
        mock_file = MagicMock()
        self.mock_open.return_value.__enter__.return_value = mock_file
        # One module, with two instances
        instances = [
            {'name': 'foo', 'param': 1},
            {'name': 'bar', 'param': 2}
        ]
        self.mock_yaml.return_value = self._setup_module_config(enabled=True, instances=instances)
        # Mock importlib
        mock_spec = MagicMock()
        self.mock_spec.return_value = mock_spec
        mock_mod = MagicMock()
        self.mock_mod.return_value = mock_mod
        # The class to instantiate
        class Dummy:
            def __init__(self, **kwargs):
                self.kwargs = kwargs
        setattr(mock_mod, 'TestModule', Dummy)
        mock_spec.loader.exec_module.side_effect = lambda mod: mod.__setattr__('TestModule', Dummy)
        from module_loader import ModuleLoader
        loader = ModuleLoader(config_folder='modules', environment='robot')
        loader.modules = loader.load_yaml_files()
        # Patch module_from_spec to return our mock_mod
        self.mock_mod.return_value = mock_mod
        self.mock_mod.side_effect = lambda spec: mock_mod
        # Actually test load_modules
        with patch('importlib.util.module_from_spec', return_value=mock_mod):
            instances_dict = loader.load_modules()
        self.assertIn('TestModule_foo', instances_dict)
        self.assertIn('TestModule_bar', instances_dict)
        self.assertIsInstance(instances_dict['TestModule_foo'], Dummy)
        self.assertEqual(instances_dict['TestModule_foo'].kwargs['name'], 'foo')

    def test_load_modules_no_config(self):
        self.mock_walk.return_value = [('modules/test', [], ['config.yml'])]
        mock_file = MagicMock()
        self.mock_open.return_value.__enter__.return_value = mock_file
        # config is None
        self.mock_yaml.return_value = self._setup_module_config(enabled=True, config=None)
        mock_spec = MagicMock()
        self.mock_spec.return_value = mock_spec
        mock_mod = MagicMock()
        class Dummy:
            def __init__(self, **kwargs):
                self.kwargs = kwargs
        setattr(mock_mod, 'TestModule', Dummy)
        mock_spec.loader.exec_module.side_effect = lambda mod: mod.__setattr__('TestModule', Dummy)
        from module_loader import ModuleLoader
        loader = ModuleLoader(config_folder='modules', environment='robot')
        loader.modules = loader.load_yaml_files()
        with patch('importlib.util.module_from_spec', return_value=mock_mod):
            instances_dict = loader.load_modules()
        # When config is None, instance_name becomes 'TestModule_TestModule' (module_name + '_' + None)
        self.assertIn('TestModule_TestModule', instances_dict)
        self.assertIsInstance(instances_dict['TestModule_TestModule'], Dummy)

    def test_load_modules_import_error(self):
        self.mock_walk.return_value = [('modules/test', [], ['config.yml'])]
        mock_file = MagicMock()
        self.mock_open.return_value.__enter__.return_value = mock_file
        self.mock_yaml.return_value = self._setup_module_config(enabled=True)
        mock_spec = MagicMock()
        self.mock_spec.return_value = mock_spec
        mock_mod = MagicMock()
        setattr(mock_mod, 'TestModule', lambda **kwargs: None)
        # Simulate import error
        def raise_import(mod):
            raise Exception('Import error')
        mock_spec.loader.exec_module.side_effect = raise_import
        from module_loader import ModuleLoader
        loader = ModuleLoader(config_folder='modules', environment='robot')
        loader.modules = loader.load_yaml_files()
        with patch('importlib.util.module_from_spec', return_value=mock_mod):
            # Should not raise, just print error
            instances_dict = loader.load_modules()
        self.assertIsInstance(instances_dict, dict)

    def test_set_messaging_service(self):
        from module_loader import ModuleLoader
        class Dummy:
            def __init__(self):
                self.messaging_service = None
        modules = {
            'TestModule': Dummy(),
            'MessagingService': Dummy()
        }
        ms = object()
        ModuleLoader().set_messaging_service(modules, ms)
        self.assertIs(modules['TestModule'].messaging_service, ms)
        # MessagingService should not be set
        self.assertIsNot(modules['MessagingService'].messaging_service, ms)


if __name__ == '__main__':
    unittest.main()