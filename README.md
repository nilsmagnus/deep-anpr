# Deep ANPR

 This project is heavily inspired by https://github.com/matthewearl/deep-anpr . 
 
 Work in progress, but something is working. 
 
 # The idea
 1. Instead of using a moving window, use houghman-transform to identify the rectangle of the license-plate
 2. Use a deep-network to identify what is written on the license-plate
 
 Substituting the windowing approach hopefully saves some time. 

#dependencies
 
The project has the following dependencies:

* [TensorFlow](https://tensorflow.org)
* OpenCV
* NumPy 
