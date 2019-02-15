#!/usr/bin/python2.4
#
# Copyright 2008 Google Inc. All Rights Reserved.

"""Reads the EXIF headers from geo-tagged photos. and creates a KML file.

Reads the EXIF headers from geo-tagged photos and creates a KML file with
a PhotoOverlay element for each file. Requires the open source EXIF.py file
downloadable at:

http://sourceforge.net/projects/exif-py/
 
  GetFile(): Handles the opening of an individual file.
  GetHeaders(): Reads the headers from the file.
  DmsToDecimal(): Converts EXIF GPS headers data to a decimal degree.
  GetGps(): Parses out the the GPS headers from the headers data.
  CreateKmlDoc(): Creates an XML document object to represent the KML document.
  CreatePhotoOverlay: Creates an individual PhotoOverlay XML element object.
  CreateKmlFile(): Creates and writes out a KML document to file.
"""

__author__ = 'mmarks@google.com (Mano Marks)'


import sys
import xml.dom.minidom
import EXIF


def GetFile(file_name):
  """Handles opening the file.

  Args:
    file_name: the name of the file to get

  Returns:
    A file
  """

  the_file = None

  try:
    the_file = open(file_name, 'rb')
    
  except IOError:
    the_file = None
    
  return the_file


def GetHeaders(the_file):
  """Handles getting the EXIF headers and returns them as a dict.

  Args:
    the_file: A file object

  Returns:
    a dict mapping keys corresponding to the EXIF headers of a file.
  """

  data = EXIF.process_file(the_file, 'UNDEF', False, False, False)
  return data


def DmsToDecimal(degree_num, degree_den, minute_num, minute_den,
                 second_num, second_den):
  """Converts the Degree/Minute/Second formatted GPS data to decimal degrees.

  Args:
    degree_num: The numerator of the degree object.
    degree_den: The denominator of the degree object.
    minute_num: The numerator of the minute object.
    minute_den: The denominator of the minute object.
    second_num: The numerator of the second object.
    second_den: The denominator of the second object.

  Returns:
    A deciminal degree.
  """

  degree = float(degree_num)/float(degree_den)
  minute = float(minute_num)/float(minute_den)/60
  second = float(second_num)/float(second_den)/3600
  return degree + minute + second


def GetGps(data):
  """Parses out the GPS coordinates from the file.

  Args:
    data: A dict object representing the EXIF headers of the photo.

  Returns:
    A tuple representing the latitude, longitude, and altitude of the photo.
  """

  lat_dms = data['GPS GPSLatitude'].values
  long_dms = data['GPS GPSLongitude'].values
  latitude = DmsToDecimal(lat_dms[0].num, lat_dms[0].den,
           
  lat_dms[1].num, lat_dms[1].den,
  lat_dms[2].num, lat_dms[2].den)
  longitude = DmsToDecimal(long_dms[0].num, long_dms[0].den,
  long_dms[1].num, long_dms[1].den,
  long_dms[2].num, long_dms[2].den)
  if data['GPS GPSLatitudeRef'].printable == 'S': latitude *= -1
  if data['GPS GPSLongitudeRef'].printable == 'W': longitude *= -1
  altitude = None

  try:
    alt = data['GPS GPSAltitude'].values[0]
    altitude = alt.num/alt.den
    if data['GPS GPSAltitudeRef'] == 1: altitude *= -1

  except KeyError:
    altitude = 0
  
  return latitude, longitude, altitude


def CreateKmlDoc():
  """Creates a KML document."""

  kml_doc = xml.dom.minidom.Document()
  #kml_element = kml_doc.createElementNS('http://www.opengis.net/kml/2.2', 'kml')
 # kml_element.setAttribute('xmlns', 'http://www.opengis.net/kml/2.2')
  kml_element = kml_doc.appendChild(kml_element)
  document = kml_doc.createElement('Document')
  kml_element.appendChild(document)
  return kml_doc
  

