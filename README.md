# Trash_Sorting_Robot

## Helpful Resources:

* [Recycle Image Set](https://github.com/garythung/trashnet)
* [How to Train Tensorflow Object Detection Model on Windows 10](https://github.com/EdjeElectronics/TensorFlow-Object-Detection-API-Tutorial-Train-Multiple-Objects-Windows-10)
* [How to Train Tensorflow Lite Object Detection Model in Cloud TPUs](https://medium.com/tensorflow/training-and-serving-a-realtime-mobile-object-detector-in-30-minutes-with-cloud-tpus-b78971cf1193)
* [How to Build and Install Tensorflow From Source on Windows 10](https://medium.com/@amsokol.com/how-to-build-and-install-tensorflow-gpu-cpu-for-windows-from-source-code-using-bazel-d047d9342b44)
* [Object Detection with Google Coral USB Accelerator](https://www.pyimagesearch.com/2019/05/13/object-detection-and-image-classification-with-google-coral-usb-accelerator/)
* [3D Printed Robtic Arm](https://howtomechatronics.com/tutorials/arduino/diy-arduino-robot-arm-with-smartphone-control/)
* [USB-to-Serial Communication with Raspberry Pi and Arduino](https://www.sunfounder.com/blog/rpi-ard/)

## Repository Contents:

### [Tensorflow - files used for training model](https://github.com/bandofpv/Trash_Sorting_Robot/tree/master/Tensorflow):
* [CSV](https://github.com/bandofpv/Trash_Sorting_Robot/tree/master/Tensorflow/CSV) - .csv files of both the train and test image set
* [Images](https://github.com/bandofpv/Trash_Sorting_Robot/tree/master/Tensorflow/Images) - .jpg images of recycling materials and .xml files of the annotated images
* [SaveModel](https://github.com/bandofpv/Trash_Sorting_Robot/tree/master/Tensorflow/SaveModel) - frozen graph of trained model
* [TFLite](https://github.com/bandofpv/Trash_Sorting_Robot/tree/master/Tensorflow/TFLite) - .tflite file of trained model and .tflite file of compiled model for Google Coral USB Accelerator
* [TFRecord](https://github.com/bandofpv/Trash_Sorting_Robot/tree/master/Tensorflow/TFRecord) - .record files of both the train and test images set used for training
* [ssd_mobilenet_v2_quantized_300x300_coco_2019_01_03](https://github.com/bandofpv/Trash_Sorting_Robot/tree/master/Tensorflow/ssd_mobilenet_v2_quantized_300x300_coco_2019_01_03) - .config, .ckpt, and .pb files of the quantized model used for transfer learning
* [labelmap.pbtxt](https://github.com/bandofpv/Trash_Sorting_Robot/blob/master/Tensorflow/labelmap.pbtxt) - label map used for training

## Tutorial:

### WIP!!!
