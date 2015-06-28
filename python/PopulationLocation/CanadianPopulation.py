# Functions for Calculating Canadian Population Locations

import csv
import mechanize
from bs4 import BeautifulSoup

from urlparse import urljoin

# Use BeautifulSoup to get Coordinates from wikipedia
def GetCanadaCensusInfoFromWikipedia(outFile):
    # Get the information on the census divisions:
    # Name, Province, Population, Illustrative
    # If there is no illustrative, fill it with Name
    
    br = mechanize.Browser()

    url = "http://en.wikipedia.org/wiki/List_of_census_divisions_of_Canada_by_population"
    response = br.open(url)
    soup = BeautifulSoup(br.response().read())
    
    table = soup.find_all('tr')

    print "Looking at the table:"
    rowNum = 0
    locations = []
    errorRows = []
    for row in table:
        print "Evaluating row: ", rowNum
        print "-----------------------"
        columns = row.find_all('td')
        try:
            # Test that the first column is a number, incidating it was used in 2011 census
            int(columns[0].find('span','sorttext').text)
            # Column 2 - Census Division 
            name = columns[2].find('span','sorttext').text.encode('utf-8')
            print name
            print "*** Getting href to the census division's wikipedia page"
            locURL = columns[2].find('span','sorttext')
            locURL = locURL.a['href'].encode('utf-8')
            locURL = urljoin(url,locURL)
            print locURL

            # Get the lat/lon coordinates from the census division page
            latlon = GetCoordinatesFromWikipediaPage(br,locURL)

            # Column 4 - Province (abbreviated)
            province = columns[4].find('span','sorttext').text.encode('utf-8')

            # Column 5 - Population from 2011 census
            population = int(columns[5].text.replace(',',''))

            # Column 8 - Illustrative census subdivision
            illustrative = columns[8].text.encode('utf-8')
            illustrativeURL = ''

            if illustrative != '':
                illustrativeURL = columns[8]
                #print illustrativeURL
                illustrativeURL = illustrativeURL.a['href'].encode('utf-8')
                illustrativeURL = urljoin(url, illustrativeURL)
                print "*** Getting href to the census illustrative division's wikipedia page"
                print illustrativeURL
                # If we couldn't retrieve the latlon from the division's page, try the subdivision's page
                if latlon is None:
                    print "**** Calculating latlon from Illustrative"
                    latlon = GetCoordinatesFromWikipediaPage(br,illustrativeURL)
            else:
                print "NO ILLUSTRATIVE"

            #print latlon
            if latlon is None:
                print "!!!!! NO COORDINATES !!!!!!"
                latlon = None,None

            # Create a list of the data we used to calculate the population and location
            thisLocation = [name, province, population, illustrative,latlon[0],latlon[1]]
            # Append this division's list to the master list of all divisions
            locations.append(thisLocation)
            print "*** This location"
            print thisLocation

        except ValueError,AttributeError:
            None
        except:
            None

        print "======================="
        rowNum += 1

    # Write all locations to the outfile
    with open(outFile, "wb") as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        for line in locations:
            writer.writerow(line)
    print "Printing Error Rows"
    print errorRows

# Get the lat/lon coordinates of a municipality from the city's wikipedia page
def GetCoordinatesFromWikipediaPage(br, url):
    response = br.open(url)
    soup = BeautifulSoup(br.response().read())
    latlon = soup.find(class_="geo")
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

def FindPercentageOfCanadaPopulation(latitude):
    populations = FindNorthAndSouthPopulations(latitude)
    totalPopulation = populations[0] + populations[1]
    percentNorth = float(populations[0]) / totalPopulation * 100
    percentSouth = float(populations[1]) / totalPopulation * 100
    print "Total population = ", totalPopulation
    print "Population living north of latitude {0:.5f} is {1}.".format(latitude, populations[0])
    print "Population living south of latitude {0:.5f} is {1}.".format(latitude, populations[1])
    print "{0:.2f}% of Canada's population lives north of latitude {1:.5f}!".format(percentNorth, latitude)
    print "{0:.2f}% of Canada's population lives south of latitude {1:.5f}!".format(percentSouth, latitude)
    
    #print "Population living south of %d is %d." % (latitude, populations[1])


br = mechanize.Browser()
