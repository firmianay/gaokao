# -*- coding: utf_8 -*-

import config
import json
from itertools import islice

class ZhiYuan():
    def __init__(self, config):
        self.region = config.get('region')
        self.subject = config.get('subject')
        self.firstLine = config.get('firstLine')
        self.score = config.get('score')
        self.rank = config.get('rank')
        self.preScore = {
            '2016':'',
            '2015':'',
            '2014':''
        }
        self.preRank = {
            '2016':'',
            '2015':'',
            '2014':''
        }
        self.majors_1 = {}
        self.majors_2 = {}
        self.majors_3 = {}
        self.ratio = [0.4, 0.3, 0.3]
        self.probability = {}


    def generate(self):

        with open('./data/2016tj.txt', 'r') as f:
            for line in islice(f, 1, None):
                line = line.split()
                if self.rank > int(line[4])-int(line[3]) and self.rank < int(line[4]):
                    self.preScore['2016'] = line[0]
                    if self.subject == '理科':
                        self.preRank['2016'] = "%s~%s" % (int(line[4])-int(line[3]), line[4])
                    elif self.subject == '文科':
                        self.preRank['2016'] = "%s~%s" % (int(line[2])-int(line[1]), line[2])

        with open('./data/2015tj.txt', 'r') as f:
            for line in islice(f, 1, None):
                line = line.split()
                if self.rank > int(line[4])-int(line[3]) and self.rank < int(line[4]):
                    self.preScore['2015'] = line[0]
                    if self.subject == '理科':
                        self.preRank['2015'] = "%s~%s" % (int(line[4])-int(line[3]), line[4])
                    elif self.subject == '文科':
                        self.preRank['2015'] = "%s~%s" % (int(line[2])-int(line[1]), line[2])

        with open('./data/2014tj.txt', 'r') as f:
            for line in islice(f, 1, None):
                line = line.split()
                if self.rank > int(line[4])-int(line[3]) and self.rank < int(line[4]):
                    self.preScore['2014'] = line[0]
                    if self.subject == '理科':
                        self.preRank['2014'] = "%s~%s" % (int(line[4])-int(line[3]), line[4])
                    elif self.subject == '文科':
                        self.preRank['2014'] = "%s~%s" % (int(line[2])-int(line[1]), line[2])

        with open('./data/2016zy.txt', 'r')as f:
            for line in islice(f, 1, None):
                line = line.split()
                if int(self.preScore['2016'].split("~")[1]) >= int(line[1]):
                    self.majors_1[line[0]] = 1
                else:
                    self.majors_1[line[0]] = 0

        with open('./data/2015zy.txt', 'r')as f:
            for line in islice(f, 1, None):
                line = line.split()
                if int(self.preScore['2015'].split("~")[1]) >= int(line[1]):
                    self.majors_2[line[0]] = 1
                else:
                    self.majors_2[line[0]] = 0

        with open('./data/2014zy.txt', 'r')as f:
            for line in islice(f, 1, None):
                line = line.split()
                if int(self.preScore['2014'].split("~")[1]) >= int(line[1]):
                    self.majors_3[line[0]] = 1
                else:
                    self.majors_3[line[0]] = 0

        major_1 = self.majors_1.keys()
        major_2 = self.majors_2.keys()
        major_3 = self.majors_3.keys()
        all_majors = list(major_1 | major_2 | major_3)
        for m in all_majors:
            prob = 0
            num = 0

            if m in major_1:
                num += 1
            if m in major_2:
                num += 2
            if m in major_3:
                num += 4

            if num == 7:
                if self.majors_1[m] == 1:
                    prob += 0.4
                if self.majors_2[m] == 1:
                    prob += 0.3
                if self.majors_3[m] == 1:
                    prob += 0.3
            elif num == 6:
                if self.majors_2[m] == 1:
                    prob += 0.5
                if self.majors_3[m] == 1:
                    prob += 0.5
            elif num == 5:
                if self.majors_1[m] == 1:
                    prob += 0.6
                if self.majors_3[m] == 1:
                    prob += 0.4
            elif num == 4:
                if self.majors_3[m] == 1:
                    prob += 1
            elif num == 3:
                if self.majors_1[m] == 1:
                    prob += 0.5
                if self.majors_2[m] == 1:
                    prob += 0.5
            elif num == 2:
                if self.majors_2[m] == 1:
                    prob += 1
            elif num == 1:
                if self.majors_1[m] == 1:
                    prob += 1

            self.probability[m] = prob


    def printResult(self):
        obj = {
            '省份':self.region,
            '科目':self.subject,
            '你的分数':self.score,
            '你的排名':self.rank,
            '对应往年成绩':self.preScore,
            '对应往年排名':self.preRank,
            '2016录取情况':self.majors_1,
            '2015录取情况':self.majors_2,
            '2014录取情况':self.majors_3,
            '2017录取预测':self.probability
        }
        print(json.dumps(obj, indent=4, ensure_ascii=False))

    def start(self):
        self.generate()
        self.printResult()


if __name__ == "__main__":
    Z = ZhiYuan(config.config)
    Z.start()
