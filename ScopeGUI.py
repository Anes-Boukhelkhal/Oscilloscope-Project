import serial # for receiving ADC values from STM32
from matplotlib import pyplot as plt # for general plotting
from matplotlib.ticker import MultipleLocator # to adjust x-axis tick marks (time / div)
import numpy as np # for calculations


mySerial = serial.Serial("COM5", 115200) # mySerial is an object which is connected to the STM32 Virtual ST-Link Port which is COM5 running at 115200 baud

voltSamples = [] 
sampleRate = 10 # (rate = 10 times per second, based on HAL_DELAY in STM32 loop, which is set to 100 ms)
figure, axes = plt.subplots() # plt.subplots returns a tuple containing the figure and axes, assigned to figure and axes variables using commas

plt.ion() # Enabling interactive mode (not using plt.show() because an oscilloscope is a dynamic graph)

while 1 == 1:
    # line = mySerial.readline().decode().strip() # Decode bytes from the serial stream and return them into a line as a clean string (needs to be inside while loop to display changing ADC values)
    # print(line)
    
   adcSample = int(mySerial.readline()) # cast to int from readLine() which returns bytes  
   voltSample = float(adcSample * 3.3 / 4095) # conversion from ADC 12 bit values (0-4095) to voltage values
   voltSamples.append(voltSample)
   voltSampleSize = 100
   
   if len(voltSamples) == voltSampleSize:
      voltSamples.pop(0) # remove first sample after reaching voltSampleSize



   timeIntervals = voltSampleSize / sampleRate # time divisions (time / div) for x-axis is equal to the range of the voltSamples / ADC sampling rate
   print(timeIntervals)
    

   axes.clear() # need to clear before plotting data and axes (if you clear after, graph gets erased and you see nothing)

   axes.plot(voltSamples)
   axes.xaxis.set_major_locator(MultipleLocator(10)) # major tick mark every timeIntervals ms

   axes.set_xlabel("Time  (ms)")
   axes.set_ylabel("Voltage (V)")
    
   plt.pause(0.0001)

    


