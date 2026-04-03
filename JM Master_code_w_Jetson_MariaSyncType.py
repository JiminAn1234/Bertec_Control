from Header_BertecControl import BertecController
from Header_NexusControl import NexusController
from Header_JetsonControl import JetsonController
from time import sleep
import random
import time

def main():  
    subject_name = "AB01_Jimin"

    # model_name = "CSmodel"
    # model_name = "JMmodel"
    # model_name = "CSmodel2"
    model_name = "JMmodel3"

    condition_name = "LG_15p350ms"
    condition_name = "LG_25p100ms"
    condition_name = "LG_15p200ms"
    condition_name = "LG_15p100ms"
    condition_name = "LG_5p100ms"
    condition_name = "LG_15p400ms"
    condition_name = "LG_20p100ms"
    condition_name = "LG_15p250ms"
    condition_name = "LG_NoAssi"
    condition_name = "LG_15p150ms"
    condition_name = "LG_15p300ms"
    condition_name = "LG_15p50ms"
    condition_name = "LG_10p100ms"

    condition_name = "RA_15p300ms"
    condition_name = "RA_5p100ms"
    condition_name = "RA_15p150ms"
    condition_name = "RA_15p400ms"
    condition_name = "RA_25p100ms"
    condition_name = "RA_NoAssi"
    condition_name = "RA_15p50ms"
    condition_name = "RA_15p200ms"
    condition_name = "RA_20p100ms"
    condition_name = "RA_10p100ms"
    condition_name = "RA_15p350ms"
    condition_name = "RA_15p250ms"
    condition_name = "RA_15p100ms"

    condition_name = "RD_15p250ms"
    condition_name = "RD_15p100ms"
    condition_name = "RD_20p100ms"
    condition_name = "RD_15p50ms"
    condition_name = "RD_15p350ms"
    condition_name = "RD_5p100ms"
    condition_name = "RD_10p100ms"
    condition_name = "RD_15p400ms"
    condition_name = "RD_15p150ms"
    condition_name = "RD_25p100ms"
    condition_name = "RD_15p300ms"
    condition_name = "RD_NoAssi"
    condition_name = "RD_15p200ms"


    trial_start_sec = 5  # To reach steady state before starting the trial

    trial_notes = " "
    trial_description = " "

    # Create an instance of BertecControl
    Bertec = BertecController()
    res = Bertec.start_connection()
    command = 1
    trial_number = 0

    while(command):
        
        trial_number += 1
        trial_name = model_name + "-" + subject_name + "-" + condition_name + '-' + str(trial_number)
        print("\nTrial name: ", trial_name)

        # Connect Jetson
        Jetson = JetsonController("172.24.44.177", 10)
        Jetson.start_server()
        # Jetson.send_trial_info(trial_name, trial_start_sec, trial_duration_sec)

        # Port number should match with the port number in Nexus
        port_number = int(input("Input Port number:"))

        # Create Nexus instance
        packet_id= random.randint(0, 2**32 - 1) 
        Nexus = NexusController(name= trial_name, notes = trial_notes, description = trial_description, database_path = " ",
        delay_ms = 0, packet_id = packet_id, port = port_number)
        
        command = input("Input protocol number (exit for 0):")
        

        if (command == '1'):
            
            speed_1 = -0.8
            trial_duration_sec = 35
            target_duration_sec = 35
            
            sleep(9)

            print(f"\nTreadmill speed: {speed_1} m/s")
            params = {
                'leftVel': str(speed_1),                'leftAccel': '0.3',                'leftDecel': '0.3',
                'rightVel': str(speed_1),               'rightAccel': '0.3',               'rightDecel': '0.3'}
            res = Bertec.run_treadmill(params['leftVel'], params['leftAccel'], params['leftDecel'], params['rightVel'], params['rightAccel'], params['rightDecel'])
               
            # 1. Trigger Jetson
            Jetson.send_message("exo on")

            # Sleep until the steady state is reached
            sleep(trial_start_sec)

            #  In this case, we want the sleeping until the target duration starting time before the end. 
            sleep(trial_duration_sec - target_duration_sec)

            # 2. Trigger Nexus Capture
            Nexus.notify()
            
            sleep(target_duration_sec)
            # sleep(trial_duration_sec)

            # 2. Stop Treadmill
            print("\nTreadmill stop")
            params = {
                'leftVel': '0',                'leftAccel': '0.3',                'leftDecel': '0.3',
                'rightVel': '0',               'rightAccel': '0.3',               'rightDecel': '0.3'}
            res = Bertec.run_treadmill(params['leftVel'], params['leftAccel'], params['leftDecel'], params['rightVel'], params['rightAccel'], params['rightDecel'])
        

        elif (command == '2'): # FOR RAMP Ascent

            speed_1 = 0.8 # For Ramp Ascent
            # speed_1 = -0.8 # For Ramp Descent

            trial_duration_sec = 35
            target_duration_sec = 35
            
            sleep(10)

            print(f"\nTreadmill speed: {speed_1} m/s")
            params = {
                'leftVel': str(speed_1),                'leftAccel': '0.3',                'leftDecel': '0.3',
                'rightVel': str(speed_1),               'rightAccel': '0.3',               'rightDecel': '0.3'}
            res = Bertec.run_treadmill(params['leftVel'], params['leftAccel'], params['leftDecel'], params['rightVel'], params['rightAccel'], params['rightDecel'])
               
            # 1. Trigger Jetson
            Jetson.send_message("exo on")

            # Sleep until the steady state is reached
            sleep(trial_start_sec)

            #  In this case, we want the sleeping until the target duration starting time before the end. 
            sleep(trial_duration_sec - target_duration_sec)

            # 2. Trigger Nexus Capture
            Nexus.notify()
            
            sleep(target_duration_sec)

            # 2. Stop Treadmill
            print("\nTreadmill stop")
            params = {
                'leftVel': '0',                'leftAccel': '0.3',                'leftDecel': '0.3',
                'rightVel': '0',               'rightAccel': '0.3',               'rightDecel': '0.3'}
            res = Bertec.run_treadmill(params['leftVel'], params['leftAccel'], params['leftDecel'], params['rightVel'], params['rightAccel'], params['rightDecel'])



        elif (command == '6'):
            print("Using get_force_data")
            res = Bertec.get_force_data()
        elif (command == '0'):
            print("Exiting program")
            Bertec.stop_connection()
            command = 0


    Bertec.stop_connection()
    Nexus.close_socket()

if __name__ == "__main__":
    main()