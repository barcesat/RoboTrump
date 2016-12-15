__author__ = 'zivla_000'
import csv
from random import randint

DEFAULT_INSULT = 'blat'

class InsultsFileReader(object):

    def __init__(self):
        self.readInsultsFile()

    def readInsultsFile(self):
        self.insultsDic = {}
        with open('insults.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self.insultsDic[row['end_score']] = row

    def getInsult(self, score):
        myEndScore = 0
        for end_score in self.insultsDic:
            if score <= int(end_score):
                row = self.insultsDic[end_score]
		texts = row['text'].split('@@')
		rand = randint(0, len(texts)) - 1
		chosenText = texts[rand]
                return (chosenText, row['torsoPlay'])
            
        return (DEFAULT_INSULT, '')