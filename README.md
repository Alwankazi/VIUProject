# VIUProject
**Virtual Assistant For Visually Impaired User using OpenCV and RASA**

**Requirnments -** <br>
* Flask <br>
* RASA  <br>
* Google Chrome <br>

**Download these files and save them into Detect folder:**<br>
[frozen_east_text_detection.pb](https://drive.google.com/file/d/1mH7g9xZgAy6hcfgwes_pBB2jgvq6YsSH/view?usp=sharing)<br>
[yolov3.weights](https://drive.google.com/file/d/1TDEzvfDhCpibxUt2i4ThQniyoey_8ex2/view?usp=sharing)<br>

**Download Rasa Trained Model and save into /VIU/models:**<br>
[20200506-082357.tar.gz](https://drive.google.com/file/d/1F5k8qZgpGzk81CMetZQouzyk_kQa9u9m/view?usp=sharing)<br>

**Import VIU.sql to your database and change the database connections in the following files:**<br>
* app.py
* VIU/actions.py

**Running the Flask Web App Server -**<br>
```bash
cd VIUProject-master
Python app.py
```
**Running the RASA server -**<br>
```bash
cd VIU
rasa run -m models --endpoints endpoints.yml --port 5002 --credentials credentials.yml
rasa run actions
```
**Once Web server and RASA server start access the application on Google Chrome - http://localhost:5000/detection**<br>

