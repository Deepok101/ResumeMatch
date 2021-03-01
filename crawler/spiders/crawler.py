import scrapy
import nltk
from bs4 import BeautifulSoup
import requests
import keyword
import re
import w3lib.html
import time

# nltk.download('stopwords')
# nltk.download('wordnet')
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger') 


def read_training_urls(url_file):
    "Read the urls from training url file"
    try:
        fp = open(url_file,mode='r',encoding='utf-8')
        lines = fp.readlines()
        fp.close()
        urls = []
        for line in lines:
            if re.search(r'http(s)',line):
                urls.append(line.strip('\n'))
    except Exception as e:
        print(str(e))
        urls = None
    finally:
        return urls

def get_tech_jargon(input_lines):
    "Return a list of tech jargon found in the sentence"
    # function to test if something is a noun
    is_noun = lambda pos: 'NNP' in pos 
    # Break the sentence down to words
    tokenized = nltk.word_tokenize(input_lines)  
    #remove the Python keywords
    python_keywords = keyword.kwlist
    nouns = [word for (word, pos) in nltk.pos_tag(tokenized) if is_noun(pos) and word not in set(nltk.corpus.stopwords.words('english'))] #and word.isalnum() and word not in python_keywords]
    # nouns = [noun for noun in nouns if noun.isalnum() and noun not in python_keywords]
    return nouns


def read_url_contents(url):
    relatednouns = []
    response = requests.get(url)
    html = response.text 
    soup = BeautifulSoup(html)
    nouns = get_tech_jargon(soup.text)
    relatednouns = relatednouns + nouns
    # freq_words = nltk.FreqDist(relatednouns)
    return relatednouns

class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
            'https://www.w3schools.com/whatis/whatis_fullstack.asp'        
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, meta={"proxy": "https://163.172.184.246:3128"})
    

    def parse(self, response):
        # for href in response.css('div.w3-light-grey a::attr(href)'):
        #     next_page = response.urljoin(href)
        #     print(next_page)
            # yield response.follow(href, callback=self.parse)
        # page = response.url.split("/")[-2]
        # filename = f'{page}.html'
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        # self.log(f'Saved file {filename}')
        # output= w3lib.html.remove_tags(response.body)
        # print(output)
        next_page = response.css('div.w3-light-grey a::attr(href)')
        i = 0
        words = []
        for href in next_page:
            if i == 20:
                break
            time.sleep(2)
            url = response.urljoin(href.get())
            words += read_url_contents(url)
            i+=1

        yield {
            "words": nltk.FreqDist(words).most_common()
        }