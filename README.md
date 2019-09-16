# Face-Tag
An Album creator based on the faces of a reference image

Amongst a pool of images with different people, the Face-Tag app based on a reference image, creates a number of folders with each person from the reference image. The GUI developed helps the user to input the path of the images directory and the reference image.

### Face-recognition:
The algorithm uses a face-recognition library which uses [dlib](http://dlib.net/)'s state-of-the-art face recognition built with deep learning. Based on the eigen values of the recognized faces from the reference image, we encode the faces in the directory to compare them with each of the face found.

### GUI
The GUI developed on Tkinter looks as follow

![GUI](https://imgur.com/nTh6Qiq.png)
