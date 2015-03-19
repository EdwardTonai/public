# Experimental file for PopulationLocation

# csv is 98-310-XWE2011002-801.CSV

import csv
import mechanize
from bs4 import BeautifulSoup
import time
import sys

from urlparse import urljoin

import xml.etree.ElementTree as ET

def GetProvince(abbr):
    abbreviations = {"Ont.":"Ontario", "Que.":"Quebec", "N.S.":"Nova Scotia", "N.B.": "New Brunswick", "Man.": "Manitoba", "B.C.":"British Columbia", "P.E.I.":"Price Edward Island", "Sask.": "Saskatchewan", "Alta.": "Alberta", "N.L.": "Newfoundland and Labrador", "N.W.T.": "Northwest Territories", "Y.T.": "Yukon", "Nvt.": "Nunavut"}
    try:
        province = abbreviations[abbr]
    except:
        province = None
    return province


def GetLocations():
    f = open('98-310-XWE2011002-801.CSV')
    # f = open('TestCanadaPop.CSV')
    csv_f = csv.reader(f)

    for row in csv_f:
        try:
            int(row[0])
            leftP = row[1].find("(")
            rightP = row[1].find(")")
            location = row[1][0:leftP-1]
            province = GetProvince(row[1][leftP+1:rightP])
            #print row[0],location, province, row[4]
            query = '{0}, {1} coordinates'.format(location,province)
            print query
        except:
            None


def GetLatLongOld(location):
    response = br.open("http://www.latlong.net/")
    response1 = br.response()
    for form in br.forms():
        if form.attrs['id'] == 'latlongform':
            br.form = form
            break
    print "We have the form"
    for control in br.form.controls:
        print control
        if control.name is None:
            print "----", control.type
    print "let's find the control"
    print br.form.controls[2]
    print br.form.controls[2].type # text
    print br.form.controls[2].name # lat
    print br[br.form.controls[2].name] #
        #print "type=%s, name=%s value=%s" % (control.type, control.name, br[control.name])
    br.form.controls[0].__setattr__("value","Seattle, WA")
    print br.form.controls[0]
    print br.form.controls[0].value
    br.form.controls[2].__setattr__("value","99999")
    print br.form.controls[2]
    print br.form.controls[2].value
    print "Submitting"
    response = br.submit()
    print response.read()
    print "Submission complete"

    #response = br.open("http://www.latlong.net/")
    #response1 = br.response()
    for form in br.forms():
        if form.attrs['id'] == 'latlongform':
            br.form = form
            break
    print "We have the form"
    for control in br.form.controls:
        print control
        if control.name is None:
            print "----", control.type

    
def GetLatLong(location):
    response = br.open("http://www.findlatitudeandlongitude.com/")
    response1 = br.response
    for form in br.forms():
        print form
    br.select_form(name='load_location')
    br['address'] = location
    data = br.submit(nr=1)
    print "Submitted"
    #print data.read()
    #print br.response().read()


def MechanizeLatLong():
    # This is the code
    
    br = mechanize.Browser()
    #GetLatLong("Seatac, WA")
    
    response = br.open("http://www.findlatitudeandlongitude.com/")
    response1 = br.response
    for form in br.forms():
        print form
        br.select_form(name='load_location')
        br['address'] = "SeaTac, WA"
        br['zipcode'] = "89109"
        br['lat'] = "21.324"
        br['lon'] = "-157.838"

        data = br.submit(nr=1)
        print "Submitted"

        soup = BeautifulSoup(br.response().read())
        test = soup.find_all('span', id = "lon_address")
        for spans in test:
            print spans.text


from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def WebdriverLatLong():

    browser = webdriver.Firefox()

    browser.get('http://www.findlatitudeandlongitude.com/')
    #assert 'Yahoo' in browser.title
    
    elem = browser.find_element_by_name('address')  # Find the search box
    elem.send_keys('Seattle, WA' + Keys.RETURN)

    time.sleep(2)

    testLong = browser.find_element_by_id('lon_dec')
    testLat = browser.find_element_by_id('lat_dec')
    print testLong.text
    print testLat.text

    elem.clear()
    elem.send_keys('Las Vegas, NV' + Keys.RETURN)

    time.sleep(2)

    testLong = browser.find_element_by_id('lon_dec')
    testLat = browser.find_element_by_id('lat_dec')
    print testLong.text
    print testLat.text

    

    time.sleep(10)

    browser.quit()

