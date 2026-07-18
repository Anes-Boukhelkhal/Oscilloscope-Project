# Building an STM32-Based Oscilloscope GUI

## How it works:
- Signals from the STM32's onboard DAC peripheral are sampled by the ADC peripheral at a rate of 20 samples per second, where ADC1 and DAC are connected using jumper wires
- ADC samples are transmitted from STM32 ST/Link Virtual COM port to a Python program usiong Pyserial using UART at 115200 baud
- Python program involves Matplotlib to plot live voltage and time data with adjustable volts/div and time/div axes

## Future plans:
- Add vertical and horizontal position sliders
- Migrate Python code from Matplotlib to PyQtGraph for improved performance
- Add button to select between sine, square, triangle, sawtooth waves
- Add option to start/stop waveform capture
- Add trigger functionality

## Current state (07/16/26): 
<img width="1914" height="1031" alt="image" src="https://github.com/user-attachments/assets/145d660e-b5fa-4639-9830-5ed2e4d941b4" />
