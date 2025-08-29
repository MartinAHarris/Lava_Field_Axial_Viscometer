# Lava Field Penetrometer
Files used to acquire data for the lava penetrometer are found within Files For Raspi folder

Instructions:
The primary code needed to run and collect data with the penetrometer device can be found as “Penetrometer_execution_code.py” 
This code requires a few edits for the user to specify the working directory and is code specific to the electronic sensors documented in the associated manuscript. If different sensors are used, the code will need to be amended accordingly. Additionally, the code is written to run with two toggle switches. If the user chooses not to use this method, the code will need to be amended to remove the loops calling upon the switches

Additional files include:
“Distance_sensor_test_code.py” used for troubleshooting distance sensor.
“Force_guage_test_code.py” used for troubleshooting force gauge.
“Instructions to get code to run on boot.txt” 

-------------------------------------------------------------------------------------------------------------

Files used to  process data for the lava penetrometer are found within Files For Data Processing 

## Instructions

The first step will be to retreate the time-date stamped files from the raspi (or single baord computer) within the penetrometer device.
Next, you will execute the "First_selection.py" for the desired penetrometer .txt file. This file will create a pop-up window to perform the first selection by draging the mouse across the area of interest. When you close the pop-up window, it saves the selected data as selected_dat.txt

Next, you can run the "Second_selection.py" file and in the pop-up window, you will select the selected_dat.txt file instead of the original penetrometer .txt file. You will then go through another round of data selection with the mouse. When you close this window, you it saves the data as selected_dat.txt again.

Lastly, you can run the "Process_selected_data.py" and in the pop-up window, select the selected_dat.txt file. This will produce a seires of plots that can be commented on or off as desired, and a .csv file that contains the calibrated viscosity values. 

-------------------------------------------------------------------------------------------------
Files for custom machined parts can be found in the `Penetrometer_parts` folder
Within the folder your will find complete 'Assembly' images and individual PDFs for each piece with their specifications. 
These can be used to replicate the precise pieces used in the penetrometer device or to modify as the builder see's fit.
