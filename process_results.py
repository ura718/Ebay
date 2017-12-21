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
  print "ACK: %s " % results['ack']
  print "Item Search URL: %s " % results['itemSearchURL']
  print "Total Pages: %s   " % results['paginationOutput']['totalPages']
  print "Total Entries: %s " % results['paginationOutput']['totalEntries']
  print "Page Number: %s   " % results['paginationOutput']['pageNumber']
  print "Entries Per Page: %s " % results['paginationOutput']['entriesPerPage']
  print

  # Deep Nested Dictionary
  print "AutoPay: %s " % results['searchResult']['item'][0]['autoPay']
  print "Condition: %s " % results['searchResult']['item'][0]['condition']['conditionDisplayName']
  print "ConditionId: %s " % results['searchResult']['item'][0]['condition']['conditionId']
  print "Country: %s " % results['searchResult']['item'][0]['country']
  print "Gallery URL: %s " % results['searchResult']['item'][0]['galleryURL']
  print "GlobalId: %s " % results['searchResult']['item'][0]['globalId']
  print "isMultiVariationListing: %s " % results['searchResult']['item'][0]['isMultiVariationListing']
  print "itemId: %s " % results['searchResult']['item'][0]['itemId']
  print "listingInfo: %s " % results['searchResult']['item'][0]['listingInfo']['bestOfferEnabled']
  print "buyItNowAvailable: %s " % results['searchResult']['item'][0]['listingInfo']['buyItNowAvailable']
  print "endTime: %s " % results['searchResult']['item'][0]['listingInfo']['endTime']
  print "listingType: %s " % results['searchResult']['item'][0]['listingInfo']['listingType']
  print "startTime: %s "  % results['searchResult']['item'][0]['listingInfo']['startTime']
  print "watchCount: %s " % results['searchResult']['item'][0]['listingInfo']['watchCount']



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



