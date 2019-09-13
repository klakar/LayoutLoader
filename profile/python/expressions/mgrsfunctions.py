# -*- coding: utf-8 -*-
"""
Functions for the Layout Loader plugin Military Templates
"""

from qgis.core import *
from qgis.gui import *

"""
Functions to be used with grid coordinates (mostly)
"""

def index_number(number_string):
    """
    Function that converts all input numbers in string format to unicode superscript.
    """
    numbers = ["⁰", "¹", "²", "³", "⁴", "⁵", "⁶", "⁷", "⁸", "⁹"]
    try:
        return_string = ''
        for n in number_string:
            return_string += numbers[int(n)]
    except:
        return_string = 'error'
    return return_string

@qgsfunction(args='auto', group='Military')
def utm_grid(grid_number, feature, parent):
    """
    <h2>Example:</h2><br>
    Creates UTM kilometer numbers from grid number variables.<br>
    Even 10 km numbers will have 100 km index numbers.<br>
    (Requires font with unicode support)<br><br>
    <code>
    utm_grid(@grid_number) -> '46' alt '⁵40'<br>
    </code>
    """
    grid_string = str(int(grid_number))
    km_string = ''
    if grid_string[-4:-3] == '0':
        km_string = index_number(grid_string[:-5])
    km_string += grid_string[-5:-3]
    return km_string

@qgsfunction(args='auto', group='Military') 
def mgrs(easting, northing, epsg, feature, parent): 
	"""
	<i>Requires mgrspy from Boundless<br>
	included in Layout Loarder plugin</i><br><br>
	Find MGRS from X and Y coordinate in EPSG.<br>
	<br>
	<h2>Example:</h2><br>
	<code>
	mgrs( 495395, 6392411, 32633) -> '33VVD94574973545'<br><br>
	mgrs( 15.048564, 57.405484, 4326) -> '33VWD1453591543'<br><br>
	</code>
	"""
	crsSrc = QgsCoordinateReferenceSystem(epsg)
	crsDst = QgsCoordinateReferenceSystem(4326)
	xform = QgsCoordinateTransform(crsSrc, crsDst,QgsProject.instance())
	pt = xform.transform(easting,northing)
	from mgrspy import mgrs
	mgrs_out = mgrs.toMgrs(pt[1],pt[0],5) # Latitude first...
	return mgrs_out
