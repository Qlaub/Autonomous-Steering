# Autonomous Driving Car Project

## Purpose
Predicting the steering wheel angle of a car given an image of the road ahead of the car. Predictions are made using a convolutional neural network trained on 33,749 road images.

## Current Implementation
Testing runs on local machine. 10,000 test images are processed and then displayed using a tkinter GUI, which allows the user to navigate through the results. Pictures with their associated accuracies are displayed, and can be sorted by highest and lowest accuracy. Training and testing scripts are hosted on GitHub while dataset is too large to be hosted without compression. 

![Screenshot of command prompt open in the background with tkinter GUI in the foreground](/assets/images/neural-net.png?raw=true "Current Implementation Screenshot")

## Future Implementation
Web application hosted on AWS that runs the Python test scripts on the back-end server and then displays the results on an interactive website. Project is in development and will be done in Spring 2022.

## Dataset
Dataset of road images taken from NVIDIA.

## Developed using
* Python