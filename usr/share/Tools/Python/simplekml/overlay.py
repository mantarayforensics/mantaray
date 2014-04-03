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

from simplekml.base import *
from simplekml.constants import *


class ViewVolume(Kmlable):
    """
    Defines how much of the current scene is visible.

    Keyword Arguments:
    leftfov (float)   -- left angle from camera (default None)
    rightfov (float)  -- right angle from camera (default None)
    bottomfov (float) -- bottom angle from camera (default None)
    topfov (float)    -- top angle from camera (default None)
    near (float)      -- distance to camera (default None)

    Properties:
    Same as arguments.

    """

    def __init__(self,
                 leftfov=0,
                 rightfov=0,
                 bottomfov=0,
                 topfov=0,
                 near=0):
        """
        Creates a viewvolume element.

        Keyword Arguments:
        leftfov (float)   -- left angle from camera (default None)
        rightfov (float)  -- right angle from camera (default None)
        bottomfov (float) -- bottom angle from camera (default None)
        topfov (float)    -- top angle from camera (default None)
        near (float)      -- distance to camera (default None)

        """
        super(ViewVolume, self).__init__()
        self._kml["leftFov"] = leftfov
        self._kml["rightFov"] = rightfov
        self._kml["bottomFov"] = bottomfov
        self._kml["topFov"] = topfov
        self._kml["near"] = near

    @property
    def leftfov(self):
        """
        Angle, in degrees, accepts float.

        """
        return self._kml['leftFov']
    
    @leftfov.setter
    def leftfov(self, leftfov):
        self._kml['leftFov'] = leftfov

    @property
    def rightfov(self):
        """
        Angle, in degrees, accepts float.

        """
        return self._kml['rightFov']
    
    @rightfov.setter
    def rightfov(self, rightfov):
        self._kml['rightFov'] = rightfov

    @property
    def topfov(self):
        """
        Angle, in degrees, accepts float.

        """
        return self._kml['topFov']
    
    @topfov.setter
    def topfov(self, topFov):
        self._kml['topFov'] = topFov

    @property
    def bottomfov(self):
        """
        Angle, in degrees, accepts float.

        """
        return self._kml['bottomFov']
    
    @bottomfov.setter
    def bottomfov(self, bottomFov):
        self._kml['bottomFov'] = bottomFov
        
    @property
    def near(self):
        """
        Measurement of viewing direction from the camera, accepts float."""
        return self._kml['near']
    
    @near.setter
    def near(self, near):
        self._kml['near'] = near


class ImagePyramid(Kmlable):
    """
    A hierarchical set of images.

    Keyword Arguments:
    titlesize (int)     -- size of the tiles, in pixels. (default 256)
    maxwidth (int)      -- width (pixels) of the original image (default None)
    maxheight (int)     -- height (pixels) of the original image (default None)
    gridorigin (string) -- string from [GridOrigin] constants(default lowerLeft)

    Properties:
    Same as arguments.

    """
    
    def __init__(self,
                 titlesize=256,
                 maxwidth=0,
                 maxheight=0,
                 gridorigin=GridOrigin.lowerleft):
        """
        Creates an imagepyramid element.

        Keyword Arguments:
        titlesize (int)     -- size of the tiles, in pixels. (default 256)
        maxwidth (int)      -- width of the original image (default None)
        maxheight (int)     -- height of the original image (default None)
        gridorigin (string) -- string [GridOrigin] constants(default lowerLeft)

        """
        super(ImagePyramid, self).__init__()
        self._kml["titleSize"] = titlesize
        self._kml["maxWidth"] = maxwidth
        self._kml["maxHeight"] = maxheight
        self._kml["gridOrigin"] = gridorigin

    @property
    def titlesize(self):
        """Size of the tiles, in pixels, accepts int."""
        return self._kml["titleSize"]

    @titlesize.setter
    def titlesize(self, titlesize):
        self._kml["titleSize"] = titlesize

    @property
    def maxwidth(self):
        """Width in pixels of the original image, accepts int."""
        return self._kml["maxWidth"]

    @maxwidth.setter
    def maxwidth(self, maxwidth):
        self._kml["maxWidth"] = maxwidth

    @property
    def maxheight(self):
        """Height in pixels of the original image, accepts int."""
        return self._kml["maxHeight"]

    @maxheight.setter
    def maxheight(self, maxheight):
        self._kml["maxHeight"] = maxheight

    @property
    def gridorigin(self):
        """
        Specifies where to begin numbering the tiles, accepts string."""
        return self._kml["gridOrigin"]

    @gridorigin.setter
    def gridorigin(self, gridorigin):
        self._kml["gridOrigin"] = gridorigin

