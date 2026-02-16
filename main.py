import os, sys
from time import sleep, time
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
    parser.add_argument('--env', default='robot', help="Set the environment (default: robot)")
    args = parser.parse_args()
    env = args.env

    # Dynamically load and initialize modules, passing env
    loader = ModuleLoader(config_folder="config", environment=env)
    module_instances = loader.load_modules()

    # Set messaging service for all modules
    messaging_service = module_instances['MessagingService'].messaging_service
    loader.set_messaging_service(module_instances, messaging_service)

    # Add your business logic here using module_instances as needed
    # Example: module_instances[0].some_method()
    # vision = module_instances['vision']
    
    
    # Inject bno055 modules into personality if both are enabled
    # ['ControllerHandler', 'WaveshareOLED', 'MessagingService', 'TFTDisplayEye', 'InputRecorder', 'Laser', 'Personality', 'Motion', 'PiTemperature', 'XboxController', 'TelegramBot', 'Animate', 'LogWrapper', 'BNO055_imu_head', 'BNO055_imu_body', 'Vision', 'TTSModule', 'Servo_leg_r_tilt', 'Servo_leg_r_hip', 'Servo_leg_r_knee', 'Servo_leg_r_ankle', 'Servo_neck_pan', 'Servo_neck_tilt', 'Servo_neck_tilt2', 'Servo_leg_l_tilt', 'Servo_leg_l_hip', 'Servo_leg_l_knee', 'Servo_leg_l_ankle', 'ChatGPT'])
    if 'Personality' in module_instances and 'BNO055_imu_head' and 'BNO055_imu_body' in module_instances:
        personality = module_instances['Personality']
        BNO055_imu_head = module_instances['BNO055_imu_head']
        personality.imu['head'] = BNO055_imu_head
        BNO055_imu_body = module_instances['BNO055_imu_body']
        personality.imu['body'] = BNO055_imu_body
        # Store all servo modules in personality for easy access within Personality.servos
        for key, module in module_instances.items():
            if key.startswith('Servo_'):
                personality.servos[key] = module        
        
    
    
    ## output all module instance keys for reference
    print(module_instances.keys())
    # dict_keys(['ArduinoSerial', 'NeoPx', 'BrailleSpeak', 'Animate', 'Vision', 'PiTemperature', 'Servo_leg_l_hip', 'Servo_leg_l_knee', 'Servo_leg_l_ankle', 'Servo_leg_r_hip', 'Servo_leg_r_knee', 'Servo_leg_r_ankle', 'Servo_tilt', 'Servo_pan', 'Translator', 'Tracking_tracking', 'Sensor', 'Buzzer_buzzer'])

    # Use animate to nod head
    # messaging_service.publish('animate', action='head_nod')
    # sleep(1)
    # messaging_service.publish('animate', action='head_shake')
    
    # Enable translator in log wrapper
    # log.translator = module_instances['Translator'] # Set the translator for the log wrapper

    # Use braillespeak to say hi
    # messaging_service.publish('speak', msg="Hi")
    
    # Play happy birthday with buzzer
    # messaging_service.publish('play', song="happy birthday") # Also available: 'merry christmas'
    
    # Check temperature of Raspberry Pi
    # messaging_service.subscribe('temperature', callback) # callback should accept 'value' as a parameter
    
    # Move pi servo
    # messaging_service.publish('piservo:move', angle=30)
    # messaging_service.publish('piservo:move', angle=-30)
    
    # Move servo
    # messaging_service.publish('servo:<identifier>:mv', percentage=50) # e.g. servo:pan:mv
    # messaging_service.publish('servo:<identifier>:mvabs', percentage=50) # Absolute position. e.g. servo:pan:mvabs

    # Test emotion analysis
    # messaging_service.publish('speech', text='I am so happy today!')
    
    # Test speech input
    # messaging_service.publish('speech:listen')
    
    # Inject controller into controller handler if both are enabled
    if 'ControllerHandler' in module_instances and 'XboxController' in module_instances:
        controller_handler = module_instances['ControllerHandler']
        xbox_controller = module_instances['XboxController']
        controller_handler.controller = xbox_controller
        controller_handler.start()
        
    # Use the new SystemLoop class to run the main loop
    from system_loop import SystemLoop
    system_loop = SystemLoop(messaging_service)
    system_loop.start()

if __name__ == '__main__':
    main()
