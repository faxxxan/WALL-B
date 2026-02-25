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
          - <module>.py   (Python implementation)
          - config.yml    (module configuration)
          - README.md     (documentation)
          - tests/        (unit tests)
        
        Example config.yml:
        ---
        buzzer:
            enabled: true # Required
            path: "modules.audio.buzzer.buzzer.Buzzer" # Required
            config: # Passed as **kwargs to the module's __init__ method
                pin: 27
                name: 'buzzer'
        
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

    def load_yaml_files(self):
        """Recursively search config_folder for config.yml files and load module configurations."""
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
                        if not module_config.get('enabled', False):
                            continue
                        # If 'environment' is specified, filter by self.environment
                        env_field = module_config.get('environment')
                        print(f"[ModuleLoader] Found module: {module_name} with environment filter: {env_field}")
                        if env_field is not None:
                            if isinstance(env_field, str):
                                if env_field != self.environment:
                                    continue
                            elif isinstance(env_field, list):
                                if self.environment not in env_field:
                                    continue
                        loaded_modules.append(module_config)
                except yaml.YAMLError as e:
                    print(f"Error loading {file_path}: {e}")
        return loaded_modules

    def set_messaging_service(self, module_instances, messaging_service):
        """Set the messaging service for the modules."""
        # Iterate through the module instances, extract name and module
        for name, module in module_instances.items():
            # get module name from object
            # if module is not messaging_service:
            if 'MessagingService' in name:
                continue
            module.messaging_service = messaging_service

    def load_modules(self):
        """Dynamically load and instantiate the modules based on the config."""
        instances = {}  # Use a dictionary to store instances for easy access
        for module in self.modules:
            print(f"Enabling {module['path']}")
            module_path = module['path'].rsplit('.', 1)[0].replace('.', '/')
            module_name = module['path'].split('.')[-1]
            instances_config = module.get('instances', [module.get('config')])
            shared_config = module.get('config', {})
            if instances_config[0] is None:
                instances_config = [{}]

            # Dynamically load the module
            spec = importlib.util.spec_from_file_location(module_name, f"{module_path}.py")
            mod = importlib.util.module_from_spec(spec)
            try:
                spec.loader.exec_module(mod)
            except Exception as e:
                print(f"Error loading module {module_name}: {e}")

            # If multiple instances, pass shared config to each instance
            multiple_instances = 'instances' in module and isinstance(module['instances'], list) and len(module['instances']) > 0
            for instance_config in instances_config:
                # Merge shared config if multiple instances
                if multiple_instances:
                    # Avoid overwriting instance-specific keys with shared config
                    merged_config = {**shared_config, **instance_config}
                else:
                    merged_config = instance_config
                instance_name = module_name + '_' + instance_config.get('name') if instance_config.get('name') is not None else module_name
                instance = getattr(mod, module_name)(**merged_config)
                instances[instance_name] = instance

        print("All modules loaded")
        return instances
