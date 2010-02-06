#!/usr/bin/env python
# coding=utf8

import urllib2
from urllib import quote
from BeautifulSoup import BeautifulStoneSoup

class Forecast():
   def __init__(self, location):
      self.location = quote(location)
      return

   def GetXMLForecast(self):
      """ Retrieve (and return) the urlopen() object with the XML for a given location """
      xmlforecast = urllib2.urlopen("http://api.wunderground.com/auto/wui/geo/ForecastXML/index.xml?query=%s" % self.location)
      return xmlforecast

   def RetrieveForecast(self, days=1, unicode=True, low=True, high=True, conditions=True,
         sunrise=False, sunset=False, moon_percent=False, moon_age=False):
      """ Parse out the forecast from the information obtained by
          GetXMLForecast(). Return a dictionary like the following:
          {
            1: {
               "high": {
                  "fahrenheit": 27,
                  "celsius": -3
               },
               
               "low": {
                  "fahrenheit": 16,
                  "celsius": -9
               },

               "conditions": "Mostly Cloudy",
            }
          }

          If unicode is True, display °'s with temperatures, but
          temperature is *always* returned as a string.
      """
      urlobject = self.GetXMLForecast()
      soup = BeautifulStoneSoup(urlobject)
      if days > 6:
         raise "You've requested too many days. Days must be <= 6."
      key = days + 2
      output_dict = {}
      for day in range(2, key):
         print day
         loopday = soup.findChildren("forecastday")[day]

         # Initialize the dictionary.
         day_dict = output_dict[int(loopday.period.string)] = {}
         if low == True:
            lowf = int(loopday.low.fahrenheit.string)
            lowc = int(loopday.low.celsius.string)

            day_dict["low"] = {
                  "fahrenheit": str(lowf),
                  "celsius": str(lowc)
            }

            if unicode == True:
               day_dict["low"]["fahrenheit"] += "°"
               day_dict["low"]["celsius"] += "°"
      return output_dict


a = Forecast("New York, NY")
print a.RetrieveForecast(unicode=False, days=3)
