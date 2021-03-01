# -*- coding: utf-8 -*-
import requests
import bs4
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

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
    soup = BeautifulSoup(page.text, "html.parser")

    return soup


def get_js_data(q, numberOfPosting):
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    driver = webdriver.Chrome("./chromedriver", options=chrome_options)

    driver.get("https://www.indeed.com/jobs?q=data%20scientist&start=0")

    data = driver.execute_script("return jobmap")
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


extract_jobs_qualification("data+scientist", "0")
