# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

import MySQLdb
from datetime import datetime
import bs4
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
import requests
import json

hostname = "localhost"
username = "root"
password = "ArAl2799"
DBName = "VIU"
class ActionFindLocation(Action):

    def name(self) -> Text:
        return "action_findObject"     

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        try: 
            db = MySQLdb.connect(hostname,username,password,DBName) 
        # If connection is not successful 
        except: 
            print("Can't connect to database") 
            return 0
        # If Connection Is Successful 
        print("Connected")
        
        cursor = db.cursor()
        object_name = tracker.get_slot('object')
        color = tracker.get_slot('color')

        if (color == None):
            print(object_name)
            query= "select object_location from VIU.Objects where object_name='"+object_name+"'"
            print(query)
            cursor.execute(query)
            result1 = cursor.fetchone() 
            print(result1)
            if(result1 == None):
                result = "None"
            else:
                result = result1[0]
        elif(color == None and object_name == None):
            result = "None"
            dispatcher.utter_message("Sorry not able to detect the object. Please ask again. ")
        else:
            print(color)
            print(object_name)
            query= "select object_location from VIU.Objects where object_name='"+object_name+"' AND object_color='"+color+"'"
            print(query)
            cursor.execute(query)
            result1 = cursor.fetchone() 
            print(result1)
            if(result1 == None):
                result = "None"
            else:
                result = result1[0]
            
            
        db.close()
        if(result == "None"): 
            dispatcher.utter_message("Sorry not able to detect the "+ object_name+". ")
        elif(result == "Front"): 
            dispatcher.utter_message("The "+ object_name +" is in "+ result +" of you. ")
        else:
           dispatcher.utter_message("The "+ object_name +" is on your "+ result+". ")

        return [SlotSet("location", result if result is not None else [])]

class ActionFindColor(Action):

    def name(self) -> Text:
        return "action_findColor"     

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        try: 
            db = MySQLdb.connect(hostname,username,password,DBName) 
        # If connection is not successful 
        except: 
            print("Can't connect to database") 
            return 0
        # If Connection Is Successful 
        print("Connected")
        
        cursor = db.cursor()
        object_name = tracker.get_slot('object')
        # color = tracker.get_slot('color')

        print(object_name)
        query= "select object_color from VIU.Objects where object_name='"+object_name+"'"
        print(query)
        cursor.execute(query)
        result1 = cursor.fetchone() 
        print(result1)
        if(result1 == None):
            result = "None"
        else:
            result = result1[0]
            
        db.close()
        if(result != "None"): 
            dispatcher.utter_message("The color of "+ object_name +" is "+ result+". ")
        else:
            dispatcher.utter_message("Sorry not able to recognize the color on"+ object_name+". ")

        return [SlotSet("color", result if result is not None else [])]

class ActionFindCount(Action):

    def name(self) -> Text:
        return "action_findCount"     

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        try: 
            db = MySQLdb.connect(hostname,username,password,DBName) 
        # If connection is not successful 
        except: 
            print("Can't connect to database") 
            return 0
        # If Connection Is Successful 
        print("Connected")
        
        cursor = db.cursor()
        object_name = tracker.get_slot('object')
        color = tracker.get_slot('color')

        if (color == None and object_name == None):
            result = "None"
        elif (color == None):
            print(object_name)
            query= "select COUNT(object_name) from VIU.Objects where object_name='"+object_name+"'"
            print(query)
            cursor.execute(query)
            result1 = cursor.fetchone() 
            print(result1)
            if(result1 == None):
                result = "None"
            else:
                result = result1[0]
        else:
            print(color)
            print(object_name)
            query= "select COUNT(object_name) from VIU.Objects where object_name='"+object_name+"' AND object_color='"+color+"'"
            print(query)
            cursor.execute(query)
            result1 = cursor.fetchone() 
            print(result1)
            if(result1 == None):
                result = "None"
            else:
                result = result1[0]
                print(result)
            
        db.close()
        if(result == "None" or result == 0 ):
            dispatcher.utter_message("Sorry there are no "+ object_name+"s.")
        elif(result == 1):
            dispatcher.utter_message("There is "+ str(result)+" "+ object_name+". ")
        elif(result >= 2):
            dispatcher.utter_message("There are "+ str(result)+" "+ object_name+"s.")

        return [SlotSet("count", result if result is not None else [])]

class ActionTime(Action):

    def name(self) -> Text:
        return "action_Time"     

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # datetime object containing current date and time
        now = datetime.now()
        
        t = now.strftime("%H : %M")
        dispatcher.utter_message("The current time is "+t+". ")
	
        return [SlotSet("location", None),SlotSet("count", None),SlotSet("object", None),SlotSet("color", None)]

class ActionDate(Action):

    def name(self) -> Text:
        return "action_Date"     

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # datetime object containing current date and time
        now = datetime.now()

        d = now.strftime("%d %B, %Y")
        dispatcher.utter_message("Today's date is "+d+". ")
    
        return [SlotSet("location", None),SlotSet("count", None),SlotSet("object", None),SlotSet("color", None)]

class ActionDateTime(Action):

    def name(self) -> Text:
        return "action_DateTime"     

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        now = datetime.now()
        
        d = now.strftime("%d %B, %Y ")
        t = now.strftime("%H:%M")
        dispatcher.utter_message("Today's date is "+d+" and current time is "+t+". ")
	
        return [SlotSet("location", None),SlotSet("count", None),SlotSet("object", None),SlotSet("color", None)]

