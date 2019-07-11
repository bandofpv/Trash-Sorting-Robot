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

# filter out RuntimeWarning from a divide by zero error in angle calculation 
warnings.filterwarnings("ignore", category=RuntimeWarning)

# stop is used to reset the counting variables
stop = 0

# count variables used to track the number of frames detected of each object
cardboardCount = 0
glassCount = 0
metalCount = 0
paperCount = 0
plasticCount = 0

# variables used to send to Arduino about location of object
inputDistance = ' 0'
inputAngle = ' 90'

# create variables to connect the RPI to Arduino via USB
port = "/dev/ttyACM0"
rate = 9600

# start the serial communication
s1 = serial.Serial(port,rate)
s1.flushInput()

# done is used to tell program that the arm is done moving
done = 1

# list of strings that the Arduino will send to RPI
comp_list=["Done Moving\r\n","Connected to Arduino\r\n"]

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

    # make three circles indicating the arm's range of motion
	cv2.circle(orig, (275, 445), 390, (0, 0, 255), 3, 8, 0)
	cv2.circle(orig, (275, 445), 340, (0, 0, 255), 3, 8, 0)
	cv2.circle(orig, (275, 445), 290, (0, 0, 255), 3, 8, 0)

	# loop over the results
	for r in results:
		# extract the bounding box and box and predicted class label
		box = r.bounding_box.flatten().astype("int")
		(startX, startY, endX, endY) = box
		label = labels[r.label_id]

		# center coordinates of object detected
		centerX = ((endX - startX) // 2) + startX
		centerY = ((endY - startY) // 2) + startY

		# calculate the distance from arm to object
		calcDistance = int(math.sqrt(((centerX - 275)**2)+((centerY - 445)**2)))

		# if object is close to the closest circle
		if calcDistance <= 314:
			inputDistance = ' 1'

					# if object is close to the middle circle
		if calcDistance >= 315 and calcDistance <= 364:
			inputDistance = ' 2'

		# if obejct is close to the furthest circle
		if calcDistance >= 365:
			inputDistance = ' 3'

		# calculate angle of object to arm
		angle = int(math.atan((centerY - 445)/(centerX - 275))*180/math.pi)

		# calculated angle gives angles between (-90,90) NOT (0,180)
		# if statements used to convert the (-90,90) angles to (0,180)
		if angle > 0:
			angle = abs(angle - 180)
			
		if angle < 0:
			angle = -angle
			
		if angle == 90: 
			angle = 0

		# convert (0,180) angle to a string to send to Arduino
		inputAngle = ' ' + str(angle)

		# create circle of center of object
		cv2.circle(orig, (centerX, centerY), 5, (0, 0, 255), -1)

		# create circle of where the arm is 
		cv2.circle(orig, (275, 370), 5, (0, 0, 255), -1)
		
		# create line connecting the arm and object location with the angle calculated too
		cv2.line(orig, (centerX, centerY), (275, 370), (0, 0, 255), 1)
		cv2.putText(orig, str(angle), (260, 360), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

		# create name and bounding box around object
		cv2.rectangle(orig, (startX, startY), (endX, endY), (0, 255, 0))
		y = startY - 15 if startY - 15 > 15 else startY + 15
		text = "{}: {:.2f}%".format(label, r.score * 100)
		cv2.putText(orig, text, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)      

		# if the arm is done moving
		if done == 1:	
			# increase each count variable when it detects that object	
			# NOTE: I commented out the first two if statements for demo purposes
			# uncomment them for your own purposes
			#if label == "cardboard":
				#cardboardCount += 1
				
			#if label == "glass":
				#glassCount += 1
				
			if label == "metal":
				metalCount += 1
				
			if label == "paper":
				paperCount += 1
				
			if label == "plastic":
				plasticCount += 1
	
	# if the Arduino sends data to the RPI
	if s1.inWaiting()>0:
		# take the input and print it
		inputValue = s1.readline()
		print(inputValue.decode())
		# if the Arduino tells RPI that it is done moving
		if inputValue.decode() == "Done Moving\r\n":
			done = 1
		# if the input is in the comp_list
		if inputValue.decode() in comp_list:
			# cardboard has been detected for at least 20 frames
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
				
			# glass has been detected for at least 20 frames
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
			
			# metal has been detected for at least 20 frames
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
	
			# paper has been detected for at least 20 frames
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
			
			# plastic has been detected for at least 20 frames
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
		
		# if stop equals 1 than reset all counting variables
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
