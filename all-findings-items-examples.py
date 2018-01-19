#!/usr/bin/python
# -*- coding: utf-8 -*-


#
# Test printing out elements from dictionary results{} 
# print examples on how to target specific items
#
#




import pprint

############################################
#
# Snippet code test
# 
def snippet_test():

  # Testing snippet from large pool of data
  results={'itemSearchURL': 'http://www.ebay.com/sch/i.html?_nkw=Python&_ddo=1&_ipg=100&_pgn=1', 'paginationOutput': {'totalPages': '986', 'entriesPerPage': '100', 'pageNumber': '1', 'totalEntries': '98526'}, 'ack': 'Success', 'timestamp': '2017-12-19T20:35:44.689Z', 'searchResult': {'item': [{'itemId': '132440104531', 'topRatedListing': 'false', 'globalId': 'EBAY-US', 'title': 'TAHARI LARGE  GENUINE EMBOSSED PYTHON SOFT SUEDE LEATHER HANDBAG With DUSTBAG', 'country': 'US', 'primaryCategory': {'categoryId': '63852', 'categoryName': 'Handbags & Purses'}, 'autoPay': 'true', 'galleryURL': 'http://thumbs4.ebaystatic.com/m/mXUiDhunyDVevnlxthxpvew/140.jpg', 'shippingInfo': {'expeditedShipping': 'true', 'shippingType': 'Calculated', 'handlingTime': '3', 'oneDayShippingAvailable': 'false', 'shipToLocations': 'Worldwide'}, 'location': 'Lancaster,CA,USA', 'postalCode': '93539', 'returnsAccepted': 'false', 'viewItemURL': 'http://www.ebay.com/itm/TAHARI-LARGE-GENUINE-EMBOSSED-PYTHON-SOFT-SUEDE-LEATHER-HANDBAG-DUSTBAG-/132440104531', 'sellingStatus': {'currentPrice': {'_currencyId': 'USD', 'value': '49.99'}, 'timeLeft': 'P29DT23H36M17S', 'convertedCurrentPrice': {'_currencyId': 'USD', 'value': '49.99'}, 'sellingState': 'Active'}, 'paymentMethod': 'PayPal', 'isMultiVariationListing': 'false', 'condition': {'conditionId': '3000', 'conditionDisplayName': 'Pre-owned'}, 'listingInfo': {'listingType': 'FixedPrice', 'gift': 'false', 'bestOfferEnabled': 'true', 'watchCount': '1', 'startTime': '2017-12-19T20:12:01.000Z', 'buyItNowAvailable': 'false', 'endTime': '2018-01-18T20:12:01.000Z'}}]}}


  print "Total Pages: {0}".format(results['paginationOutput']['totalPages'])
  print "Ack: {0}".format(results['ack'])
  print "TimeStamp: {0}".format(results['timestamp'])
  print


  for item in results['searchResult']['item']:
    print 'ItemID: %s' % item['itemId']
    print 'Title: %s' % item['title']
    print 'CategoryID: %s' % item['primaryCategory']['categoryId']

  print

  '''
  for x in results['searchResult']:
    print "%s" % x
    
  print 50 * '-'

  for item in results['searchResult']['item']:
    # dict
    print "%s" % item
    print 50 * '-'
    for k in item.iteritems():
        print k

  '''

  pp = pprint.PrettyPrinter(indent=1)
  pp.pprint(results)



def main():
  snippet_test()



if __name__ == '__main__':
      main()
