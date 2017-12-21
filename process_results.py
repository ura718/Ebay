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

  #print type(results)

  # Display total pages, entries, number of pages and entries per page
  print "Total Pages: %s   " % results['paginationOutput']['totalPages']
  print "Total Entries: %s " % results['paginationOutput']['totalEntries']
  print "Page Number: %s   " % results['paginationOutput']['pageNumber']
  print "Entries Per Page: %s " % results['paginationOutput']['entriesPerPage']

  
  for item in results['searchResult']['item']:
    if item['topRatedListing'] == 'true':
      #print 'top rated: %s ' % item['topRatedListing']
      #print 'ItemID: %s' % item['itemId']
      print 'Title: %s' % item['title']
      #print 'CategoryID: %s' % item['primaryCategory']['categoryId']


if __name__ == '__main__':
  main()



