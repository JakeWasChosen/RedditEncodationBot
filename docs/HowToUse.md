#Arguments


#base:
--e / --encode
--d / --decode
  

#addional
type: base32,  aliases: b32, Description: Encode/Decode in base32


type: base64, aliases: b64, Description: Encode/Decode in base64


type: rot13, aliases: r13, Description: Encode/Decode in rot13


type: hex, Description: Encode/Decode in hex


type: base85, aliases: b85, Description: Encode/Decode in base85


type: ascii85, aliases: a85, description: Encode/Decode in ASCII85


type: morse, Description: Encode/Decode in morse code


type: binary, aliases: b, Description: Encode/Decode in binary
                                  



#notes:
links do not work with url shorteners
links only work with pastebin/github gists or any website that has a raw page or direct text file


### Optional arguments
* -con or --config enter configuration mode
* --subreddit \<subreddit> or -s \<subreddit> specify which subreddit to download images from, omit the /r/ (default is wallpapers)
* --limit \<number> or -l \<number> specify how many posts to search as a whole number (default is 25)
* --threads \<number> or -t \<number> specify how many download threads to spawn
* --re or -r will try to re download every post previously downloaded
* --nc or --noclean don't delete small images
* --ns or --nosort skip sorting out previosuly downloaded images
* --na or --noalbum skip imgur albums
* --log save a log of posts skipped
* --verbose or -v print skipped posts to console
* --section or -se \<section> Specify which section you want to scrape (hot, new, top, rising)
* --ratiolock or -rlock \<lock strength> Lock downloaded images to a certain aspect ratio, the value of the lock will determine the allowed margin of error, 0 for no lock, 1 for fully locked (only exactly matching aspect ratios), I recommend a value between 0.9 and 1 for decent results.
* --search or -q \<query> scrape all search results of chosen subreddit