<!-- Find Location -->
## A_path
* greet
  - utter_greet
  - utter_assistance
* search_object
  - action_findObject
  - utter_did_that_help
* affirm
  - utter_happy
  - utter_moreAssistance
* reading_text
  - action_Read
  - utter_moreAssistance
* goodbye
  - utter_goodbye

## B_path
* greet
  - utter_greet
  - utter_assistance
* search_object{"color": "red", "object": "cup"}
  - slot{"color": "red"}
  - slot{"object": "cup"}
  - action_findObject
  - slot{"location": ["center"]}
  - utter_did_that_help
  - action_resetSlots
  - slot{"location": ["None"],"color": ["None"] , "object": ["None"],"count": [0]}
* deny
  - utter_assistance
* search_object
  - action_findObject
  - utter_did_that_help
* goodbye
  - utter_goodbye



## C_path
* greet
    - utter_greet
    - utter_assistance
* reading_text
  - action_Read
  - utter_moreAssistance
* search_object{"color": "red", "object": "cup"}
    - slot{"color": "red"}
    - slot{"object": "cup"}
    - action_findObject
    - slot{"location": ["center"]}
    - utter_did_that_help
    - action_resetSlots
    - slot{"location": ["None"],"color": ["None"] , "object": ["None"],"count": [0]}
* search_object{"color": "yellow", "object": "banana"}
    - slot{"color": "yellow"}
    - slot{"object": "banana"}
    - action_findObject
    - slot{"location": ["left"]}
    - utter_moreAssistance
    - action_resetSlots
    - slot{"location": ["None"],"color": ["None"] , "object": ["None"],"count": [0]}
* date_time
  - action_DateTime
  - utter_moreAssistance
* reading_text
  - action_Read
  - utter_moreAssistance
* search_object{"object": "banana"}
    - slot{"object": "banana"}
    - action_findObject
    - slot{"location": ["left"]}
    - utter_did_that_help
    - action_resetSlots
    - slot{"location": ["None"],"color": ["None"] , "object": ["None"],"count": [0]}
* search_object{"object": "banana"}
    - slot{"object": "banana"}
    - action_findObject
    - slot{"location": ["left"]}
    - utter_did_that_help
    - action_resetSlots
    - slot{"location": ["None"],"color": ["None"] , "object": ["None"],"count": [0]}
* deny
    - utter_assistance
* goodbye
    - utter_goodbye

## D_path
* greet
    - utter_greet
    - utter_assistance
* search_object{"object": "banana"}
    - slot{"object": "banana"}
    - action_findObject
    - slot{"location": ["top left"]}
    - utter_did_that_help
    - action_resetSlots
    - slot{"location": ["None"],"color": ["None"] , "object": ["None"],"count": [0]}
* search_object{"object": "cup"}
    - slot{"object": "cup"}
    - action_findObject
    - slot{"location": ["left"]}
    - utter_moreAssistance
    - action_resetSlots
    - slot{"location": ["None"],"color": ["None"] , "object": ["None"],"count": [0]}
* search_object{"color": "red","object": "cup"}
    - slot{"object": "cup"}
    - action_findObject
    - slot{"location": ["right"]}
    - action_resetSlots
    - slot{"location": ["None"],"color": ["None"] , "object": ["None"],"count": [0]}
    - utter_goodbye
* weather
    - action_Weather
    - utter_moreAssistance
* search_object{"object": "banana"}
    - slot{"object": "banana"}
    - action_findObject
    - slot{"location": ["bottom left"]}
    - action_resetSlots
    - slot{"location": ["None"],"color": ["None"] , "object": ["None"],"count": [0]}
* deny
    - utter_assistance
* goodbye
    - utter_goodbye


<!-- Find Color -->

## Color_path
* greet
  - utter_greet
  - utter_assistance
* weather
    - action_Weather
    - utter_moreAssistance
* person_recognize
    - action_RecognizePerson
    - utter_moreAssistance
