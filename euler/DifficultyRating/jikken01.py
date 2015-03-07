# Difficulty Rating Experiment File 01
# Messing around with BeautifulSoup and Mechanize in python

import mechanize

import time

from bs4 import BeautifulSoup

import xml.etree.ElementTree as ET

import operator

# The following opens Project Euler and reads it.
# Here I verified that it opened the home page for not signed in people
def OpenEuler():
    br = mechanize.Browser()
    response = br.open("http://www.projecteuler.net/")
    print response.read()
    response1 = br.response()
    print response1.read()


def OpenEulerSignIn():
    br = mechanize.Browser()
    response = br.open("http://www.projecteuler.net/sign_in")
    print response.read()
    response1 = br.response()
    print response1.read()

# Sign in to Euler using the given password and username
# Opened the friends page to verify successful login
def EulerSignInNewBrowser(username, password):
    br = mechanize.Browser()
    response = br.open("http://www.projecteuler.net/sign_in")
    #print response.read()
    response1 = br.response()
    #print response1.read()
    for form in br.forms():
        print "Form name:", form.name
        print form

    br.select_form(name='sign_in_form')
    br['username'] = username
    br['password'] = password
    br.submit()

    time.sleep(5)

    response = br.open("https://projecteuler.net/friends")
    print response.read()
    response1 = br.response()
    print response1.read()

# Version if sign in, passing in the browser 
# so I can use the same sign in for other pages
# and I don't have to worry about cookies
def EulerSignIn(username, password, br):
    response = br.open("http://www.projecteuler.net/sign_in")
    #print response.read()
    response1 = br.response()
    #print response1.read()
    for form in br.forms():
        print "Form name:", form.name
        print form

    br.select_form(name='sign_in_form')
    br['username'] = username
    br['password'] = password
    br.submit()

def OpenEulerFriends(br):
    response = br.open("https://projecteuler.net/friends")
    #print response.read()
    #response1 = br.response()
    #print response1.read()

def OpenEulerArchives(br):
    response = br.open("https://projecteuler.net/archives")
    #print response.read()
    #response1 = br.response()
    #print response1.read()

# I think this should be able to look at the response already handled by Mechanize
def SoupArchives(br):
    soup = BeautifulSoup(br.response().read())
    body_tag = soup.body
    all_paragraphs = soup.find_all('p')
    logo_img = soup.find('header').find('div',id="logo").img

def ExamineFriends(br):
    print "-- Getting friends --"
    OpenEulerFriends(br)
    time.sleep(1)

    # http://stackoverflow.com/questions/2224602/parsing-table-with-beautifulsoup-and-write-in-text-file
    print "Reading table"
    soup = BeautifulSoup(br.response().read())
    #body_tag - soup.body
    #friendTable = soup.find("table", {"class" : "detail-char"})
    friendTable = soup.find("table")

    #records = [] # store all of the records in this list
    for row in friendTable.find_all('tr'):
        col = row.find_all('td')
        print (row.prettify())
        print "-----------------"
        print row.table
        print "------------------"
        print row.a
        print "========================="
        #name = col[0].string.strip()
        #record = name
        #records.append(record)
        if row.table is None:
            print "Ed - Table is none"

def GetFriends(br):
    print "-- Getting friends --"
    OpenEulerFriends(br)
    time.sleep(1)

    # http://stackoverflow.com/questions/2224602/parsing-table-with-beautifulsoup-and-write-in-text-file
    print "Reading table"
    soup = BeautifulSoup(br.response().read())
    #body_tag - soup.body
    #friendTable = soup.find("table", {"class" : "detail-char"})
    friendTable = soup.find("table")

    print "Listing friends:"
    print "-----------------"
    friends = []
    #records = [] # store all of the records in this list
    for row in friendTable.find_all('tr'):
        if row.table is None:
            if row.a is not None:
                #print row.a
                line = ET.fromstring(str(row.a))
                print line.text
                friends.append(line.text)
    return friends

# At this point, what am I thinking?  I have the user names.
# Next, I need the list of problems solved.

def GetFriendProgress(username, br):
    print "-- Getting progress for : ", username
    url = "https://projecteuler.net/progress=" + username
    response = br.open(url)
    print response.read()

# Looking at the table, we are looking for <td class="problem_solved">
# and then get the text for that element, which should be the problem number
# and add that to a list.

# Given a username and a browser (already logged in to Project Euler)
# Return a string list of all solved problems by that user
def GetFriendSolved(username, br):
    #print "-- Getting progress for : ", username
    url = "https://projecteuler.net/progress=" + username
    response = br.open(url)
    #print response.read()
    soup = BeautifulSoup(br.response().read())
    solvedProblems = []
    solved = soup.find_all('td','problem_solved')
    for problem in solved:
        heading = problem.find('div','heading')
        solvedProblems.append(heading.text.split(' ')[1])
    solvedProblems = [x.encode('ascii') for x in solvedProblems]
    return solvedProblems

# Now, go through all of the archived pages and get the difficulty rating of every problem

def GetProblemRatings(br):
    print "-- Going to Archives page"
    url = "https://projecteuler.net/archives"
    response = br.open(url)
    soup = BeautifulSoup(br.response().read())
    #print (soup.prettify())
    pagination = soup.find('div','pagination')
    pages = len(pagination.find_all('a'))

    ratings = ['-1'] * (pages * 50)
    
    #table = soup.find_all('table','grid').tbody.find_all('tr')
    table = soup.find_all('tr')
    
    for row in table:
        idNumber = row.find('td','id_column')
        rating = row.find('td','difficulty_column')
        if idNumber is not None and rating is not None:
            difficultyRating = rating.text.split(' ')[2]
            difficultyRating = difficultyRating[:difficultyRating.find("%")]
            ratings[int(idNumber.text)] = difficultyRating

    for i in range(2,pages+1):
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
    return ratings
    
# http://stackoverflow.com/questions/613183/sort-a-python-dictionary-by-value        
    
# So what do I do now?
# 1 - Get all the problem ratings
# 2 - Get Anthony's problems as a list
# 3 - Create a dictionary with the information
# 4 - Generate a sorted list from the dictionary

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

br = mechanize.Browser()
print "Use EulerSignIn(username, password, br)"
print "Then run GetFriendDifficulty(br)"
# ratings = GetProblemRatings(br)
# problems = GetFriendSolved('afairchild',br)
# solvedRatings = GetUserDifficulty(ratings, problems)
# sortedSolved = sorted(solvedRatings.items(), key=operator.itemgetter(1))
# sortedSolved.reverse()



