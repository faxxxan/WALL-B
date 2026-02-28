import os, sys
import signal
from modules.config import Config
from module_loader import ModuleLoader

def main():
    print('Starting...')
    # Throw exception to safely exit script when terminated
    signal.signal(signal.SIGTERM, Config.exit)

    # Get environment argument (default to 'robot') using argparse
    import argparse
    parser = argparse.ArgumentParser(description="Modular Biped Main Script")
    parser.add_argument('--env', default='archie', help="Set the environment (e.g. archie, buddy, cody, server, laptop)")
    args = parser.parse_args()
    env = args.env

    # Dynamically load and initialize modules, passing env
    loader = ModuleLoader(config_folder="modules", environment=env)
    module_instances = loader.load_modules()

    # Inject messaging service and all module-to-module dependencies declared in the
    # environment YAML file (inject: / on_inject: blocks).
    loader.inject_dependencies(module_instances)

    # Use the new SystemLoop class to run the main loop
    from system_loop import SystemLoop
    system_loop = SystemLoop(module_instances['MessagingService'].messaging_service, module_instances.get('Personality'))
    system_loop.start()

if __name__ == '__main__':
    main()
