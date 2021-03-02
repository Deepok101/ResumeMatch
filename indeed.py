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


# Get Job title from the input
def extract_job_title_from_result(q, numberOfPosting):
    jobs = []
    soup = create_soup(q, numberOfPosting)
    for div in soup.find_all(name="div", class_="row"):
        for a in div.find_all(name="a", attrs={"data-tn-element": "jobTitle"}):
            jobs.append(a["title"])
    return(jobs)


def create_soup(q, numberOfPosting, specificJob=None):
    url = "https://www.indeed.com/jobs?q={}&start={}&vjk={}".format(
        q, numberOfPosting, specificJob)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    return soup


def get_js_data(q, numberOfPosting):
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    driver = webdriver.Chrome("./chromedriver.exe", options=chrome_options)

    driver.get("https://www.indeed.com/jobs?q={}&start={}".format(q, numberOfPosting))

    print("https://www.indeed.com/jobs?q={}&start={}".format(q, numberOfPosting))

    try:
        data = driver.execute_script("return jobmap")
    finally:
        driver.quit()
    return data


def extract_jobs(q, numberOfPosting):
    jobs = []
    soup = create_soup(q, numberOfPosting)
    for job in soup.find_all(name="div", class_="row"):
        jobs.append(job)
    return(jobs)


def extract_jobs_qualification(q, numberOfPosting):
    jobs_qualification = []
    dynamic_data = get_js_data(q, numberOfPosting)
    for key in dynamic_data.keys():
        jk = dynamic_data[key]["jk"]      
        print(jk)





def extract_dynamic_keys(q, numberOfPosting):
    keylist = []
    dynamic_data = get_js_data(q, numberOfPosting)
    for key in dynamic_data.keys():
        keylist.append(dynamic_data[key]["jk"])

    return keylist

def get_specific_posting_text(key, to_csv=False):

    #get soup for specific job page
    url = "https://www.indeed.com/viewjob?jk={}".format(key)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    result = soup.find("div", id="jobDescriptionText")

    list_items = soup.find_all("ul")
    list_array = []

    indeed_site_words = ["Hiring Lab", "Career Advice", "Browse Jobs", "Browse Companies","Salaries","Find Certifications", "Indeed Events", 
                            "Work at Indeed", "Countries", "About", "Help Center", "© 2021 Indeed", "Do Not Sell My Personal Information", 
                            "Accessibility at Indeed", "Privacy Center", "Cookies", "Privacy", "Terms"]

    for parent in list_items:
        #all this parent's children belong to one list
        children = parent.children

        siblings = []

        for c in children:
            if c.string != None and c.string != "" and all(c.string != x for x in indeed_site_words):
                siblings.append(c.string)

                if os.path.exists("data.csv"):
                    append_write = 'a' # append if already exists
                else:
                    append_write = 'w' # make a new file if not
                
                if to_csv:
                    with open("data.csv", append_write, encoding="utf-8") as csvFile:    
                        csvFile.write("{}, \n".format(c.string.strip().replace(",","")))

        # print(siblings)
        if siblings != []:
            list_array.append(siblings)
        
        filtered = list(filter(any, siblings))
    
    # print(list_array)
    return list_array

def search_to_csv(query, numrecords):
    q = query.replace(" ", "+")
    for i in range(1, numrecords, 15): #15 records per page
        print(i)
        keylist = extract_dynamic_keys(q, i)
        for key in keylist:
            get_specific_posting_text(key, True)


search_to_csv("data scientist", 16)
search_to_csv("angular", 16)
search_to_csv("react", 16)
search_to_csv("machine learning", 16)
search_to_csv("ai", 16)

search_to_csv("frontend", 16)
search_to_csv("backend", 16)
search_to_csv("database engineer", 16)
search_to_csv("it", 16)
search_to_csv("software", 16)
search_to_csv("developer", 16)
search_to_csv( "intern", 16)


# get_specific_posting_text("954f3848245a4b0c", True) #ibm 
# get_specific_posting_text("ca5a8e09e6e7c403") #facebook
# get_specific_posting_text("e546d67d799dc109") #bell
# get_postings_body("data scientist")
# extract_jobs_qualification("data+scientist", "0")
