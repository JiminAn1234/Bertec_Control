
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

    speed_condition = "15bpm"
    task_condition = "Squat"

    trial_name = subject_name + "_" + speed_condition + "_" + task_condition

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

        # Since the locomotion is Squat, we need to set the treadmill speed to 0 m/s!!!!!!!!!!!!!!!!!!!!!!
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
            
            sleep(65)

            # 1. Stop Jetson
            #Jetson.send_message("exo off")

            # 2. Stop Treadmill
            print("\nTreadmill stop")
            params = {
                'leftVel': '0',                'leftAccel': '0.5',                'leftDecel': '0.5',
                'rightVel': '0',               'rightAccel': '0.5',               'rightDecel': '0.5'}
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