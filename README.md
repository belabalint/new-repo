# python-testprogram
Short description:
This repo alongside an other one (GHT) is to test an EEG device. This one is responsible for the data-analysis.
The program takes in the measurements in txt files, processess them, and shows if there are any errors, and then puts out a .xlsx file of the results.

Longer description:
It converts the incoming .txt to a pandas df, which includes the time and the measured voltage for each of the 18 electrodes.
The test begins with 60 second noise test with zero voltage on all electrodes, then a 5hz sinewave with and without a 1MOhm resistance on each of the electrodes.(see example input)
It finds the 0 timepoint by continously fourier transforming 100 timepoints until we find an acceptable amplitude, it checks if the minimum and maximum values in the noise test are less then 6 microvolts apart, then again by a fourier transform finds the amplitude on each electrode and if it's in the preferable range, it passed the test.
