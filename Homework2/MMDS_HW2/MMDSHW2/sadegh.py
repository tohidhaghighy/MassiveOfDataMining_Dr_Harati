import os
from cityhash import CityHash32
from math import ceil
from collections import defaultdict
import itertools as it

# Absolute path to documents
PATH_TO_DOCS = "/docs/"

def chunks(l, n):
    """
    l - list to be chunked.
    n - size of chunks.
    Generates n-sized chunks from a list
    """
    for i in range(0, len(l), n):
        yield l[i:i+n]

def extract_kshingles(doc, k):
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

def hash_kshingles(raw_shingles):
    """
    raw_shingles - set of raw string k-shingles
    Returns a set of hashed k-shingles
    """
    hashed_shingles = set()
    for rs in raw_shingles:
        # Hash the shingle to a 32-bit integer.
        hs = CityHash32(rs)
        hashed_shingles.add(hs)
    return hashed_shingles

def sim(doc_x, doc_y, k):
    """
    x, y - documnets.
    k - length of shingles.
    Returns jaccard similarity of two strings (0:0.5)
    """
    kshingles_x = extract_kshingles(doc_x, k)
    kshingles_y = extract_kshingles(doc_y, k)
    hashed_shingles_x = list(hash_kshingles(kshingles_x))
    hashed_shingles_y = list(hash_kshingles(kshingles_y))
    union = hashed_shingles_x + hashed_shingles_y
    intersection = []
    for x in hashed_shingles_x:
        if x in hashed_shingles_y:
            intersection.append(x)
            hashed_shingles_y.remove(x)
    jaccard_similarity = len(intersection) / len(union)
    return jaccard_similarity

def sim_files(file_x, file_y, k):
    """
    file_x, file_y - documnets files.
    k - length of shingles.
    Returns jaccard similarity of two fils (0:0.5)
    """
    doc_x, doc_y = "", ""
    with open(os.path.join(PATH_TO_DOCS, file_x), 'r') as doc:
        doc_x = doc.read()
    with open(os.path.join(PATH_TO_DOCS, file_y), 'r') as doc:
        doc_y = doc.read()
    return sim(doc_x, doc_y, k)

class CharacteristicMatrix:
    """A model for storing and finding similar docs by LSH"""

    def __init__(self):
        # Stores shingles length
        self.k = 9
        # Stores hashed shingles for doc (doc_name : hashed shingles list)
        self.doc_shingles = {}
        # Stores set of all shingles (shingle)
        self.total_shingles_set = set()
        # Stored (ordered) list of all total_shingles
        self.total_shingles_list = []
        # Stores characteristic_matrix (doc_name : characteristic vector list)
        self.characteristic_matrix = {}
        # Stores minhash signature matrix (doc_name : list of minhash signatures for [h1,...,hr])
        self.minhash_signature_matrix = {}
        # Stores buckets for all band (bucket : [list of doc_name])
        self.lsh_buckets = defaultdict(list)

    def add_doc(self, doc_name, doc_content):
        """
        doc_name - name of the file.
        doc_content - content string.
        Adds documents to doc_shingles and updates total_shingles_set
        """
        raw_shingles = extract_kshingles(doc_content, self.k)
        hashed_shingles = hash_kshingles(raw_shingles)
        # Uniting hashed shingles with current total_shingles_set
        self.total_shingles_set |= hashed_shingles
        self.doc_shingles[doc_name] = list(hashed_shingles)

    def create_charactersitic_matrix(self):
        """
        Creates characteristic matrix for added documnets
        """
        self.total_shingles_list = list(self.total_shingles_set)
        for doc in self.doc_shingles:
            #making vector of zeros
            self.characteristic_matrix[doc] = [0] * len(self.total_shingles_list)
            for shingle in self.doc_shingles[doc]:
                i = self.total_shingles_list.index(shingle)
                self.characteristic_matrix[doc][i] = 1
        return self.characteristic_matrix

    def hash_row_number(self, hash_id, x):
        """
            returns permutation's hash
        """
        hash_range = len(self.total_shingles_list)
        if (hash_id ==0):
            return x
        else:
            return (x*hash_id + hash_id - 1) % hash_range
        return x

    def create_minhash_signature(self, r):
        """
        r - number of hash functions h1, h2, h3, h4,...,hr.
        Creates minhash signature matrix
        """
        #Initializing minhash signature matrix by inf
        for doc in self.characteristic_matrix: #for each column
            self.minhash_signature_matrix[doc] = [len(self.total_shingles_list)] * r

        for i, shingle in enumerate(self.total_shingles_list):
            print("row = {}".format(i))
            for hash_id in range(r):
                h_i = self.hash_row_number(hash_id, i)
                for doc in self.characteristic_matrix:
                    if(self.characteristic_matrix[doc][i] != 0):
                        self.minhash_signature_matrix[doc][hash_id] = min(self.minhash_signature_matrix[doc][hash_id],
                            h_i)

    def get_similar_docs_by_lsh(self, band_size):
        """
        band_size - number of rows in each band.
        Returns dictionary of buckets that docs mapped into.
        """
        for doc in self.minhash_signature_matrix:
            i=1
            for chunk in chunks(self.minhash_signature_matrix[doc], band_size):
                bucket = CityHash32("".join(str(x) for x in chunk)+str(i))
                i = i+1
                self.lsh_buckets[bucket].append(doc)
        return self.lsh_buckets

def main():
    cm = CharacteristicMatrix()
    file_names = os.listdir(PATH_TO_DOCS)
    for file_name in file_names:
        with open(os.path.join(PATH_TO_DOCS, file_name), 'r') as doc:
            content = doc.read()
            cm.add_doc(str(file_name), content)
    cm.create_charactersitic_matrix()
    cm.create_minhash_signature(200)
    buckets = cm.get_similar_docs_by_lsh(100)
    similars = {}
    for k in buckets:
        if(len(buckets[k])>1):
            similars[k] = buckets[k]
    print("buckets = {}".format(similars))

if (__name__ == "__main__"):
    main()
