__author__ = 'zivla_000'
import csv


class PlayListReader(object):

    def __init__(self):
        self.playFilesDic = {}

    def readPlayFile(self, fileName):

        if (self.playFilesDic.has_key(fileName)):
            print('mem read')
            return self.playFilesDic[fileName]

        playList = []
        with open('.\playFiles\\' + fileName) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                playList.append(row)

        print ('real read')
        self.playFilesDic[fileName] = playList
        return playList
