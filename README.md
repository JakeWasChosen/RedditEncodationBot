# Encodation (Praw encode/decode bot)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License: MIT](https://img.shields.io/badge/License-MIT-314e9f.svg)](https://opensource.org/licenses/MIT)
## For info on how to use the bot please read the [docs](https://github.com/JakeWasChosen/RedditEncodationBot/blob/master/docs/HowToUse.md)

Encode/decode text using a commandline style syntax

Going into a little more detail the script will:

1. Wait until somebody mentions it, or it gets a private message
2. If the pm contains unsubscribe it adds the user to a 'blacklist' so no matter what the user sends it doesn't reply
3. It checks if the user is on a blacklist if not it parses the arguments the user sends
4. (TODO) it calls the logic()  function and checks if the question has been asked before using a LRU cache
5. If not then it encodes/decodes the text and adds it the LRU cache
6. Replys to the user with the appropriate response


Inspiration was drawn from another project of mine [edoC](https://github.com/JakeWasChosen/edoC)

#### Features
* Encode or decode in
   - base32
   - base64
   - base85
   - rot13
   - hex
   - ascii85
   - morse
   - binary
   * with more to come
* ability to unsubscribe
* a blacklist

#todo
* (MAYBE) integrate Bella into this somehow
* Add a check whenever you add a new user into the blacklist and keep the more severe offence (maybe in a later commit)

## Install process
1. Download and install python from https://www.python.org/ (If you're unsure download version 3.5 and chose default install)
2. Clone or download/extract the repository
3. Install requirements with
```
py -m pip install -r requirements.txt
```
(You might have to use python or python3 instead of py depending on your system/install)
4. Fill out the data in settings.env.example 
5. rename it to settings.env

### Setting up your settings.env file
The new version of praw requires you to identify the script before you can use it, this is fortunately quite easy, just follow the steps below.
1. Go to [this page on reddit](https://www.reddit.com/prefs/apps/) (you might have to log in)
2. Scroll down to the bottom and click the "Create another app" button
3. Tick off 'script' and fill out the remaining boxes
4. You'll now be able to see your app in the list
5. Open your settings.env file in your favourite text editor
6. Replace CLIENT_ID with the weird line of characters under the "personal use script" label, keep the quotations
7. Repeat step 6 for the CLIENT_SECRET field, this time using the characters next to the "secret"
8. The rest are labed in the file / i'm too lazy too fill out the rest

#### Requirements
read requirements.txt 

## Usage
The script can be run by running main.py