# Given a browser already pointed to findlatitudeandlogitude.com
# Do Search for a location, and return a tuple of the lat/long
def SearchForLatLon(br, location):
    elem = br.find_element_by_name('address')  # Find the search box
    elem.clear()
    elem.send_keys(location + Keys.RETURN)

    time.sleep(4)

    testLon = br.find_element_by_id('lon_dec')
    testLat = br.find_element_by_id('lat_dec')

    lat = float(testLat.text.strip()[10:-1])
    lon = float(testLon.text.strip()[11:-1])
    
    latlon = (lat,lon)
    return latlon

def GetCensusPopulations():
    # First, get the coordinates of all of Xxxxxxxx, Province
    # Second, go through the CSV to get all of the locations
    # For each location, get the lat/long
    # if latitude is < 47.6062095, add population to south
    # else add the population to north
    # What are issues?  
    # If the lat/long is the same as Xxx, Province, note that and add population to unknown
    # If you couldn't come up with a province (province = none0, add it to unknown
    # in all error cases, add the location to the list of unknown locations
    
    provinces = ["Ontario", "Quebec", "Nova Scotia", "New Brunswick", "Manitoba", "British Columbia", "Prince Edward Island", "Saskatchewan", "Alberta", "Newfoundland and Labrador", "Northwest Territories", "Yukon", "Nunavut"]
    
    browser = webdriver.Firefox()

    browser.get('http://www.findlatitudeandlongitude.com/')

    #print SearchForLatLon(browser,"Seattle, WA")
    #print SearchForLatLon(browser,"Las Vegas, NV")
    #print SearchForLatLon(browser,"Alberta")

    provinceLatLon = {}
    for province in provinces:
        provinceLatLon[province] = SearchForLatLon(browser, "Xxxxxxx, " + province)

    with open("provinces.csv", "wb") as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        for province in provinces:
            writer.writerow([province,provinceLatLon[province][0],provinceLatLon[province][1]])

    print provinceLatLon

    f = open('98-310-XWE2011002-801.CSV')
    #f = open('testlocations.CSV')
    csv_f = csv.reader(f)

    south = 0
    north = 0
    unknown = 0
    problemLocations = []
    locations = []
    for row in csv_f:
        try:
            #print row
            int(row[0])
            
            leftP = row[1].find("(")
            rightP = row[1].find(")")
            location = row[1][0:leftP-1]
            provinceRaw = row[1][leftP+1:rightP]
            province = GetProvince(provinceRaw)
            #print row[0],location, province, row[4]
            query = '{0}, {1}'.format(location,province)
            print query
            latlon = SearchForLatLon(browser, query)
            population = int(row[4])
            
            # info I want for the output file:  
            # Location, Province (raw), Population, Lat, Long, Issues Flag
            issues = False
            if province is not None:
                if latlon != provinceLatLon[province]:
                    if latlon[0] < 47.6062095:
                        south += population
                    else:
                        north += population
                else:
                    unknown += population
                    print "problem province None: ", query
                    problemLocations.append(query)
                    print problemLocations
                    issues = True
            else:
                unknown += population
                print "problem", location, province
                testLocation = location + ", " + provinceRaw
                print testLocation
                problemLocations.append(testLocation)
                print problemLocations
                issues = True
            thisLocation = [location, provinceRaw, population, latlon[0], latlon[1], issues]
            locations.append(thisLocation)
        except:
            None
        print north, south
    print locations
    print problemLocations
    print unknown
    print "North", north
    print "South", south

    with open("locations.csv", "wb") as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        for line in locations:
            writer.writerow(line)

    #latlon = SearchForLatLon(browser, query)
    browser.quit()

