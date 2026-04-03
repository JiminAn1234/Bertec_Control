from Header_BertecControl import BertecController
from Header_NexusControl import NexusController
from Header_JetsonControl import JetsonController
from time import sleep
import random
import time

def main():  
    # subject_name = "AB01_Jimin"
    subject_name = "AB02_Rajiv"
    # subject_name = "AB03_Amy"
    # subject_name = "AB04_Changseob"
    # subject_name = "AB05_Maria"
    # subject_name = "AB07_Leo"
    # subject_name = "AB08_Adrian"
    # subject_name = "AB11_Ryan"
    # subject_name = "AB13_Hridayam"
    # subject_name = "AB15_Daniel"
    # subject_name = "AB16_Ilseung"
    # subject_name = "AB17_Jinwoo"  


    # model_name = "IMUOnly_fixed"
    # model_name = "IMUOnly_fixed_DEP"
    model_name = "IMUOnly_fixed_SemiDEP"

    task = "LG"; speed_1 = 1.2
    task = "RA"; speed_1 = 0.8
    task = "RD"; speed_1 = -0.8

    speed = "1p2mps"
    speed = "0p8mps"
    
    # speed = "0p2mps"
    # speed = "0p4mps"
    # speed = "0p6mps"
    # speed = "0p8mps"
    # speed = "1p0mps"
    # speed = "1p2mps"
    # speed = "1p4mps"

    # speed_1 = 1.2

    condition_name = task + speed

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

        # Port number should match with the port number in Nexus
        port_number = int(input("Input Port number:"))

        # Create Nexus instance
        packet_id= random.randint(0, 2**32 - 1) 
        Nexus = NexusController(name= trial_name, notes = trial_notes, description = trial_description, database_path = " ",
        delay_ms = 0, packet_id = packet_id, port = port_number)
        
        command = input("Input protocol number (exit for 0):")
        
        if (command == '1'):
            # speed_1 = 0.6
            trial_duration_sec = 65
            target_duration_sec = 35 # This should match with the Vicon's "stop after duration"
            
            # sleep(9) # In case of one person operation, give some time to get up on the treadmill

            print(f"\nTreadmill speed: {speed_1} m/s")
            params = {
                'leftVel': str(speed_1),                'leftAccel': '0.2',               'leftDecel': '0.2',
                'rightVel': str(speed_1),               'rightAccel': '0.2',              'rightDecel': '0.2'}
            res = Bertec.run_treadmill(params['leftVel'], params['leftAccel'], params['leftDecel'], params['rightVel'], params['rightAccel'], params['rightDecel'])
               
            # 1. Trigger Jetson
            Jetson.send_message("exo on")

            sleep(trial_start_sec)             # Sleep until the steady state is reached

            #  In this case, we want the sleeping until the target duration starting time before the end. 
            sleep(trial_duration_sec - target_duration_sec)

            # 2. Trigger Nexus Capture
            Nexus.notify()
            
            sleep(target_duration_sec)
            
            # additional time for exo off before treadmill stops
            sleep(2)
            
            # 2. Stop Treadmill
            print("\nTreadmill stop")
            params = {
                'leftVel': '0',                'leftAccel': '0.2',                'leftDecel': '0.2',
                'rightVel': '0',               'rightAccel': '0.2',               'rightDecel': '0.2'}
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