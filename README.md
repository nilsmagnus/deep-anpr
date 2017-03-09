# Deep ANPR


This is work in progress to detect the position of a numberplate in a image.

# Strategy

- generate training-set on the fly to do training
- until inference is acceptable, do
  - save the trained model
  - do inference in an android app
  - adjust model size/complexity


# Notes

- Norwegian numberplate ratio is (9:2), (width:height)
- backgrounds can be downloaded from http://vision.princeton.edu/projects/2010/SUN/SUN397.tar.gz