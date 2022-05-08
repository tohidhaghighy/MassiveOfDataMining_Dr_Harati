import os
import sys
import pandas as pd
import numpy as np
import math
import hashlib
from nltk import ngrams
from tokenizer import tokenize,TOK

all_files = os.listdir('docs/')
#print(all_files)

newlist=[]
for skk in all_files:
    if skk!=".DS_Store":
        newlist.append(int(skk))
    
newlist.sort()
#print(newlist)
shingl=input("Insert shingling length : ")
num=int(shingl)

listofitems=[]

#لیست فایل های داخل دایرکتوری
for j in newlist:
    hasharray=[]
    #تبدیل توابع به لیستی از کلمات
    file1 = open("docs/"+ str(j) +"","r+")
    array1 = []
    for token in tokenize(file1.read().lower()):
        kind,txt,val = token
        if txt !=None and txt!="." and txt!=",":
            array1.append(txt)
    for shingle in range(len(array1)-(num-1)):
        strshin=""
        for count in range(shingle ,shingle + num):
            strshin=strshin+' '+array1[count]
        hasharray.append(strshin)       
    print(hasharray)






