import os
import numpy as np
import pandas as pd
from LSH import LSH

allfiles=os.listdir('docs/')

all_text=[]

# for i in range(1,436):
#     a = pd.read("docs/"+str(i),sep="\t", header=None)
#     all_text.append(a.iloc[0].values)

# shing=LSH()
# print(all_text[5])
# shing.make_matrix(al_text)
for i in range(1,436):
    with open('docs/{doc_name}'.format(doc_name=i)) as fp:
        doc = fp.read()
        print(doc)