# -*- coding: utf_8 -*-

import config
from itertools import islice

class ZhiYuan():
    def __init__(self, config):
        self.region = config.get('region')
        self.subject = config.get('subject')
        self.firstLine = config.get('firstLine')
        self.score = config.get('score')
        self.rank = config.get('rank')
        self.preScore = {
            'score_1':'',
            'score_2':'',
            'score_3':''
        }
        self.preRank = {
            'rank_1':'',
            'rank_2':'',
            'rank_3':''
        }
        self.majors_1 = {}
        self.majors_2 = {}
        self.majors_3 = {}
        self.ratio = [0.4, 0.3, 0.3]
        self.probability = {}


    def generate(self):

        with open('./2016tj.txt', 'r') as f:
            for line in islice(f, 1, None):
                line = line.split()
                if self.rank > int(line[4])-int(line[3]) and self.rank < int(line[4]):
                    self.preScore['score_1'] = line[0]
                    if self.subject == '理科':
                        self.preRank['rank_1'] = "%s~%s" % (int(line[4])-int(line[3]), line[4])
                    elif self.subject == '文科':
                        self.preRank['rank_1'] = "%s~%s" % (int(line[2])-int(line[1]), line[2])

        with open('./2015tj.txt', 'r') as f:
            for line in islice(f, 1, None):
                line = line.split()
                if self.rank > int(line[4])-int(line[3]) and self.rank < int(line[4]):
                    self.preScore['score_2'] = line[0]
                    if self.subject == '理科':
                        self.preRank['rank_2'] = "%s~%s" % (int(line[4])-int(line[3]), line[4])
                    elif self.subject == '文科':
                        self.preRank['rank_2'] = "%s~%s" % (int(line[2])-int(line[1]), line[2])

        with open('./2014tj.txt', 'r') as f:
            for line in islice(f, 1, None):
                line = line.split()
                if self.rank > int(line[4])-int(line[3]) and self.rank < int(line[4]):
                    self.preScore['score_3'] = line[0]
                    if self.subject == '理科':
                        self.preRank['rank_3'] = "%s~%s" % (int(line[4])-int(line[3]), line[4])
                    elif self.subject == '文科':
                        self.preRank['rank_3'] = "%s~%s" % (int(line[2])-int(line[1]), line[2])

        with open('./2016zy.txt', 'r')as f:
            for line in islice(f, 1, None):
                line = line.split()
                if int(self.preScore['score_1'].split("~")[1]) >= int(line[1]):
                    self.majors_1[line[0]] = 1
                else:
                    self.majors_1[line[0]] = 0

        with open('./2015zy.txt', 'r')as f:
            for line in islice(f, 1, None):
                line = line.split()
                if int(self.preScore['score_2'].split("~")[1]) >= int(line[1]):
                    self.majors_2[line[0]] = 1
                else:
                    self.majors_2[line[0]] = 0

        with open('./2014zy.txt', 'r')as f:
            for line in islice(f, 1, None):
                line = line.split()
                if int(self.preScore['score_3'].split("~")[1]) >= int(line[1]):
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
        print(obj)

    def start(self):
        self.generate()
        self.printResult()


if __name__ == "__main__":
    Z = ZhiYuan(config.config)
    Z.start()
