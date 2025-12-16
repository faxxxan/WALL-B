# ModuleLoader Documentation

## Overview

The `ModuleLoader` class is responsible for dynamically loading and instantiating modules in the project based on YAML configuration files. It supports environment-based filtering, allowing selective loading of modules depending on the specified environment (e.g., 'robot', 'dev'). This approach enables modular, configurable, and environment-aware system composition.

## Key Features

1. **Dynamic Module Loading**: Loads Python modules and classes at runtime using paths specified in YAML config files.
2. **Environment Filtering**: Only loads modules enabled for the current environment, supporting both string and list-based environment fields.
3. **Configurable Instantiation**: Passes configuration parameters from YAML directly to module constructors via `**kwargs`.
4. **Messaging Service Integration**: Optionally injects a messaging service into loaded modules for inter-module communication.
5. **Multiple Instances**: Supports creating multiple instances of a module with different configurations.

## Configuration File Example

A typical module configuration file (e.g., `config/buzzer.yml`):

```yaml
buzzer:
  enabled: true
  path: "modules.audio.buzzer.Buzzer"
  config:
    pin: 27
    name: 'buzzer'
  environment: ['robot', 'dev']  # Optional: restricts loading to these environments
```

## Class Reference

### `ModuleLoader.__init__(config_folder='config', environment=None)`
- **config_folder**: Directory containing YAML config files for modules.
- **environment**: The current environment (string). Only modules matching this environment are loaded. Defaults to 'robot' if not specified.

### `load_yaml_files()`
- Scans the config folder for `.yml` files.
- Loads and parses each YAML file.
- For each module config:
  - Skips if `enabled` is not `true`.
  - If `environment` is specified, only includes the module if the current environment matches (supports string or list).
- Returns a list of enabled module configs for the current environment.

### `load_modules()`
- Iterates over the filtered module configs.
- Dynamically loads the specified Python class using the `path` field.
- Instantiates each module, passing config as `**kwargs`.
- Supports multiple instances per module if the `instances` field is present.
- Returns a dictionary of module instances, keyed by a combination of class and instance name.

### `set_messaging_service(module_instances, messaging_service)`
- Injects a messaging service into all loaded modules (except those named 'MessagingService').
- Sets the `messaging_service` attribute on each module instance.

## Environment Filtering Logic

- If a module config includes an `environment` field:
  - If it is a string, the module is loaded only if it matches the current environment.
  - If it is a list, the module is loaded if the current environment is in the list.
  - If not present, the module is loaded for all environments.

## Example: Environment Filtering

Given the following config:

```yaml
example_module:
  enabled: true
  path: modules.example.ExampleModule
  environment: 'dev'
```

### Usage Example

```bash
./startup.sh dev
./startup.sh # defaults to 'robot' environment
```