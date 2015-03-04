# Difficulty Rating Experiment File 01
# Messing around with BeautifulSoup and Mechanize in python

import mechanize

import time

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
    print response.read()
    #response1 = br.response()
    #print response1.read()

def OpenEulerArchives(br):
    response = br.open("https://projecteuler.net/archives")
    print response.read()
    #response1 = br.response()
    #print response1.read()


br = mechanize.Browser()
