
from Header_BertecControl import BertecController
from Header_NexusControl import NexusController
from Header_JetsonControl import JetsonController
from time import sleep
import random
import time

def main():  

    # subject_name = "AB01_Jimin"    
    # subject_name = "AB04_Changseob"
    # subject_name = "AB05_Maria"
    # subject_name = "AB07_Leo"
    # subject_name = "AB02_Rajiv"
    # subject_name = "AB11_Ryan"
    # subject_name = "AB12_Ray"
    # subject_name = "AB03_Amy"
    # subject_name = "AB13_Hridayam"
    # subject_name = "AB14_Evy"
    subject_name = "AB08_Adrian"

    # task_condition = "RA"
    task_condition = "RD"

    # degree_condition = "5deg"
    degree_condition = "10deg"

    # speed_condition = "0mps"
    # speed_condition = "0p4mps"    
    # speed_condition = "0p6mps"
    # speed_condition = "0p8mps"
    # speed_condition = "1p0mps"
    # speed_condition = "transient_15sec"
    speed_condition = "transient_30sec"

    trial_name = subject_name + "_" + degree_condition + "_" + speed_condition + "_" + task_condition

    trial_notes = "on 250619"
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

            # For RA
            # speed_1 = 0.4
            # speed_1 = 0.6
            # speed_1 = 0.8
            # speed_1 = 1.0
            
            #  For RD
            # speed_1 = -0.4
            # speed_1 = -0.6
            # speed_1 = -0.8
            speed_1 = -1.0
            
            print(f"\nTreadmill speed: {speed_1} m/s")
            params = {
                'leftVel': str(speed_1),                'leftAccel': '0.3',                'leftDecel': '0.3',
                'rightVel': str(speed_1),               'rightAccel': '0.3',               'rightDecel': '0.3'}
            res = Bertec.run_treadmill(params['leftVel'], params['leftAccel'], params['leftDecel'], params['rightVel'], params['rightAccel'], params['rightDecel'])

            sleep(5)

            # 1. Trigger Jetson
            Jetson.send_message("exo on")

            # 2. Trigger Nexus Capture
            Nexus.notify()
            
            sleep(30)

            # 1. Stop Jetson
            #Jetson.send_message("exo off")

            sleep(1)

            # 2. Stop Treadmill
            print("\nTreadmill stop")
            params = {
                'leftVel': '0',                'leftAccel': '0.3',                'leftDecel': '0.3',
                'rightVel': '0',               'rightAccel': '0.3',               'rightDecel': '0.3'}
            res = Bertec.run_treadmill(params['leftVel'], params['leftAccel'], params['leftDecel'], params['rightVel'], params['rightAccel'], params['rightDecel'])

        # Transient 15s
        elif (command == '3'):

            # speed_1 = 1.0
            speed_1 = -1.0 # For RD
            
            accel_1 = 0.133
            
            print(f"\nTreadmill speed: {speed_1} m/s")
            params = {
                'leftVel': str(speed_1),                'leftAccel': str(accel_1),                'leftDecel': str(accel_1),
                'rightVel': str(speed_1),               'rightAccel': str(accel_1),               'rightDecel': str(accel_1)}
            res = Bertec.run_treadmill(params['leftVel'], params['leftAccel'], params['leftDecel'], params['rightVel'], params['rightAccel'], params['rightDecel'])

            # 1. Trigger Jetson
            Jetson.send_message("exo on")

            # 2. Trigger Nexus Capture
            Nexus.notify()
            
            sleep(8)

            # 2. Stop Treadmill
            speed_2 = 0
            print(f"\nTreadmill speed: {speed_2} m/s")
            params = {
                'leftVel': str(speed_2),                'leftAccel': str(accel_1),                'leftDecel': str(accel_1),
                'rightVel': str(speed_2),               'rightAccel': str(accel_1),               'rightDecel': str(accel_1)}
            res = Bertec.run_treadmill(params['leftVel'], params['leftAccel'], params['leftDecel'], params['rightVel'], params['rightAccel'], params['rightDecel'])

            sleep(7)

        # Transient 30s
        elif (command == '4'):

            # speed_1 = 1.0
            speed_1 = -1.0 # For RD
            
            accel_1 = 0.067
            
            print(f"\nTreadmill speed: {speed_1} m/s")
            params = {
                'leftVel': str(speed_1),                'leftAccel': str(accel_1),                'leftDecel': str(accel_1),
                'rightVel': str(speed_1),               'rightAccel': str(accel_1),               'rightDecel': str(accel_1)}
            res = Bertec.run_treadmill(params['leftVel'], params['leftAccel'], params['leftDecel'], params['rightVel'], params['rightAccel'], params['rightDecel'])

            # 1. Trigger Jetson
            Jetson.send_message("exo on")

            # 2. Trigger Nexus Capture
            Nexus.notify()            
            sleep(16)

            # 2. Stop Treadmill
            speed_2 = 0
            print(f"\nTreadmill speed: {speed_2} m/s")
            params = {
                'leftVel': str(speed_2),                'leftAccel': str(accel_1),                'leftDecel': str(accel_1),
                'rightVel': str(speed_2),               'rightAccel':str(accel_1),               'rightDecel': str(accel_1)}
            res = Bertec.run_treadmill(params['leftVel'], params['leftAccel'], params['leftDecel'], params['rightVel'], params['rightAccel'], params['rightDecel'])

            sleep(14) 

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