* search_object{"object": "cup"}
  - slot{"object": "cup"}
  - action_findObject
  - slot{"location": ["center"]}
  - utter_did_that_help
* object_color {"object": "cup"}
  - slot{"object": "cup"}
  - action_findColor
  - slot{"color": ["blue"]}
  - utter_assistance
  - action_resetSlots
  - slot{"location": ["None"],"color": ["None"] , "object": ["None"],"count": [0]}
* deny
  - utter_assistance
* search_object
  - action_findObject
  - utter_did_that_help
  - utter_moreAssistance
* object_color
  - action_findColor
  - utter_moreAssistance
* reading_text
  - action_Read
  - utter_moreAssistance
* goodbye
  - utter_goodbye



## E_path
* greet
    - utter_greet
    - utter_assistance
* object_color {"object": "cup"}
    - slot{"object": "cup"}
    - action_findColor
    - slot{"color": ["blue"]}
    - utter_moreAssistance
    - action_resetSlots
    - slot{"location": ["None"],"color": ["None"] , "object": ["None"],"count": [0]}
* search_object{"object": "banana"}
    - slot{"object": "banana"}
    - action_findObject
    - slot{"location": ["left"]}
    - utter_did_that_help
    - action_resetSlots
    - slot{"location": ["None"],"color": ["None"] , "object": ["None"],"count": [0]}
* date
    - action_Date
    - utter_moreAssistance
* reading_text
  - action_Read
  - utter_moreAssistance
* person_recognize
    - action_RecognizePerson
    - utter_moreAssistance
* object_color{"object": "banana"}
    - slot{"object": "banana"}
    - action_findColor
    - slot{"color": ["green"]}
    - utter_did_that_help
    - action_resetSlots
    - slot{"location": ["None"],"color": ["None"] , "object": ["None"],"count": [0]}
* deny
    - utter_assistance
* goodbye
    - utter_goodbye


<!-- Find Count -->

## Count_path
* greet
  - utter_greet
  - utter_assistance
* date
  - action_Date
  - utter_moreAssistance
* person_recognize
    - action_RecognizePerson
    - utter_moreAssistance
* reading_text
  - action_Read
  - utter_moreAssistance
* search_object{"object": "cup"}
  - slot{"object": "cup"}
  - action_findObject
  - slot{"location": ["center"]}
  - utter_did_that_help
* object_color {"object": "cup"}
  - slot{"object": "cup"}
  - action_findColor
  - slot{"color": ["blue"]}
  - utter_moreAssistance
* object_count {"object": "cup", "color": ["blue"] }
  - slot{"object": "cup"}
  - action_findCount
  - slot{"count":[3]}
  - utter_moreAssistance
  - action_resetSlots
  - slot{"location": ["None"],"color": ["None"] , "object": ["None"],"count": [0]}
* deny
  - utter_assistance
* goodbye
  - utter_goodbye



## F_path
* greet
    - utter_greet
    - utter_assistance
* object_count {"object": "cup"}
    - slot{"object": "cup"}
    - action_findCount
    - slot{"count": [2]}
    - utter_moreAssistance
    - action_resetSlots
    - slot{"location": ["None"],"color": ["None"] , "object": ["None"], "count": [0]}
* search_object{"object": "banana"}
    - slot{"object": "banana"}
    - action_findObject
    - slot{"location": ["left"]}
    - utter_did_that_help
* reading_text
  - action_Read
  - utter_moreAssistance
* object_color{"object": "banana"}
    - slot{"object": "banana"}
    - action_findColor
    - slot{"color": ["yellow"]}
    - utter_did_that_help
    - utter_moreAssistance
* person_recognize
    - action_RecognizePerson
    - utter_moreAssistance
* latest_news
    - action_News
    - utter_moreAssistance
* reading_text
  - action_Read
  - utter_moreAssistance
* object_count {"object": "banana"}
    - slot{"object": "banana"}
    - action_findCount
    - slot{"count": [2]}
    - utter_moreAssistance
    - action_resetSlots
    - slot{"location": ["None"],"color": ["None"] , "object": ["None"], "count": [0]}
