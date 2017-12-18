import requests
import sys

# by route substring, return the route id
getRoutes = '/Routes'
def getRoute(routeString):
  routes = getJson(getRoutes)
  route = search(routes, 'Description', routeString, 'Route')
  return route['Route']

# by route id and a direction substring, returns the direction id
getDirections = '/Directions/{ROUTE}'
def getDirection(routeId, directionString):
  getDirection = getDirections.format(ROUTE=routeId)
  directions = getJson(getDirection)
  direction = search(directions, 'Text', directionString, 'Direction')
  return direction['Value']

# by route id, direction id, and stop substring, return the stop id
getStops = '/Stops/{ROUTE}/{DIRECTION}'
def getStop(routeId, directionId, stopString):
  getStop = getStops.format(ROUTE=routeId, DIRECTION=directionId)
  stops = getJson(getStop)
  stop = search(stops, 'Text', stopString, 'Stop')
  return stop['Value']

# by route id, direction id, and stop id, return the next departure text
getTimepointDepartures = '/{ROUTE}/{DIRECTION}/{STOP}'
def getDepartureTime(routeId, directionId, stopId):
  getDeparture = getTimepointDepartures.format(ROUTE=routeId, DIRECTION=directionId, STOP=stopId)
  departures = getJson(getDeparture)
  if len(departures) == 0:
    sys.exit('No more buses departing today')
  else:
    return departures[0]['DepartureText']

# iterates through a list of dictionaries and matches a field based on a search parameter
noMatchError = '{MATCHNAME} param "{SEARCH}" matched no {MATCHNAME}'
manyMatchError = '{MATCHNAME} param "{SEARCH}" matched more than one {MATCHNAME}:\n{MANYMATCHES}'
def search(list, field, search, matchName):
  matches = []
  for item in list:
    if search.upper() in item[field].upper():
      matches.append(item)
  #some error handling if the entered text does not return a valid response
  if len(matches) == 0:
    sys.exit(noMatchError.format(MATCHNAME=matchName, SEARCH=search))
  elif len(matches) > 1:
    manyMatches = ''
    for match in matches:
      manyMatches += '  ' + match[field] + '\n'
    sys.exit(manyMatchError.format(MATCHNAME=matchName, SEARCH=search, MANYMATCHES=manyMatches))
  else:
    return matches[0]


nextripURL = 'http://svc.metrotransit.org/NexTrip'
def getJson(url):
  try:
    return requests.request('GET', nextripURL + url + '?format=json').json()
  except:
    sys.exit("Error reaching api")
#takes in parameters from terminal
if (len(sys.argv) == 4):
  routeSubstring = sys.argv[1]
  directionSubstring = sys.argv[3]
  stopSubstring = sys.argv[2]

  routeId = getRoute(routeSubstring)
  directionId = getDirection(routeId, directionSubstring)
  stopId = getStop(routeId, directionId, stopSubstring)

  print(getDepartureTime(routeId, directionId, stopId))
else:
  sys.exit('Invalid parameters: bus.py <route> <stop> <direction>')

