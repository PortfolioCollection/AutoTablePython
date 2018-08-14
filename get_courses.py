from bs4 import BeautifulSoup as bs
from requests import get
import json
import time

def scrape_courses():
    key = 'kb9KIShIHfdjfdB5v2P22V739i9c0yH7'
    j = 0
    while True:
        limit = 100
        skip = j*100
        #url = 'https://cobalt.qas.im/api/1.0/courses/filter?key='+key+'&limit='+str(limit)+"&q=code:'CSC'"
        url = 'https://cobalt.qas.im/api/1.0/courses/filter?key=kb9KIShIHfdjfdB5v2P22V739i9c0yH7&q=code:"CSC" AND term:"2018 Fall" OR term:"2019"&limit=100&skip='+str(skip)
        response = get(url)
        #print(response)
        data = response.json()
    
        #print(data)
        for i in range(len(data)):
            print(data[i]["id"])
            print("-----------------------")
        print("-------------------------------"+str(skip+len(data))+"-------------------------------------")
        if len(data) < 100:
            break
        j+=1

start_time = time.time()
scrape_courses()
print("--- Full algorithm %s seconds ---" % (time.time() - start_time))
    
