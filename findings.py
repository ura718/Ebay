#!/usr/bin/python

#
# test finding api and write output to file
#
#

import os
from ebaysdk.finding import Connection as Finding
from ebaysdk.exception import ConnectionError



try:
  
  api = Finding(config_file='ebay.yaml')

  api_dictionary = {
    'keywords': 'Python',
    'itemFilter' : [
      {'name': 'Condition', 'value': 'Used'},
      {'name': 'MinPrice', 'value': '200', 'paramName': 'Currency', 'paramValue': 'USD'},
      {'name': 'MaxPrice', 'value': '400', 'paramName': 'Currency', 'paramValue': 'USD'},
    ],
    'pageinationInput': {
      'entriesPerPage': '0..1',
      'pageNumber': '0..1'
    },
    'sortOrder': 'CurrentPriceHighest'

  }



  # Execute api HTTP request to ebay and provide dictionary parameters
  response = api.execute('findItemsAdvanced', api_dictionary)
 

 
  # Return diction of the HTTP response
  response = response.dict()

except ConnectionError as e:
  print e
  print e.response.dict()



# Get current running file without extention
file = os.path.splitext(__file__)[0]

# Write output from api to file
with open(file + '.out', 'w') as f1:
  f1.write('%s' % response)


'''
for item in response['searchResult']['item']:
  print "ItemID: %s" % item['itemId']
  #print "Title: %s" % item['title']
  #print "CategoryID: %s" % item['primaryCategory']['categoryId'].value

'''


