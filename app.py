#!/usr/bin/env python
from flask import Flask, render_template, Response, current_app, redirect,url_for, request, jsonify, send_file
from imutils.video import WebcamVideoStream
from imutils.object_detection import non_max_suppression
import numpy as np
import speech_recognition as speechrecog
from gtts import gTTS
import face_recognition
from camera import Camera
import os, glob, gc, requests, subprocess, cv2, MySQLdb, io, face_recognition, time, imutils, argparse , json, pytesseract
from collections import deque

import subprocess
from google.cloud import texttospeech
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="VIU-Assistant-aa70d8f5f9d2.json"


app = Flask(__name__)
vs = WebcamVideoStream(src=0).start()


camera = None

#Database Connection
hostname = "206.189.139.161"
username = "lol"
password = "lol"
DBName = "VIU"

try: 
    db = MySQLdb.connect(hostname,username,password,DBName) 
    # If connection is not successful 
except: 
    print("Can't connect to database") 
    # If Connection Is Successful 
print("Connected")
cursor = db.cursor()


#Loading Objects Dataset To Neural Network
net = cv2.dnn.readNet("Detect/yolov3.weights", "Detect/yolov3.cfg")
classes = []
with open("Detect/coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]
layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
colors = np.random.uniform(0, 255, size=(len(classes), 3))

# define the two output layer names for the EAST detector model that
# we are interested -- the first is the output probabilities and the
# second can be used to derive the bounding box coordinates of text
layerNames = [
    "feature_fusion/Conv_7/Sigmoid",
    "feature_fusion/concat_3"]

# load the pre-trained EAST text detector
print("[INFO] loading EAST text detector...")
TextNet = cv2.dnn.readNet("Detect/frozen_east_text_detection.pb")

#Text Decoding 
def decode_predictions(scores, geometry):
    (numRows, numCols) = scores.shape[2:4]
    rects = []
    confidences = []
    
    # loop over the number of rows
    for y in range(0, numRows):
		# extract the scores (probabilities), followed by the
		# geometrical data used to derive potential bounding box
		# coordinates that surround text
        scoresData = scores[0, 0, y]
        xData0 = geometry[0, 0, y]
        xData1 = geometry[0, 1, y]
        xData2 = geometry[0, 2, y]
        xData3 = geometry[0, 3, y]
        anglesData = geometry[0, 4, y]
        
        # loop over the number of columns
        for x in range(0, numCols):
            # if our score does not have sufficient probability,
            # # ignore it
            if scoresData[x] < 0.5:
                continue
            
            # compute the offset factor as our resulting feature
            # maps will be 4x smaller than the input image
            (offsetX, offsetY) = (x * 4.0, y * 4.0)
            # extract the rotation angle for the prediction and
            # then compute the sin and cosine
            angle = anglesData[x]
            cos = np.cos(angle)
            sin = np.sin(angle)
            # use the geometry volume to derive the width and height of the bounding box
            h = xData0[x] + xData2[x]
            w = xData1[x] + xData3[x]
            # compute both the starting and ending (x, y)-coordinates for the text prediction bounding box
            endX = int(offsetX + (cos * xData1[x]) + (sin * xData2[x]))
            endY = int(offsetY - (sin * xData1[x]) + (cos * xData2[x]))
            startX = int(endX - w)
            startY = int(endY - h)
            # add the bounding box coordinates and probability score to our respective lists
            rects.append((startX, startY, endX, endY))
            confidences.append(scoresData[x])
            # return a tuple of the bounding boxes and associated confidences
    return (rects, confidences)


#Video Streaming Page
@app.route('/')
def index():
    return render_template('index.html')

def detection():
    while True:
            #Reading Frame and Resizing 
            imgIn = vs.read()
            img = imutils.resize(imgIn, width=600)
            (height, width) = img.shape[:2]
            # ratio = imgIn.shape[0] / float(img.shape[0])

            
            # Passing frame to neural network to find the blobs of objects
            blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)

            net.setInput(blob)
            outs = net.forward(output_layers)

            # Passing the frame to neural network to detect the text 
            blob = cv2.dnn.blobFromImage(img, 1.0, (416, 416),(123.68, 116.78, 103.94), swapRB=True, crop=False)
            TextNet.setInput(blob)
            (scores, geometry) = TextNet.forward(layerNames)
            
            # Defining the lower and upper range of the colors in the HSV color space.
            lower = {'red':(166, 84, 141), 'green':(66, 122, 129), 'blue':(97, 100, 117), 'yellow':(23, 59, 119), 'orange':(0, 50, 80)} #assign new item lower['blue'] = (93, 10, 0)
            upper = {'red':(186,255,255), 'green':(86,255,255), 'blue':(117,255,255), 'yellow':(54,255,255), 'orange':(20,255,255)}
            #Removing all the data from database to update with new information when new frame data is available
            try:
                query="DELETE FROM VIU.TextInfo;"
                cursor.execute(query)
                db.commit()
            except:
                print("Recheck Database Connection TextInfo")
            try: 
                orig = img.copy()
                (origH, origW) = img.shape[:2]

                (newW, newH) = (416, 416)
                rW = origW / float(newW)
                rH = origH / float(newH)

                (H, W) = img.shape[:2]
                # decode the predictions, then  apply non-maxima suppression 
                (rects, confidences) = decode_predictions(scores, geometry)
                boxes = non_max_suppression(np.array(rects), probs=confidences)
                # initialize the list of results
                results = []
                # loop over the bounding boxes
                for (startX, startY, endX, endY) in boxes:
                    # Padding particular box of detected text for better recognition
                    startX = int(startX * rW)
                    startY = int(startY * rH)
                    endX = int(endX * rW)
                    endY = int(endY * rH)
                    dX = int((endX - startX) * 0.5)
                    dY = int((endY - startY) * 0.5)
                    
                    startX = max(0, startX - dX)
                    startY = max(0, startY - dY)
                    endX = min(origW, endX + (dX * 2))
                    endY = min(origH, endY + (dY * 2))

                    roi = orig[startY:endY, startX:endX]

                    #L For language 
                    #OEM For Lines
                    config = ("-l eng --oem 1 --psm 7")
                    text = pytesseract.image_to_string(roi, config=config)

                    # add the bounding box coordinates and OCR'd text to the list
                    # of results
                    results.append(((startX, startY, endX, endY), text))
                    
                # sort the results bounding box coordinates from top to bottom
                results = sorted(results, key=lambda r:r[0][1])

                # loop over the results
                for ((startX, startY, endX, endY), text) in results:
                    # display the text OCR'd by Tesseract
                    text = "".join([c if ord(c) < 128 else "" for c in text]).strip()
                    img = img.copy()
                    cv2.rectangle(img, (startX, startY), (endX, endY),(0, 0, 255), 2)
                    cv2.putText(img, text, (startX, startY - 20),cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)
                    #Removing all the data from database to update with new information when new frame data is available
                    try:
                        query="INSERT INTO VIU.TextInfo (Text) VALUES ('"+text+"');"
                        cursor.execute(query)
                        db.commit()
                    except:
                        print("Recheck Database Connection TextInfo 2")
                
            except:
                print("Unable to read text")

            try:
                class_ids = []
                confidences = []
                boxes = []
                colorbox = []
                position = [] 
                #Looping through each blob to find the class using its confidence level 
                for out in outs:
                    for detection in out:
                        scores = detection[5:]
                        class_id = np.argmax(scores)
                        confidence = scores[class_id]
                        if confidence > 0.5:
                                # Object class detected
                                center_x = int(detection[0] * width)
                                center_y = int(detection[1] * height)
                                w = int(detection[2] * width)
                                h = int(detection[3] * height)

                                # Finds Rectangle coordinates
                                x = int(center_x - w / 2)
                                y = int(center_y - h / 2)

                                # Crop Image from the frame to find that particular objects color
                                if( x < 0):
                                    a = 0
                                    crop_img = img[y:y+h-25, x:a+w-25] 
                                elif( y < 0):
                                    b = 0
                                    crop_img = img[y:b+h-25, x:x+w-25] 
                                else:
                                    crop_img = img[y:y+h-25, x:x+w-25]   

                                try:
                                    #If the class detected is person then no color recognition
                                    if (str(classes[class_id])== "person"):
                                        color = "----"
                                        colorbox.append(color)
                                        
                                    else:
                                        #Initalize color as empty string 
                                        color="undetected"
                                        #Smoothen the image using blur
                                        blurred = cv2.GaussianBlur(crop_img,(11,11), 0) 
                                        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
                                        #for each color in dictionary check object by applying all different masks
                                        for key, value in upper.items():
                                            kernel = np.ones((9,9),np.uint8)
                                            mask = cv2.inRange(hsv, lower[key], upper[key])
                                            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
                                            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
                                                
                                            # find contours in the mask 
                                            cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                                                cv2.CHAIN_APPROX_SIMPLE)[-2]

                                            #If any counter found then color detected
                                            if len(cnts) > 0:
                                                c = max(cnts, key=cv2.contourArea)
                                                color = key
                                         
                                        colorbox.append(color)
                                #Exception for undetected color
                                except: 
                                    color = "undetected"
                                    colorbox.append(color)

                                #Frame divided into 9 blocks based on x and y axis of the frame
                                if(x < 200 and y < 114):
                                    position.append("Left") 
                                    #Top Left
                                elif(x < 200 and y< 227 and y>114):
                                    position.append("Left")
                                    #Left Middle
                                elif(x < 200 and y>227):
                                    position.append("Bottom Left")
                                    #Bottom Left
                                elif(x < 400 and x > 200 and y< 114):
                                    position.append("Front")
                                    #Up-Straight
                                elif(x < 400 and x > 200 and y< 227 and y>114):
                                    position.append("Front")
                                    #Center
                                elif(x < 400 and x > 200 and y>227):
                                    position.append("Front")
                                    #Bottom-Straight
                                elif(x > 400 and y< 114):
                                    position.append("Right")
                                    #Top Right
                                elif(x > 400 and y< 227 and y>114):
                                    position.append("Right")
                                    #Middle Right
                                elif(x > 400 and y>227):
                                    position.append("Right")
                                    #Bottom Right

                                #Storing All The Data Of Each Object
                                boxes.append([x, y, w, h])
                                confidences.append(float(confidence))
                                class_ids.append(class_id)
                                 
                indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

                #Removing all the data from database to update with new information when new frame data is available
                try:
                    query1="DELETE FROM VIU.Objects;"
                    cursor.execute(query1)
                    query2="DELETE FROM VIU.People;"
                    cursor.execute(query2)
                    db.commit()
                except:
                    print("Recheck Database Connection Object and People")
            
                
                font = cv2.FONT_HERSHEY_PLAIN
                #Retriving all the data to display on screen
                for i in range(len(boxes)):
                    if i in indexes:
                        x, y, w, h = boxes[i]
                        label = str(classes[class_ids[i]])
                        color = colorbox[i]
                        try:
                            obj_position = position[0]
                            position.pop(0)
                        except:
                            obj_position = " "

                        text = "{} {} {}".format(color,label, obj_position)
                        colorarray = colors[i]
                        # Inserting the data of object name, color and location for each object into the database
                        try:
                            query="INSERT INTO VIU.Objects (object_name, object_color, object_location) VALUES ('"+label+"','"+color+"','"+str(obj_position)+"');"
                            cursor.execute(query)
                            db.commit()
                        except:
                            print("Recheck Database Connection Inserting Objects")
            
                        #Printing data On the frame
                        cv2.rectangle(img, (x, y), (x + w, y + h), colorarray, 2)
                        cv2.putText(img, text, (x, y + 30), font, 3, colorarray, 3)
            #Exception if at anypoint object detection fails
            except:
                print("Crashed In Object Detection")    
            
            try:
                # Load images from database and encodes.
                known_face_encodings =[]
                known_face_names =[]
                for filepath in glob.iglob(r'static/faces/*.jpg'):
                    face_image = face_recognition.load_image_file(filepath)
                    filepath= filepath[13:]
                    filepath= filepath[:-4]
                    known_face_names.append(filepath)
                    face_encoding = face_recognition.face_encodings(face_image)[0]
                    #Array of encoded faces
                    known_face_encodings.append(face_encoding)
                
                face_locations = []
                face_encodings = []
                face_names = []
                process_this_frame = True

                # Resize frame size for faster face recognition processing
                small_frame = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)
                
                # Convert the image from BGR color space to RGB color space for face recognition
                rgb_small_frame = small_frame[:, :, ::-1]
                # Only process every other frame of video to save time
                if process_this_frame:
                    # Find all the faces and face encodings in the current frame of video
                    face_locations = face_recognition.face_locations(rgb_small_frame)
                    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

                    
                    face_names = []
                    
                    for face_encoding in face_encodings:
                        # Match current frame face with the encodings if any match then face recognized
                        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                        name = "Unknown"
                        
                        if (known_face_encodings == []):
                            print("Store Faces In DB")
                        else:
                            # Known face with the smallest distance to the face in current face
                            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                            best_match_index = np.argmin(face_distances)
                            if matches[best_match_index]:
                                name = known_face_names[best_match_index]

                        face_names.append(name)
                        
                process_this_frame = not process_this_frame
            
                # Display the results
                for (top, right, bottom, left), name in zip(face_locations, face_names):
                    # Scale back up face locations since the frame we detected in was scaled 
                    top *= 4
                    right *= 4
                    bottom *= 4
                    left *= 4
                    # Draw a box around the face to display on screen
                    cv2.rectangle(img, (left, top), (right, bottom), (0, 0, 255), 2)
                    cv2.rectangle(img, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                    font = cv2.FONT_HERSHEY_DUPLEX
                    cv2.putText(img, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
                    #Inserting result into database
                    try:
                        query="INSERT INTO VIU.People (People) VALUES ('"+name+"');"
                        cursor.execute(query)
                        db.commit()
                    except:
                        print("Recheck Database Connection Inserting People")

                encode_return_code, image_buffer = cv2.imencode('.jpg', img)
                io_buf = io.BytesIO(image_buffer)
                
                yield (b'--img\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + io_buf.read() + b'\r\n')
            #Exception if face recognition fails
            except:
                print("Crashed In Face Recognition")

            else: 
                encode_return_code, image_buffer = cv2.imencode('.jpg', img)
                io_buf = io.BytesIO(image_buffer)
                
                yield (b'--img\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + io_buf.read() + b'\r\n')

#Results Display   
@app.route('/video_feed')
def video_feed():
    return Response(
        detection(),
        mimetype='multipart/x-mixed-replace; boundary=img',
    )

@app.route('/static/response/')
def download_file(filename):
    # print(filename)
    return send_file('static/response', mimetype="audio/mpeg", 
         as_attachment=True, 
         attachment_filename="output.mp3")

#Web page to Add face into database
@app.route('/detection', methods=['GET','POST'])
def voicerecognition():
    bot_message = " "
    if request.method == 'POST':
        message = json.loads(request.data)
        print (message['message'])
        #Pass query to rasa server
        r = requests.post('http://localhost:5002/webhooks/rest/webhook', json={"message":message['message']})

        for i in r.json():
            #Response retrived from server
            bot_message = bot_message+' '+i['text']
        print(bot_message)
         

        # Instantiates a client
        client = texttospeech.TextToSpeechClient()

        # Set the text input to be synthesized
        synthesis_input = texttospeech.types.SynthesisInput(text=bot_message)

        # Build the voice request, select the language code ("en-US") and the ssml
        # voice gender ("neutral")
        voice = texttospeech.types.VoiceSelectionParams(
            language_code='en-US',
            ssml_gender=texttospeech.enums.SsmlVoiceGender.NEUTRAL)

        # Select the type of audio file you want returned
        audio_config = texttospeech.types.AudioConfig(
            audio_encoding=texttospeech.enums.AudioEncoding.MP3)

        # Perform the text-to-speech request on the text input with the selected
        # voice parameters and audio file type
        response = client.synthesize_speech(synthesis_input, voice, audio_config)

        # The response's audio_content is binary.
        with open('./static/response/output.mp3', 'wb') as out:
            # Write the response to the output file.
            out.write(response.audio_content)
            print('Audio content written to file "output.mp3"')
            #Plays the audio out
        subprocess.call(['mpg321',"./static/response/output.mp3"])
            # return send_file('./static/response/output.mp3', attachment_filename='output.mp3')
    return render_template('detection.html')

   
#Camera function for adding face into database
def get_camera():
    global camera
    if not camera:
        camera = Camera()

    return camera


#Web page to Add face into database
@app.route('/add_face', methods=['GET','POST'])
def add_person():
    return render_template("addperson.html")


def gen(camera):
    while True:
        frame = camera.get_feed()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')



@app.route('/capture/')
def capture():
    camera = get_camera()
    stamp = camera.capture()
    return redirect(url_for('show_capture', timestamp=stamp))

def stamp_file(timestamp):
    return "faces/" + timestamp +".jpg"

@app.route('/capture/image/<timestamp>', methods=['POST', 'GET'])
def show_capture(timestamp):
    path = stamp_file(timestamp)
    #Image captured is posted and saved with the name provided by the user
    if request.method == 'POST':
        name=request.form.get('name')
        os.rename("static/faces/"+timestamp+".jpg", "static/faces/"+name+".jpg")
    else:
        print("Error Name")
     
    return render_template('capture.html',
        stamp=timestamp, path=path)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True)

