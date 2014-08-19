# Project Euler 022
# Names scores
# Not 571860170
# not 571860170


import argparse

parser = argparse.ArgumentParser()
parser.add_argument("fileName")
args = parser.parse_args()

file_name = args.fileName

print 'Looking at file: ', file_name

all_names = open(file_name,'r')

def score_letter(letter):
    return ord(letter) - ord("A") + 1

def score_name(name):
    score = 0
    print name
    for letter in name:
        print letter
        score = score + score_letter(letter)
        print score
    return score

total_score = 0L

for line in all_names:
    name_line = line.split(",")
    name_list = []
    for name in name_line:
        name_list.append(name[1:-1])
    name_list.sort()
    list_number = 0
    for name in name_list:
        list_number += 1
        score = score_name(name)
        print "base score = ", score
        print "multiplier = ", list_number
        score *= list_number
        print "score = ", score
        total_score += score
print total_score