* deny
    - utter_assistance
* goodbye
    - utter_goodbye

## G_path
* greet
    - utter_greet
    - utter_assistance
* object_count{"object": "bottle"}
    - slot{"object": "bottle"}
    - action_findCount
    - utter_moreAssistance
    - action_resetSlots
    - slot{"location": null}
    - slot{"count": null}
    - slot{"object": null}
    - slot{"color": null}
* person_recognize
    - action_RecognizePerson
    - utter_moreAssistance
* reading_text
  - action_Read
  - utter_moreAssistance
* object_count{"object": "bottle"}
    - slot{"object": "bottle"}
    - action_findCount
    - slot{"count": 0}
    - utter_moreAssistance
    - action_resetSlots
    - slot{"location": null}
    - slot{"count": null}
    - slot{"object": null}
    - slot{"color": null}
* person_recognize
    - action_RecognizePerson
    - utter_moreAssistance
* object_count{"object": "person"}
    - slot{"object": "person"}
    - action_findCount
    - slot{"count": 4}
    - utter_moreAssistance
    - action_findObject
    - slot{"location": "Left"}
    - utter_did_that_help
* object_color
    - action_findColor
    - slot{"color": "pink"}
    - utter_assistance
    - action_resetSlots
    - slot{"location": null}
    - slot{"count": null}
    - slot{"object": null}
    - slot{"color": null}
* reading_text
  - action_Read
  - utter_moreAssistance
* object_count{"color": "white"}
    - slot{"color": "white"}
    - action_findCount
    - utter_assistance
    - action_resetSlots
    - slot{"location": null}
    - slot{"count": null}
    - slot{"object": null}
    - slot{"color": null}
* object_count{"color": "white", "object": "cat"}
    - slot{"color": "white"}
    - slot{"object": "cat"}
    - action_findCount
    - slot{"count": 1}
    - utter_assistance
    - action_resetSlots
    - slot{"location": null}
    - slot{"count": null}
    - slot{"object": null}
    - slot{"color": null}
* person_recognize
    - action_RecognizePerson
    - utter_moreAssistance
* latest_news
    - action_News
    - utter_moreAssistance
* object_count{"color": "white"}
    - slot{"color": "white"}
    - action_findCount
    - slot{"count": 3}
    - utter_moreAssistance
    - action_resetSlots
    - slot{"location": null}
    - slot{"count": null}
    - slot{"object": null}
    - slot{"color": null}
* goodbye
    - utter_goodbye

## H_path
* greet
    - utter_greet
    - utter_assistance
* object_count{"object": "bottle"}
    - slot{"object": "bottle"}
    - action_findCount
    - utter_moreAssistance
    - action_resetSlots
    - slot{"location": null}
    - slot{"count": null}
    - slot{"object": null}
    - slot{"color": null}
* date
    - action_Date
    - utter_moreAssistance
* object_count{"object": "person"}
    - slot{"object": "person"}
    - action_findCount
    - slot{"count": 4}
    - utter_moreAssistance
    - action_findObject
    - slot{"location": "Left"}
    - utter_did_that_help
* time
    - action_Time
    - utter_moreAssistance
* reading_text
  - action_Read
  - utter_moreAssistance
* object_count{"color": "white"}
    - slot{"color": "white"}
    - action_findCount
    - utter_moreAssistance
    - action_resetSlots
    - slot{"location": null}
    - slot{"count": null}
    - slot{"object": null}
    - slot{"color": null}
* date_time
    - action_DateTime
    - utter_moreAssistance
* object_count{"object": "person"}
    - slot{"object": "person"}
    - action_findCount
    - slot{"count": 4}
    - utter_moreAssistance
    - action_findObject
    - slot{"location": "Left"}
    - utter_did_that_help
* weather
    - action_Weather
    - utter_moreAssistance
* goodbye
    - utter_goodbye
