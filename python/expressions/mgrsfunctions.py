# -*- coding: utf-8 -*-
"""
Functions to help in creating MGRS notation on map layouts.
Adapted for QGIS 3 using 'mgrspy' from Boundless.

"""

from qgis.core import *
from qgis.gui import *

"""
Functions for MGRS lettering based on UTM easting/northing coordinates.
"""

from qgis.utils import iface 


@qgsfunction(args='auto', group='Advanced Layout') 
def mgrs(easting, northing, epsg, feature, parent): 
	"""
	<i>
	Create MGRS from X and Y coordinate in EPSG.<br>
	<br>
	<h2>Example:</h2><br>
	<code>
	mgrs( 495395, 6392411, 32633) -> '33VVD94574973545'<br><br>
	mgrs( 15.048564, 57.405484, 4326) -> '33VWD1453591543'<br><br>
	</code>
	"""
	crsSrc = QgsCoordinateReferenceSystem(epsg)
	crsDst = QgsCoordinateReferenceSystem(4326)
	xform = QgsCoordinateTransform(crsSrc, crsDst, QgsProject.instance())
	pt = xform.transform(easting,northing)
	from mgrspy import mgrs
	mgrs_out = mgrs.toMgrs(pt[1],pt[0],5) # Latitude first...
	return mgrs_out
