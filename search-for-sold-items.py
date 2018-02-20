#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Search for items that have already been sold
# e.g:
#   script -s 'bose solo 5'
#
#

import os
import datetime
import time
from ebaysdk.finding import Connection as Finding
from ebaysdk.exception import ConnectionError
from optparse import OptionParser





#################################################
#
# Help Menu
#
def menu():
  usage = "usage: %prog -s \"search string\" "

  parser = OptionParser(usage=usage)
  parser.add_option("-s", action="store", type="str", dest="search")

  (options, args) = parser.parse_args()

  return options.search





#################################################
#
# Run Finding API
#
def FindingAPI(search_input, pageNumber):

  try:
    api = Finding(config_file='config/ebay.yaml')

    api_dictionary = {
      'keywords': search_input,
      #'itemFilter' : [
        #{'name': 'Condition', 'value': 'Used'},
        #{'name': 'MinPrice', 'value': '200', 'paramName': 'Currency', 'paramValue': 'USD'},
        #{'name': 'MaxPrice', 'value': '400', 'paramName': 'Currency', 'paramValue': 'USD'},
      #],
      'pageinationInput': {
        'entriesPerPage': '100',
        'pageNumber': pageNumber
      },
      'sortOrder': 'CurrentPriceHighest'

    }

    # Execute api HTTP request to ebay and provide dictionary parameters
    response = api.execute('findCompletedItems', api_dictionary)
 
    # Return diction of the HTTP response
    response = response.dict()

    return response

  except ConnectionError as e:
    print e
    print e.response.dict()





#################################################
#
# Calculate how long it took to sell an item
#
def calculateSoldTime(startTime, endTime):


  '''
  e.g: 2018-02-17T16:20:02.592Z
    replace date/time by 'T' => [2018-02-17 16:20:02.592Z]
    replace date/time by '.' => [2018-02-17 16:20:02 592Z]
    splity by spaces and get from [0:2] range which is only up to 2nd element excluding 3rd [2018-02-17 16:20:02]
    parse string [2018-02-17 16:20:02] back to datetime format
  '''


  startTime = ' '.join((startTime).replace('T', ' ').replace('.', ' ').split()[0:2])
  endTime   = ' '.join((endTime  ).replace('T', ' ').replace('.', ' ').split()[0:2])

  startTime = datetime.datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S')
  endTime   = datetime.datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S')

  soldTime = endTime - startTime


  return soldTime





#################################################
#
# Put Results from Finding API into hash for easy access
#
def showResults(results):

  ### The (results['searchResult']['item']) is an array that holds all sold items found per page.
  ### We loop through this array and extract elements that we can work with


  data = {}
  for i in range(len(results['searchResult']['item'])):
    try:
      data['itemId']               = results['searchResult']['item'][i]['itemId']
      data['title']                = results['searchResult']['item'][i]['title']
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
      data['watchCount']           = '0'


   ### Calculate how long it took to sell the item
    try:
      totalSoldTime = calculateSoldTime((data['startTime']), (data['endTime']))
    except:
      continue


    ### Use the .encode('utf-8') to address weird characters
    print "{0}, [{1:20}], {2}, {3}, {4}".format(data['itemId'], \
                            totalSoldTime, \
                            data['currencyValue'], \
                            data['title'].encode('utf-8'), \
                            data['viewItemURL'] )





def main():

  search_input = menu()
 
  results = FindingAPI(search_input, pageNumber=1)
   

  ### HEADING: Display total pages, entries, number of pages and entries per page
  try:
    print "Ack: %s         " % results['ack']
    print "Timestamp: %s   " % results['timestamp']
    print "Version: %s     " % results['version']
    print "Total Pages: %s " % results['paginationOutput']['totalPages']      # e.g: (6 pages)
    print "TotalEntries %s " % results['paginationOutput']['totalEntries']    # e.g: (515 entries)
    print
  except KeyError, e:
    print "[-] %s" % e 



  showResults(results)



if __name__ == '__main__':
  main()



