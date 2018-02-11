#!/usr/bin/python

# -*- coding: utf-8 -*-

'''
Author: Yuri Medvinsky
Info: 
  ise ebay api to search for completed items that were sold on ebay.
  Then print out information pertaining to those listings.
'''



from ebaysdk.finding import Connection as Finding
from ebaysdk.exception import ConnectionError
from optparse import OptionParser
import datetime
import pprint
import time
import sys
import os





#################################################
#
# Help Menu
#
def menu():
  usage = "usage: %prog -d [number of days] -c [categoryid]"

  parser = OptionParser(usage=usage)
  parser.add_option("-c", action="store", type="int", dest="CategoryID")
  parser.add_option("-d", action="store", type="int", dest="days", default="30")

  (options, args) = parser.parse_args()

  return options.CategoryID, options.days






#################################################
#
# Run Finding API for Ebay to search for 
# completed items that were sold
#
#def findingAPI(page, numEntriesPerPage, earlierDay, nowTime, categoryID):
def findingAPI(page, earlierDay, nowTime, categoryID):


  ### Reference config file to get APPID
  api = Finding(config_file='config/ebay.yaml')



  # Setup api_request options to later pass to api execution
  api_request = {
    'categoryId': categoryID,
    'itemFilter': [
      {'name': 'MinPrice',      'value': '30'},          # Minimum Price
      {'name': 'MaxPrice',      'value': '10000'},       # Maximum Price
      {'name': 'SoldItemsOnly', 'value': 'True'},        # Show only successfully sold items
      {'name': 'LocatedIn',     'value': 'US'},          # Located in United States
      {'name': 'StartTimeFrom', 'value': earlierDay},    # Time in UTC format YYYY-MM-DDTHH:MM:SS.000Z (Z for Zulu Time). (e.g: '2018-01-1T08:00:01')
      {'name': 'EndTimeTo',     'value': nowTime}        # Time in UTC format YYYY-MM-DDTHH:MM:SS.000Z (Z for Zulu Time). (e.g: '2018-01-19T14:30:01')
    ],
    'paginationInput': {
      'entriesPerPage': 100,
      'pageNumber': page
      #'pageNumber': '1'                                 # e.g: custom page
    }
  } 


  ### Execute against findCompletedItems with designated api_request options
  api.execute('findCompletedItems', api_request)

  ### Return results as json form dictionary
  results = api.response.dict()
    
  return results






#################################################
#
# Take current date/time and subtrace given time days
#
def CalculateDate(days):

  earlierDay = datetime.datetime.now() - datetime.timedelta(days=days, hours=0, minutes=0, seconds=0)
  earlierDay = earlierDay.strftime("%Y-%m-%dT%H:%M:%S")

  return earlierDay





#################################################
#
# Calculate how long it took to sell an item
#
def calculateSoldTime(startTime, endTime):

  startTime = ' '.join((startTime).replace('T', ' ').replace('.', ' ').split()[0:2])
  endTime   = ' '.join((endTime).replace('T', ' ').replace('.', ' ').split()[0:2])

  startTime = datetime.datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S')
  endTime   = datetime.datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S')

  soldTime = endTime - startTime


  return soldTime






#################################################
#
# Write to File
# 
def writeToFile(data, totalSoldTime, File):


  ### Write to file
  with open(File, 'a') as f:
    f.write("{0}, {1}, {2}, {3:7}, [{4:16}], {5}\n".format(data['categoryId'], \
                                                 data['categoryName'], \
                                                 data['itemId'], \
                                                 data['currencyValue'], \
                                                 totalSoldTime, \
                                                 data['viewItemURL']))






#################################################
#
# Get Header info
#
def getHEADER(results):

  ### HEADING: Display total pages, entries, number of pages and entries per page
  try:
    print "Ack: %s       " % results['ack']
    print "Timestamp: %s " % results['timestamp']
    print "Version: %s   " % results['version']
    print
  except KeyError, e:
    print "[-] %s" % e






 
