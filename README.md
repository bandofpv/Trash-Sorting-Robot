# Trash_Sorting_Robot

## Helpful Resources:

* [Recycle Image Set](https://github.com/garythung/trashnet)
* [How to Train Tensorflow Object Detection Model on Windows 10](https://github.com/EdjeElectronics/TensorFlow-Object-Detection-API-Tutorial-Train-Multiple-Objects-Windows-10)
* [How to Train Tensorflow Lite Object Detection Model in Cloud TPUs](https://medium.com/tensorflow/training-and-serving-a-realtime-mobile-object-detector-in-30-minutes-with-cloud-tpus-b78971cf1193)
* [How to Build and Install Tensorflow From Source on Windows 10](https://medium.com/@amsokol.com/how-to-build-and-install-tensorflow-gpu-cpu-for-windows-from-source-code-using-bazel-d047d9342b44)
* [Object Detection with Google Coral USB Accelerator](https://www.pyimagesearch.com/2019/05/13/object-detection-and-image-classification-with-google-coral-usb-accelerator/)
* [USB-to-Serial Communication with Raspberry Pi and Arduino](https://www.sunfounder.com/blog/rpi-ard/)
* [3D Printed Robtic Arm](https://howtomechatronics.com/tutorials/arduino/diy-arduino-robot-arm-with-smartphone-control/)

## Repository Contents:

### [Arduino](https://github.com/bandofpv/Trash_Sorting_Robot/tree/master/Arduino) - files used for Arduino to control robotic arm:
* [basicMovement](https://github.com/bandofpv/Trash_Sorting_Robot/tree/master/Arduino/basicMovement) - .ino file to perform basic movement with robotic arm
* [roboticArm](https://github.com/bandofpv/Trash_Sorting_Robot/tree/master/Arduino/roboticArm) - .ino file to control robotic arm to pick up and drop off a piece of recycling detected from the Raspberry Pi

### [Documentation](https://github.com/bandofpv/Trash_Sorting_Robot/tree/master/Documentation) - files documenting my build process:
* [Bill_of_Materials.pdf](https://github.com/bandofpv/Trash_Sorting_Robot/blob/master/Documentation/Bill_of_Materials.pdf) - .pdf file including all my parts used in my project 

### [RPI](https://github.com/bandofpv/Trash_Sorting_Robot/tree/master/RPI) - files used for Raspberry Pi to perform object detection:
* [recycle_ssd_mobilenet_v2_quantized_300x300_coco_2019_01_03](https://github.com/bandofpv/Trash_Sorting_Robot/tree/master/RPI/recycle_ssd_mobilenet_v2_quantized_300x300_coco_2019_01_03) - .tflite and .txt files of the trained recycle model and lables to perform object detection
* [recycle_detection.py](https://github.com/bandofpv/Trash_Sorting_Robot/blob/master/RPI/recycle_detection.py) - python code used to perform object detection and communicate with Arduino

### [Tensorflow](https://github.com/bandofpv/Trash_Sorting_Robot/tree/master/Tensorflow) - files used for training model:
* [CSV](https://github.com/bandofpv/Trash_Sorting_Robot/tree/master/Tensorflow/CSV) - .csv files of both the train and test image set
* [Images](https://github.com/bandofpv/Trash_Sorting_Robot/tree/master/Tensorflow/Images) - .jpg images of recycling materials and .xml files of the annotated images
* [SaveModel](https://github.com/bandofpv/Trash_Sorting_Robot/tree/master/Tensorflow/SaveModel) - frozen graph of trained model
* [TFLite](https://github.com/bandofpv/Trash_Sorting_Robot/tree/master/Tensorflow/TFLite) - .tflite file of trained model and .tflite file of compiled model for Google Coral USB Accelerator
* [TFRecord](https://github.com/bandofpv/Trash_Sorting_Robot/tree/master/Tensorflow/TFRecord) - .record files of both the train and test images set used for training
* [ssd_mobilenet_v2_quantized_300x300_coco_2019_01_03](https://github.com/bandofpv/Trash_Sorting_Robot/tree/master/Tensorflow/ssd_mobilenet_v2_quantized_300x300_coco_2019_01_03) - .config, .ckpt, and .pb files of the quantized model used for transfer learning
* [labelmap.pbtxt](https://github.com/bandofpv/Trash_Sorting_Robot/blob/master/Tensorflow/labelmap.pbtxt) - label map used for training

## Tutorial:

### WIP!!!
