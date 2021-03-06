import logging
from linkedin_jobs_scraper import LinkedinScraper
from linkedin_jobs_scraper.events import Events, EventData
from linkedin_jobs_scraper.query import Query, QueryOptions, QueryFilters
from linkedin_jobs_scraper.filters import RelevanceFilters, TimeFilters, TypeFilters, ExperienceLevelFilters

import requests
import bs4
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import sys
from bs4 import Tag, NavigableString
import math
import re
import os
import pdb
import time
import psycopg2
from configparser import ConfigParser
from indeed import config

import indeed

from joblib import load
import sklearn
import pandas as pd


# Change root logger level (default is WARN)
logging.basicConfig(level = logging.INFO)


def parse_html(jobkey, html, update=False): #returns array X s.t X[0] = required, X[1] = bonus

    soup = BeautifulSoup(html, 'html.parser')
    list_items = soup.find_all("ul")

    # print(list_items)
    
    list_array = []
    buildingList = [] #for cases when job listings do a single <ul> per requirement
    skip = False

    if list_items != []:
        for parent in list_items:  

            #either this parent's children is a huge list or this parent's children is a list of exactly one item  
            children = parent.children
            if len(list(parent.children)) == 1:
                # print(buildingList)
                #are we just starting this list, in the middle, or ending it?

                #no matter what, add this single object to the list
                for c in children:
                    if c.string != None and c.string != "":
                        buildingList.append(c.string.strip().replace(",","\n"))

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
                    if c.string != None and c.string != "":
                        siblings.append(c.string.strip().replace(",","\n"))

            
                # print(siblings)
                if siblings != []:
                    list_array.append(siblings)

    else:
        # somehow <li> without <ul> ...
        li_list = soup.find_all("li")
        nextSiblingChar = "li"
        if li_list == []:
            li_list = soup.find_all("p")
            nextSiblingChar = "p"

            if li_list == []:
                skip = True

        for listitem in li_list:
            #are we starting list, appending, or ending?
            if listitem.find_next_sibling(nextSiblingChar): #if next sibling is li then don't end, keep appending
                if listitem.string != None and listitem.string != "":
                    buildingList.append(listitem.string.strip().replace(",","\n"))
            else:
                list_array.append(buildingList)
                buildingList = []

    if skip:
        return_arr = ['','']
    else:
        x_input = []
        for s in list_array:
            x_input.append("".join(s))

        try:
            probabilityLists = model.predict_proba(vectorizer.transform(pd.Series(x_input)))
        except:
            return ['','']
        #get index i,j of best two values probabilityLists[i][2] and probabilityLists[j][2]
        bestProb = 0
        bestIndex = 0

        for i in range(len(probabilityLists)):
            if probabilityLists[i][1]>bestProb and probabilityLists[i][1]>0.01:
                bestProb = probabilityLists[i][1]
                bestIndex = i

        secondBest = 0
        secondBestIndex = 0

        for i in range(len(probabilityLists)):
            if probabilityLists[i][1] > secondBest and i != bestIndex and probabilityLists[i][1] > 0:
                secondBest = probabilityLists[i][1]
                secondBestIndex = i

        print("{},{}; probs:{},{}".format(bestIndex,secondBestIndex, bestProb,secondBest))

        return_arr = []
            
        if (bestProb>0):
            return_arr.append(x_input[bestIndex])
        else:
            return_arr.append("")

        if(secondBest > 0):
            return_arr.append(x_input[secondBestIndex])
        else:
            return_arr.append("")

    # print(return_arr)
    return return_arr


def update_records():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        # print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params, sslmode="require")
		
        # create a cursor
        cur = conn.cursor()

        getRowsSql = "SELECT jobkey, descrip FROM jobs;" #where basicreq IS NULL and bonusreq IS NULL

        cur.execute(getRowsSql)
        allRows = cur.fetchall()
        
        numUpdates = 0

        for row in allRows:
            key = str(row[0])
            html = str(row[1])

            print(key)

            arr = parse_html(key, html)
            sql1 = "update jobs set basicreq = %s where jobkey = %s"
            sql2 = "update jobs set bonusreq = %s where jobkey = %s"
            data1 = (str(arr[0]), key)
            data2 = (str(arr[1]), key)

            # print(data1)
            # print(data2)

            cur.execute(sql1, data1)
            cur.execute(sql2, data2)
  
       
	# close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.commit()
            conn.close()
            print('Database connection closed.')




def insert_to_database_record(key, title, description, location, company, url, date, basicreq, bonusreq):
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params, sslmode="require")
        # create a cursor
        cur = conn.cursor()
	# execute a statement
        # display the PostgreSQL database server version

        sql = "INSERT INTO jobs(jobkey, jobname, descrip, location, companyname, url, date, basicreq, bonusreq) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s);"
        data = (key, title, description, location, company, url, date, basicreq, bonusreq)

        cur.execute(sql,data)
        conn.commit()
       
	# close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

def on_data(data: EventData):
    # print('[ON_DATA]', data.title, data.company, data.date, data.link, data.place, data.description_html)  
    reqs = parse_html(data.job_id, data.description_html)
    insert_to_database_record(data.job_id, data.title, data.description_html, data.place, data.company, data.link, data.date, reqs[0], reqs[1])
    


def on_error(error):
    print('[ON_ERROR]', error)


def on_end():
    print('[ON_END]')

def scrape(query, numresults):
    scraper = LinkedinScraper(
        chrome_executable_path=None, # Custom Chrome executable path (e.g. /foo/bar/bin/chromedriver) 
        chrome_options=None,  # Custom Chrome options here
        headless=False,  # Overrides headless mode only if chrome_options is None
        max_workers=1,  # How many threads will be spawned to run queries concurrently (one Chrome driver for each thread)
        slow_mo=1,  # Slow down the scraper to avoid 'Too many requests (429)' errors
    )

    # Add event listeners
    scraper.on(Events.DATA, on_data)
    scraper.on(Events.ERROR, on_error)
    scraper.on(Events.END, on_end)

    queries = [
        Query(
            query=query,
            options=QueryOptions(
                locations=['Montreal'],
                optimize=True,  # Blocks requests for resources like images and stylesheet
                limit=numresults  # Limit the number of jobs to scrape
            )
        ),
        # Query(
        #     query='database',
        #     options=QueryOptions(
        #         locations=['United States'],
        #         optimize=False,
        #         limit=5,
        #         filters=QueryFilters(
        #             # company_jobs_url='https://www.linkedin.com/jobs/search/?geoId=101174742&keywords=amazon&location=Canada',  # Filter by companies
        #             relevance=RelevanceFilters.RECENT,
        #             time=TimeFilters.MONTH,
        #             type=[TypeFilters.FULL_TIME, TypeFilters.INTERNSHIP],
        #             experience=None,
        #         )
        #     )
        # ),
    ]

    scraper.run(queries)

if __name__ == "__main__":
    try:
        model = load('model.joblib')
        vectorizer = load('vectorizer.joblib')

        # update_records()
        query = sys.argv[1:]
        for q in query:
            print("next.....")
            scrape(q, 200)
            time.sleep(1)
    except Exception as e:
        print(e)











