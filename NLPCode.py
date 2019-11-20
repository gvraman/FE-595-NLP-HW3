# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 22:28:26 2019

@author: gaura
"""

import os
import zipfile
from pathlib import Path
directory=os.getcwd()
file_path = Path(directory)  #setting the working directory
if file_path.exists():
    folder = os.path.join(directory, 'Combined')
    os.mkdir('Extracted')   # creating new folder for extracted files
    dest = os.path.join(directory, 'Extracted')
    os.chdir(folder)

# Unzip all files and store it in Extracted folder
    for file in os.listdir(folder):
        f,e = file.split(".")
        if file.endswith(".zip"):
            file_name = os.path.abspath(file)
            new = os.path.join(dest, f)
            os.mkdir(new)
            zip_ref = zipfile.ZipFile(file_name) 
            zip_ref.extractall(new) 
            zip_ref.close() 
    os.chdir(directory)
    os.chdir(dest)
    read_files = []
    for root, dirs, files in os.walk(dest):
        if "__MACOSX" in root.split("\\") :
            continue
        for file in files:
            if file.endswith(".txt"):
                read_files.append(os.path.join(root, file))
    os.chdir(directory)
    with open("combined.txt", "wb") as outfile:
        for f in read_files:
            with open(f, "rb") as infile:
                outfile.write(infile.read())
    with open("MaleHeroes.txt", "wb") as male:
        with open("combined.txt",'rb') as fp:
            for line in fp:
                if  b"He's" in line:
                    male.write(line)
    with open("FemaleHeroes.txt", "wb") as female:
        with open("combined.txt",'rb') as fp:
            for line in fp:
                line = line.replace(b"\\",b"")
                if  b"She's" in line:
                    female.write(line)
else:
    print("No such directory!")

# Sentiment Analysis
from textblob import TextBlob
import pandas as pd

'''
Combined_data = pd.read_csv("combined.txt", sep = "\n", header = None)
Combined_data.columns = ["Text"]
'''

#Creating data frames to store the text files
M_data = pd.read_csv("MaleHeroes.txt", sep ="\n", header = None)
M_data.columns = ["Text"]

F_data = pd.read_csv("FemaleHeroes.txt", sep ="\n", header = None)
F_data.columns = ["Text"]

#Function to return sentiment polarity of each observation of textblob
def sentiment_calc(text):
    try:
        return TextBlob(text).sentiment[0]
    except:
        return None
'''
def text_blob(text):
    try:
        return TextBlob(text)
    except:
        return None
#Combined_data["TextBlob"] = Combined_data["Text"].apply(text_blob)
'''

#Computing top and bottom results for sentiment
M_data["Sentiment"] = M_data["Text"].apply(sentiment_calc)
M_data_sorted = M_data.sort_values("Sentiment")
Bottom_M = M_data_sorted["Text"].head(10)
Top_M = M_data_sorted["Text"].tail(10)

F_data["Sentiment"] = F_data["Text"].apply(sentiment_calc)
F_data_sorted = F_data.sort_values("Sentiment")
Bottom_F = F_data_sorted["Text"].head(10)
Top_F = F_data_sorted["Text"].tail(10)


#Writing all the ouputs to text files
Top_M.to_csv(r'Top10_Male.txt', header=None, index=None, sep=',')
Bottom_M.to_csv(r'Bottom10_Male.txt', header=None, index=None, sep=',')
Top_F.to_csv(r'Top10_Female.txt', header=None, index=None, sep=',')
Bottom_F.to_csv(r'Bottom10_Female.txt', header=None, index=None, sep=',')


#Computing most common descriptors
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize 
from collections import Counter

newStopWords = ["He's","She's"]
stopwords = set(stopwords.words('english')) 
for i in newStopWords:
    stopwords.add(i)
    print(i)
file1 = open("combined.txt") 
line = file1.read()
text = line.split()
print(text)
cnt = Counter()

for word in text: 
    if word not in stopwords: 
        cnt[word] += 1

common_words = cnt.most_common(10)
common_words

#Writing the output for common descriptors to a text file
with open("Top10_Descriptors.txt", "w") as descriptors:
    for i in common_words:
        descriptors.write("{}\n".format(i))