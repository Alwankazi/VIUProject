# VIUProject
Virtual Assistant For Visually Impaired User using OpenCV and RASA
<pre>
Requirnments -
          1- Flask
          2- RASA
          3- Google Chrome

Download these files and save them in to Detect folder -
frozen_east_text_detection.pb - https://drive.google.com/file/d/1mH7g9xZgAy6hcfgwes_pBB2jgvq6YsSH/view?usp=sharing
yolov3.weights - https://drive.google.com/file/d/1TDEzvfDhCpibxUt2i4ThQniyoey_8ex2/view?usp=sharing

Running the Flask Web App Server -
                           1- Change directory to the folder
                           2- Python app.py
                   
Running the RASA server -
                   1- cd VIU 
                   2- rasa run -m models --endpoints endpoints.yml --port 5002 --credentials credentials.yml
                   3- rasa run actions
 
Once Web server and RASA server start access the application on - http://localhost:5000/detection
</pre>
