import glob
import os
import re
import math
from parser1 import parseTokensFromText
import json
import pickle
import os
document="C://TweetStudy//12//12//"
extend="00*.dat"
filename="C://TweetStudy//12//12//textdump.txt"
text={}
os.chdir(document)
file1 = open(filename, "+a")
for file in glob.glob(extend):
    f=open(file,'r', encoding='utf-8',errors='ignore')
    for line in f:
        line_object=json.loads(line)
        tweet_text = line_object['text']
        tweet_id =file + line_object['id_str']
       
        file1.write(tweet_id+":"+re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",tweet_text)+"\n" )                  

file1.close()
