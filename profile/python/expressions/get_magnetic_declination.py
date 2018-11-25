from qgis.core import *
from qgis.gui import *

import urllib.request
import urllib.parse
import xml.dom.minidom
import re

def getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)


@qgsfunction(args='auto', group='Military')
def get_magnetic_declination(lat, long, feature, parent):
    """
    <h1>Get Magnecti Declination</h1>
    <p>This function requires Internet connection</p>
    The function takes two arguments:
    <ul>
    <li>Latitude (degrees)</li>
    <li>Longitude (degrees)</li>
    </ul>
    <h3>Example:</h3>
    <p>get_magnetic_declination(14.9353, 57.3994)</p><br><br>
    <i>Uses data from www.ngdc.noaa.gov and the code is based on a python function by Kevan Ahlquist</i>
    """
    
    #encode URL parameters
    params = urllib.parse.urlencode({'lat1': lat, 'lon1': long, 'resultFormat': 'xml'})
    #Load XML file
    f = urllib.request.urlopen("http://www.ngdc.noaa.gov/geomag-web/calculators/calculateDeclination?%s" % params)
    #Process XML file into object tree and get only declination info
    dom = xml.dom.minidom.parseString(f.read())
    myString = getText(dom.getElementsByTagName("declination")[0].childNodes)
    # At this point the string still contains some formatting, this removes it
    declination = round(float(re.findall(r"[-+]?\d*\.\d+|\d+", myString)[0]),1)
    
    return declination
