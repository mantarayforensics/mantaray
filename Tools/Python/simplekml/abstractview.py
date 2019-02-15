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

from simplekml.base import Kmlable
from simplekml.constants import *
from simplekml.timeprimitive import *
from simplekml.makeunicode import u

class AbstractView(Kmlable): #TODO: gxViewerOptions
    """_Base class, extended by Camera and LookAt."""
    def __init__(self,
                 longitude=None,
                 latitude=None,
                 altitude=None,
                 heading=None,
                 tilt=None,
                 altitudemode=None,
                 gxaltitudemode=None,
                 gxtimespan=None,
                 gxtimestamp=None):
        super(AbstractView, self).__init__()
        self._kml["longitude"] = longitude
        self._kml["latitude"] = latitude
        self._kml["altitude"] = altitude
        self._kml["heading"] = heading
        self._kml["tilt"] = tilt
        self._kml["altitudeMode"] = altitudemode
        self._kml["gx:AltitudeMode"] = gxaltitudemode
        self._kml["gx:TimeSpan"] = gxtimespan
        self._kml["gx:TimeStamp"] = gxtimestamp

    @property
    def longitude(self):
        """Decimal degree value in WGS84 datum, accepts float."""
        return self._kml['longitude']

    @longitude.setter
    def longitude(self, longitude):
        self._kml['longitude'] = longitude

    @property
    def latitude(self):
        """Decimal degree value in WGS84 datum, accepts float."""
        return self._kml['latitude']

    @latitude.setter
    def latitude(self, latitude):
        self._kml['latitude'] = latitude

    @property
    def altitude(self):
        """Height above the earth in meters (m), accepts int."""
        return self._kml['altitude']

    @altitude.setter
    def altitude(self, altitude):
        self._kml['altitude'] = altitude

    @property
    def heading(self):
        """Rotation about the z axis, accepts float."""
        return self._kml['heading']

    @heading.setter
    def heading(self, heading):
        self._kml['heading'] = heading

    @property
    def tilt(self):
        """Rotation about the x axis, accepts float."""
        return self._kml['tilt']

    @tilt.setter
    def tilt(self, tilt):
        self._kml['tilt'] = tilt

    @property
    def altitudemode(self):
        """
        Specifies how the altitude for the Camera is interpreted.

        Accepts [AltitudeMode] constants.

        """
        return self._kml['altitudeMode']

    @altitudemode.setter
    def altitudemode(self, altitudemode):
        self._kml['altitudeMode'] = altitudemode

    @property
    def gxaltitudemode(self):
        """
        Specifies how the altitude for the Camera is interpreted.

        With the addition of being relative to the sea floor.
        Accepts [GxAltitudeMode] constants.

        """
        return self._kml['gx:altitudeMode']

    @gxaltitudemode.setter
    def gxaltitudemode(self, gxaltmode):
        self._kml['gx:altitudeMode'] = gxaltmode

    @property
    def gxtimestamp(self):
        """Represents a single moment in time, accepts [GxTimeStamp]."""
        if self._kml['gx:TimeStamp'] is None:
            self._kml['gx:TimeStamp'] = GxTimeStamp()
        return self._kml['gx:TimeStamp']

    @gxtimestamp.setter
    def gxtimestamp(self, gxtimestamp):
        self._kml['gx:TimeStamp'] = gxtimestamp

    @property
    def gxtimespan(self):
        """Period of time, accepts [GxTimeSpan]."""
        if self._kml['gx:TimeSpan'] is None:
            self._kml['gx:TimeSpan'] = GxTimeSpan()
        return self._kml['gx:TimeSpan']

    @gxtimespan.setter
    def gxtimespan(self, gxtimespan):
        self._kml['gx:TimeSpan'] = gxtimespan


class Camera(AbstractView): # --Document--
    """A virtual camera that views the scene.

    Keyword Arguments:
    longitude (float)           -- decimal degree (default None)
    latitude (float)            -- decimal degree  (default None)
    altitude (float)            -- height from earth (m) (default None)
    heading (float)             -- rotation about the z axis (default None)
    tilt (float)                -- rotation about the x axis (default None)
    altitudemode (string)       -- alt use See [AltitudeMode] (default None)
    gxaltitudemode (string)     -- alt use. See [GxAltitudeMode] (default None)
    gxtimespan ([GxTimeSpan])   -- a single moment in time (default None)
    gxtimestamp ([GxTimeStamp]) -- a period of time (default None)
    roll (float)                -- rotation about the y axis (default None)

    Properties:
    Same as arguments.

    """

    def __init__(self, roll=None, **kwargs):
        """
        Creates a camera that views the scene.

        Keyword Arguments:
        longitude (float)          -- decimal degree (default None)
        latitude (float)           -- decimal degree  (default None)
        altitude (float)           -- height from earth (m) (default None)
        heading (float)            -- rotation about the z axis (default None)
        tilt (float)               -- rotation about the x axis (default None)
        altitudemode (string)      -- alt use See [AltitudeMode] (default None)
        gxaltitudemode (string)    -- alt use.See [GxAltitudeMode](default None)
        gxtimespan ([GxTimeSpan])  -- a single moment in time (default None)
        gxtimestamp ([GxTimeStamp])-- a period of time (default None)
        roll (float)               -- rotation about the y axis (default None)

        """
        super(Camera, self).__init__(**kwargs)
        self._kml['roll'] = roll

    @property
    def roll(self):
        """Rotation about the y axis, accepts float."""
        return self._kml['roll']

    @roll.setter
    def roll(self, roll):
        self._kml['roll'] = roll


class LookAt(AbstractView): # --Document--
    """Positions the camera in relation to the object that is being viewed.

    Keyword Arguments:
    longitude (float)           -- decimal degree (default None)
    latitude (float)            -- decimal degree  (default None)
    altitude (float)            -- height from earth (m) (default None)
    heading (float)             -- rotation about the z axis (default None)
    tilt (float)                -- rotation about the x axis (default None)
    altitudemode (string)       -- alt use See [AltitudeMode] (default None)
    gxaltitudemode (string)     -- alt use. See [GxAltitudeMode] (default None)
    gxtimespan ([GxTimeSpan])   -- a single moment in time (default None)
    gxtimestamp ([GxTimeStamp]) -- a period of time (default None)
    range                       -- distance from point (default None)

    Properties:
    Same as arguments.

    """

    def __init__(self, range=None, **kwargs):
        """
        Creates a LookAt element that positions the camera.

        Keyword Arguments:
        longitude (float)          -- decimal degree (default None)
        latitude (float)           -- decimal degree  (default None)
        altitude (float)           -- height from earth (m) (default None)
        heading (float)            -- rotation about the z axis (default None)
        tilt (float)               -- rotation about the x axis (default None)
        altitudemode (string)      -- alt use See [AltitudeMode] (default None)
        gxaltitudemode (string)    -- alt use.See [GxAltitudeMode](default None)
        gxtimespan ([GxTimeSpan])   -- a single moment in time (default None)
        gxtimestamp ([GxTimeStamp])-- a period of time (default None)
        range                      -- distance from point (default None)

        """
        super(LookAt, self).__init__(**kwargs)
        self._kml['range'] = range

    @property
    def range(self):
        """Distance in meters from the point, accepts int."""
        return self._kml['range']

    @range.setter
    def range(self, range):
        self._kml['range'] = range


