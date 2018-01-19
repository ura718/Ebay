#!/usr/bin/python
# -*- coding: utf-8 -*-

import ast




############################################
#
# Get results from file that contains findings output
# in dictionary format. That is why we are using ast 
# otherwise format will be as string when reading out of file.
# 
def GetResults():

  """ read findings file output and process its elements """

  file='search.out'
  with open(file, 'rb') as f1:
    results = f1.read()


  # convert results output from str to dict
  results = ast.literal_eval(results)

  return results





def main():

  results = GetResults()

  
  # Display total pages, entries, number of pages and entries per page
  try:
    print "ACK: %s " % results['ack']
  except KeyError, e:
    print "[-] %s" % e

  try:
    print "Item Search URL: %s " % results['itemSearchURL']
  except KeyError, e:
    print "[-] %s" % e
  
  try:
    print "Total Pages: %s   " % results['paginationOutput']['totalPages']
  except KeyError, e:
    print "[-] %s" % e


  try:
    print "Total Entries: %s " % results['paginationOutput']['totalEntries']
  except KeyError, e:
    print "[-] %s" % e


  try:
    print "Page Number: %s   " % results['paginationOutput']['pageNumber']
  except KeyError, e:
    print "[-] %s" % e

  try:
    print "Entries Per Page: %s " % results['paginationOutput']['entriesPerPage']
  except KeyError, e:
    print "[-] %s" % e


  print 50*'-'


  # Deeply Nested Dictionary
  try:
    print "AutoPay: %s " % results['searchResult']['item'][0]['autoPay']
  except KeyError, e:
    print "[-] %s" % e

  try:
    print "Condition: %s " % results['searchResult']['item'][0]['condition']['conditionDisplayName']
  except KeyError, e:
    print "[-] %s" % e

  try:
    print "ConditionId: %s " % results['searchResult']['item'][0]['condition']['conditionId']
  except KeyError, e:
    print "[-] %s" % e

  try:
    print "Country: %s " % results['searchResult']['item'][0]['country']
  except KeyError, e:
    print "[-] %s" % e

  try:
    print "Gallery URL: %s " % results['searchResult']['item'][0]['galleryURL']
  except KeyError, e:
    print "[-] %s" % e

  try:
    print "GlobalId: %s " % results['searchResult']['item'][0]['globalId']
  except KeyError, e:
    print "[-] %s" % e

  try:
    print "isMultiVariationListing: %s " % results['searchResult']['item'][0]['isMultiVariationListing']
  except KeyError, e:
    print "[-] %s" % e

  try:
    print "itemId: %s " % results['searchResult']['item'][0]['itemId']
  except KeyError, e:
    print "[-] %s" % e

  try:
    print "listingInfo: %s " % results['searchResult']['item'][0]['listingInfo']['bestOfferEnabled']
  except KeyError, e:
    print "[-] %s" % e

  try:
    print "buyItNowAvailable: %s " % results['searchResult']['item'][0]['listingInfo']['buyItNowAvailable']
  except KeyError, e:
    print "[-] %s" % e

  try:
    print "endTime: %s " % results['searchResult']['item'][0]['listingInfo']['endTime']
  except KeyError, e:
    print "[-] %s" % e

  try:
    print "gift: %s " % results['searchResult']['item'][0]['listingInfo']['gift']
  except KeyError, e:
    print "[-] %s" % e

  try:
    print "listingType: %s " % results['searchResult']['item'][0]['listingInfo']['listingType']
  except KeyError, e:
    print "[-] %s" % e

  try:
    print "startTime: %s "  % results['searchResult']['item'][0]['listingInfo']['startTime']
  except KeyError, e:
    print "[-] %s" % e

  try:
    print "watchCount: %s " % results['searchResult']['item'][0]['listingInfo']['watchCount']
  except KeyError, e:
    print "[-] %s" % e

  try:
    print "location: %s " % results['searchResult']['item'][0]['location']
  except KeyError, e:
    print "[-] %s" % e

  try:
    print "paymentMethod: %s " % results['searchResult']['item'][0]['paymentMethod']
  except KeyError, e:
    print "[-] %s" % e

  try:
    print "postalCode: %s " % results['searchResult']['item'][0]['postalCode']
  except KeyError, e:
    print "[-] %s" % e

  try:
    print "categoryId: %s " % results['searchResult']['item'][0]['primaryCategory']['categoryId']
  except KeyError, e:
    print "[-] %s" % e

  try:
    print "categoryName: %s " % results['searchResult']['item'][0]['primaryCategory']['categoryName']
  except KeyError, e:
    print "[-] %s" % e

  try:
    print "returnsAccepted: %s " % results['searchResult']['item'][0]['returnsAccepted']
  except KeyError, e:
    print "[-] %s" % e

  try:
    print "Converted currencyId: %s " % results['searchResult']['item'][0]['sellingStatus']['convertedCurrentPrice']['_currencyId']
  except KeyError, e:
    print "[-] %s" % e

  try:
    print "value: %s " % results['searchResult']['item'][0]['sellingStatus']['convertedCurrentPrice']['value']
  except KeyError, e:
    print "[-] %s" % e

  try:
    print "currentPrice CurrencyId: %s " % results['searchResult']['item'][0]['sellingStatus']['currentPrice']['_currencyId']
  except KeyError, e:
    print "[-] %s" % e

  try:
    print "currentPrice value: %s " % results['searchResult']['item'][0]['sellingStatus']['currentPrice']['value']
  except KeyError, e:
    print "[-] %s" % e

  try:
    print "sellingState: %s " % results['searchResult']['item'][0]['sellingStatus']['sellingState']
  except KeyError, e:
    print "[-] %s" % e

  try:
    print "timeLeft: %s " % results['searchResult']['item'][0]['sellingStatus']['timeLeft']
  except KeyError, e:
    print "[-] %s" % e

  try:
    print "expeditedShipping: %s " % results['searchResult']['item'][0]['shippingInfo']['expeditedShipping']
  except KeyError, e:
    print "[-] %s" % e

  try:
    print "handlingTime: %s " % results['searchResult']['item'][0]['shippingInfo']['handlingTime']
  except KeyError, e:
    print "[-] %s" % e

  try:
    print "oneDayShippingAvailable: %s " % results['searchResult']['item'][0]['shippingInfo']['oneDayShippingAvailable']
  except KeyError, e:
    print "[-] %s" % e
  
  try:
    print "shipToLocations: %s " % results['searchResult']['item'][0]['shippingInfo']['shipToLocations']
  except KeyError, e:
    print "[-] %s" % e

  try:
    print "shippingType: %s " % results['searchResult']['item'][0]['shippingInfo']['shippingType']
  except KeyError, e:
    print "[-] %s" % e

  try:
    print "title: %s " % results['searchResult']['item'][0]['title']
  except KeyError, e:
    print "[-] %s" % e

  try:
    print "topRatedListing: %s " % results['searchResult']['item'][0]['topRatedListing']
  except KeyError, e:
    print "[-] %s" % e

  try:
    print "Item URL: %s " % results['searchResult']['item'][0]['viewItemURL']
  except KeyError, e:
    print "[-] %s" % e

  try:
    print "timestamp: %s " % results['timestamp']
  except KeyError, e:
    print "[-] %s" % e


  ''' 
  for item in results['searchResult']['item']:
    if item['topRatedListing'] == 'true':
      #print 'top rated: %s ' % item['topRatedListing']
      #print 'ItemID: %s' % item['itemId']
      #print 'Title: %s' % item['title']
      #print 'CategoryID: %s' % item['primaryCategory']['categoryId']
  '''

if __name__ == '__main__':
  main()



