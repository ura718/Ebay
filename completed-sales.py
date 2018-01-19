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




#################################################
#
# Subtract x number of days from today and return value
#
def CalculateDate(days):

  # Convert current time to epoch time
  epoch = int(time.time())
  
  # Subtract x days from current epoch time, (e.g: seven days = 60 * 60 * 24 * 7 = 604800)
  minusDays = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime(epoch - (60 * 60 * 24 * days)))
  
  return minusDays




#################################################
#
# Run Finding API for Ebay to search for 
# completed items that were sold
#
def runAPI():
  # Reference config file to get APPID
  api = Finding(config_file='config/ebay.yaml')


  page = 1
  days = 1
  minusDays = CalculateDate(days)
  nowTime = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime())


  # Setup api_request options to later pass to api execution
  api_request = {
    'categoryId': '100223',
    'itemFilter': [
      {'name': 'MinPrice', 'value': '10'},               # Minimum Price
      {'name': 'MaxPrice', 'value': '1000'},             # Maximum Price
      {'name': 'SoldItemsOnly', 'value': 'True'},        # Show only successfully sold items
      {'name': 'LocatedIn', 'value': 'US'},              # Located in United States
      {'name': 'StartTimeFrom', 'value': minusDays},     # Time in UTC format YYYY-MM-DDTHH:MM:SS.000Z (Z for Zulu Time). (e.g: '2018-01-1T08:00:01')
      {'name': 'EndTimeTo', 'value': nowTime}            # Time in UTC format YYYY-MM-DDTHH:MM:SS.000Z (Z for Zulu Time). (e.g: '2018-01-19T14:30:01')
    ],
    'paginationInput': {
      'entriesPerPage': '100',
      'pageNumber': page
      #'pageNumber': '1'
    }
  } 



  # Execute against findCompletedItems with designated api_request options
  api.execute('findCompletedItems', api_request)

  # Return results as json form dictionary
  results = api.response.dict()
  
  return results





def main():
 
  results = runAPI()

  
  # HEADING: Display total pages, entries, number of pages and entries per page
  try:
    print "Ack: %s " % results['ack']
    print "Timestamp: %s " % results['timestamp']
    print "Version: %s " % results['version']
    print
    print "-"*150
  except KeyError, e:
    print "[-] %s" % e




  """
   - Show me only those items that have been sold
   - Get length of array item, and loop through each element of that array.
  """

  try:
    for i in range(len(results['searchResult']['item'])):

      # Test watchcount for KeyError (its when value of key is not present). If so assign default value of zero
      try:
        results['searchResult']['item'][i]['listingInfo']['watchCount']
      except KeyError:
        results['searchResult']['item'][i]['listingInfo']['watchCount'] = 0


      # Print Category ID and Name
      print "{0:3}) CategoryID: {1}, Category Name: {2}".format(i, \
                                      results['searchResult']['item'][i]['primaryCategory']['categoryId'], \
                                      results['searchResult']['item'][i]['primaryCategory']['categoryName'])

      # Print selected items from finding api
      print "{0:3}) Top Rated: {1:5}, Market: {2:7}, Currency: {3:3}, Price: {4}, Selling State: {5}, Listing: {6}, WatchCount: {7}".format(i, \
                                      results['searchResult']['item'][i]['topRatedListing'], \
                                      results['searchResult']['item'][i]['globalId'], \
                                      results['searchResult']['item'][i]['sellingStatus']['currentPrice']['_currencyId'], \
                                      results['searchResult']['item'][i]['sellingStatus']['currentPrice']['value'], \
                                      results['searchResult']['item'][i]['sellingStatus']['sellingState'], \
                                      results['searchResult']['item'][i]['listingInfo']['listingType'], \
                                      results['searchResult']['item'][i]['listingInfo']['watchCount'])

      print "{0:3}) Condition:  {1}".format(i, results['searchResult']['item'][i]['condition']['conditionDisplayName'])


      # Extract Date and Time. Use replace() function to replace elements with spaces. Then grab first two elements date and time
      (startDate, startTime) = (results['searchResult']['item'][i]['listingInfo']['startTime']).replace('T', ' ').replace('.', ' ').split()[0:2]
      (endDate, endTime) = (results['searchResult']['item'][i]['listingInfo']['endTime']).replace('T', ' ').replace('.', ' ').split()[0:2]
      print "{0:3}) Start Time: {1} {2}".format(i, startDate, startTime)
      print "{0:3}) End Time:   {1} {2}".format(i, endDate, endTime)


      print "{0:3}) {1}".format(i, results['searchResult']['item'][i]['viewItemURL'])
      print "-"*150

  except KeyError, e:
    print "No Search Results Found"
    print "Try to adjust itemFilter options"
    print e




if __name__ == '__main__':
  main()
