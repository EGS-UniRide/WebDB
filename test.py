# import gps               # the gpsd interface module
import pymongo           # mongoDB py lib
from datetime import datetime

# session = gps.gps(mode=gps.WATCH_ENABLE)

myclient = pymongo.MongoClient("mongodb://mongodb:27017/")
mydb = myclient["mydatabase"]


mycol = mydb["data"]
data = mycol.find()

for doc in data:
    print(doc)