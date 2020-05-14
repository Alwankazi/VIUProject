# VIUProject
**Virtual Assistant For Visually Impaired User using OpenCV and RASA**

**Requirnments -** <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1- Flask <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2- RASA  <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;3- Google Chrome <br>

**Download these files and save them into Detect folder:**<br>
&nbsp;&nbsp;&nbsp;&nbsp;[frozen_east_text_detection.pb](https://drive.google.com/file/d/1mH7g9xZgAy6hcfgwes_pBB2jgvq6YsSH/view?usp=sharing)<br>
&nbsp;&nbsp;&nbsp;&nbsp;[yolov3.weights](https://drive.google.com/file/d/1TDEzvfDhCpibxUt2i4ThQniyoey_8ex2/view?usp=sharing)<br>

**Download Rasa Trained Model and save into /VIU/models:**<br>
&nbsp;&nbsp;&nbsp;&nbsp;[20200506-082357.tar.gz](https://drive.google.com/file/d/1F5k8qZgpGzk81CMetZQouzyk_kQa9u9m/view?usp=sharing)<br>

**Running the Flask Web App Server -**<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1- Change directory to the folder<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2- Python app.py<br>
                   
**Running the RASA server -**<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1- cd VIU <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2- rasa run -m models --endpoints endpoints.yml --port 5002 --credentials credentials.yml<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;3- rasa run actions<br>
 
**Once Web server and RASA server start access the application on - http://localhost:5000/detection**<br>

