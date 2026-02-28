import os
import yaml
import importlib.util
from pubsub import pub

class ModuleLoader:
    def __init__(self, config_folder='modules', environment=None):
        """
        ModuleLoader class
        :param config_folder: root folder to search for module config.yml files (searched recursively)
        :param environment: name of the environment to load (e.g. 'archie', 'laptop', 'server').
            Must match a YAML file in <config_folder>/environments/<environment>.yml.

        Each module lives in its own directory containing:
          - <module>.py   (Python implementation, filename matches directory name)
          - config.yml    (generic module configuration with 'class' key for the Python class name)
          - README.md     (documentation)
          - tests/        (unit tests)

        Which modules are enabled, and any device-specific configuration overrides, are
        controlled by a per-environment file:
          <config_folder>/environments/<environment>.yml

        Example environment file (modules/environments/archie.yml):
        ---
        messaging_service:
            enabled: true
        logwrapper:
            enabled: true
        gpio_motion:
            enabled: true
            config:            # merged over the module's generic config
                pin: 9
        bus_servo:
            enabled: true
            instances:         # replaces the module's instances list
              - name: leg_r_tilt
                id: 1
                range: [2511, 3944]

        Example module config.yml (modules/gpio/motion/config.yml):
        ---
        gpio_motion:
            class: Motion      # Python class name (required)
            config:            # generic defaults (device-specific values go in environment file)
                test_on_boot: false

        Example:
        loader = ModuleLoader(environment='archie')
        modules = loader.load_modules()

        Reference module once loaded:
        translator_inst = modules['Translator']
        """
        self.config_folder = config_folder
        self.environment = environment or 'archie'
        print(f"[ModuleLoader] Loading modules for environment: {self.environment}")
        self.modules = self.load_yaml_files()

    def _load_environment_config(self):
        """Load the environment YAML file to determine which modules are active and their overrides."""
        env_file = os.path.join(self.config_folder, 'environments', f'{self.environment}.yml')
        if not os.path.exists(env_file):
            print(f"[ModuleLoader] Warning: environment file not found: {env_file}")
            return {}
        with open(env_file, 'r') as f:
            try:
                return yaml.safe_load(f) or {}
            except yaml.YAMLError as e:
                print(f"Error loading {env_file}: {e}")
                return {}

    def load_yaml_files(self):
        """Recursively search config_folder for config.yml files and load enabled module configurations."""
        env_config = self._load_environment_config()

        config_files = []
        for root, dirs, files in os.walk(self.config_folder):
            # Skip the environments subdirectory — those are not module config files
            dirs[:] = [d for d in dirs if d != 'environments']
            for f in files:
                if f == 'config.yml':
                    config_files.append(os.path.join(root, f))

        loaded_modules = []
        for file_path in config_files:
            with open(file_path, 'r') as stream:
                try:
                    config = yaml.safe_load(stream)
                    for module_name, module_config in config.items():
                        # Check if this module is enabled in the environment file
                        env_entry = env_config.get(module_name, {})
                        if not env_entry.get('enabled', False):
                            continue
                        print(f"[ModuleLoader] Loading module: {module_name}")

                        # Merge environment config overrides into module config (shallow merge)
                        env_config_override = env_entry.get('config', {})
                        if env_config_override:
                            module_config['config'] = {**(module_config.get('config') or {}), **env_config_override}

                        # Environment can also supply/override the instances list
                        if 'instances' in env_entry:
                            module_config['instances'] = env_entry['instances']

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
