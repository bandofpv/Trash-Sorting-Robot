# USAGE
# python detect_video.py --model mobilenet_ssd_v2/mobilenet_ssd_v2_coco_quant_postprocess_edgetpu.tflite --labels mobilenet_ssd_v2/coco_labels.txt

# import the necessary packages
from edgetpu.detection.engine import DetectionEngine
from imutils.video import FPS
from imutils.video import VideoStream
from PIL import Image
import argparse
import imutils
import time
import cv2
import serial
import math
import warnings

warnings.filterwarnings("ignore", category=RuntimeWarning)

stop = 0

cardboardCount = 0
glassCount = 0
metalCount = 0
paperCount = 0
plasticCount = 0

inputDistance = ' 0'
inputAngle = ' 90'

port = "/dev/ttyACM0"
rate = 9600

s1 = serial.Serial(port,rate)
s1.flushInput()

done = 1

comp_list=["Flash complete\r\n","Connected to Arduino\r\n"]

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-m", "--model", required=True,
	help="path to TensorFlow Lite object detection model")
ap.add_argument("-l", "--labels", required=True,
	help="path to labels file")
ap.add_argument("-c", "--confidence", type=float, default=0.3,
	help="minimum probability to filter weak detections")
args = vars(ap.parse_args())

# initialize the labels dictionary
print("[INFO] parsing class labels...")
labels = {}

# loop over the class labels file
for row in open(args["labels"]):
	# unpack the row and update the labels dictionary
	(classID, label) = row.strip().split(maxsplit=1)
	labels[int(classID)] = label.strip()

# load the Google Coral object detection model
print("[INFO] loading Coral model...")
model = DetectionEngine(args["model"])

# initialize the video stream and allow the camera sensor to warmup,
# and initialize the FPS counter
print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()
#vs = VideoStream(usePiCamera=False).start()
time.sleep(5)
fps = FPS().start()

# loop over the frames from the video stream
while True:
	# grab the frame from the threaded video stream and resize it
	# to have a maximum width of 500 pixels
	frame = vs.read()
	frame = imutils.resize(frame, width=500)
	orig = frame.copy()

	# prepare the frame for object detection by converting (1) it
	# from BGR to RGB channel ordering and then (2) from a NumPy
	# array to PIL image format
	frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
	frame = Image.fromarray(frame)

	# make predictions on the input frame
	start = time.time()
	results = model.DetectWithImage(frame, threshold=args["confidence"],
		keep_aspect_ratio=True, relative_coord=False)
	end = time.time()
	
	cv2.circle(orig, (275, 445), 390, (0, 0, 255), 3, 8, 0)
	cv2.circle(orig, (275, 445), 340, (0, 0, 255), 3, 8, 0)
	cv2.circle(orig, (275, 445), 290, (0, 0, 255), 3, 8, 0)

	# loop over the results
	for r in results:
		# extract the bounding box and box and predicted class label
		box = r.bounding_box.flatten().astype("int")
		(startX, startY, endX, endY) = box
		label = labels[r.label_id]

		if label != "cardboard!":
			centerX = ((endX - startX) // 2) + startX
			centerY = ((endY - startY) // 2) + startY
			
			calcDistance = int(math.sqrt(((centerX - 250)**2)+((centerY - 500)**2)))
			
			if calcDistance <= 314:
				inputDistance = ' 1'
				
			if calcDistance >= 315 and calcDistance <= 364:
				inputDistance = ' 2'
				
			if calcDistance >= 365:
				inputDistance = ' 3'

			# draw the bounding box and label on the image
			centerX = ((endX - startX) // 2) + startX
			centerY = ((endY - startY) // 2) + startY
			
			angle = int(math.atan((centerY - 500)/(centerX - 275))*180/math.pi)
			angle = angle 
				
			if angle > 0:
				angle = abs(angle - 180)
				
			if angle < 0:
				angle = -angle
				
			if angle == 90: 
				angle = 0
				
			inputAngle = ' ' + str(angle)
			
			cv2.circle(orig, (centerX, centerY), 5, (0, 0, 255), -1)
			cv2.circle(orig, (275, 370), 5, (0, 0, 255), -1)
			cv2.line(orig, (centerX, centerY), (250, 370), (0, 0, 255), 1)
			cv2.putText(orig, str(angle), (260, 360), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
			
			cv2.rectangle(orig, (startX, startY), (endX, endY), (0, 255, 0))
			y = startY - 15 if startY - 15 > 15 else startY + 15
			text = "{}: {:.2f}%".format(label, r.score * 100)
			cv2.putText(orig, text, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)      
			
			if done == 1:		
				if label == "cardboard":
					print(label);
					cardboardCount += 1
					
				if label == "glass":
					glassCount += 1
					
				if label == "metal":
					print(label)
					metalCount += 1
					
				if label == "paper":
					paperCount += 1
					
				if label == "plastic":
					plasticCount += 1
	
	if s1.inWaiting()>0:
		inputValue = s1.readline()
		print(inputValue.decode())
		if inputValue.decode() == "Flash complete\r\n":
			done = 1
		if inputValue.decode() in comp_list:
			if cardboardCount >= 20 and done == 1 and angle != 0:
				print("Cardboard frames:", cardboardCount)
				print(inputDistance);
				print(inputAngle);
				s1.write(bytes('1', 'utf-8'))
				s1.write(bytes(' 1', 'utf-8'))
				s1.write(bytes(inputDistance, 'utf-8'))
				s1.write(bytes(inputAngle, 'utf-8'))
				stop = 1
				done = 0
				
			if glassCount >= 20 and done == 1 and angle != 0:
				print("Glass frames:", glassCount)
				print(inputDistance);
				print(inputAngle);
				s1.write(bytes('1', 'utf-8'))
				s1.write(bytes(' 2', 'utf-8'))
				s1.write(bytes(inputDistance, 'utf-8'))
				s1.write(bytes(inputAngle, 'utf-8'))
				stop = 1
				done = 0
				
			if metalCount >= 20 and done == 1 and angle != 0:
				print("Metal frames:", metalCount)
				print(inputDistance);
				print(inputAngle);
				s1.write(bytes('1', 'utf-8'))
				s1.write(bytes(' 3', 'utf-8'))
				s1.write(bytes(inputDistance, 'utf-8'))
				s1.write(bytes(inputAngle, 'utf-8'))
				stop = 1
				done = 0
	
			if paperCount >= 20 and done == 1 and angle != 0:
				print("Paper frames:", paperCount)
				print(inputDistance);
				print(inputAngle);
				s1.write(bytes('1', 'utf-8'))
				s1.write(bytes(' 4', 'utf-8'))
				s1.write(bytes(inputDistance, 'utf-8'))
				s1.write(bytes(inputAngle, 'utf-8'))
				stop = 1
				done = 0
				
			if plasticCount >= 20 and done == 1 and angle != 0:
				print("Plastic frames:", plasticCount)
				print(inputDistance);
				print(inputAngle);
				s1.write(bytes('1', 'utf-8'))
				s1.write(bytes(' 1 ', 'utf-8'))
				s1.write(bytes(inputDistance, 'utf-8'))
				s1.write(bytes(inputAngle, 'utf-8'))
				stop = 1
				done = 0
		
		if stop == 1:
			cardboardCount = 0
			glassCount = 0
			metalCount = 0
			paperCount = 0
			plasticCount = 0
			stop = 0
				
	# show the output frame and wait for a key press
	cv2.imshow("Frame", orig)
	key = cv2.waitKey(1) & 0xFF

	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break

	# update the FPS counter
	fps.update()

# stop the timer and display FPS information
fps.stop()
print("[INFO] elapse time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()