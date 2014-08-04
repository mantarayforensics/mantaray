"""
simplekml
Copyright 2011 Kyle Lancaster

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

Contact me at kyle.lan@gmail.com
"""

from simplekml.styleselector import *
from simplekml.coordinates import *


class Box(Kmlable):
    """_Base class for box elements."""

    def __init__(self,
                 north=None,
                 south=None,
                 east=None,
                 west=None):
        super(Box, self).__init__()
        self._kml["north"] = north
        self._kml["south"] = south
        self._kml["east"] = east
        self._kml["west"] = west
        
    @property
    def north(self):
        """
        Latitude of the north edge of the bounding box, in decimal degrees
        from 0 to 90, accepts float.

        """
        return self._kml['north']
    
    @north.setter
    def north(self, north):
        self._kml['north'] = north
        
    @property
    def south(self):
        """
        Latitude of the south edge of the bounding box, in decimal degrees
        from 0 to 90, accepts float.

        """
        return self._kml['south']
    
    @south.setter
    def south(self, south):
        self._kml['south'] = south
        
    @property
    def east(self):
        """
        Longitude of the east edge of the bounding box, in decimal degrees
        from 0 to 90, accepts float.

        """
        return self._kml['east']
    
    @east.setter
    def east(self, east):
        self._kml['east'] = east
        
    @property
    def west(self):
        """
        Longitude of the west edge of the bounding box, in decimal degrees
        from 0 to 90, accepts float.

        """
        return self._kml['west']
    
    @west.setter
    def west(self, west):
        self._kml['west'] = west


class LatLonBox(Box):
    """
    Specifies where the top, bottom, right, and left sides of a bounding box
    for the ground overlay are aligned.

    Keyword Arguments:
    north (float)    -- north edge latitude (default None)
    south (float)    -- south edge latitude (default None)
    east (float)     -- east edge longitude (default None)
    west (float)     -- west edge longitude (default None)
    rotation (float) -- rotation about center (default None)

    Properties:
    Same as arguments.

    """
    def __init__(self, rotation=None, **kwargs):
        """
        Creates latlonbox element.

        Keyword Arguments:
        north (float)    -- north edge latitude (default None)
        south (float)    -- south edge latitude (default None)
        east (float)     -- east edge longitude (default None)
        west (float)     -- west edge longitude (default None)
        rotation (float) -- rotation about center (default None)

        """
        super(LatLonBox, self).__init__(**kwargs)
        self._kml['rotation'] = rotation
        
    @property
    def rotation(self):
        """
        Rotation of the overlay about its center, in degrees.
        Values can be 180, accepts float.

        """
        return self._kml['rotation']
    
    @rotation.setter
    def rotation(self, rotation):
        self._kml['rotation'] = rotation


class LatLonAltBox(Box):
    """
    A bounding box that describes an area of interest defined by geographic coordinates and altitudes.

    Keyword Arguments:
    north (float)          -- north edge latitude (default None)
    south (float)          -- south edge latitude (default None)
    east (float)           -- east edge longitude (default None)
    west (float)           -- west edge longitude (default None)
    minaltitude (float)    -- min altitude in meters (default None)
    maxaltitude (float)    -- max altitude in meters (default None)
    altitudemode (string)  -- alt use See [AltitudeMode] (default None)

    Properties:
    Same as arguments.

    """
    def __init__(self,
                 minaltitude=0,
                 maxaltitude=0,
                 altitudemode=AltitudeMode.clamptoground,
                 **kwargs):
        """
        Creates a latlonaltbox element.

        Keyword Arguments:
        north (float)          -- north edge latitude (default None)
        south (float)          -- south edge latitude (default None)
        east (float)           -- east edge longitude (default None)
        west (float)           -- west edge longitude (default None)
        minaltitude (float)    -- min altitude in meters (default None)
        maxaltitude (float)    -- max altitude in meters (default None)
        altitudemode (string)  -- alt use See [AltitudeMode] (default None)

        """
        super(LatLonAltBox, self).__init__(**kwargs)
        self._kml["minAltitude"] = minaltitude
        self._kml["maxAltitude"] = maxaltitude
        self._kml["altitudeMode"] = altitudemode

    @property
    def minaltitude(self):
        """Minimum altitude in meters, accepts float."""
        return self._kml["minAltitude"]

    @minaltitude.setter
    def minaltitude(self, minAltitude):
        self._kml["minAltitude"] = minAltitude

    @property
    def maxaltitude(self):
        """Maximum altitude in meters, accepts float."""
        return self._kml["maxAltitude"]

    @maxaltitude.setter
    def maxaltitude(self, maxaltitude):
        self._kml["maxAltitude"] = maxaltitude

    @property
    def altitudemode(self):
        """
        Specifies how the altitude for the Camera is interpreted.
        Accepts [AltitudeMode] constants.

        """
        return self._kml["altitudeMode"]

    @altitudemode.setter
    def altitudemode(self, altitudemode):
        self._kml["altitudeMode"] = altitudemode