def GetCensusDivisions():
    # Get the information on the census divisions:
    # Name, Province, Population, Illustrative
    # If there is no illustrative, fill it with Name
    
    br = mechanize.Browser()

    url = "http://en.wikipedia.org/wiki/List_of_census_divisions_of_Canada_by_population"
    response = br.open(url)
    soup = BeautifulSoup(br.response().read())
    
    table = soup.find_all('tr')

    print "Looking at the table:"
    
    locations = []
    for row in table:
        print "Here comes the row"
        #print row.text
        print "------------------"
        columns = row.find_all('td')
        try:
            # Test that the first column is a number, incidating it was used in 2011 census
            int(columns[0].find('span','sorttext').text)

            #print columns[0].find('span','sorttext').text
            #print "*"
            #print columns[1].find('span','sorttext').text
            #print "**"
            
            name = columns[2].find('span','sorttext').text
            print name
            print "***"
            province = columns[4].find('span','sorttext').text
            print province
            print "****"
            population = int(columns[5].text.replace(',',''))
            print population
            # int(data.replace(',', ''))
            print "*****"
            illustrative = columns[8].text
            print illustrative
            if illustrative == '':
                illustrative = name
                print illustrative
            #print "******"
            #print columns[8].a # gives the href
            #print "*******"
            #print columns[8].a.text # alternate
            thisLocation = [name.encode('utf-8'), province, population, illustrative.encode('utf-8')]
            locations.append(thisLocation)
        except:
            None
        print "=================="
    print locations
    with open("divisions.csv", "wb") as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        for line in locations:
            writer.writerow(line)

# next:  Selenium Webdriver to go to the page and find the coordinates

def GetCoordinatesSelenium():
    # start on the wikipedia census division page
    browser = webdriver.Firefox()
    
    url = 'http://en.wikipedia.org/wiki/List_of_census_divisions_of_Canada_by_population'

    browser.get(url)

    # Get the information on the census divisions:
    # Name, Province, Population, Illustrative
    # If there is no illustrative, fill it with Name
    
    br = mechanize.Browser()

    url = "http://en.wikipedia.org/wiki/List_of_census_divisions_of_Canada_by_population"
    response = br.open(url)
    soup = BeautifulSoup(br.response().read())
    
    table = soup.find_all('tr')

    print "Looking at the table:"
    rownum = 0
    locations = []
    for row in table:
        rownum += 1
        print "Here comes the row ", rownum
        #print row.text
        print "------------------"
        columns = row.find_all('td')
        try:
            # Test that the first column is a number, incidating it was used in 2011 census
            int(columns[0].find('span','sorttext').text)

            #print columns[0].find('span','sorttext').text
            #print "*"
            #print columns[1].find('span','sorttext').text
            #print "**"
            
            name = columns[2].find('span','sorttext').text
            print name
            print "***"
            province = columns[4].find('span','sorttext').text
            print province
            print "****"
            population = int(columns[5].text.replace(',',''))
            print population
            # int(data.replace(',', ''))
            print "*****"
            illustrative = columns[8].text
            print illustrative
            if illustrative == '':
                illustrative = name
                print illustrative
            #print "******"
            #print columns[8].a # gives the href
            #print "*******"
            #print columns[8].a.text # alternate
            thisLocation = [name.encode('utf-8'), province, population, illustrative.encode('utf-8')]
            locations.append(thisLocation)
            '''
            time.sleep(4)
            print "clicking link"
            link = browser.find_element_by_link_text(name)
            link.click()
            browser.wait_for_page_to_load("5000")

            # In this section, I'm having difficulty getting the coordinates from the 
            # wikipedia page after I click the link to the district.  Would be nice!
            print "Getting Coordinates maybe"
            wholepage = find_element_by_xpath("//*").get_attribute("outerHTML")
            print wholepage

            # maybe can try getting from here:  <span class="geo">

            geo = browser.find_element_by_class.name('geo')
            print "Printing coordinates maybe"
            print geo.text

            print "Going back"
            browser.back()
            '''
            print "we done"
            return 5
        except:
            None
            print "Error"
            if rownum > 2:
                return 0
            #return 0
        print "=================="

# What are my thoughts on the previous function?
# What about the getting coordinates?  Did I try BeautifulSoup?
    
# Assuming you are already on the census division page, look for the coordinates
# Good example:  Toronto - http://en.wikipedia.org/wiki/Toronto
# Fail example:  Montreal - http://en.wikipedia.org/wiki/Urban_agglomeration_of_Montreal
# Example - Alberta only coordiantes in upper right - http://en.wikipedia.org/wiki/Division_No._6,_Alberta
def GetCoordinatesFromPageSoup():
    br = mechanize.Browser()
    url = "http://en.wikipedia.org/wiki/Toronto"
    response = br.open(url)
    soup = BeautifulSoup(br.response().read())
    

