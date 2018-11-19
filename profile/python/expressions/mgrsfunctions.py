# -*- coding: utf-8 -*-
"""
Functions for the Layout Loader plugin Military Templates
"""

from qgis.core import *
from qgis.gui import *

"""
Functions to be used with grid coordinates (mostly)
"""


@qgsfunction(args='auto', group='Military') 
def mgrs(easting, northing, epsg, feature, parent): 
	"""
	<i>Requires mgrspy from Boundless<br>
	pip install mgrspy</i><br><br>
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
