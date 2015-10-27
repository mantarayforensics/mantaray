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

import xml.dom.minidom
import zipfile
import codecs
import os

from simplekml.base import Kmlable, KmlElement
from simplekml.featgeom import Document
from simplekml.makeunicode import u


class Kml(object):
    """
    The main class that represents a KML file.

    This class represents a KML file, and the compilation of the KML file will
    be done through this class. The base feature is a document, all arguments
    passed to the class on creation are the same as that of a [Document]. To
    change any properties after creation you can do so through the `document`
    property (eg. `kml.document.name = "Test"`). For a description of what the
    arguments mean see the KML reference documentation published by Google:
    http://code.google.com/apis/kml/documentation/kmlreference.html

    Keyword Arguments:
    name (string)              -- name of placemark (default None)
    visibility (int)           -- whether the feature is shown (default 1)
    open (int)                 -- whether open or closed in Places (default 0)
    atomauthor (string)        -- author of the document (default None)
    atomlink (string)          -- URL containing this KML (default None)
    address (string)           -- standard address (default None)
    xaladdressdetails (string) -- address as xAL (default None)
    phonenumber (string)       -- phone number for Maps mobile (default None)
    snippet ([Snippet])        -- short description of feature (default None)
    description (string)       -- description shown in balloon (default None)
    camera ([Camera])          -- camera that views the scene (default None)
    lookat ([LookAt])          -- camera relative to feature (default None)
    timestamp ([TimeStamp])    -- single moment in time (default None)
    timespan ([TimeSpan])      -- period of time (default None)
    region ([Region])          -- bounding box of features (default None)

    Properties:
    document ([Document])      -- [Document] or [Folder] (default [Document])

    Public Methods:
    newpoint                   -- Creates a new [Point]
    newlinestring              -- Creates a new [LineString]
    newpolygon                 -- Creates a new [Polygon]
    newmultigeometry           -- Creates a new [MultiGeometry]
    newgroundoverlay           -- Creates a new [GroundOverlay]
    newscreenoverlay           -- Creates a new [ScreenOverlay]
    newphotooverlay            -- Creates a new [PhotoOverlay]
    newnetworklink             -- Creates a new [NetworkLink]
    newmodel                   -- Creates a new [Model]
    newschema                  -- Creates a new [Schema]
    newgxtrack                 -- Creates a new [GxTrack]
    newgxmultitrack            -- Creates a new [GxMultiTrack]
    kml                        -- Returns the generated kml as a string
    save                       -- Saves to a KML file
    savekmz                    -- Saves to a KMZ file

    """

    def __init__(self, **kwargs):
        """
        Creates the Kml document with a [Document] as the top level feature.

        Keyword Arguments:
        name (string)            -- name of placemark (default None)
        visibility (int)         -- whether the feature is shown (default 1)
        open (int)               -- whether open or closed in Places (default 0)
        atomauthor (string)      -- author of the document (default None)
        atomlink (string)        -- URL containing this KML (default None)
        address (string)         -- standard address (default None)
        xaladdressdetails(string)-- address as xAL (default None)
        phonenumber (string)     -- phone number for Maps mobile (default None)
        snippet ([Snippet])      -- short description of feature (default None)
        description (string)     -- description shown in balloon (default None)
        camera ([Camera])        -- camera that views the scene (default None)
        lookat ([LookAt])        -- camera relative to feature (default None)
        timestamp ([TimeStamp])  -- single moment in time (default None)
        timespan ([TimeSpan])    -- period of time (default None)
        region ([Region])        -- bounding box of features (default None)

        """
        self._feature = Document(**kwargs)

    @property
    def document(self):
        """
        The top level item in the kml document.

        A top level document is required for a kml document, the default is an
        instance of the [Document] class. This property can be set to an
        instance of a container class: [Document] or [Folder]
        """
        return self._feature

    @document.setter
    def document(self, doc):
        self._feature = doc

    def _genkml(self, format=True):
        """
        Returns the kml as a string or as a single line or formatted.

        Keyword arguments:
        format (bool) -- format the resulting kml "prettyprint" (default True)

        """
        kml_tag = 'xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:xal="urn:oasis:names:tc:ciq:xsdschema:xAL:2.0"'
        xmlstr = u("<kml {0}>{1}</kml>").format(kml_tag, self._feature.__str__())
        if format:
           KmlElement.patch()
           kmlstr = xml.dom.minidom.parseString(xmlstr.encode("utf-8"))
           KmlElement.unpatch()
           return kmlstr.toprettyxml(indent="    ", newl="\n", encoding="UTF-8").decode("utf-8")
        else:
            return xmlstr

    def parsetext(self, parse=True):
        """
        Sets the behavior of how text tags are parsed.

        If True the values of the text tags (<name>, <description> and <text>)
        are escaped, so that the values are rendered properly. If False, the
        values are left as is. If the CDATA element is being used to escape
        the text strings, them set this to False.

        Keyword arguments:
        parse (bool) -- whether to parse text values

        """
        Kmlable._parsetext(parse)

    def kml(self, format=True):
        """
        Returns a string containing the KML.

        Keyword arguments:
        format (bool) -- format the resulting kml "prettyprint" (default True)

        """
        Kmlable._setkmz(False)
        return self._genkml(format)

    def save(self, path, format=True):
        """
        Save the kml to the given file supplied by path.

        Keyword arguments:
        path (string) -- the path of the kml file to be saved
        format (bool) -- format the resulting kml "prettyprint" (default True)

        """
        Kmlable._setkmz(False)
        out = self._genkml(format)
        f = codecs.open(path, 'wb', 'utf-8')
        try:
            f.write(out)
        finally:
            f.close()

    def savekmz(self, path, format=True):
        """
        Save the kml as a kmz file to the given file supplied by `path`.

        Keyword arguments:
        path (string) -- the path of the kmz file to be saved
        format (bool) -- format the resulting kml "prettyprint" (default True)

        """
        Kmlable._setkmz()
        out = self._genkml(format).encode('utf-8')
        kmz = zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED)
        kmz.writestr("doc.kml", out)
        for image in Kmlable._getimages():
            kmz.write(image, os.path.join('files', os.path.split(image)[1]))
        kmz.close()
        Kmlable._clearimages()

    def newdocument(self, **kwargs):
        """
        Creates a new [Document] and attaches it to this KML document.

        Returns an instance of [Document] class.

        Keyword Arguments:
        Same as [Document].
        """
        return self.document.newdocument(**kwargs)

    def newfolder(self, **kwargs):
        """
        Creates a new [Folder] and attaches it to this KML document.

        Returns an instance of [Folder] class.

        Keyword Arguments:
        Same as [Folder].
        """
        return self.document.newfolder(**kwargs)

    def newpoint(self, **kwargs):
        """
        Creates a new [Point] and attaches it to this KML document.

        Returns an instance of [Point] class.

        Keyword Arguments:
        Same as [Point].
        """
        return self.document.newpoint(**kwargs)

    def newlinestring(self, **kwargs):
        """
        Creates a new [LineString] and attaches it to this KML document.

        Returns an instance of [LineString] class.

        Keyword Arguments:
        Same as [LineString].
        """
        return self.document.newlinestring(**kwargs)

    def newpolygon(self, **kwargs):
        """
        Creates a new [Polygon] and attaches it to this KML document.

        Returns an instance of [Polygon] class.

        Keyword Arguments:
        Same as [Polygon].
        """
        return self.document.newpolygon(**kwargs)

    def newmultigeometry(self, **kwargs):
        """
        Creates a new [MultiGeometry] and attaches it to this KML document.

        Returns an instance of [MultiGeometry] class.

        Keyword Arguments:
        Same as [MultiGeometry].
        """
        return self.document.newmultigeometry(**kwargs)

    def newgroundoverlay(self, **kwargs):
        """
        Creates a new [GroundOverlay] and attaches it to this KML document.

        Returns an instance of [GroundOverlay] class.

        Keyword Arguments:
        Same as [GroundOverlay].
        """
        return self.document.newgroundoverlay(**kwargs)

    def newscreenoverlay(self, **kwargs):
        """
        Creates a new [ScreenOverlay] and attaches it to this KML document.

        Returns an instance of [ScreenOverlay] class.

        Keyword Arguments:
        Same as [ScreenOverlay].
        """
        return self.document.newscreenoverlay(**kwargs)

    def newphotooverlay(self, **kwargs):
        """
        Creates a new [PhotoOverlay] and attaches it to this KML document.

        Returns an instance of [PhotoOverlay] class.

        Keyword Arguments:
        Same as [PhotoOverlay].
        """
        return self.document.newphotooverlay(**kwargs)

    def newnetworklink(self, **kwargs):
        """
        Creates a new [NetworkLink] and attaches it to the this KML document.

        Returns an instance of [NetworkLink] class.

        Keyword Arguments:
        Same as [NetworkLink].
        """
        return self.document.newnetworklink(**kwargs)

    def newmodel(self, **kwargs):
        """
        Creates a new [Model] and attaches it to this KML document.

        Returns an instance of [Model] class.

        Keyword Arguments:
        Same as [Model].
        """
        return self.document.newmodel(**kwargs)

    def newschema(self, **kwargs):
        """
        Creates a new [Schema] and attaches it to this KML document.

        Returns an instance of [Schema] class.

        Keyword Arguments:
        Same as [Schema].
        """
        return self.document.newschema(**kwargs)

    def newgxtrack(self, **kwargs):
        """
        Creates a new [GxTrack] and attaches it to this KML document.

        Returns an instance of [GxTrack] class.

        Keyword Arguments:
        Same as [GxTrack].
        """
        return self.document.newgxtrack(**kwargs)

    def newgxmultitrack(self, **kwargs):
        """
        Creates a new [GxMultiTrack] and attaches it to this KML document.

        Returns an instance of [GxMultiTrack] class.

        Keyword Arguments:
        Same as [GxMultiTrack].
        """
        return self.document.newgxmultitrack(**kwargs)


if __name__ == "__main__":
    pass