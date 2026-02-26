import os
import yaml
import importlib.util
from pubsub import pub

class ModuleLoader:
    def __init__(self, config_folder='modules', environment=None):
        """
        ModuleLoader class
        :param config_folder: root folder to search for module config.yml files (searched recursively)

        Each module lives in its own directory containing:
          - <module>.py   (Python implementation, filename matches directory name)
          - config.yml    (module configuration with 'class' key for the Python class name)
          - README.md     (documentation)
          - tests/        (unit tests)

        Which modules are enabled is controlled by a single file:
          <config_folder>/enabled.yml

        Example module config.yml:
        ---
        buzzer:
            class: Buzzer  # Python class name (required)
            config:        # Passed as **kwargs to __init__ (optional)
                pin: 27
                name: 'buzzer'

        Example enabled.yml:
        ---
        buzzer:
            enabled: true
        messaging_service:
            enabled: true

        Example:
        loader = ModuleLoader()
        modules = loader.load_modules()

        Reference module once loaded:
        translator_inst = modules['Translator']
        """
        self.config_folder = config_folder
        self.environment = environment or 'robot'
        print(f"[ModuleLoader] Loading modules for environment: {self.environment}")
        self.modules = self.load_yaml_files()

    def _load_enabled_config(self):
        """Load enabled.yml from the config folder to determine which modules are active."""
        enabled_file = os.path.join(self.config_folder, 'enabled.yml')
        if not os.path.exists(enabled_file):
            return {}
        with open(enabled_file, 'r') as f:
            try:
                return yaml.safe_load(f) or {}
            except yaml.YAMLError as e:
                print(f"Error loading {enabled_file}: {e}")
                return {}

    def load_yaml_files(self):
        """Recursively search config_folder for config.yml files and load enabled module configurations."""
        enabled = self._load_enabled_config()

        config_files = []
        for root, dirs, files in os.walk(self.config_folder):
            for f in files:
                if f == 'config.yml':
                    config_files.append(os.path.join(root, f))

        loaded_modules = []
        for file_path in config_files:
            with open(file_path, 'r') as stream:
                try:
                    config = yaml.safe_load(stream)
                    for module_name, module_config in config.items():
                        # Enabled status and environment come from enabled.yml
                        enabled_entry = enabled.get(module_name, {})
                        if not enabled_entry.get('enabled', False):
                            continue
                        env_field = enabled_entry.get('environment')
                        print(f"[ModuleLoader] Found module: {module_name} with environment filter: {env_field}")
                        if env_field is not None:
                            if isinstance(env_field, str):
                                if env_field != self.environment:
                                    continue
                            elif isinstance(env_field, list):
                                if self.environment not in env_field:
                                    continue
                        # Infer the Python file path from the config.yml directory
                        dir_path = os.path.dirname(file_path)
                        dir_name = os.path.basename(dir_path)
                        module_config['_py_file'] = os.path.join(dir_path, f"{dir_name}.py")
                        module_config['_class'] = module_config.get('class')
                        loaded_modules.append(module_config)
                except yaml.YAMLError as e:
                    print(f"Error loading {file_path}: {e}")
        return loaded_modules

    def set_messaging_service(self, module_instances, messaging_service):
        """Set the messaging service for the modules."""
        for name, module in module_instances.items():
            if 'MessagingService' in name:
                continue
            module.messaging_service = messaging_service

    def load_modules(self):
        """Dynamically load and instantiate the modules based on the config."""
        instances = {}  # Use a dictionary to store instances for easy access
        for module in self.modules:
            py_file = module['_py_file']
            class_name = module['_class']
            print(f"Enabling {class_name} from {py_file}")
            instances_config = module.get('instances', [module.get('config')])
            shared_config = module.get('config', {})
            if instances_config[0] is None:
                instances_config = [{}]

            # Dynamically load the module from its inferred file path
            spec = importlib.util.spec_from_file_location(class_name, py_file)
            mod = importlib.util.module_from_spec(spec)
            try:
                spec.loader.exec_module(mod)
            except Exception as e:
                print(f"Error loading module {class_name}: {e}")

            # If multiple instances, merge shared config into each instance config
            multiple_instances = 'instances' in module and isinstance(module['instances'], list) and len(module['instances']) > 0
            for instance_config in instances_config:
                if multiple_instances:
                    # Avoid overwriting instance-specific keys with shared config
                    merged_config = {**shared_config, **instance_config}
                else:
                    merged_config = instance_config
                instance_name = class_name + '_' + instance_config.get('name') if instance_config.get('name') is not None else class_name
                instance = getattr(mod, class_name)(**merged_config)
                instances[instance_name] = instance

        print("All modules loaded")
        return instances
