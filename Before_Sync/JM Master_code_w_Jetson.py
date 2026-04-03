# Drafted by Changseob Song, 11/1/2024
# This is an example code to trigger starts of Vicon Nexus and Bertec FIT5

from Header_BertecControl import BertecController
from Header_NexusControl import NexusController
from Header_JetsonControl import JetsonController
from time import sleep
import random
import time

def main():  
    
    # trial_name = "AB01_Jimin_1p2ms_NoAssi"
    #trial_name = "AB01_Jimin_1p2ms_5p100ms"
    #trial_name = "AB01_Jimin_1p2ms_10p100ms"
    #trial_name = "AB01_Jimin_1p2ms_15p100ms"
    #trial_name = "AB01_Jimin_1p2ms_20p100ms"
    # trial_name = "AB01_Jimin_1p2ms_25p100ms"

    # Don't foregt NoExo
    # trial_name = "AB04_Changseob_1p2ms_NoAssi"
    # trial_name = "AB04_Changseob_1p2ms_5p100ms"
    # trial_name = "AB04_Changseob_1p2ms_10p100ms"
    # trial_name = "AB04_Changseob_1p2ms_15p100ms"
    trial_name = "AB04_Changseob_1p2ms_20p100ms"
    # trial_name = "AB04_Changseob_1p2ms_25p100ms"

    # Don't foregt NoExo
    # trial_name = "AB05_Maria_1p2ms_NoAssi"
    # trial_name = "AB05_Maria_1p2ms_5p100ms"
    # trial_name = "AB05_Maria_1p2ms_10p100ms"
    # trial_name = "AB05_Maria_1p2ms_15p100ms"
    # trial_name = "AB05_Maria_1p2ms_20p100ms"    
    # trial_name = "AB05_Maria_1p2ms_25p100ms"    

    
    trial_notes = "250430 Run by master python script."
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

            speed_1 = 1.2

            print(f"\nTreadmill speed: {speed_1} m/s")
            params = {
                'leftVel': str(speed_1),                'leftAccel': '0.5',                'leftDecel': '0.5',
                'rightVel': str(speed_1),               'rightAccel': '0.5',               'rightDecel': '0.5'}
            res = Bertec.run_treadmill(params['leftVel'], params['leftAccel'], params['leftDecel'], params['rightVel'], params['rightAccel'], params['rightDecel'])

            sleep(5)

            # 1. Trigger Jetson
            Jetson.send_message("exo on")

            # 2. Trigger Nexus Capture
            Nexus.notify()
            
            sleep(60)

            # 1. Stop Jetson
            #Jetson.send_message("exo off")

            # 2. Stop Treadmill
            print("\nTreadmill stop")
            params = {
                'leftVel': '0',                'leftAccel': '0.5',                'leftDecel': '0.5',
                'rightVel': '0',               'rightAccel': '0.5',               'rightDecel': '0.5'}
            res = Bertec.run_treadmill(params['leftVel'], params['leftAccel'], params['leftDecel'], params['rightVel'], params['rightAccel'], params['rightDecel'])

        elif (command == '2'):

            speed_1 = 1.0
            print(f"\nTreadmill speed: {speed_1} m/s")
            params = {
                'leftVel': str(speed_1),                'leftAccel': '0.75',                'leftDecel': '0.5',
                'rightVel': str(speed_1),               'rightAccel': '0.75',               'rightDecel': '0.5'}
            res = Bertec.run_treadmill(params['leftVel'], params['leftAccel'], params['leftDecel'], params['rightVel'], params['rightAccel'], params['rightDecel'])

            sleep(5)

            # 1. Trigger Jetson
            Jetson.send_message("exo on")

            # 2. Trigger Nexus Capture
            Nexus.notify()
            
            sleep(15)

            # 1. Stop Jetson
            #Jetson.send_message("exo off")

            sleep(1)

            # 2. Stop Treadmill
            print("\nTreadmill stop")
            params = {
                'leftVel': '0',                'leftAccel': '0.5',                'leftDecel': '0.5',
                'rightVel': '0',               'rightAccel': '0.5',               'rightDecel': '0.5'}
            res = Bertec.run_treadmill(params['leftVel'], params['leftAccel'], params['leftDecel'], params['rightVel'], params['rightAccel'], params['rightDecel'])

        
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

            # 1. Stop Jetson
            #Jetson.send_message("exo off")

            # 2. Stop Treadmill
            speed_2 = 0
            print(f"\nTreadmill speed: {speed_2} m/s")
            params = {
                'leftVel': str(speed_2),                'leftAccel': str(accel_1),                'leftDecel': str(accel_1),
                'rightVel': str(speed_2),               'rightAccel': str(accel_1),               'rightDecel': str(accel_1)}
            res = Bertec.run_treadmill(params['leftVel'], params['leftAccel'], params['leftDecel'], params['rightVel'], params['rightAccel'], params['rightDecel'])

            sleep(7.5)

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

            #Jetson.send_message("exo off")


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