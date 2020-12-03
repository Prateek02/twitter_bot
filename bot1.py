import random
import time

from lxml.html import fromstring
import nltk
nltk.download('punkt')
import requests

from twitter import OAuth, Twitter

import credentials

tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

oauth = OAuth(
        credentials.access_token,
        credentials.access_token_secret,
        credentials.consumer_key,
        credentials.consumer_secret
    )
t = Twitter(auth=oauth)

HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5)'
                      ' AppleWebKit/537.36 (KHTML, like Gecko) Cafari/537.36'
        }

def extract_paratext(paras):
    """Extracts text from <p> elements and returns a clean, tokenized random
    paragraph."""

    paras = [para.text_content() for para in paras if para.text_content()]
    para = random.choice(paras)
    return tokenizer.tokenize(para)

def extract_text(para):
    """Returns a sufficiently-large random text from a tokenized paragraph,
    if such text exists. Otherwise, returns None."""

    for _ in range(10):
        text = random.choice(para)
        if text and 60 < len(text) < 210:
            return text

    return None


def scrape_helptostudy():
    """Scrapes content from the homepage blog."""
    url = 'https://www.helptostudy.com/'
    r = requests.get(url, headers=HEADERS)
    tree = fromstring(r.content)
    links = tree.xpath('//h1[@class="entry-title"]/a/@href')

    for link in links:
        r = requests.get(link, headers=HEADERS)
        blog_tree = fromstring(r.content)
        paras = blog_tree.xpath('//div[@class="entry-content"]/p')
        para = extract_paratext(paras)
        text = extract_text(para)
        if not text:
            continue

        yield '"%s" %s' % (text, link)

def scrape_career():
    """Scrapes content from the Career blog."""
    url = 'https://www.helptostudy.com/category/career/'
    r = requests.get(url, headers=HEADERS)
    tree = fromstring(r.content)
    links = tree.xpath('//h1[@class="entry-title"]/a/@href')

    for link in links:
        r = requests.get(link, headers=HEADERS)
        blog_tree = fromstring(r.content)
        paras = blog_tree.xpath('//div[@class="entry-content"]/p')
        para = extract_paratext(paras)
        text = extract_text(para)
        if not text:
            continue

        yield '"%s" %s' % (text, link)


def main():
    """Encompasses the main loop of the bot."""
    print('---Bot started---\n')
    news_funcs = ['scrape_helptostudy', 'scrape_career']
    news_iterators = []
    for func in news_funcs:
        news_iterators.append(globals()[func]())
    while True:
        for i, iterator in enumerate(news_iterators):
            try:
                tweet = next(iterator)
                post="{}?ref=pr #scholarship #helptostudy #student ".format(tweet)
                t.statuses.update(status=post)
                print(post, end='\n\n')
                time.sleep(480)
            except StopIteration:
                news_iterators[i] = globals()[newsfuncs[i]]()

if __name__ == "__main__":
    main()
