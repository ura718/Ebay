#!/usr/bin/python

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

  # Show only completed items for specific category
  api.execute('findCompletedItems', {'categoryId': '619'})

  results = api.response.dict()
  
  return results



'''
{'ack': 'Success', 'timestamp': '2018-01-17T05:38:38.040Z', 'version': '1.13.0', 'searchResult': {'item': [{'itemId': '172986666895', 'topRatedListing': 'false', 'globalId': 'EBAY-US', 'title': u'Pioneer stereo turntable PL-70L\u2161', 'country': 'JP', 'primaryCategory': {'categoryId': '48460', 'categoryName': 'DJ Turntables'}, 'autoPay': 'false', 'galleryURL': 'http://thumbs4.ebaystatic.com/m/mvahl02AsBVZqXx8ctbAr_g/140.jpg', 'shippingInfo': {'expeditedShipping': 'false', 'shipToLocations': 'Worldwide', 'shippingServiceCost': {'_currencyId': 'USD', 'value': '178.0'}, 'oneDayShippingAvailable': 'false', 'handlingTime': '10', 'shippingType': 'Flat'}, 'location': 'Japan', 'returnsAccepted': 'true', 'viewItemURL': 'http://www.ebay.com/itm/Pioneer-stereo-turntable-PL-70L-/172986666895', 'sellingStatus': {'currentPrice': {'_currencyId': 'USD', 'value': '2650.0'}, 'convertedCurrentPrice': {'_currencyId': 'USD', 'value': '2650.0'}, 'sellingState': 'EndedWithoutSales'}, 'paymentMethod': 'PayPal', 'isMultiVariationListing': 'false', 'condition': {'conditionId': '3000', 'conditionDisplayName': 'Used'}, 'listingInfo': {'listingType': 'FixedPrice', 'gift': 'false', 'bestOfferEnabled': 'true', 'watchCount': '3', 'startTime': '2017-11-18T05:09:45.000Z', 'buyItNowAvailable': 'false', 'endTime': '2018-01-17T05:37:40.000Z'}}
'''


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
   - Show me only those items that have been sold from top sellers
   - We are getting length of search result itmes which is an array. And we are looping through each element of that array.
  """
  for i in range(len(results['searchResult']['item'])):
    if results['searchResult']['item'][i]['sellingStatus']['sellingState'] == 'EndedWithSales' and results['searchResult']['item'][i]['topRatedListing'] == 'true':
      print "{0:3}) Top Rated: {1:5}, Market: {2:7}, Currency: {3:3}, Price: {4}, Selling State: {5}, Listing: {6}, URL: {7}".format(i, \
                                                                          results['searchResult']['item'][i]['topRatedListing'], \
                                                                          results['searchResult']['item'][i]['globalId'], \
                                                                          results['searchResult']['item'][i]['sellingStatus']['currentPrice']['_currencyId'], \
                                                                          results['searchResult']['item'][i]['sellingStatus']['currentPrice']['value'], \
                                                                          results['searchResult']['item'][i]['sellingStatus']['sellingState'], \
                                                                          results['searchResult']['item'][i]['listingInfo']['listingType'], \
                                                                          results['searchResult']['item'][i]['viewItemURL'])

if __name__ == '__main__':
  main()
