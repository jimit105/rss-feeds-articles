# -*- coding: utf-8 -*-
"""
@author: Jimit.Dholakia
"""

from datetime import datetime, timedelta
import time
import os
import itertools
import feedparser
import urllib.parse
import dateutil.parser
import signal
import sys

os.environ['TZ'] = 'Asia/Kolkata'
if os.name != 'nt':
    time.tzset()

TIME_FMT = '%b %d, %Y %H:%M:%S %Z'

RSS_FEEDS = ['https://medium.com/feed/@jimit105',
             'https://jimit105.github.io/pytricks/rss.xml',
             'https://scitech105.blogspot.com/rss.xml',
             'https://jimit105.github.io/medium-articles/rss.xml',
             'https://www.pyimagesearch.com/feed/',
             'https://machinelearningmastery.com/feed/',
             'https://www.fast.ai/atom.xml',
             'https://openai.com/blog/rss/',
             'https://research.fb.com/feed/',
             'http://googleaiblog.blogspot.com/atom.xml',
             'https://blogs.microsoft.com/ai/feed/',
             'https://www.analyticsvidhya.com/feed/',
             'https://www.hackerearth.com/blog/machine-learning/feed',
             'https://mlfromscratch.com/rss/',
             'https://www.mygreatlearning.com/blog/category/artificial-intelligence/feed/',
             'https://blog.tensorflow.org/atom.xml',
             'http://feeds.feedburner.com/kdnuggets-data-mining-analytics',
             'https://lazyprogrammer.me/feed/'
             ]

TOP_N = 200


def handler(signum, frame):
    print('Signal handler called with signal', signum)
    sys.exit('Took too long.. Goodbye!')
    
    
def parse_date(input_date):
    dt = dateutil.parser.parse(input_date)
    dt2 = dt - timedelta(seconds=time.timezone)
    return dt2


def convert_timezone(datetime_struct_time):
    dt = datetime.fromtimestamp(time.mktime(datetime_struct_time))
    dt2 = dt - timedelta(seconds=time.timezone)
    return dt2


def fetch_feeds(feed_url):
    try:
        feed = feedparser.parse(feed_url)
        output = []

        for entry in feed.entries:
            if entry.updated_parsed is None:
                article = '<p><a href="' + entry.link + '" target="_blank">' + entry.title + '</a><br/>' + feed.feed.title + \
                    ' | ' + \
                    parse_date(entry.updated).strftime(
                        TIME_FMT) + '</p>'

                output.append((article, parse_date(entry.updated)))

            else:
                article = '<p><a href="' + entry.link + '" target="_blank">' + entry.title + '</a><br/>' + feed.feed.title + \
                    ' | ' + \
                    convert_timezone(entry.updated_parsed).strftime(
                        TIME_FMT) + '</p>'

                output.append(
                    (article, convert_timezone(entry.updated_parsed)))
                
        print('Fetching complete for ' + feed_url)

    except Exception as e:
        print('Fetching failed for ' + feed_url + '\tException: ' + str(e))
        print('Exception:', str(e))

    return output

signal.signal(signal.SIGALRM, handler)
signal.alarm(300)
result = list(map(fetch_feeds, RSS_FEEDS))
signal.alarm(0)
merged = list(itertools.chain(*result))
merged = list(set(merged))
output = sorted(merged, key=lambda x: x[-1], reverse=True)


all_articles = ''
for article in output[:TOP_N]:
    all_articles += article[0]

current_time = time.strftime(TIME_FMT, time.localtime())
action_badge = ''
maintainer_badge = '[![Maintained by Jimit Dholakia](https://img.shields.io/badge/Maintained%20by-Jimit%20Dholakia-yellowgreen)](https://github.com/jimit105)'
linkedin_badge = '[![LinkedIn: jimit105](https://img.shields.io/badge/LinkedIn-jimit105-blue)](https://www.linkedin.com/in/jimit105/)'
header = action_badge + '\n' + maintainer_badge + '\n' + linkedin_badge + '\n![Last Updated](https://img.shields.io/badge/Last%20Updated%20on-' + \
    urllib.parse.quote(current_time) + '-brightgreen)' + '\n\n'


complete_text = header + all_articles

with open('README.md', 'w') as f:
    f.write(complete_text)

print('RSS Feeds Update Complete')
