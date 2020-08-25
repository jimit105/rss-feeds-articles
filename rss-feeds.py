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

os.environ['TZ'] = 'Asia/Kolkata'
time.tzset()

RSS_FEEDS = ['https://medium.com/feed/@jimit105',
             'https://thecodelens.blogspot.com/feeds/posts/default',
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
             'https://nanonets.com/blog/rss/',
             'https://www.mygreatlearning.com/blog/category/artificial-intelligence/feed/',
             'https://www.mygreatlearning.com/blog/category/data-science/rss'
             ]

TOP_N = 200


def convert_timezone(datetime_struct_time):
    dt = datetime.fromtimestamp(time.mktime(datetime_struct_time))
    dt2 = dt - timedelta(seconds=time.timezone)
    return dt2


def fetch_feeds(feed_url):
    feed = feedparser.parse(feed_url)
    output = []

    for entry in feed.entries:
        article = '<p><a href="' + entry.link + '" target="_blank">' + entry.title + '</a><br/>' + feed.feed.title + \
            ' | ' + \
            convert_timezone(entry.updated_parsed).strftime(
                '%b %d, %Y %X %Z') + '</p>'
        output.append((article, convert_timezone(entry.updated_parsed)))

    return output


result = list(map(fetch_feeds, RSS_FEEDS))
merged = list(itertools.chain(*result))
output = sorted(merged, key=lambda x: x[-1], reverse=True)


all_articles = ''
for article in output[:TOP_N]:
    all_articles += article[0]

current_time = time.strftime('%b %d, %Y %X %Z', time.localtime())
action_badge = '![RSS Feeds Update](https://github.com/jimit105/rss-feeds-articles/workflows/RSS%20Feeds%20Update/badge.svg)'
header = action_badge + '\n![Last Updated](https://img.shields.io/badge/Last%20Updated%20on-' + \
    urllib.parse.quote(current_time) + '-brightgreen)' + '\n\n'


complete_text = header + all_articles

with open('README.md', 'w') as f:
    f.write(complete_text)

print('RSS Feeds Update Complete')
