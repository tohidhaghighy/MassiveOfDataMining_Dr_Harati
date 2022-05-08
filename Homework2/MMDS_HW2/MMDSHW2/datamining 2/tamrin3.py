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

hasharray=[]
arraylistofdoc=[]
allhashes=[]
arraylistnumber=[]
countnum=0
for j in newlist:
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
        allhashes.append(strshin)
        hashvalue = int(hashlib.sha256(strshin.encode('utf-8')).hexdigest(), 16) % 10**8
        if hashvalue not in hasharray:
            hasharray.append(hashvalue)
            arraylistofdoc.append(str(j))
            countnum=countnum+1
            arraylistnumber.append(countnum)
        else :
            for f in range(len(hasharray)):
                if hasharray[f]==hashvalue:
                    arraylistofdoc[f]=arraylistofdoc[f]+" "+str(j)

print(arraylistofdoc)
arraynumber1=[]
# h1 = x + 1
for num1 in arraylistnumber:
    arraynumber1.append((num1+1)%countnum)

arraynumber2=[]
# h1 = 2x + 3
for num1 in arraylistnumber:
    arraynumber2.append(((2*num1)+3)%countnum)



#print(arraynumber1)
#print(arraynumber2)

newlistcount1=0
# پیدا کردن ارایه ترکیبی از ارایه 1
#تعریف کردن یک ارایه تمام صفر برای تعریف کردن یک ارایه تمام صفر
arrayresponse=np.zeros(len(newlist)+1, dtype = int)
#شروع خط به خط کلمات بر اساس کلمات از اولین تا اخرین
for signitur in range(len(arraynumber1)):
    # یافتن فایل هایی که ان کلمه در ان است
    number1s=arraylistofdoc[signitur].split()
    #حذف تکراری ها در بین فایل ها یعنی یک کلمه در یک فایل ممکن است چند بار تکرار شود
    number1swithoutreapet=list(set(number1s))
    #هر جا کلمه در فایل بود بس مقدارش 1 است پس مقدار ان را در ارایه جایگزین میکنیم
    for splinum in number1swithoutreapet:
        if int(arrayresponse[int(splinum)]) == 0:
            arrayresponse[int(splinum)]=int(arraynumber1[signitur])


# پیدا کردن ارایه ترکیبی از ارایه 2     
#تعریف کردن یک ارایه تمام صفر برای تعریف کردن یک ارایه تمام صفر
arrayresponse1=np.zeros(len(newlist)+1, dtype = int)
#شروع خط به خط کلمات بر اساس کلمات از اولین تا اخرین
for signitur in range(len(arraynumber2)):
    # یافتن فایل هایی که ان کلمه در ان است
    number2s=arraylistofdoc[signitur].split()
    #حذف تکراری ها در بین فایل ها یعنی یک کلمه در یک فایل ممکن است چند بار تکرار شود
    number2swithoutreapet=list(set(number2s))
    #هر جا کلمه در فایل بود بس مقدارش 1 است پس مقدار ان را در ارایه جایگزین میکنیم
    for splinum in number2swithoutreapet:
        if int(arrayresponse1[int(splinum)]) == 0:
            arrayresponse1[int(splinum)]=int(arraynumber2[signitur])

        
print(arrayresponse1)
print(arrayresponse)

