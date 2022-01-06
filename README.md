# Encodation (Praw encode/decode bot)


##For info on how to use the bot please read the [docs](https://github.com/JakeWasChosen/RedditEncodationBot/blob/master/docs/HowToUse.md)
Encode/decode text using a commandline style syntax

Going into a little more detail the script will:

1. Query Reddit for an amount of posts (25 by default)
2. Sift through the reddit posts finding direct image links and imgur posts/albums
3. Extract all image links from any imgur albums found and add them to the link pool
4. Check whether any of the links has been downloaded before, sorting out those who has
5. Download all the now sorted links
6. Go through all downloaded images deleting images smaller than the minimum size, and those with a different aspect ratio


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
* add a subreddit blacklist
* make the log syntax better (line where the error happened/more details)

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
