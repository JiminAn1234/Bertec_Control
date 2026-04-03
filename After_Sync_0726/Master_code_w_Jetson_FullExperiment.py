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
    # subject_name = "AB02_Rajiv"
    # subject_name = "AB12_Ray"

    task = "LG"
    # task = "RA"
    # task = "RD"

    # magnitude = "0p"
    # magnitude = "5p"
    # magnitude = "10p"
    magnitude = "15p"
    # magnitude = "20p"

    delay = "0ms"
    # delay = "100ms"
    # delay = "200ms"
    # delay = "300ms"
    # delay = "400ms"

    trial_start_sec = 0
    trial_duration_sec = 120

    trial_notes = " "
    trial_description = " "

    # Create an instance of BertecControl
    Bertec = BertecController()
    res = Bertec.start_connection()
    command = 1
    trial_number = 16
    while(command):
        
        trial_number += 1
        trial_name = f"{subject_name}_{task}_{magnitude}_{delay}_{trial_number}"
        print("\nTrial name: ", trial_name)

        # Connect Jetson
        # Jetson = JetsonController("172.24.44.177", 10)
        # Jetson.start_server()
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

            sleep(10)
            
            print(f"\nTreadmill speed: {speed_1} m/s")
            params = {
                'leftVel': str(speed_1),                'leftAccel': '0.4',                'leftDecel': '0.4',
                'rightVel': str(speed_1),               'rightAccel': '0.4',               'rightDecel': '0.4'}
            res = Bertec.run_treadmill(params['leftVel'], params['leftAccel'], params['leftDecel'], params['rightVel'], params['rightAccel'], params['rightDecel'])
            

            sleep(trial_start_sec)

            # 2. Trigger Nexus Capture
            Nexus.notify()

            
            sleep(trial_duration_sec)

            # 2. Stop Treadmill
            print("\nTreadmill stop")
            params = {
                'leftVel': '0',                'leftAccel': '0.4',                'leftDecel': '0.4',
                'rightVel': '0',               'rightAccel': '0.4',               'rightDecel': '0.4'}
            res = Bertec.run_treadmill(params['leftVel'], params['leftAccel'], params['leftDecel'], params['rightVel'], params['rightAccel'], params['rightDecel'])

        elif (command == '2'):
            
            speed_1 = 1.2

            sleep(15)

            # 2. Trigger Nexus Capture
            Nexus.notify()
            
            sleep(5)

            print(f"\nTreadmill speed: {speed_1} m/s")
            params = {
                'leftVel': str(speed_1),                'leftAccel': '0.4',                'leftDecel': '0.4',
                'rightVel': str(speed_1),               'rightAccel': '0.4',               'rightDecel': '0.4'}
            res = Bertec.run_treadmill(params['leftVel'], params['leftAccel'], params['leftDecel'], params['rightVel'], params['rightAccel'], params['rightDecel'])
            
            sleep(trial_duration_sec)

            # 2. Stop Treadmill
            print("\nTreadmill stop")
            params = {
                'leftVel': '0',                'leftAccel': '0.4',                'leftDecel': '0.4',
                'rightVel': '0',               'rightAccel': '0.4',               'rightDecel': '0.4'}
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