def GetCoordinatesSoup():
    # Get the information on the census divisions:
    # Name, Province, Population, Illustrative
    # If there is no illustrative, fill it with Name
    
    br = mechanize.Browser()

    url = "http://en.wikipedia.org/wiki/List_of_census_divisions_of_Canada_by_population"
    response = br.open(url)
    soup = BeautifulSoup(br.response().read())
    
    table = soup.find_all('tr')

    print "Looking at the table:"
    rownum = 0
    locations = []
    errorRows = []
    for row in table:
        rownum += 1
        print "Here comes the row ", rownum
        #print row.text
        print "------------------"
        columns = row.find_all('td')
        try:
            # Test that the first column is a number, incidating it was used in 2011 census
            int(columns[0].find('span','sorttext').text)

            #print columns[0].find('span','sorttext').text
            #print "*"
            #print columns[1].find('span','sorttext').text
            #print "**"
            
            name = columns[2].find('span','sorttext').text.encode('utf-8')
            print name
            print "And href"
            locURL = columns[2].find('span','sorttext')
            print locURL
            locURL = locURL.a['href'].encode('utf-8')
            print locURL
            locURL = urljoin(url,locURL)
            print locURL
            latlon = GetCoordinatesFromWikipediaPage(br,locURL)
            print "***"
            province = columns[4].find('span','sorttext').text.encode('utf-8')
            print province
            print "****4 - getting population"
            population = int(columns[5].text.replace(',',''))
            print population
            # int(data.replace(',', ''))
            print "*****5 - Getting illustrative"
            illustrative = columns[8].text.encode('utf-8')
            illustrativeURL = ''
            print illustrative
            if illustrative != '':
                illustrativeURL = columns[8]
                #print illustrativeURL
                illustrativeURL = illustrativeURL.a['href'].encode('utf-8')
                print illustrativeURL
                illustrativeURL = urljoin(url, illustrativeURL)
                print illustrativeURL
                if latlon is None:
                    print "Calculating latlon from Illustrative"
                    latlon = GetCoordinatesFromWikipediaPage(br,illustrativeURL)
            else:
                print "NO ILLUSTRATIVE"
                
            print "******6"
            print latlon
            if latlon is None:
                latlon = None,None
            #print columns[8].a # gives the href
            print "*******7"
            #print columns[8].a.text # alternate
            thisLocation = [name, province, population, illustrative,latlon[0],latlon[1]]
            locations.append(thisLocation)
            print thisLocation

            '''
            time.sleep(4)
            print "clicking link"
            link = browser.find_element_by_link_text(name)
            link.click()
            browser.wait_for_page_to_load("5000")

            # In this section, I'm having difficulty getting the coordinates from the 
            # wikipedia page after I click the link to the district.  Would be nice!
            print "Getting Coordinates maybe"
            wholepage = find_element_by_xpath("//*").get_attribute("outerHTML")
            print wholepage

            # maybe can try getting from here:  <span class="geo">

            geo = browser.find_element_by_class.name('geo')
            print "Printing coordinates maybe"
            print geo.text

            print "Going back"
            browser.back()
            
            if rownum > 3:
                print "we done"
                return locations
            '''
        except ValueError,AttributeError:
            None
        except:
            None
            #print sys.exc_info()[0]
            #errorRows.append(rownum)
            
            #if rownum > 2:
            #    return 0
            #return 0
        print "=================="
    print locations
    with open("divisionpopulations.csv", "wb") as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        for line in locations:
            writer.writerow(line)
    print errorRows



# 
def GetCoordinatesFromWikipediaPage(br, url):
    print "Getting location coordinates:"
    print url
    response = br.open(url)
    print "X1"
    soup = BeautifulSoup(br.response().read())
    print "X2"
    latlon = soup.find(class_="geo")
    print "X3"
    if latlon is not None:
        return tuple([float(x) for x in latlon.text.split(';')])
        print latlon.text
    else:
        return None

def FindNorthAndSouthPopulations(lat):
    north = 0
    south = 0
    with open('CanadaPopulations.csv','rb') as csvfile:
        divisions = csv.reader(csvfile, delimiter=',')
        for division in divisions:
            print division[0], division[2], division[4]
            if float(division[4]) < lat:
                south += int(division[2])
            else:
                north += int(division[2])
            print north, south
    print "North = ", north
    print "South = ", south
    return north, south

br = mechanize.Browser()
testMontreal = 'http://en.wikipedia.org/wiki/Montr%C3%A9al_(region)'
    
