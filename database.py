# -*- coding: utf-8 -*-git
import requests
import bs4
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from bs4 import Tag, NavigableString
import math
import re
import os
import pdb
import time
import psycopg2
from configparser import ConfigParser
import config

import indeed

from joblib import load
import sklearn
import pandas as pd

def annotate_qualifications():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = indeed.config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params, sslmode="require")
		
        # create a cursor
        cur = conn.cursor()
        
	# execute a statement

        # display the PostgreSQL database server version

        getRowsSql = "SELECT jobkey FROM jobs where basicreq IS NULL and bonusreq IS NULL;"

        cur.execute(getRowsSql)
        allRows = cur.fetchall()
        
        numUpdates = 0

        for row in allRows:
            key = str(row[0])
            # print(key)

            url = "https://www.indeed.com/viewjob?jk={}".format(key)
            page = requests.get(url)
            soup = BeautifulSoup(page.content, 'html.parser')

            result = soup.find_all("div", id="jobDescriptionText")

            list_items = soup.find_all("ul")
            list_array = []

            indeed_site_words = ["Hiring Lab", "Career Advice", "Browse Jobs", "Browse Companies","Salaries","Find Certifications", "Indeed Events", 
                                    "Work at Indeed", "Countries", "About", "Help Center", "© 2021 Indeed", "Do Not Sell My Personal Information", 
                                    "Accessibility at Indeed", "Privacy Center", "Cookies", "Privacy", "Terms"]


            buildingList = [] #for cases when job listings do a single <ul> per requirement

            for parent in list_items:    

                #either this parent's children is a huge list or this parent's children is a list of exactly one item  
                children = parent.children
                if len(list(parent.children)) == 1:
                    # print(buildingList)
                    #are we just starting this list, in the middle, or ending it?

                    #no matter what, add this single object to the list
                    for c in children:
                        if c.string != None and c.string != "" and all(c.string != x for x in indeed_site_words):
                            buildingList.append(c.string.strip().replace(",",""))

                    #we are ending if the next is not a <ul>
                    next = parent.find_next_sibling()
                    if not next is None:
                        if not (next.name == "ul"):
                            #save to list, and re-init the list
                            list_array.append(buildingList)
                            buildingList = []
                    
                

                if len(list(parent.children)) >= 1:
                    siblings = []
                    #big list, should just process this normally
                    for c in children:
                        if c.string != None and c.string != "" and all(c.string != x for x in indeed_site_words):
                            siblings.append(c.string.strip().replace(",",""))

                
                    # print(siblings)
                    if siblings != []:
                        list_array.append(siblings)

            model = load('model.joblib')
            vectorizer = load('vectorizer.joblib')
        
            numMatches = 0
            qualList = []
            for i in range(len(list_array)):
                # print(i)
                
                lists = list_array[i]

                if numMatches == 2 or i == len(list_array) - 1 :
                    

                    if len(qualList) > 0:
                        numUpdates+=1
                        # print("here")

                        firstQuals = "\n".join(qualList[0])
                        query1 = "update jobs set basicreq = %s where jobkey = %s"
                        print(firstQuals)
                        data1 = (firstQuals, key)
                        cur.execute(query1, data1)

                    if len(qualList) == 2:
                        numUpdates +=1
                        # print("here2")
                        secondQuals = "\n".join(qualList[1])
                        query2 = "update jobs set bonusreq = %s where jobkey = %s"
                        data2 = (secondQuals, key)

                        print(secondQuals)
                        cur.execute(query2, data2)

                    numMatches=0
                    qualList = []

                    break
                    




                #model
                
                try:
                    df = pd.Series(lists)
                    x = vectorizer.transform(df)

                    y = model.predict(x)[0]
                # print(lists)
           

                    if(y == "y"):
                        numMatches += 1
                        qualList.append(lists)
                except:
                    print("try failed with key {}".format(key))
                    continue
            
        


        



       
	# close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.commit()
            conn.close()
            print('Database connection closed.')

        if numUpdates is not None:
            print(numUpdates)


annotate_qualifications()