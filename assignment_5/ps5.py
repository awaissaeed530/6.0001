# 6.0001/6.00 Problem Set 5 - RSS Feed Filter

import feedparser as feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz
import re


# -----------------------------------------------------------------------

# ======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
# ======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

# ======================
# Data structure design
# ======================

# Problem 1


class NewsStory:
    guid: string
    title: string
    description: string
    link: string
    pubdate: datetime

    def __init__(self, guid, title, description, link, pubdate):
        self.guid = guid
        self.title = title
        self.description = description
        self.link = link
        self.pubdate = pubdate

    def get_guid(self):
        return self.guid

    def get_title(self):
        return self.title

    def get_description(self):
        return self.description

    def get_link(self):
        return self.link

    def get_pubdate(self):
        return self.pubdate


# ======================
# Triggers
# ======================


class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError

# PHRASE TRIGGERS

# Problem 2


class PhraseTrigger(Trigger):
    phrase: string

    def __init__(self, phrase):
        self.phrase = phrase

    def is_phrase_in(self, query):
        # Turn punctuation into whitespace
        query = query.translate(str.maketrans(
            string.punctuation, ' '*len(string.punctuation)))
        # Remove extra whitespaces
        query = ' '.join(query.split())
        return re.search(r'\b' + self.phrase.lower() + r'\b', query.lower())


# Problem 3
class TitleTrigger(PhraseTrigger):
    phrase: string

    def __init__(self, phrase):
        self.phrase = phrase

    def evaluate(self, story):
        return super().is_phrase_in(story.title)


# Problem 4
class DescriptionTrigger(PhraseTrigger):
    phrase: string

    def __init__(self, phrase):
        self.phrase = phrase

    def evaluate(self, story):
        return super().is_phrase_in(story.description)

# TIME TRIGGERS

# Problem 5


class TimeTrigger(Trigger):
    time: datetime

    def __init__(self, time):
        self.time = datetime.strptime(time, "%d %b %Y %H:%M:%S")


# Problem 6
class BeforeTrigger(TimeTrigger):
    def __init__(self, time):
        self.time = datetime.strptime(time, "%d %b %Y %H:%M:%S")

    def evaluate(self, story: NewsStory):
        return story.get_pubdate().replace(tzinfo=None) < self.time.replace(tzinfo=None)


class AfterTrigger(TimeTrigger):
    def __init__(self, time):
        self.time = datetime.strptime(time, "%d %b %Y %H:%M:%S")

    def evaluate(self, story: NewsStory):
        return story.get_pubdate().replace(tzinfo=None) > self.time.replace(tzinfo=None)

# COMPOSITE TRIGGERS

# Problem 7


class NotTrigger(Trigger):
    trigger: Trigger

    def __init__(self, trigger):
        self.trigger = trigger

    def evaluate(self, story):
        return not self.trigger.evaluate(story)

# Problem 8


class AndTrigger(Trigger):
    left_trigger: Trigger
    right_trigger: Trigger

    def __init__(self, left_trigger, right_trigger):
        self.left_trigger = left_trigger
        self.right_trigger = right_trigger

    def evaluate(self, story):
        return self.left_trigger.evaluate(story) and self.right_trigger.evaluate(story)

# Problem 9


class OrTrigger(Trigger):
    left_trigger: Trigger
    right_trigger: Trigger

    def __init__(self, left_trigger, right_trigger):
        self.left_trigger = left_trigger
        self.right_trigger = right_trigger

    def evaluate(self, story):
        return self.left_trigger.evaluate(story) or self.right_trigger.evaluate(story)

# ======================
# Filtering
# ======================

# Problem 10


def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    # TODO: Problem 10
    result = list()
    for story in stories:
        if all(trigger.evaluate(story) for trigger in triggerlist):
            result.append(story)
    return result


# ======================
# User-Specified Triggers
# ======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file
    Returns: a list of trigger objects specified by the trigger configuration file.
    """
    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)

    triggers = list()
    for line in lines:
        args = line.split(',')
        if (args[1].lower() == 'title'):
            triggers.append(TitleTrigger(args[2]))
        elif (args[1].lower() == 'description'):
            triggers.append(DescriptionTrigger(args[2]))
        elif (args[1].lower() == 'before'):
            triggers.append(BeforeTrigger(args[2]))
        elif (args[1].lower() == 'after'):
            triggers.append(AfterTrigger(args[2]))
        elif (args[1].lower() == 'and'):
            triggers.append(AndTrigger(args[2], args[3]))
        elif (args[1].lower() == 'or'):
            triggers.append(OrTrigger(args[2], args[3]))
    return triggers


SLEEPTIME = 120  # seconds -- how often we poll


def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        # Problem 11
        triggerlist = read_trigger_config('triggers.txt')

        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT, fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica", 14),
                    yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []

        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(
                    END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(
                    END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            # stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)

            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()
