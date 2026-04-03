# Drafted by Changseob Song, 11/1/2024
# This is an example code to trigger starts of Vicon Nexus and Bertec FIT5

from Header_BertecControl import BertecController
from Header_NexusControl import NexusController
from Header_JetsonControl import JetsonController
from time import sleep
import random
import time

def main():  
    subject_name = "AB01_Jimin"
    # subject_name = "AB11_Ryan"
    # subject_name = "AB05_Maria"
    # subject_name = "AB04_Changseob"

    # condition_name = "Exo_Scale0"
    # condition_name = "Exo_Scale10"
    # condition_name = "Exo_Scale15"
    # condition_name = "Exo_Scale20"

    # condition_name = "15p_0ms"
    # condition_name = "15p_100ms"
    # condition_name = "15p_200ms"
    # condition_name = "15p_300ms"
    # condition_name = "15p_400ms"
    # condition_name = "15p_500ms"

    # condition_name = "15p_50ms"
    # condition_name = "15p_150ms"
    # condition_name = "15p_250ms"
    # condition_name = "15p_350ms"
    condition_name = "15p_450ms"    

    trial_start_sec = 5  # To reach steady state before starting the trial
    trial_duration_sec = 30

    trial_notes = " "
    trial_description = " "

    # Create an instance of BertecControl
    Bertec = BertecController()
    res = Bertec.start_connection()
    command = 1
    trial_number = 0
    while(command):
        
        trial_number += 1
        trial_name = subject_name + "-" + condition_name + '-' + str(trial_number)
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
            
            speed_1 = 1.2
            trial_duration_sec = 30
            target_duration_sec = 30
            
            sleep(10)
            print(f"\nTreadmill speed: {speed_1} m/s")
            params = {
                'leftVel': str(speed_1),                'leftAccel': '0.2',                'leftDecel': '0.5',
                'rightVel': str(speed_1),               'rightAccel': '0.2',               'rightDecel': '0.5'}
            res = Bertec.run_treadmill(params['leftVel'], params['leftAccel'], params['leftDecel'], params['rightVel'], params['rightAccel'], params['rightDecel'])
               
            # 1. Trigger Jetson
            Jetson.send_message("exo on")

            # Sleep until the steady state is reached
            sleep(trial_start_sec)

            # # Sleep until target duration starting time
            # sleep(trial_duration_sec - target_duration_sec)

            #  In this case, we want the sleeping until the target duration starting time before the end. 
            sleep(trial_duration_sec - target_duration_sec)

            # 2. Trigger Nexus Capture
            Nexus.notify()
            
            sleep(target_duration_sec)
            # sleep(trial_duration_sec)

            # 2. Stop Treadmill
            print("\nTreadmill stop")
            params = {
                'leftVel': '0',                'leftAccel': '0.5',                'leftDecel': '0.2',
                'rightVel': '0',               'rightAccel': '0.5',               'rightDecel': '0.2'}
            res = Bertec.run_treadmill(params['leftVel'], params['leftAccel'], params['leftDecel'], params['rightVel'], params['rightAccel'], params['rightDecel'])
        

        elif (command == '4'):

            speed_1 = 1.5
            accel_1 = 0.1
            print(f"\nTreadmill speed: {speed_1} m/s")
            params = {
                'leftVel': str(speed_1),                'leftAccel': str(accel_1),                'leftDecel': str(accel_1),
                'rightVel': str(speed_1),               'rightAccel': str(accel_1),               'rightDecel': str(accel_1)}
            res = Bertec.run_treadmill(params['leftVel'], params['leftAccel'], params['leftDecel'], params['rightVel'], params['rightAccel'], params['rightDecel'])

            # 1. Trigger Jetson
            Jetson.trigger_jetson("exo on")

            # 2. Trigger Nexus Capture
            Nexus.notify()
            
            sleep(15)

            #Jetson.trigger_jetson("exo off")


            # 2. Stop Treadmill
            speed_2 = 0
            print(f"\nTreadmill speed: {speed_2} m/s")
            params = {
                'leftVel': str(speed_2),                'leftAccel': str(accel_1),                'leftDecel': str(accel_1),
                'rightVel': str(speed_2),               'rightAccel':str(accel_1),               'rightDecel': str(accel_1)}
            res = Bertec.run_treadmill(params['leftVel'], params['leftAccel'], params['leftDecel'], params['rightVel'], params['rightAccel'], params['rightDecel'])

            sleep(15) 

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