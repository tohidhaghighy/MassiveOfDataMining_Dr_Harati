import numpy as np 
import pandas as np

class LSH:
    all_text=[]
    def __init__(self):
        pass

    def extract_kshingles(self,doc, k):
        """
        doc - string that should be divided to shingles.
        k - length of shingles.
        Returns a set of k-shingles
        """
        shingles = set()
        if (k<=len(doc)):
           for i in range(0, (len(doc)-k+1)):
               shingles.add(doc[i:i+k])
        return shingles

    def make_matrix(self,all_docs):
        for i in all_docs:
            print(i)
            extract_kshingles(i.iloc[0].values,9)
        pass

    def signiture(self):
        pass
