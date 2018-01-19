#!/usr/bin/python


#
# Author: Yuri Medvinsky
# Info: Use ebay api to search for completed items that were sold on ebay.
#  Then print out information pertaining to those listings.
#




from ebaysdk.finding import Connection as Finding
from ebaysdk.exception import ConnectionError


#################################################
#
# Run Finding API for Ebay to search for 
# completed items
#
def runAPI():
  # Reference config file to get APPID
  api = Finding(config_file='ebay.yaml')

  api_request = {
    'categoryId': '100223',
    'itemFilter': [
      {'name': 'MinPrice', 'value': '20'},
      {'name': 'MaxPrice', 'value': '1000'}
    ],
    'paginationInput': {
      'entriesPerPage': '100',
      'pageNumber': '1'
    }
  } 


  api.execute('findCompletedItems', api_request)

  results = api.response.dict()
  
  return results





def main():

  results = runAPI()

  # Display total pages, entries, number of pages and entries per page
  try:
    print "Ack: %s " % results['ack']
    print "Timestamp: %s " % results['timestamp']
    print "Version: %s " % results['version']
  except KeyError, e:
    print "[-] %s" % e


  """
   - Show me only those items that have been sold
   - Get length of array item, and loop through each element of that array.
  """
  for i in range(len(results['searchResult']['item'])):
    if results['searchResult']['item'][i]['sellingStatus']['sellingState'] == 'EndedWithSales':


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
      (sDate, sTime) = (results['searchResult']['item'][i]['listingInfo']['startTime']).replace('T', ' ').replace('.', ' ').split()[0:2]
      (eDate, eTime) = (results['searchResult']['item'][i]['listingInfo']['endTime']).replace('T', ' ').replace('.', ' ').split()[0:2]
      print "{0:3}) Start Time: {1} {2}".format(i, sDate, sTime)
      print "{0:3}) End Time:   {1} {2}".format(i, eDate, eTime)


      print "{0:3}) {1}".format(i, results['searchResult']['item'][i]['viewItemURL'])
      print "-"*150



if __name__ == '__main__':
  main()
