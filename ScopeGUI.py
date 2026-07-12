import serial # for receiving ADC values from STM32
from matplotlib import pyplot as plt # for general plotting
from matplotlib.ticker import MultipleLocator # to adjust x-axis tick marks (time / div)
from matplotlib.widgets import Slider # adjustable X (time/div) and Y axis (volts/div) (Slider class imported from widgets module of Matplotlib package/library)
import numpy as np # for calculations like ranges with steps

# TODO: Add volts/div slider
# TODO: Add option to select between sine, square, triangle, sawtooth waves (need to interface with STM32)
# TODO: Add option to pause 
# TODO (Advanced): Add trigger functionality

mySerial = serial.Serial("COM5", 115200) # mySerial is an object which is connected to the STM32 Virtual ST-Link Port which is COM5 running at 115200 baud

plt.ion() # Enabling interactive mode (not using plt.show(), not even inside the loop, because an oscilloscope is a dynamic graph)

voltageReference = 3.3 # Voltage the MCU is powered by
voltSamples = [] # volt samples an empty list
voltSampleSize = 500 # increased sample size so entire waveform is graphed at higher time/div rather than stopping in between, although FIXME: lower time/div waveform appears frozen
sampleRate = 20 # (rate = 10 times per second, based on HAL_DELAY in STM32 loop, which is set to 10 ms (1000 ms / 50 ms = 20)) # TODO: add variable to pull HAL_DELAY value and thus sample rate from stm32 firmware instead of manually changing it every time
totalTime = voltSampleSize / sampleRate * 1000 # initial total time (time) in ms for x-axis is equal to the range of the voltSamples / ADC sampling rate
timePerDiv = 500 # oscilloscopes usually have 10 horizontal divs
figure, axes = plt.subplots() # plt.subplots returns a tuple containing the figure and axes, assigned to figure and axes variables using commas
figure.canvas.manager.set_window_title("STM32 Oscilloscope GUI")
figure.subplots_adjust(bottom = 0.25) # adds a 0.25 (25 % of figure) margin below the axes plot so that time / div slider appears below the plot not inside it

axes.set_title("STM32 Oscilloscope GUI", fontdict = dict (fontsize = 20, fontweight = "bold")) 

timePerDivSlider = Slider(ax = plt.axes([0.35, 0.10, 0.4, 0.05]), label = "Time/div slider (ms)", valmin = 1, valmax = 3000, valinit = timePerDiv) # FIXME: GUI crashes when clicking at a point in the slider rather than scrolling to it # interactive time/div Slider object, plt.axes() is a function from the plt (pyplot) module that returns an axes object
# FIXME: if time/div left at initial timePerDiv ms, waveform stops updating when it reaches the end unless you scroll through the slider (problem fixed when you go back to initial timePerDiv setting after that)

def adjustTimePerDiv (val): # need to pass an argument for voltSampleSize to actually be changed by .on_changed method in next line
   totalTime = timePerDivSlider.val * 10 # oscilloscopes usually have 10 horizontal divs
   global voltSampleSize
   voltSampleSize = int (sampleRate * totalTime / 1000) # this is an int class object, not a function
   axes.set_xlim(1, totalTime)
   figure.canvas.draw()  # entire figure redrawn when x-scale is changed

timePerDivSlider.on_changed(adjustTimePerDiv) # event driven (when adjusted using mouse), therefore no need to be put inside loop, also when this method is used, timePerDiv changes, also, the function OBJECT itself is passed to be used later and not at that instant (kind of like function pointers in C/C++)



while 1 == 1:

   # FOR DEBUGGING #

   # (for UART) line = mySerial.readline().decode().strip() # Decode bytes from the serial stream and return them into a line as a clean string (needs to be inside while loop to display changing ADC values)
   # print(line)
   # timePerDiv = timePerDivSlider.val
   print("time / div (ms): " + str(timePerDivSlider.val) + " | volt Sample Size: " + str(voltSampleSize))
   
   #################

   adcSample = int(mySerial.readline()) # cast to int from readLine() which returns bytes # FIXME: occasionally get error: ValueError: invalid literal for int() with base 10: b'\n' and have to re-run the program
   voltSample = float(adcSample * voltageReference / 4095) # conversion from ADC 12-bit values (0-4095) to voltage values (Vref of MCU is 3.3 V)
  
   if (voltSample <= voltageReference):  # Used to ensure erroneous readings above vref are not added to the list
      voltSamples.append(voltSample)
   
   if len(voltSamples) > voltSampleSize: # FIXME: when time/div is smaller, waveform does not update automatically because voltSampleSize is much higher than what can be displayed on screen || Need to use > sign when adjusting time/div because if going from larger to smaller time/div the voltsSampleSize decreases even though the list length may be a lot larger at that instant, so the length needs to shrink immediately
      voltSamples.pop(0) # remove first sample after reaching voltSampleSize 
      
   axes.clear() # need to clear before plotting data and axes (if you clear after, graph gets erased and you see nothing)   
   
   timeSamples = np.arange(len(voltSamples)) / sampleRate * 1000 # time samples in ms, and is related to the varying length of volt samples 
   
   axes.grid(True)
   axes.plot(timeSamples, voltSamples)
   
   axes.set_xlim(0, timePerDivSlider.val * 10)
   axes.xaxis.set_major_locator(MultipleLocator(timePerDivSlider.val)) # major tick mark every timePerDiv ms, MultipleLocator(timePerDivSlider.val) defines an object using a constructor, and that object is passed to this axes method
   axes.tick_params('x', labelbottom = False) # hide numbers from x-axis tick marks (many options for second argument of this method)
   axes.set_ylabel("Voltage (V)")
   
   plt.pause(0.0001) # entire window pauses for a short interval before redrawing, not just the graph 