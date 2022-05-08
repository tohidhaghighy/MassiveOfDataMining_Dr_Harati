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
# لیست مقادیر هش شده
hasharray=[]
# لیست مقادیر در چه داکیومنت های است
arraylistofdoc=[]

#لیست فایل های داخل دایرکتوری
for j in newlist:
    file1 = open("docs/"+ str(j) +"","r+")
    array1 = []
    # تا بع توکن برای جدا کردن کلمات یک فایل
    for token in tokenize(file1.read().lower()):
        kind,txt,val = token
        # برای اینکه نقطه و ویرگول رو کلمه به حساب نیاورد
        if txt !=None and txt!="." and txt!=",":
            array1.append(txt)
    # ساخت جملات با شینگل های دریافتی از ورودی
    for shingle in range(len(array1)-(num-1)):
        strshin=""
        for count in range(shingle ,shingle + num):
            strshin=strshin+' '+array1[count]
        # هش کردم جملات شینگل
        hashvalue = int(hashlib.sha256(strshin.encode('utf-8')).hexdigest(), 16) % 10**8
        # اینجا برای این است که تکراری ها حذف و فقط مقادیر فایل ان نگه داری شود
        if hashvalue not in hasharray:
            hasharray.append(hashvalue)
            arraylistofdoc.append(str(j))
        else :
            for f in range(len(hasharray)):
                if hasharray[f]==hashvalue:
                    arraylistofdoc[f]=arraylistofdoc[f]+" "+str(j)
                    
print(hasharray)
print(arraylistofdoc)