#################################################
#
# Show results from ebay that have been sold
#
def showResults(results, File): 
  

  
  ### The (results['searchResult']['item']) is an array that holds all sold items found per page. 
  ### We loop through this array and extract elements that we can work with
 

  data = {}   
  for i in range(len(results['searchResult']['item'])):
    try:
      data['itemId']               = results['searchResult']['item'][i]['itemId']
      data['categoryId']           = results['searchResult']['item'][i]['primaryCategory']['categoryId']
      data['categoryName']         = results['searchResult']['item'][i]['primaryCategory']['categoryName']
      data['topRatedListing']      = results['searchResult']['item'][i]['topRatedListing']
      data['globalId']             = results['searchResult']['item'][i]['globalId']
      data['currencyId']           = results['searchResult']['item'][i]['sellingStatus']['currentPrice']['_currencyId']
      data['currencyValue']        = results['searchResult']['item'][i]['sellingStatus']['currentPrice']['value']
      data['sellingState']         = results['searchResult']['item'][i]['sellingStatus']['sellingState']
      data['listingType']          = results['searchResult']['item'][i]['listingInfo']['listingType']
      #data['conditionDisplayName'] = results['searchResult']['item'][i]['condition']['conditionDisplayName']
      data['startTime']            = results['searchResult']['item'][i]['listingInfo']['startTime']
      data['endTime']              = results['searchResult']['item'][i]['listingInfo']['endTime']
      #data['watchCount']           = results['searchResult']['item'][i]['listingInfo']['watchCount']
      data['viewItemURL']          = results['searchResult']['item'][i]['viewItemURL']

    except KeyError:
      #continue
      raise



    ### This means that conditionDisplayName is empty and it needs to have something
    try:
      data['conditionDisplayName'] = results['searchResult']['item'][i]['condition']['conditionDisplayName']
    except KeyError:
      data['conditionDisplayName'] = 'n/a'



    ### This means that watchcount is empty and it needs to have something
    try:
      data['watchCount']           = results['searchResult']['item'][i]['listingInfo']['watchCount']
    except KeyError:
      data['watchCount']           = 'n/a'
     


    ### Calculate how long it took to sell the item
    try:
      totalSoldTime = calculateSoldTime((data['startTime']), (data['endTime']))
    except:
      continue



    ### Save data to file
    writeToFile(data, totalSoldTime, File)
  

     




def getCategoryIDFromFile():
  print "Reading Category ID File"
  if os.path.isfile('categoryid.txt') == True:
    with open('categoryid.txt') as f:
      content = f.readlines()

      categoryID = {}
      for i in content:
        i = ''.join(i.split())
        categoryID[i.split(',')[0]] = i.split(',')[1]


  return categoryID






def main():

  ### Receive options from user input
  (categoryID, days)=menu()


  ### If categoryID is not provided by user, access file and store in hash
  if categoryID == None:
    categoryID = getCategoryIDFromFile()



  ### Create Empty File
  File = 'short-listings.txt'
  open(File, 'w').close()



  ### Calculate From Date the time from which to search
  earlierDay = CalculateDate(days)                              


  ### Calculate Todays Date and Time or time to which to search
  nowTime = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")



  #########################################################################
  ### Initial run of findingAPI() function to identify how many pages exist and
  ### how many entries per page exist
  ###
  ### The page variable is used to retreive the total number of pages
  page = 1
  results = findingAPI(page, earlierDay, nowTime, categoryID)



  try:
    totalPages   = int(results['paginationOutput']['totalPages'])      # e.g: (6 pages)
    totalEntries = int(results['paginationOutput']['totalEntries'])    # e.g: (515 entries)

    print "totalPages:   {0}".format(totalPages)
    print "totalEntries: {0}".format(totalEntries)

  except KeyError:
    pass




  ### Display header information (e.g: ack, version, timestamp) 
  getHEADER(results)



  while totalPages >= 1:

    ### Results from findingAPI contain all sold items found per page
    results = findingAPI(page, earlierDay, nowTime, categoryID)

    pageNumber = results['paginationOutput']['pageNumber']
    print
    print "Page Number: {0}".format(pageNumber) 


    ### Show results from Ebay 
    showResults(results, File)



    ### loop over number of sold items found per page
    for i in range(len(results['searchResult']['item'])):
      print i, results['searchResult']['item'][i]['viewItemURL']  


    totalPages = totalPages - 1
    page = page + 1


  

  #pp = pprint.PrettyPrinter(indent=1)
  #pp.pprint(results)





if __name__ == '__main__':
  main()
