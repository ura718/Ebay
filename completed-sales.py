#!/usr/bin/python

# -*- coding: utf-8 -*-

'''
Author: Yuri Medvinsky
Info: 
  Use ebay api to search for completed items that were sold on ebay.
  Then print out information pertaining to those listings.
'''



from ebaysdk.finding import Connection as Finding
from ebaysdk.exception import ConnectionError
import datetime
import time
import sys
import pprint





#################################################
#
# Run Finding API for Ebay to search for 
# completed items that were sold
#
def runAPI(page, numEntriesPerPage, minusDays, nowTime):


  ### Reference config file to get APPID
  api = Finding(config_file='config/ebay.yaml')



  # Setup api_request options to later pass to api execution
  api_request = {
    'categoryId': '15687',
    'itemFilter': [
      {'name': 'MinPrice',      'value': '30'},          # Minimum Price
      {'name': 'MaxPrice',      'value': '1000'},        # Maximum Price
      {'name': 'SoldItemsOnly', 'value': 'True'},        # Show only successfully sold items
      {'name': 'LocatedIn',     'value': 'US'},          # Located in United States
      {'name': 'StartTimeFrom', 'value': minusDays},     # Time in UTC format YYYY-MM-DDTHH:MM:SS.000Z (Z for Zulu Time). (e.g: '2018-01-1T08:00:01')
      {'name': 'EndTimeTo',     'value': nowTime}        # Time in UTC format YYYY-MM-DDTHH:MM:SS.000Z (Z for Zulu Time). (e.g: '2018-01-19T14:30:01')
    ],
    'paginationInput': {
      'entriesPerPage': numEntriesPerPage,
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
# Subtract x number of days from today and return value
#
def CalculateDate(days):

  ### Convert current time to epoch time
  epoch = int(time.time())
  
  ### Subtract x days from current epoch time, (e.g: seven days = 60 * 60 * 24 * 7 = 604800)
  minusDays = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime(epoch - (60 * 60 * 24 * days)))
  
  return minusDays






#################################################
#
# Write to File
# 
def WriteToFile(categoryName, categoryId, itemId, currencyValue, viewItemURL):


  ### Write to file
  with open('listings.txt', 'a') as f:
    f.write("{0}, {1}, {2}, {3:5}, {4}\n".format(categoryName, categoryId, itemId, currencyValue, viewItemURL))










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
    #print "-"*150
  except KeyError, e:
    print "[-] %s" % e









 
#################################################
#
# Show results from ebay
#
def showResults(results): 
  

  """
   - Show me only those items that have been sold
   - Get length of array item, and loop through each element of that array.
  """

  try:
    for i in range(len(results['searchResult']['item'])):

      ### Test watchcount for KeyError (its when value of key is not present). If so assign default value of zero
      try:
        watchCount = results['searchResult']['item'][i]['listingInfo']['watchCount']
      except KeyError:
        watchCount = results['searchResult']['item'][i]['listingInfo']['watchCount'] = 0



      ### Definitions 
      itemId               = results['searchResult']['item'][i]['itemId']
      categoryId           = results['searchResult']['item'][i]['primaryCategory']['categoryId']
      categoryName         = results['searchResult']['item'][i]['primaryCategory']['categoryName']
      topRatedListing      = results['searchResult']['item'][i]['topRatedListing']
      globalId             = results['searchResult']['item'][i]['globalId']
      currencyId           = results['searchResult']['item'][i]['sellingStatus']['currentPrice']['_currencyId']
      currencyValue        = results['searchResult']['item'][i]['sellingStatus']['currentPrice']['value']
      sellingState         = results['searchResult']['item'][i]['sellingStatus']['sellingState']
      listingType          = results['searchResult']['item'][i]['listingInfo']['listingType']
      conditionDisplayName = results['searchResult']['item'][i]['condition']['conditionDisplayName']
      startTime            = results['searchResult']['item'][i]['listingInfo']['startTime']
      endTime              = results['searchResult']['item'][i]['listingInfo']['endTime']
      viewItemURL          = results['searchResult']['item'][i]['viewItemURL']




      ### Print Category ID and Name
      print "{0:3}) CategoryID: {1}, Category Name: {2}".format(i, categoryId, categoryName)
                                      
                                     

      ### Print selected items from finding api
      print "{0:3}) Top Rated: {1:5}, Market: {2:7}, Currency: {3:3}, Price: {4}, Selling State: {5}, Listing: {6}, WatchCount: {7}".format(i, \
                                      topRatedListing, \
                                      globalId, \
                                      currencyId, \
                                      currencyValue, \
                                      sellingState, \
                                      listingType, \
                                      watchCount)

      print "{0:3}) Condition:  {1}".format(i, conditionDisplayName)


      ### Extract Date and Time. Use replace() function to replace elements with spaces. Then grab first two elements date and time
      (startDate, startTime) = (startTime).replace('T', ' ').replace('.', ' ').split()[0:2]
      (endDate, endTime)     =   (endTime).replace('T', ' ').replace('.', ' ').split()[0:2]

      print "{0:3}) Start Time: {1} {2}".format(i, startDate, startTime)
      print "{0:3}) End Time:   {1} {2}".format(i, endDate, endTime)


      ### URL
      print "{0:3}) {1}".format(i, viewItemURL)
      print "-"*150



      ### Save data to file
      WriteToFile(categoryName, categoryId, itemId, currencyValue, viewItemURL)


  except KeyError, e:
    print "No Search Results Found"
    print "Try to adjust itemFilter options"
    print e




def main():


  ### Create Empty File
  open('listings.txt', 'w').close()



  ### The page variable is used to retreive page number
  ### The days variable is used to deduct number of days from today
  page = 1
  days = 2


  ### Calculate From Date the time from which to search
  minusDays = CalculateDate(days)                              


  ### Calculate Todays Date and Time or time to which to search
  nowTime = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime())  


  ### Qeury api to understand how many pages exist by sampling page header
  numEntriesPerPage = 100
  results = runAPI(page, numEntriesPerPage, minusDays, nowTime)



  totalPages   = int(results['paginationOutput']['totalPages'])      # e.g: (6 pages)
  totalEntries = int(results['paginationOutput']['totalEntries'])    # e.g: (515 entries)


  print "totalPages:   {0}".format(totalPages)
  print "totalEntries: {0}".format(totalEntries)


  ### Get header information (e.g: ack, version, timestamp) 
  getHEADER(results)



  ### Now loop through total number of pages and get all sold items per page
  for page in range(1, totalPages+1):

    ### Get API Results
    results = runAPI(page, numEntriesPerPage, minusDays, nowTime)

 
    ### Get Page Number 
    pageNumber = results['paginationOutput']['pageNumber']
    print "Page Number: {0} Total Entries: {1} \n".format(pageNumber, totalEntries) 



    ### Show results from Ebay 
    showResults(results)



    ### Calculate how many entries are left to fit on one page
    totalEntries = totalEntries - numEntriesPerPage



    '''
    print "{0}, {1}".format(results['searchResult']['item'][0]['itemId'], results['searchResult']['item'][0]['viewItemURL'])
    results = runAPI(page=2, days=5, numEntriesPerPage=100)
    print "{0}, {1}".format(results['searchResult']['item'][0]['itemId'], results['searchResult']['item'][0]['viewItemURL'])

    pp = pprint.PrettyPrinter(indent=1)
    pp.pprint(results)
    '''







if __name__ == '__main__':
  main()
