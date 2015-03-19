# Script to display your Project Euler friends and the problems they've solved, in order of difficulty rating

import sys
import mechanize
import time
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import operator


# Version if sign in, passing in the browser 
# so I can use the same sign in for other pages
# and I don't have to worry about cookies
def EulerSignIn(username, password, br):
    print "Signing in to Project Euler as:", username
    response = br.open("http://www.projecteuler.net/sign_in")
    response1 = br.response()

    br.select_form(name='sign_in_form')
    br['username'] = username
    br['password'] = password
    br.submit()


def GetProblemRatings(br):
    print "-- Going through archives pages",
    url = "https://projecteuler.net/archives"
    response = br.open(url)
    soup = BeautifulSoup(br.response().read())

    pagination = soup.find('div','pagination')
    pages = len(pagination.find_all('a'))

    ratings = ['-1'] * (pages * 50)

    table = soup.find_all('tr')
    
    for row in table:
        idNumber = row.find('td','id_column')
        rating = row.find('td','difficulty_column')
        if idNumber is not None and rating is not None:
            difficultyRating = rating.text.split(' ')[2]
            difficultyRating = difficultyRating[:difficultyRating.find("%")]
            ratings[int(idNumber.text)] = difficultyRating

    for i in range(2,pages+1):
        print '.',
        url = "https://projecteuler.net/archives;page=" + str(i)
        response = br.open(url)
        soup = BeautifulSoup(br.response().read())
        
        table = soup.find_all('tr')
        
        for row in table:
            idNumber = row.find('td','id_column')
            rating = row.find('td','difficulty_column')
            if idNumber is not None and rating is not None:
                difficultyRating = rating.text.split(' ')[2]
                difficultyRating = difficultyRating[:difficultyRating.find("%")]
                ratings[int(idNumber.text)] = difficultyRating

    ratings = [x.encode('ascii') for x in ratings]
    print
    return ratings


def GetFriends(br):
    print "-- Getting friends"
    br.open("https://projecteuler.net/friends")
    time.sleep(1)

    soup = BeautifulSoup(br.response().read())

    friendTable = soup.find("table")

    print
    print "Friends:"
    print "---------"
    friends = []

    for row in friendTable.find_all('tr'):
        if row.table is None:
            if row.a is not None:
                #print row.a
                line = ET.fromstring(str(row.a))
                print line.text
                friends.append(line.text)
    print
    return friends


# Given a username and a browser (already logged in to Project Euler)
# Return a string list of all solved problems by that user
def GetFriendSolved(username, br):
    url = "https://projecteuler.net/progress=" + username
    response = br.open(url)
    soup = BeautifulSoup(br.response().read())
    solvedProblems = []
    solved = soup.find_all('td','problem_solved')
    for problem in solved:
        heading = problem.find('div','heading')
        solvedProblems.append(heading.text.split(' ')[1])
    solvedProblems = [x.encode('ascii') for x in solvedProblems]
    return solvedProblems


def GetUserDifficulty(ratings, problems):
    allRatings = {}
    for problem in problems:
        allRatings[problem] = int(ratings[int(problem)])
    return allRatings


def GetFriendDifficulty(br):
    ratings = GetProblemRatings(br)
    friends = GetFriends(br)
    for friend in friends:
        problems = GetFriendSolved(friend,br)
        solvedRatings = GetUserDifficulty(ratings, problems)
        sortedSolved = sorted(solvedRatings.items(), key=operator.itemgetter(1))
        sortedSolved.reverse()
        print friend
        print sortedSolved


# Verify the correct number of arguments entered
if len(sys.argv) != 3:
    print "Correct form is EulerFriendDifficulty.py <username> <password>"
    exit()

username = sys.argv[1]
password = sys.argv[2]

br = mechanize.Browser()
EulerSignIn(username,password,br)
GetFriendDifficulty(br)

