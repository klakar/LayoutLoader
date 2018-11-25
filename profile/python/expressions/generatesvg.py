from qgis.core import *
from qgis.gui import *

'''
Written by @klaskarlsson
Licence LGPL

Optional parameters:
-g <deg> : Grid North Reference, default 0
-m <deg> : Magnetic Declination relative True North, default 0
-t <deg> : True North Reference relative Grid North, default 0

'''
import math

def generatesvg(g, m, t):

   svg1="<?xml version=\"1.0\" standalone=\"no\"?>\n"
   svg1+="<!DOCTYPE svg PUBLIC \"-//W3C//DTD SVG 1.2//EN\" \n"
   svg1+="  \"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd\">\n"
   svg1+="<svg width=\"2.5cm\" height=\"2.5cm\" viewBox=\"0 0 400 400\"\n"
   svg1+="     xmlns=\"http://www.w3.org/2000/svg\" version=\"1.1\">\n"

   svgm="  <path d=\"M 200 380 L %s %s\"\n"
   svgm+="        stroke=\"#000\" stroke-width=\"1\" />\n"
   svgm+="  <path d=\"M %s %s L %s %s %s %s z\"\n"
   svgm+="        stroke=\"#000\" stroke-width=\"1\" />\n"
   svgm+="  <text x=\"220\" y=\"365\"\n"
   svgm+="        font-size=\"15px\"\n"
   svgm+="        font-family=\"sans-serif\" >Mag Decl. = %s°\n"
   svgm+="  </text>\n"
   
   svgt="  <path d=\"M 200 380 L %s %s\"\n"
   svgt+="        stroke=\"#000\" stroke-width=\"1\" />\n"
   svgt+="  <path d=\"M %s %s L %s %s %s %s %s %s %s %s z\"\n"
   svgt+="        stroke=\"#000\" stroke-width=\"1\" />\n"
   svgt+="  <text x=\"220\" y=\"350\"\n"
   svgt+="        font-size=\"15px\"\n"
   svgt+="        font-family=\"sans-serif\" >True North = %s°\n"
   svgt+="  </text>\n"

   svgg="  <path d=\"M 200 380 L %s %s\"\n"
   svgg+="        stroke=\"#000\" stroke-width=\"1\" />\n"
   svgg+="  <text transform=\"translate(%s,%s)rotate(%s)\"\n"
   svgg+="        font-size=\"15px\"\n"
   svgg+="        font-family=\"sans-serif\"\n"
   svgg+="        text-anchor=\"middle\" >GN\n"
   svgg+="  </text>\n"
   svgg+="  <text x=\"220\" y=\"380\"\n"
   svgg+="        font-size=\"15px\"\n"
   svgg+="        font-family=\"sans-serif\" >Grid North = %s°\n"
   svgg+="  </text>\n"

   svgr="  <path d=\"M %s %s A 200 380 0 0 %s %s %s\"\n"
   svgr+="        stroke=\"#777\" fill=\"none\" stroke-width=\"0.5\" />\n"
   svgr+="  <path d=\"M %s %s A 200 380 0 0 %s %s %s\"\n"
   svgr+="        stroke=\"#777\" fill=\"none\" stroke-width=\"0.5\" />\n"
   svgr+="</svg>\n"
   
   vg = math.radians(g)
   vt = math.radians(t)
   vm = math.radians(t+m)

   xm = 200 + 300 * math.sin(vm)
   ym = 380 - 300 * math.cos(vm)
   axm = 200 + 305 * math.sin(vm)
   aym = 380 - 305 * math.cos(vm)
   bxm = 200 + 335 * math.sin(vm)
   bym = 380 - 335 * math.cos(vm)
   cxm = 200 + 305 * math.sin(vm + math.radians(2))
   cym = 380 - 305 * math.cos(vm + math.radians(2))

   generera = svg1
   generera += svgm % ( xm, ym, axm, aym, bxm, bym, cxm, cym, m)

   xt = 200 + 330 * math.sin(vt)
   yt = 380 - 330 * math.cos(vt)
   axt = 200 + 330 * math.sin(vt - math.radians(1.8))
   ayt = 380 - 330 * math.cos(vt - math.radians(1.8))
   bxt = 200 + 360 * math.sin(vt)
   byt = 380 - 360 * math.cos(vt)
   cxt = 200 + 330 * math.sin(vt + math.radians(1.8))
   cyt = 380 - 330 * math.cos(vt + math.radians(1.8))
   dxt = 200 + 349 * math.sin(vt - math.radians(2.6))
   dyt = 380 - 349 * math.cos(vt - math.radians(2.6))
   ext = 200 + 349 * math.sin(vt + math.radians(2.6))
   eyt = 380 - 349 * math.cos(vt + math.radians(2.6))

   generera += svgt % ( xt, yt, axt, ayt, bxt, byt, cxt, cyt, dxt, dyt, ext, eyt, t)

   xg = 200 + 360 * math.sin(vg)
   yg = 380 - 360 * math.cos(vg)
   axg = 200 + 363 * math.sin(vg)
   ayg = 380 - 363 * math.cos(vg)

   generera += svgg % (xg, yg, axg, ayg, g, g)

   xrt1 = 200 + 300 * math.sin(vg)
   yrt1 = 380 - 300 * math.cos(vg)
   xrt2 = 200 + 300 * math.sin(vt)
   yrt2 = 380 - 300 * math.cos(vt)

   xrm1 = 200 + 280 * math.sin(vt)
   yrm1 = 380 - 280 * math.cos(vt)
   xrm2 = 200 + 280 * math.sin(vm)
   yrm2 = 380 - 280 * math.cos(vm)
   
   if (vm <= vt):
      mp = 0
   else:
      mp = 1
   if (vt <= vg):
      tp = 0
   else:
      tp = 1

   generera += svgr % (xrt1, yrt1, tp, xrt2, yrt2, xrm1, yrm1, mp, xrm2, yrm2)

   return generera

@qgsfunction(args='auto', group='Military')
def north_ref_svg(grid_north, true_north, magnetic_north, feature, parent):
    """
    <h1>Generate North Reference SVG.</h1>
    <p>Place inside HTML frame</p>
    <ul>
    <li>arg 1: Grid North (normally 0)</li>
    <li>arg 2: True North (calc)</li>
    <li>arg 3: Magnetic Declination (look up)</li>
    </ul>
    <h2>Example usage:</h2>
    <i>northref(0, 3.4, -7)</i>
    
    """
    return generatesvg(grid_north, magnetic_north, true_north)
