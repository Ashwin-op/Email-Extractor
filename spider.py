import logging
import os
import pandas as pd
import re
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from googlesearch import search

logging.getLogger('scrapy').propagate = False


# DON'T CHANGE THESE IF YOU DON'T KNOW WHAT YOU'RE DOING!
########################################################################################################################

def get_urls(tag, n, language):
    urls = [url for url in search(tag, stop=n, lang=language)][:n]
    return urls


class MailSpider(scrapy.Spider):
    name = 'email'

    def parse(self, response):

        links = LxmlLinkExtractor(allow=()).extract_links(response)
        links = [str(link.url) for link in links]
        links.append(str(response.url))

        for link in links:
            yield scrapy.Request(url=link, callback=self.parse_link)

    def parse_link(self, response):

        for word in self.reject:
            if word in str(response.url):
                return

        html_text = str(response.text)
        mail_list = re.findall('\w+@\w+\.{1}\w+', html_text)

        dic = {'email': mail_list, 'link': str(response.url)}
        df = pd.DataFrame(dic)

        df.to_csv(self.path, mode='a', header=False)
        df.to_csv(self.path, mode='a', header=False)


def ask_user(question):
    response = input(question + ' y/n' + '\n')
    if response == 'y':
        return True
    else:
        return False


def create_file(path):
    response = False
    if os.path.exists(path):
        response = ask_user('File already exists, replace?')
        if response == False: return

    with open(path, 'wb') as file:
        file.close()


def get_info(tag, n, language, path, reject=[]):
    create_file(path)
    df = pd.DataFrame(columns=['email', 'link'], index=[0])
    df.to_csv(path, mode='w', header=True)

    print('Collecting Google urls...')
    google_urls = get_urls(tag, n, language)

    print('Searching for emails...')
    process = CrawlerProcess({'USER_AGENT': 'Mozilla/5.0'})
    process.crawl(MailSpider, start_urls=google_urls, path=path, reject=reject)
    process.start()

    print('Cleaning emails...')
    df = pd.read_csv(path, index_col=0)
    df.columns = ['email', 'link']
    df = df.drop_duplicates(subset='email')
    df = df.reset_index(drop=True)
    df.to_csv(path, mode='w', header=True)

    return df


########################################################################################################################

# FILL ALL THE INFORMATION HERE

# Fill the keywords to search for
keywords = 'iiitdm kancheepuram'
# Fill here the number of top level websites to search
n = 5
# Fill the language you want to search
lang = 'en'
# Fill the name of the file you want to save it as
file = 'college.csv'
# Fill website names/keywords in which you don't want it to search
bad_words = ['facebook', 'instagram', 'youtube', 'twitter', 'wiki', 'amazon', 'flipkart', 'ebay']

########################################################################################################################

df = get_info(keywords, n, lang, file, reject=bad_words)
