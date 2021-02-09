# Indeed Job Bot
This program was designed and created by me using selenium and python

## Setup

To run this bot, you must install the requirements from the requirements.txt file
```bash
pip install -r requirements.txt
```

Enter your username, password and modify the timeout value if needed in the `config.py` file

```
main_page = '***' Default main page. no need to change

username = '' Add your username here
password = '' Add your password here

job_urls = ['',	Add as many job URLS as you like. the code will cycle through all of them.
'',
'',
....,]

questionAndAnswer['', Huge list of questions asked by indeed. Change them to fit your experience.
]

```
__NOTE: AFTER EDITING CONFIG.PY, DO NOT COMMIT THE FILE__

__NOTE: This program does not upload or store your username/password anywhere else. I will never get any passwords from this program.__


## Execute  

To execute the bot, run the following in the terminal

```
python3 easyappybot.py

OR

easyappybot.py
```

### Parameters  

```
-h 		for parameter help
-s 		Tells the bot where to start in the job search. Multiples of 25
-u		Tells the bot to search only with a specific URL (starts at 0)
-slow	Tells the bot to increase the sleep times due to slow internet
```

## Running  

This bot will begin by going to the main_url ,indeed.com, and clicking the login button. 
It will then enter the stored username and password values in the `config.py` file.
After this the bot will start the jobs search with either the first URL stored or a 
desired URL given with `-u`. The bot will scroll to the bottom of every page to appear 
human and click on the apply button if possible. The bot will then go through each question
and attempt to input an answer if it has it stored. If not, the bot will quit that application
and move on.

## Contact Information
Joseph D Cantrell
JosephCantrell@josephdcantrell.com