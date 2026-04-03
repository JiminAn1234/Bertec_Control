
from Header_BertecControl import BertecController
from Header_NexusControl import NexusController
from Header_JetsonControl import JetsonController
from time import sleep
import random
import time

def main():  
    subject_name = "AB01_Jimin"
    # subject_name = "AB12_Ray"

    # speed_condition = "0mps"
    # speed_condition = "0p2mps"
    # speed_condition = "0p4mps"    
    # speed_condition = "0p6mps"
    # speed_condition = "0p8mps"
    # speed_condition = "1p0mps"
    # speed_condition = "1p2mps"
    # speed_condition = "1p4mps"
    # speed_condition = "transient_15sec"
    speed_condition = "Mocap_Trigger_Test"
    
    trial_name = subject_name + "_" + speed_condition

    trial_notes = ""
    trial_description = (" ")
    trial_path = "D:/Jeremy/Susan/Captures/Take"

    # Create an instance of BertecControl
    Bertec = BertecController()
    res = Bertec.start_connection()
    print(res)
    command = 1
    res = ' '
    trial_number = 0

    while(command):
        
        trial_number += 1
        print("\nTrial number: ", trial_number)
        trial_name_w_number = trial_name + '_' + str(trial_number)
        print("\nTrial name: ", trial_name_w_number)

        # Connect Jetson
        Jetson = JetsonController("172.24.44.177", 10)
        Jetson.start_server()

        # Port number should match with the port number in Nexus
        # !!!! Port number need to be different from previous trial every time running this code. (EX. you can do 30 -> 31 -> 30 -> 31 ...)
        port_number = int(input("Input Port number:"))

        # Create Nexus instance
        packet_id= random.randint(0, 2**32 - 1) 
        Nexus = NexusController(name= trial_name_w_number, notes = trial_notes, description = trial_description, database_path = trial_path,
        delay_ms = 0, packet_id = packet_id, port = port_number)
        
        command = input("Input protocol number (exit for 0):")

        if (command == '1'):

            speed_1 = 0

            print(f"\nTreadmill speed: {speed_1} m/s")
            params = {
                'leftVel': str(speed_1),                'leftAccel': '0.5',                'leftDecel': '0.5',
                'rightVel': str(speed_1),               'rightAccel': '0.5',               'rightDecel': '0.5'}
            res = Bertec.run_treadmill(params['leftVel'], params['leftAccel'], params['leftDecel'], params['rightVel'], params['rightAccel'], params['rightDecel'])

            # sleep(5)

            # 1. Trigger Jetson
            Jetson.send_message("exo on")

            # 2. Trigger Nexus Capture
            Nexus.notify()
            
            sleep(10)

            # 1. Stop Jetson
            #Jetson.send_message("exo off")

            # 2. Stop Treadmill
            print("\nTreadmill stop")
            params = {
                'leftVel': '0',                'leftAccel': '0.5',                'leftDecel': '0.5',
                'rightVel': '0',               'rightAccel': '0.5',               'rightDecel': '0.5'}
            res = Bertec.run_treadmill(params['leftVel'], params['leftAccel'], params['leftDecel'], params['rightVel'], params['rightAccel'], params['rightDecel'])

        # Steady State speeds 30s
        elif (command == '2'):
            
            speed_1 = 1.2
            trial_duration_sec = 120
            target_duration_sec = 30
            
            # sleep(15)
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
            sleep(trial_start_sec + trial_duration_sec - target_duration_sec)

            # sleep(trial_start_sec)
            # # Jetson.send_message("exo on")

            # # Sleep until target duration starting time
            # sleep(trial_duration_sec - target_duration_sec)

            # Jetson.send_message("exo on")
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

        # Transient 15s
        elif (command == '3'):

            speed_1 = 1.5
            accel_1 = 0.2
            
            print(f"\nTreadmill speed: {speed_1} m/s")
            params = {
                'leftVel': str(speed_1),                'leftAccel': str(accel_1),                'leftDecel': str(accel_1),
                'rightVel': str(speed_1),               'rightAccel': str(accel_1),               'rightDecel': str(accel_1)}
            res = Bertec.run_treadmill(params['leftVel'], params['leftAccel'], params['leftDecel'], params['rightVel'], params['rightAccel'], params['rightDecel'])

            # 1. Trigger Jetson
            Jetson.send_message("exo on")

            # 2. Trigger Nexus Capture
            Nexus.notify()
            
            sleep(7.5)

            # 2. Stop Treadmill
            speed_2 = 0
            print(f"\nTreadmill speed: {speed_2} m/s")
            params = {
                'leftVel': str(speed_2),                'leftAccel': str(accel_1),                'leftDecel': str(accel_1),
                'rightVel': str(speed_2),               'rightAccel': str(accel_1),               'rightDecel': str(accel_1)}
            res = Bertec.run_treadmill(params['leftVel'], params['leftAccel'], params['leftDecel'], params['rightVel'], params['rightAccel'], params['rightDecel'])

            sleep(7.5)

        # Transient 30s
        elif (command == '4'):

            speed_1 = 1.5
            accel_1 = 0.1
            
            print(f"\nTreadmill speed: {speed_1} m/s")
            params = {
                'leftVel': str(speed_1),                'leftAccel': str(accel_1),                'leftDecel': str(accel_1),
                'rightVel': str(speed_1),               'rightAccel': str(accel_1),               'rightDecel': str(accel_1)}
            res = Bertec.run_treadmill(params['leftVel'], params['leftAccel'], params['leftDecel'], params['rightVel'], params['rightAccel'], params['rightDecel'])

            # 1. Trigger Jetson
            Jetson.send_message("exo on")

            # 2. Trigger Nexus Capture
            Nexus.notify()            
            sleep(15)

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