def CreatePhotoOverlay(kml_doc, file_name, the_file, file_iterator):
  """Creates a PhotoOverlay element in the kml_doc element.

  Args:
    kml_doc: An XML document object.
    file_name: The name of the file.
    the_file: The file object.
    file_iterator: The file iterator, used to create the id.

  Returns:
    An XML element representing the PhotoOverlay.
  """

  photo_id = 'photo%s' % file_iterator
  data = GetHeaders(the_file)
  coords = GetGps(data)
  #po = kml_doc.createElement('PhotoOverlay')
  po = kml_doc.createElement('PlaceMark')
  #po.setAttribute('id', photo_id)
  name = kml_doc.createElement('name')
  name.appendChild(kml_doc.createTextNode(file_name))
  description = kml_doc.createElement('description')
  #description.appendChild(kml_doc.createCDATASection('<a href="#%s">'
  #                                                   'Click here to fly into '
    #                                                 'photo</a>' % photo_id))
  #po.appendChild(name)
  #po.appendChild(description)
  #icon = kml_doc.createElement('Icon')
  #href = kml_doc.createElement('href')
  #href.appendChild(kml_doc.createTextNode(file_name))
  #camera = kml_doc.createElement('Camera')
  #longitude = kml_doc.createElement('longitude')
  #latitude = kml_doc.createElement('latitude')
  #altitude = kml_doc.createElement('altitude')
 # tilt = kml_doc.createElement('tilt')
  
  # Determines the proportions of the image and uses them to set FOV.
 # width = float(data['EXIF ExifImageWidth'].printable)
  #length = float(data['EXIF ExifImageLength'].printable)
 # lf = str(width/length * -20.0)
 # rf = str(width/length * 20.0)
  
#  longitude.appendChild(kml_doc.createTextNode(str(coords[1])))
 # latitude.appendChild(kml_doc.createTextNode(str(coords[0])))
 # altitude.appendChild(kml_doc.createTextNode('10'))
 # tilt.appendChild(kml_doc.createTextNode('90'))
 # camera.appendChild(longitude)
 # camera.appendChild(latitude)
#  camera.appendChild(altitude)
 # camera.appendChild(tilt)
 # icon.appendChild(href)
 # viewvolume = kml_doc.createElement('ViewVolume')
 # leftfov = kml_doc.createElement('leftFov')
 # rightfov = kml_doc.createElement('rightFov')
 # bottomfov = kml_doc.createElement('bottomFov')
 # topfov = kml_doc.createElement('topFov')
 # near = kml_doc.createElement('near')
 # leftfov.appendChild(kml_doc.createTextNode(lf))
 # rightfov.appendChild(kml_doc.createTextNode(rf))
 # bottomfov.appendChild(kml_doc.createTextNode('-20'))
 # topfov.appendChild(kml_doc.createTextNode('20'))
 # near.appendChild(kml_doc.createTextNode('10'))
 # viewvolume.appendChild(leftfov)
 # viewvolume.appendChild(rightfov)
#  viewvolume.appendChild(bottomfov)
 # viewvolume.appendChild(topfov)
 # viewvolume.appendChild(near)
 # po.appendChild(camera)
 # po.appendChild(icon)
 # po.appendChild(viewvolume)
  point = kml_doc.createElement('point')
  coordinates = kml_doc.createElement('coordinates')
  coordinates.appendChild(kml_doc.createTextNode('%s,%s,%s' %(coords[1],
                                                              coords[0],
                                                              coords[2])))
  point.appendChild(coordinates)
  po.appendChild(point)
  document = kml_doc.getElementsByTagName('Document')[0]
  document.appendChild(po)


def CreateKmlFile(file_names, new_file_name
):
  """Creates the KML Document with the PhotoOverlays, and writes it to a file.

  Args:
    file_names: A list object of all the names of the files.
    new_file_name: A string of the name of the new file to be created.
  """
  

  files = {}
  
  for file_name in file_names:
    the_file = GetFile(file_name)
    if the_file is None:
      print "'%s' is unreadable\n" % file_name
      file_names.remove(file_name)
      continue
    else:
      files[file_name] = the_file

    
  kml_doc = CreateKmlDoc()
  file_iterator = 0
  for key in files.iterkeys():
    CreatePhotoOverlay(kml_doc, key, files[key], file_iterator)
    file_iterator += 1

  #kml_file = open(new_file_name, 'w')
  kml_file = open(new_file_name, 'at+')
  kml_file.write(kml_doc.toprettyxml('  ', newl='\n', encoding='utf-8'))
  kml_file.close()
  
  
def main():
# This function was taken from EXIF.py to directly handle 
# command line arguments.

  args = sys.argv[1:]
  #newfile = args[0] + ".kml"
  #print "newfile is: " + newfile
  if len(args) < 1:

    print 'Please try again with a file name'

  else:
    CreateKmlFile(args, 'GPS_EXIF_Data.kml')
     #CreateKmlFile(args, newfile)

   
if __name__ == '__main__':
  main()
