# CS50 Tour Telegram Bot
#### Video Demo:  https://youtu.be/NCoMADpFbqs
#### Description:
This is my final project for Harvard CS50x online course.

## README content:

1. Project description
2. Technology stack
3. Installation and run
4. File structure
5. User flows specifications
6. Additional comments


## Project description

This is Telegram bot with 2 functionalities:
- getting forecast for a city you consider to visit;
- filling application for CS50 Tour agents.

Project was made with python 3.9 and aiogram framework for asynchronous Telegram bots. 
It also uses openweathermap free API to get forecast, a little bit of SpaCy library for named entity extraction and SQLite library for database storage.

Summary of forecast user flow:
- name a city;
- specify the date for forecast (3 days from tomorrow);
- wait a moment and receive you forecast; 
- answer if you want to visit the city (navigate to application flow) or not. 

Summary of application user flow:
- name a city you want to visit (if you didn't in frecast flow);
- specify a number of people for tour;
- specify you budget;
- specify approximate start date;
- specify trip duration;
- confirm your name (received from Telegram Bot API) or type correct one;
- type contact phone number;
- confirm your application.


## Technology stack
- Python 3.9
- aiogram: Telegram bot building framework
- SQLite: database management library
- openweathermap.org: free weather API
- SpaCy: named entities extraction library


## Installation and run

Entry point file is **bot.py**.

External dependencies for installation described in requirements.txt.

API key for Telegram bot API can be obtained via https://t.me/BotFather

Weather API key can be obtained at openweathermap.org.

Both Telegram and openweathermap API keys might be stored as venv variables (see bot.py).


## File structure
- **bot.py**: entry point module: 
    + sets API keys (Telegram Bot API and weather API);
    + enables logging;
    + initialize dispatcher (root router) for event handling;
    + includes next router(s);
    + launches bot.
- **/handlers**: modules for handling Telegram events (new messages from user). Files initialise separate routers and contain mostly handler functions.
    + **main_router.py**: handles events without state (when user starts using the bot or returns to main menu), main menu navigation button and unsupported message type error.
    + **forecast.py**: handles messages for all states in forecast flow, such as receiving city name and date.
    + **application.py**: handles messages for all states in application flow, such as receiving city name (if wasn't specified earlier), number of people, budget, trip start date and duration, user full name and phone number and additional comment.
- **/helpers**: helper functions like receiving and formatting forecast, new message filter ect.
    + **get_forecast.py**: contains helper functions for getting forecast data from weather API and formatting it to a proper string.
    + **utils.py**: contains the rest of helper functions, such as retrieving date and phone from user message (with regexp) and saving application to SQL database.
- **/keyboards**: separate storage of keyboard builder functions for every user flow.
    + **general.py**: contains keyboard builder functions for main menu.
    + **forecast.py**: contains keyboard builder functions for each step of forecast flow.
    + **application.py**: contains keyboard builder functions for for each step of application flow.
- **FSM.py**: module for finite state machine initialisation. It contains all states that are used in other modules for forecast and application flows functioning. 
- **application.db**: SQL database for storing applications. Contains empty table "applications.db". Function that maintains connection with database is located in /helpers/utils.py.
- **requirements.txt**: contains all dependencies.


## User flows specifications

### Main menu
- User can choose either forecast or application.
- If user types another command, bot return an error message.
- If user sends a picture, sticker, voice message or another unsupported type of message (not simple text), bot return type error message.
 
### Forecast flow
- User names any city.
    + If user input is longer then 20 characters, bot reprompts city name.
    + If user name 2 or more cities, bot uses only the first one.
- User provides date for forecast.
    + Date must be in range of 3 days from tomorrow. If not, bot reprompts.
- Bot provide forecast for specified city and date.
    + If error occured, bot returns error message and ask to try again with another city.
- Bot asks if user wants to visit the city.
    + If user chooses "yes", navigate to Application flow with the city named earlier.
    + If user chooses "no", offer to type another city.
        + User also can navigate to Application flow from here with a button.

### Application flow
- User names a city if not chosen on forecast flow.
- User provides a number of people.
    + Integer from 1 to 20.
- User provides a budget in US dollars.
    + Not less than $50 per person.
- User provides start date.
    + Not from the past.
- User provides trip duration in days.
    + Integer not more than 30.
- User confirms their username or type correct one.
    + Username is received from Telegram.
    + User can provide any text as name.
- User provides phone number.
    + Must support US phone numbers (10 digits) with spaces and other common characters.
- User confirms the application.
    + Must have a button for starting application from scratch.

User has to have an opportunity to change last answer on every step of filling application.
The must be "main menu" button for every step starting budget choice.


## Addicional comments

1. **Provided code is for development, not for production.** \
Be aware of current limitations: 
- polling mechanism probably should be replaced with webhook; 
- finite state machine data must be stored in storage device (not RAM);
- database connection should be asynchronous.


2. **User experience is not perfect**.\
The project goal was to build my very own Telegram bot using aiogram and API. I didn't care too much about UX yet.


3. **SpaCy named entities extraction is used to extract cities names, but...**  
It ignores a lot of towns and even big cities, so I decided to use it as additional tool. User can still write any text as city. I am going to improve city extraction later. 