class ActionNews(Action):

    def name(self) -> Text:
        return "action_News"     

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        news_url="https://news.google.com/news/rss"
        Client=urlopen(news_url)
        html=Client.read()
        Client.close()

        soup_page=soup(html,"html.parser")
        news_list=soup_page.findAll("item")

        dispatcher.utter_message("Today's news headlines")
        for news in news_list:
            dispatcher.utter_message(news.title.text+".")
	
        
        return [SlotSet("location", None),SlotSet("count", None),SlotSet("object", None),SlotSet("color", None)]

class ActionWeather(Action):

    def name(self) -> Text:
        return "action_Weather"     

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        send_url = 'http://api.ipstack.com/94.204.20.52?access_key=a387dd3331a81374a9bfed531568a95f&output=json&legacy=1'
        r = requests.get(send_url)
        j = json.loads(r.text)
        lat = j['latitude']
        lon = j['longitude']

        API_key = "929ba396137145ac373aebaecd1bf02f"
        base_url = "http://api.openweathermap.org/data/2.5/weather?"

        latitude = lat
        longitude = lon

        Final_url = base_url + "appid=" + API_key + "&lat=" + str(latitude) + "&lon=" + str(longitude)
        weather_data = requests.get(Final_url)
        w = json.loads(weather_data.text)

        Temprature = w['main']['temp']
        WeatherType = w['weather'][0]['description']
        Temprature =  Temprature - 273.15
        Temprature = ("%.2f" % round(Temprature, 2))
        
        dispatcher.utter_message("The outside temprature is "+ str(Temprature) +" degree celsius and today the weather is " +WeatherType+"." )
        return [SlotSet("location", None),SlotSet("count", None),SlotSet("object", None),SlotSet("color", None)]

class ActionRecognizePerson(Action):

    def name(self) -> Text:
        return "action_RecognizePerson"     

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        try: 
            db = MySQLdb.connect(hostname,username,password,DBName)  
        # If connection is not successful 
        except: 
            print("Can't connect to database") 
            return 0
        # If Connection Is Successful 
        print("Connected")
    
        cursor = db.cursor()

        query= "select COUNT(*) from VIU.People;"
        cursor.execute(query)
        result1 = cursor.fetchone() 
        Countresult = result1[0]
        if(Countresult == 0):
            dispatcher.utter_message("There is no one known to be recognized. ")
        else:
            query= "select * from VIU.People;"
            cursor.execute(query)
            result = cursor.fetchone() 
            if(Countresult == 1): 
                person = result[0]
                dispatcher.utter_message(person+" is in front of you. ")
            elif(Countresult == 2):
                resultall = cursor.fetchall() 
                Tresult = str(result[0])+" and "
                for p in resultall:
                    result = str(p[0])
                    Tresult = Tresult + result
                dispatcher.utter_message(Tresult+" are in front of you. ") 
            else:
                resultall = cursor.fetchall() 
                Tresult = str(result[0])+", "
                i=0
                for p in resultall:
                    i=i+1
                    if( i == len(resultall)-1):
                        result = str(p[0])+" and "
                        Tresult = Tresult + result
                    else:
                        result = str(p[0])+", "
                        Tresult = Tresult + result
                dispatcher.utter_message(Tresult+" are in front of you. ")

        db.close()
        return [SlotSet("location", None),SlotSet("count", None),SlotSet("object", None),SlotSet("color", None)]

class ActionRead(Action):

    def name(self) -> Text:
        return "action_Read"     

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

            try: 
                db = MySQLdb.connect(hostname,username,password,DBName)  
                # If connection is not successful 
            except: 
                print("Can't connect to database") 
                return 0
            # If Connection Is Successful 
            print("Connected")
        
            cursor = db.cursor()

            query= "select COUNT(*) from VIU.TextInfo;"
            cursor.execute(query)
            result1 = cursor.fetchone() 
            Countresult = result1[0]
            if(Countresult == 0):
                dispatcher.utter_message("There is no text to read or unable to detect. Try again. ")
            else:
                query= "select * from VIU.TextInfo;"
                cursor.execute(query)
                result = cursor.fetchone() 
                if(Countresult == 1): 
                    text = result[0]
                    dispatcher.utter_message(text+".")
                elif(Countresult == 2):
                    resultall = cursor.fetchall() 
                    Tresult = str(result[0])+" and "
                    for p in resultall:
                        result = str(p[0])
                        Tresult = Tresult + result
                    dispatcher.utter_message(Tresult+". ") 
                else:
                    resultall = cursor.fetchall() 
                    Tresult = str(result[0])+", "
                    i=0
                    for p in resultall:
                        i=i+1
                        if( i == len(resultall)-1):
                            result = str(p[0])+" and "
                            Tresult = Tresult + result
                        else:
                            result = str(p[0])+", "
                            Tresult = Tresult + result
                    dispatcher.utter_message(Tresult+". ")
            db.close()
            return [SlotSet("location", None),SlotSet("count", None),SlotSet("object", None),SlotSet("color", None)]

        
class ActionResestSlot(Action):

    def name(self) -> Text:
        return "action_resetSlots"     

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        return [SlotSet("location", None),SlotSet("count", None),SlotSet("object", None),SlotSet("color", None)]