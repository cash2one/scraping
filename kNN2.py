'''
Created on Sep 16, 2010
kNN: k Nearest Neighbors

Input:      inX: vector to compare to existing dataset (1xN)
            dataSet: size m data set of known vectors (NxM)
            labels: data set labels (1xM vector)
            k: number of neighbors to use for comparison (should be an odd number)
            
Output:     the most popular class label

@author: pbharrin
'''

import operator
from os import listdir
import base64
from pymongo import  MongoClient
client = MongoClient()
db = client['gzh']
records = db.gzhs.find({"biz":{"$exists": 1}})
collection = db.gzhs

for record in records:
    print(record["biz"])
    if record["biz"][0] == "\"":
        biz = record["biz"][1:]
        collection.remove({'wid':record["wid"]})
    elif len(record["biz"]) != 16:
        collection.remove({'wid':record["wid"]})
    else:
        biz = record["biz"]
        print(base64.b64decode(biz).decode("utf-8"))