class Lod(Kmlable):
    """
    Level of Detail describes the size of the projected region..

    Keyword Arguments:
    minlodpixels (int)   -- minimum limit of the visibility range (default 0)
    maxlodpixels (int)   -- maximum limit of the visibility range (default -1)
    minfadeextent (int)  -- min distance which the geometry fades (default 0)
    maxfadeextent (int)  -- max distance which the geometry fades (default 0)

    Properties:
    Same as arguments.

    """
    def __init__(self,
                 minlodpixels=0,
                 maxlodpixels=-1,
                 minfadeextent=0,
                 maxfadeextent=0):
        """
        Creates a Lod element.

        Keyword Arguments:
        minlodpixels (int) -- minimum limit of the visibility range (default 0)
        maxlodpixels (int) -- maximum limit of the visibility range (default -1)
        minfadeextent (int)-- min distance which the geometry fades (default 0)
        maxfadeextent (int) -- max distance which the geometry fades (default 0)

        """
        super(Lod, self).__init__()
        self._kml["minLodPixels"] = minlodpixels
        self._kml["maxLodPixels"] = maxlodpixels
        self._kml["minFadeExtent"] = minfadeextent
        self._kml["maxFadeExtent"] = maxfadeextent

    @property
    def minlodpixels(self):
        """Minimum limit of the visibility range, accepts int."""
        return self._kml["minLodPixels"]

    @minlodpixels.setter
    def minlodpixels(self, minlodpixels):
        self._kml["minLodPixels"] = minlodpixels

    @property
    def maxlodpixels(self):
        """Maximum limit of the visibility range, accepts int."""
        return self._kml["maxLodPixels"]

    @maxlodpixels.setter
    def maxlodpixels(self, maxlodpixels):
        self._kml["maxLodPixels"] = maxlodpixels

    @property
    def minfadeextent(self):
        """Minumum distance over which the geometry fades, accepts int."""
        return self._kml["minFadeExtent"]

    @minfadeextent.setter
    def minfadeextent(self, minfadeextent):
        self._kml["minFadeExtent"] = minfadeextent

    @property
    def maxfadeextent(self):
        """Maximum distance over which the geometry fades, accepts int."""
        return self._kml["maxFadeExtent"]

    @maxfadeextent.setter
    def maxfadeextent(self, maxfadeextent):
        self._kml["maxFadeExtent"] = maxfadeextent


class GxLatLonQuad(Kmlable):
    """
    Used for nonrectangular quadrilateral ground overlays.

    Keyword Arguments:
    coords (list of 4 tuples) -- four corners of quad (default None)

    Properties:
    Same as arguments.

    """
    def __init__(self, coords=None):
        """
        Creates a gxlatlonquad element.

        Keyword Arguments:
        coords (list of 4 tuples) -- four corners of quad (default None)

        """
        super(GxLatLonQuad, self).__init__()
        self._coords = None
        self._kml["coordinates"] = coords

    @property
    def coords(self):
        """
        Four corners of quad coordinates, accepts list of four tuples.

        eg. [(0, 1), (1,1), (1,0), (0,0)]
        """
        return self._coords

    @coords.setter
    def coords(self, coords):
        self._kml["coordinates"] = ''
        self._coords = coords
        for coord in coords:
            self._kml["coordinates"] += "{0},{1} ".format(coord[0], coord[1])
        self._kml["coordinates"] = self._kml["coordinates"][:-1]


class Region(Kmlable):
    """
    Used for nonrectangular quadrilateral ground overlays.

    Keyword Arguments:
    latlonaltbox ([LatLonAltBox]) --  bounding box (default None)
    lod ([Lod])                   --  level of detail (default None)

    Properties:
    Same as arguments.

    """
    def __init__(self, latlonaltbox=LatLonAltBox(), lod=Lod()):
        """
        Creates a region element.

        Keyword Arguments:
        latlonaltbox ([LatLonAltBox]) --  bounding box (default None)
        lod ([Lod])                   --  level of detail (default None)

        """
        super(Region, self).__init__()
        self._kml["LatLonAltBox"] = latlonaltbox
        self._kml["Lod"] = lod

    @property
    def latlonaltbox(self):
        """Bounding box that describes an area, accepts [LatLonAltBox]."""
        return self._kml["LatLonAltBox"]

    @latlonaltbox.setter
    def latlonaltbox(self, latlonaltbox):
        self._kml["LatLonAltBox"] = latlonaltbox

    @property
    def lod(self):
        """Level of Detail, accepts [Lod]"""
        return self._kml["Lod"]

    @lod.setter
    def lod(self, lod):
        self._kml["Lod"] = lod