#!/usr/bin/python


from ebaysdk.finding import Connection as Finding
from ebaysdk.exception import ConnectionError



try:
  
  api = Finding(config_file='ebay.yaml')


  # Execute the HTTP request
  response = api.execute('findItemsAdvanced', {
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

  })
  
  # Return diction of the HTTP response
  response = response.dict()

except ConnectionError as e:
  print e
  print e.response.dict()




with open('search.out', 'w') as f1:
  f1.write('%s' % response)


'''
for item in response['searchResult']['item']:
  print "ItemID: %s" % item['itemId']
  #print "Title: %s" % item['title']
  #print "CategoryID: %s" % item['primaryCategory']['categoryId'].value

'''





