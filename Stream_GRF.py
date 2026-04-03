#Jimin stream GRF Data

from __future__ import print_function
from vicon_dssdk import ViconDataStream
import argparse
import sys
import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('host', nargs='?', help="Host name, in the format of server:port", default = "localhost:801")
args = parser.parse_args()
client = ViconDataStream.Client()
GRFr = []
GRFl = []

try:
    client.Connect( args.host )


    # Check setting the buffer size works
    client.SetBufferSize( 1 )

    #Enable all the data type fro treadmill
    client.EnableDeviceData()


    sample_size = 3000  #Choose how long the loop goes for 

    while sample_size > 0:

        HasFrame = False
        timeout = 50
        while not HasFrame:
            print( '.' )
            try:
                if client.GetFrame():
                    HasFrame = True
                timeout=timeout-1
                if timeout < 0:
                    print('Failed to get frame')
                    sys.exit()
            except ViconDataStream.DataStreamException as e:
                client.GetFrame()

        client.SetStreamMode( ViconDataStream.Client.StreamMode.EServerPush )


        client.SetAxisMapping( ViconDataStream.Client.AxisMapping.EForward, ViconDataStream.Client.AxisMapping.ELeft, ViconDataStream.Client.AxisMapping.EUp )
        xAxis, yAxis, zAxis = client.GetAxisMapping()

        devices = client.GetDeviceNames()
        forceplates = client.GetForcePlates()
        for plate in forceplates:
            globalForceVectorData = client.GetGlobalForceVector( plate )
            if plate ==1:
                Frz = abs(globalForceVectorData[0][2])
                print(Frz)
                GRFr.append(Frz)
            if plate == 2:
                Flz = abs(globalForceVectorData[0][2])
                GRFl.append(Flz)
                print(Flz)
        
except ViconDataStream.DataStreamException as e:
    print( 'Handled data stream error', e )

    
