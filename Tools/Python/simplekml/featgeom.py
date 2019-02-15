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

from simplekml.abstractview import *
from simplekml.region import *
from simplekml.overlay import *
from simplekml.timeprimitive import *
from simplekml.icon import *
from simplekml.model import *
from simplekml.schema import *



class Feature(Kmlable):

    """_Base class extended by all features."""

    _id = 0
    def __init__(self,
                 name=None,
                 visibility=None,
                 open=None,
                 atomauthor=None,
                 atomlink=None,
                 address=None,
                 xaladdressdetails=None,
                 phonenumber=None,
                 snippet=None,
                 description=None,
                 camera=None,
                 lookat=None,
                 timestamp=None,
                 timespan=None,
                 region=None,
                 extendeddata=None):
        Feature._id += 1
        super(Feature, self).__init__()
        self._kml['name'] = name
        self._kml['visibility'] = visibility
        self._kml['open'] = open
        self._kml['atom:author'] = atomauthor
        self._kml['atom:link'] = atomlink
        self._kml['address'] = address
        self._kml['xal:AddressDetails'] = xaladdressdetails
        self._kml['phoneNumber'] = phonenumber
        self._kml['description'] = description
        self._kml['Camera'] = camera
        self._kml['LookAt'] = lookat
        self._kml['snippet_'] = snippet
        self._kml['TimeStamp'] = timestamp
        self._kml['TimeSpan'] = timespan
        self._kml['Region'] = region
        self._kml['styleUrl'] = None
        self._kml['ExtendedData'] = extendeddata
        self._id = "feat_{0}".format(Feature._id)
        self._style = None
        self._stylemap = None
        self._features = []
        self._styles = []
        self._stylemaps = []
        self._folders = []

    @property
    def name(self):
        """Name of placemark, accepts string."""
        return self._kml['name']

    @name.setter
    def name(self, name):
        self._kml['name'] = name

    @property
    def visibility(self):
        """Whether the feature is shown, accepts int 0 or 1."""
        return self._kml['visibility']

    @visibility.setter
    def visibility(self, visibility):
        self._kml['visibility'] = visibility

    @property
    def open(self):
        """Whether open or closed in Places panel, accepts int 0 or 1."""
        return self._kml['open']

    @open.setter
    def open(self, open):
        self._kml['open'] = open

    @property
    def atomauthor(self):
        """Author of the feature, accepts string."""
        return self._kml['atom:author']

    @atomauthor.setter
    def atomauthor(self, atomauthor):
        self._kml['atom:author'] = atomauthor

    @property
    def atomlink(self):
        """URL containing this KML, accepts string."""
        return self._kml['atom:link']

    @atomlink.setter
    def atomlink(self, atomlink):
        self._kml['atom:link'] = atomlink

    @property
    def address(self):
        """Standard address, accepts string."""
        return self._kml['address']

    @address.setter
    def address(self, address):
        self._kml['address'] = address

    @property
    def xaladdressdetails(self):
        """Address in xAL format, accepts string."""
        return self._kml['xal:AddressDetails']

    @xaladdressdetails.setter
    def xaladdressdetails(self, xaladdressdetails):
        self._kml['xal:AddressDetails'] = xaladdressdetails

    @property
    def phonenumber(self):
        """Phone number used by Google Maps mobile, accepts string."""
        return self._kml['phoneNumber']

    @phonenumber.setter
    def phonenumber(self, phonenumber):
        self._kml['phoneNumber'] = phonenumber

    @property
    def description(self):
        """Description shown in the information balloon, accepts string."""
        return self._kml['description']

    @description.setter
    def description(self, description):
        self._kml['description'] = description

    @property
    def camera(self):
        """Camera that views the scene, accepts [Camera]"""
        if self._kml['Camera'] is None:
            self._kml['Camera'] = Camera()
            self._kml['LookAt'] = None
        return self._kml['Camera']

    @camera.setter
    def camera(self, camera):
        self._kml['Camera'] = camera
        self._kml['LookAt'] = None

    @property
    def lookat(self):
        """Camera relative to the feature, accepts [LookAt]."""
        if self._kml['LookAt'] is None:
            self._kml['LookAt'] = LookAt()
            self._kml['Camera'] = None
        return self._kml['LookAt']

    @lookat.setter
    def lookat(self, lookat):
        self._kml['Camera'] = None
        self._kml['LookAt'] = lookat

    @property
    def snippet(self):
        """Short description of the feature, accepts [Snippet]."""
        if self._kml['snippet_'] is None:
            self._kml['snippet_'] = Snippet()
        return self._kml['snippet_']

    @snippet.setter
    def snippet(self, snippet):
        self._kml['snippet_'] = snippet

    @property
    def extendeddata(self):
        """Extra data for the feature."""
        if self._kml['ExtendedData'] is None:
            self._kml['ExtendedData'] = ExtendedData()
        return self._kml['ExtendedData']

    @extendeddata.setter
    def extendeddata(self, extendeddata):
        self._kml['ExtendedData'] = extendeddata

    @property
    def timestamp(self):
        """Single moment in time, accepts [TimeStamp]."""
        if self._kml['TimeStamp'] is None:
            self._kml['TimeStamp'] = TimeStamp()
        return self._kml['TimeStamp']

    @timestamp.setter
    def timestamp(self, timestamp):
        self._kml['TimeStamp'] = timestamp

    @property
    def timespan(self):
        """Period of time, accepts [TimeSpan]."""
        if self._kml['TimeSpan'] is None:
            self._kml['TimeSpan'] = TimeSpan()
        return self._kml['TimeSpan']

    @timespan.setter
    def timespan(self, timespan):
        self._kml['TimeSpan'] = timespan

    @property
    def region(self):
        """Bounding box of feature, accepts [Region]."""
        if self._kml['Region'] is None:
            self._kml['Region'] = Region()
        return self._kml['Region']

    @region.setter
    def region(self, region):
        self._kml['Region'] = region

    @property
    def id(self):
        """Id number of feature, read-only."""
        return self._id

    @property
    def style(self):
        """The current style of the feature, accepts [Style]."""
        if self._style is None:
            self._style = Style()
            self._setstyle(self._style)
            self._addstyle(self._style)
        return self._style

    @style.setter
    def style(self, style):
        self._setstyle(style)
        self._addstyle(style)
        self._style = style

    @property
    def stylemap(self):
        """The current StyleMap of the feature, accepts [StyleMap]."""
        if self._stylemap is None:
            self._stylemap = StyleMap()
            self._setstyle(self._stylemap)
            self._addstylemap(self._stylemap)
        return self._stylemap

    @stylemap.setter
    def stylemap(self, stylemap):
        self._setstyle(stylemap)
        self._addstylemap(stylemap)
        self._stylemap = stylemap

    @property
    def styleurl(self):
        """Reference to the current styleurl or the feature, accepts string."""
        return self._kml['styleUrl']

    @styleurl.setter
    def styleurl(self, styleurl):
        self._kml['styleUrl'] = styleurl

    @property
    def iconstyle(self):
        """IconStyle of the feature, accepts [IconStyle]."""
        return self.style.iconstyle

    @iconstyle.setter
    def iconstyle(self, iconstyle):
        self.style.iconstyle = iconstyle

    @property
    def labelstyle(self):
        """LabelStyle of the feature, accepts [LabelStyle]."""
        return self.style.labelstyle

    @labelstyle.setter
    def labelstyle(self, labelstyle):
        self.style.labelstyle = labelstyle

    @property
    def linestyle(self):
        """LineStyle of the feature, accepts [LineStyle]."""
        return self.style.linestyle

    @linestyle.setter
    def linestyle(self, linestyle):
        self.style.linestyle = linestyle

    @property
    def polystyle(self):
        """PolyStyle of the feature, accepts [PolyStyle]."""
        return self.style.polystyle

    @polystyle.setter
    def polystyle(self, polystyle):
        self.style.polystyle = polystyle

    @property
    def balloonstyle(self):
        """BalloonStyle of the feature, accepts [BalloonStyle]."""
        return self.style.balloonstyle

    @balloonstyle.setter
    def balloonstyle(self, balloonstyle):
        self.style.balloonstyle = balloonstyle

    @property
    def liststyle(self):
        """ListStyle of the feature, accepts [ListStyle]."""
        return self.style.liststyle

    @liststyle.setter
    def liststyle(self, liststyle):
        self.style.liststyle = liststyle

    def _addstyle(self, style):
        """Attaches the given style (style) to this feature."""
        if style not in self._styles:
            self._styles.append(style)

    def _addstylemap(self, style):
        """Attaches the given style (style) to this feature."""
        if style not in self._stylemaps:
            self._stylemaps.append(style)

    def _setstyle(self, style):
        self._kml['styleUrl'] = "#{0}".format(style.id)

    def __str__(self):
        for stylemap in self._stylemaps:
            self._addstyle(stylemap.normalstyle)
            self._addstyle(stylemap.highlightstyle)
        str = '<{0} id="{1}">'.format(self.__class__.__name__, self._id)
        for style in self._styles:
            str += style.__str__()
        for stylemap in self._stylemaps:
            str += stylemap.__str__()
        str += super(Feature, self).__str__()
        for folder in self._folders:
            str += folder.__str__()
        for feat in self._features:
            str += feat.__str__()
        str += "</{0}>".format(self.__class__.__name__)
        return str

    def _newfeature(self, cls, **kwargs):
        """
        Creates a new feature from the given class and attaches it to this
        feature.

        """
        feat = cls(**kwargs)
        feat._parent = self
        if isinstance(feat, Geometry):
            self._features.append(feat._placemark)
            feat._parent = self
            if feat._style is not None:
                self._addstyle(feat._style)
        else:
            self._features.append(feat)
        return feat

    def newpoint(self, **kwargs):
        """
        Creates a new [Point] and attaches it to this KML document.

        Returns an instance of [Point] class.

        Keyword Arguments:
        Same as [Point].
        """
        return self._newfeature(Point, **kwargs)

    def newlinestring(self, **kwargs):
        """
        Creates a new [LineString] and attaches it to this KML document.

        Returns an instance of [LineString] class.

        Keyword Arguments:
        Same as [LineString].
        """
        return self._newfeature(LineString, **kwargs)

    def newpolygon(self, **kwargs):
        """
        Creates a new [Polygon] and attaches it to this KML document.

        Returns an instance of [Polygon] class.

        Keyword Arguments:
        Same as [Polygon].
        """
        return self._newfeature(Polygon, **kwargs)

    def newmultigeometry(self, **kwargs):
        """
        Creates a new [MultiGeometry] and attaches it to this KML document.

        Returns an instance of [MultiGeometry] class.

        Keyword Arguments:
        Same as [MultiGeometry].
        """
        return self._newfeature(MultiGeometry, **kwargs)

    def newgroundoverlay(self, **kwargs):
        """
        Creates a new [GroundOverlay] and attaches it to this KML document.

        Returns an instance of [GroundOverlay] class.

        Keyword Arguments:
        Same as [GroundOverlay].
        """
        return self._newfeature(GroundOverlay, **kwargs)

    def newscreenoverlay(self, **kwargs):
        """
        Creates a new [ScreenOverlay] and attaches it to this KML document.

        Returns an instance of [ScreenOverlay] class.

        Keyword Arguments:
        Same as [ScreenOverlay].
        """
        return self._newfeature(ScreenOverlay, **kwargs)

    def newphotooverlay(self, **kwargs):
        """
        Creates a new [PhotoOverlay] and attaches it to this KML document.

        Returns an instance of [PhotoOverlay] class.

        Keyword Arguments:
        Same as [PhotoOverlay].
        """
        return self._newfeature(PhotoOverlay, **kwargs)

    def newmodel(self, **kwargs):
        """
        Creates a new [Model] and attaches it to this KML document.

        Returns an instance of [Model] class.

        Keyword Arguments:
        Same as [Model].
        """
        return self._newfeature(Model, **kwargs)

    def newgxtrack(self, **kwargs):
        """
        Creates a new [GxTrack] and attaches it to this KML document.

        Returns an instance of [GxTrack] class.

        Keyword Arguments:
        Same as [GxTrack].
        """
        return self._newfeature(GxTrack, **kwargs)

    def newgxmultitrack(self, **kwargs):
        """
        Creates a new [GxMultiTrack] and attaches it to this KML document.

        Returns an instance of [GxMultiTrack] class.

        Keyword Arguments:
        Same as [GxMultiTrack].
        """
        return self._newfeature(GxMultiTrack, **kwargs)


class Container(Feature):

    """_Base class, extended by Document and Folder."""

    def __init__(self, **kwargs):
        super(Container, self).__init__(**kwargs)

    def newfolder(self, **kwargs):
        """
        Creates a new [Folder] and attaches it to this container.

        Returns an instance of [Folder] class.

        Keyword Arguments:
        Same as [Folder].
        """
        return self._newfeature(Folder, **kwargs)

    def newdocument(self, **kwargs):
        """
        Creates a new [Document] and attaches it to this container.

        Returns an instance of [Document] class.

        Keyword Arguments:
        Same as [Document].
        """
        return self._newfeature(Document, **kwargs)

    def newnetworklink(self, **kwargs):
        """
        Creates a new [NetworkLink] and attaches it to the this container.

        Returns an instance of [NetworkLink] class.

        Keyword Arguments:
        Same as [NetworkLink].
        """
        return self._newfeature(NetworkLink, **kwargs)


class Document(Container):

    """
    A container for features and styles.

    Keyword Arguments:
    name (string)              -- name of placemark (default None)
    visibility (int)           -- whether the feature is shown (default None)
    open (int)                 -- whether open or closed in Places (default None)
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
    Same as arguments, with the following additional properties:
    style ([Style])            -- the current style (default None)
    liststyle ([ListStyle])    -- the current liststyle (default None)

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

    """

    def __init__(self, **kwargs):
        """
        Creates a document container.

        Keyword Arguments:
        name (string)            -- name of placemark (default None)
        visibility (int)         -- whether the feature is shown (default None)
        open (int)               -- whether open or closed in Places (default None)
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
        super(Document, self).__init__(**kwargs)

    def newschema(self, **kwargs):
        """
        Creates a new [Schema] and attaches it to the this document.

        Returns an instance of [Schema] class.

        Keyword Arguments:
        Same as [Schema].
        """
        return self._newfeature(Schema, **kwargs)


class Folder(Container):
    """
    A container for features that act like a folder.

    Keyword Arguments:
    name (string)              -- name of placemark (default None)
    visibility (int)           -- whether the feature is shown (default None)
    open (int)                 -- whether open or closed in Places (default None)
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
    Same as arguments, with the following additional properties:
    style ([Style])            -- the current style (default None)
    liststyle ([ListStyle])    -- the current liststyle (default None)

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

    """

    def __init__(self, **kwargs):
        """
        Creates a folder container.

        Keyword Arguments:
        name (string)            -- name of placemark (default None)
        visibility (int)         -- whether the feature is shown (default None)
        open (int)               -- whether open or closed in Places (default None)
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
        super(Folder, self).__init__(**kwargs)


class Placemark(Feature):

    """_A Placemark is a Feature with associated Geometry."""

    def __init__(self, geometry=None, **kwargs):
        super(Placemark, self).__init__(**kwargs)
        self._kml['Geometry_'] = geometry

    @property
    def geometry(self):
        return self._kml['Geometry_']

    @geometry.setter
    def geometry(self, geom):
        self._kml['Geometry_'] = geom


class Geometry(Kmlable):
    """_Base class for all Geometries."""

    _id = 0
    def __init__(self, **kwargs): # same arguments as feature
        super(Geometry, self).__init__()
        self._id = "geom_{0}".format(Geometry._id)
        Geometry._id += 1
        self._placemark = Placemark(**kwargs)
        self._placemark.geometry = self
        self._parent = None
        self._style = None
        self._stylemap = None

    @property
    def name(self):
        """Name of placemark, accepts string."""
        return self._placemark.name

    @name.setter
    def name(self, name):
        self._placemark.name = name

    @property
    def visibility(self):
        """Whether the feature is shown, accepts int 0 or 1."""
        return self._placemark.visibility

    @visibility.setter
    def visibility(self, visibility):
        self._placemark.visibility = visibility

    @property
    def atomauthor(self):
        """Author of the feature, accepts string."""
        return self._placemark.atomauthor

    @atomauthor.setter
    def atomauthor(self, atomauthor):
        self._placemark.atomauthor = atomauthor

    @property
    def atomlink(self):
        """URL containing this KML, accepts string."""
        return self._placemark.atomlink

    @atomlink.setter
    def atomlink(self, atomlink):
        self._placemark.atomlink = atomlink

    @property
    def address(self):
        """Standard address, accepts string."""
        return self._placemark.address

    @address.setter
    def address(self, address):
        self._placemark.address = address

    @property
    def xaladdressdetails(self):
        """Address in xAL format, accepts string."""
        return self._placemark.xaladdressdetails

    @xaladdressdetails.setter
    def xaladdressdetails(self, xaladdressdetails):
        self._placemark.xaladdressdetails = xaladdressdetails

    @property
    def phonenumber(self):
        """Phone number used by Google Maps mobile, accepts string."""
        return self._placemark.phonenumber

    @phonenumber.setter
    def phonenumber(self, phonenumber):
        self._placemark.phonenumber = phonenumber

    @property
    def description(self):
        """Description shown in the information balloon, accepts string."""
        return self._placemark.description

    @description.setter
    def description(self, description):
        self._placemark.description = description

    @property
    def camera(self):
        """Camera that views the scene, accepts [Camera]"""
        if self._placemark.camera is None:
            self._placemark.camera = Camera()
        return self._placemark.camera

    @camera.setter
    def camera(self, camera):
        self._placemark.camera = camera

    @property
    def lookat(self):
        """Camera relative to the feature, accepts [LookAt]."""
        if self._placemark.lookat is None:
            self._placemark.lookat = LookAt()
        return self._placemark.lookat

    @lookat.setter
    def lookat(self, lookat):
        self._placemark.lookat = lookat

    @property
    def snippet(self):
        """Short description of the feature, accepts [Snippet]."""
        return self._placemark.snippet

    @snippet.setter
    def snippet(self, snippet):
        self._placemark.snippet = snippet

    @property
    def extendeddata(self):
        """Short description of the feature, accepts [Snippet]."""
        return self._placemark.extendeddata

    @extendeddata.setter
    def extendeddata(self, extendeddata):
        self._placemark.extendeddata = extendeddata

    @property
    def timespan(self):
        """Period of time, accepts [TimeSpan]."""
        return self._placemark.timespan

    @timespan.setter
    def timespan(self, timespan):
        self._placemark.timespan = timespan

    @property
    def timestamp(self):
        """Single moment in time, accepts [TimeStamp]."""
        return self._placemark.timestamp

    @timestamp.setter
    def timestamp(self, timestamp):
        self._placemark.timestamp = timestamp

    @property
    def region(self):
        """Bounding box of feature, accepts [Region]."""
        return self._placemark.region

    @region.setter
    def region(self, region):
        self._placemark.region = region

    @property
    def style(self):
        """The current style of the feature, accepts [Style]."""
        if self._style is None:
            self._style = Style()
            self._placemark._setstyle(self._style)
            if self._parent is not None:
                self._parent._addstyle(self._style)
        return self._style

    @style.setter
    def style(self, style):
        self._placemark._setstyle(style)
        if self._parent is not None:
            self._parent._addstyle(style)
        self._style = style

    @property
    def stylemap(self):
        """The current StyleMap of the feature, accepts [StyleMap]."""
        if self._stylemap is None:
            self._stylemap = StyleMap()
            self._placemark._setstyle(self._stylemap)
            if self._parent is not None:
                self._parent._addstylemap(self._stylemap)
        return self._stylemap

    @stylemap.setter
    def stylemap(self, stylemap):
        self._placemark._setstyle(stylemap)
        if self._parent is not None:
            self._parent._addstylemap(stylemap)
        self._stylemap = stylemap

    @property
    def iconstyle(self):
        """IconStyle of the feature, accepts [IconStyle]."""
        return self.style.iconstyle

    @iconstyle.setter
    def iconstyle(self, iconstyle):
        self.style.iconstyle = iconstyle

    @property
    def labelstyle(self):
        """LabelStyle of the feature, accepts [LabelStyle]."""
        return self.style.labelstyle

    @labelstyle.setter
    def labelstyle(self, labelstyle):
        self.style.labelstyle = labelstyle

    @property
    def linestyle(self):
        """LineStyle of the feature, accepts [LineStyle]."""
        return self.style.linestyle

    @linestyle.setter
    def linestyle(self, linestyle):
        self.style.linestyle = linestyle

    @property
    def polystyle(self):
        """PolyStyle of the feature, accepts [PolyStyle]."""
        return self.style.polystyle

    @polystyle.setter
    def polystyle(self, polystyle):
        self.style.polystyle = polystyle

    @property
    def balloonstyle(self):
        """BalloonStyle of the feature, accepts [BalloonStyle]."""
        return self.style.balloonstyle

    @balloonstyle.setter
    def balloonstyle(self, balloonstyle):
        self.style.balloonstyle = balloonstyle

    @property
    def liststyle(self):
        """ListStyle of the feature, accepts [ListStyle]."""
        return self.style.liststyle

    @liststyle.setter
    def liststyle(self, liststyle):
        self.style.liststyle = liststyle
    
    @property
    def placemark(self):
        """The placemark that contains this feature, read-only."""
        return self._placemark


class PointGeometry(Geometry):
    """_Base class for any geometry requiring coordinates (not Polygon)."""
    def __init__(self,
                 coords=(), **kwargs):
        super(PointGeometry, self).__init__(**kwargs)
        self._kml['coordinates'] = Coordinates()
        self._kml['coordinates'].addcoordinates(list(coords))

    @property
    def coords(self):
        """
        The coordinates of the feature, accepts list of tuples.

        A tuple represents a coordinate in lat/lon. The tuple has the option of specifying a height. If no height is
        given, it defaults to zero. A point feature has just one point, therefore a list with one tuple is given.

        Examples:
        No height: `[(1.0, 1.0), (2.0, 1.0)]`
        Height:    `[(1.0, 1.0, 50.0), (2.0, 1.0, 10.0)]`
        Point:     `[(1.0, 1.0)]`
        """
        return self._kml['coordinates']

    @coords.setter
    def coords(self, coords):
        self._kml['coordinates'] = Coordinates()
        self._kml['coordinates'].addcoordinates(coords)


class LinearRing(PointGeometry):

    """A closed line string, typically the outer boundary of a Polygon.

    Keyword Arguments:
    coords (list of tuples)    -- ring coordinates (default [(0.0,0.0,0.0)]
    name (string)              -- name of placemark (default None)
    visibility (int)           -- whether the feature is shown (default None)
    open (int)                 -- whether open or closed in Places (default None)
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
    extrude (int)              -- whether to connect to the ground (default None)
    tessellate (int)           -- allowed to follow the terrain (default None)
    altitudemode (string)      -- alt use See [AltitudeMode] (default None)
    gxaltitudemode (string)    -- alt use. See [GxAltitudeMode] (default None)
    gxaltitudeoffset           -- offsets feature vertically (default None)

    Properties:
    Same as arguments, with the following additional properties:
    style ([Style])               -- stlye of feature (default None)
    stylemap ([StyleMap])         -- stylemap of feature (default None)
    liststyle ([ListStyle])       -- liststyle of feature(default None)
    balloonstyle ([BalloonStyle]) -- balloonstyle of feature(default None)
    iconstyle ([IconStyle])       -- iconstyle of feature(default None)
    labelstyle ([LabelStyle])     -- labelstyle of feature(default None)
    linestyle ( [LineStyle])      -- linestyle of feature(default None)
    polystyle ([PolyStyle])       -- polystyle of feature(default None)
    placemark ([Placemark])       -- feature's placemark(default [Placemark])

    """

    def __init__(self, coords=(),
                 extrude=None,
                 tessellate=None,
                 altitudemode=None,
                 gxaltitudemode=None,
                 gxaltitudeoffset=None,
                 **kwargs):
        """
        Creates a linearring element.

        Keyword Arguments:
        coords (list of tuples)  -- ring coordinates (default [(0.0,0.0,0.0)]
        name (string)            -- name of placemark (default None)
        visibility (int)         -- whether the feature is shown (default None)
        open (int)               -- whether open or closed in Places (default None)
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
        extrude (int)            -- connect to the ground? (default None)
        tessellate (int)         -- allowed to follow the terrain (default None)
        altitudemode (string)    -- alt use See [AltitudeMode] (default None)
        gxaltitudemode (string)  -- alt use. See [GxAltitudeMode] (default None)
        gxaltitudeoffset         -- offsets feature vertically (default None)
        
        """
        super(LinearRing, self).__init__(list(coords), **kwargs)
        self._kml['extrude'] = extrude
        self._kml['tessellate'] = tessellate
        self._kml['altitudeMode'] = altitudemode
        self._kml['gx:altitudeMode'] = gxaltitudemode
        self._kml['gx:altitudeOffset'] = gxaltitudeoffset

    def __str__(self):
        str = '<LinearRing>'
        str += super(LinearRing, self).__str__()
        str += "</LinearRing>"
        return str

    @property
    def extrude(self):
        """Connect the LinearRing to the ground, accepts int (0 or 1)."""
        return self._kml['extrude']

    @extrude.setter
    def extrude(self, extrude):
        self._kml['extrude'] = extrude

    @property
    def tessellate(self):
        """Allowe the LinearRing to follow the terrain, accepts int (0 or 1)."""
        return self._kml['tessellate']

    @tessellate.setter
    def tessellate(self, tessellate):
        self._kml['tessellate'] = tessellate

    @property
    def altitudemode(self):
        """
        Specifies how the altitude for the Camera is interpreted.

        Accepts [AltitudeMode] constants.

        """
        return self._kml['altitudeMode']

    @altitudemode.setter
    def altitudemode(self, mode):
        self._kml['altitudeMode'] = mode

    @property
    def gxaltitudemode(self):
        """
        Specifies how the altitude for the Camera is interpreted.

        With the addition of being relative to the sea floor.
        Accepts [GxAltitudeMode] constants.

        """
        return self._kml['gx:altitudeMode']

    @gxaltitudemode.setter
    def gxaltitudemode(self, mode):
        self._kml['gx:altitudeMode'] = mode

    @property
    def gxaltitudeoffset(self):
        """How much to offsets the LinearRing vertically, accepts int."""
        return self._kml['gx:altitudeOffset']

    @gxaltitudeoffset.setter
    def gxaltitudeoffset(self, offset):
        self._kml['gx:altitudeOffset'] = offset


class Point(PointGeometry):

    """
    A geographic location defined by lon, lat, and altitude.

    Keyword Arguments:
    coords (list of tuples)    -- ring coordinates (default [(0.0,0.0,0.0)]
    name (string)              -- name of placemark (default None)
    visibility (int)           -- whether the feature is shown (default None)
    open (int)                 -- whether open or closed in Places (default None)
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
    extrude (int)              -- whether to connect to the ground (default None)
    altitudemode (string)      -- alt use See [AltitudeMode] (default None)
    gxaltitudemode (string)    -- alt use. See [GxAltitudeMode] (default None)
    extendeddata ([ExtendedData]) -- extra data (default None)


    Properties:
    Same as arguments, with the following additional properties:
    style ([Style])               -- stlye of feature (default None)
    stylemap ([StyleMap])         -- stylemap of feature (default None)
    liststyle ([ListStyle])       -- liststyle of feature(default None)
    balloonstyle ([BalloonStyle]) -- balloonstyle of feature(default None)
    iconstyle ([IconStyle])       -- iconstyle of feature(default None)
    labelstyle ([LabelStyle])     -- labelstyle of feature(default None)
    linestyle ( [LineStyle])      -- linestyle of feature(default None)
    polystyle ([PolyStyle])       -- polystyle of feature(default None)
    placemark ([Placemark])       -- feature's placemark(default [Placemark])

    """

    def __init__(self,
                 extrude=None,
                 altitudemode=None,
                 gxaltitudemode=None,
                 **kwargs):
        """
        Creates a Point element.

        Keyword Arguments:
        coords (list of tuples)  -- ring coordinates (default [(0.0,0.0,0.0)]
        name (string)            -- name of placemark (default None)
        visibility (int)         -- whether the feature is shown (default None)
        open (int)               -- whether open or closed in Places (default None)
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
        extrude (int)            -- connect to the ground? (default None)
        altitudemode (string)    -- alt use See [AltitudeMode] (default None)
        gxaltitudemode (string)  -- alt use. See [GxAltitudeMode] (default None)
        extendeddata ([ExtendedData]) -- extra data (default None)

        """
        super(Point, self).__init__(**kwargs)
        self._kml['extrude'] = extrude
        self._kml['altitudeMode'] = altitudemode
        self._kml['gx:altitudeMode'] = gxaltitudemode

    @property
    def extrude(self):
        """Connect the Point to the ground, accepts int (0 or 1)."""
        return self._kml['extrude']

    @extrude.setter
    def extrude(self, extrude):
        self._kml['extrude'] = extrude

    @property
    def altitudemode(self):
        """
        Specifies how the altitude for the Camera is interpreted.

        Accepts [AltitudeMode] constants.

        """
        return self._kml['altitudeMode']

    @altitudemode.setter
    def altitudemode(self, mode):
        self._kml['altitudeMode'] = mode

    @property
    def gxaltitudemode(self):
        """
        Specifies how the altitude for the Camera is interpreted.

        With the addition of being relative to the sea floor.
        Accepts [GxAltitudeMode] constants.

        """
        return self._kml['gx:altitudeMode']

    @gxaltitudemode.setter
    def gxaltitudemode(self, mode):
        self._kml['gx:altitudeMode'] = mode

    def __str__(self):
        str = '<Point id="{0}">'.format(self._id)
        str += super(Point, self).__str__()
        str += "</Point>"
        return str


class LineString(PointGeometry):
    """
    A connected set of line segments.

    Keyword Arguments:
    coords (list of tuples)  -- ring coordinates (default [(0.0,0.0,0.0)]
    name (string)            -- name of placemark (default None)
    visibility (int)         -- whether the feature is shown (default None)
    open (int)               -- whether open or closed in Places (default None)
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
    extrude (int)            -- connect to the ground? (default None)
    tessellate (int)         -- allowed to follow the terrain (default None)
    altitudemode (string)    -- alt use See [AltitudeMode] (default None)
    gxaltitudemode (string)  -- alt use. See [GxAltitudeMode] (default None)
    gxaltitudeoffset         -- offsets feature vertically (default None)
    gxdraworder (int)        -- draw order many linestrings (default None)
    extendeddata ([ExtendedData]) -- extra data (default None)

    Properties:
    Same as arguments, with the following additional properties:
    style               -- [Style] (default None)
    stylemap            -- [StyleMap] (default None)
    liststyle           -- [ListStyle] (default None)
    balloonstyle        -- [BalloonStyle] (default None)
    iconstyle           -- [IconStyle] (default None)
    labelstyle          -- [LabelStyle] (default None)
    linestyle           -- [LineStyle] (default None)
    polystyle           -- [PolyStyle] (default None)
    placemark           -- [Placemark] (default [Placemark], read-only)

    """
    def __init__(self,
                 extrude=None,
                 tessellate=None,
                 altitudemode=None,
                 gxaltitudemode=None,
                 gxaltitudeoffset=None,
                 gxdraworder=None,
                 **kwargs):
        """
        Create a linestring element

        Keyword Arguments:
        coords (list of tuples)  -- ring coordinates (default [(0.0,0.0,0.0)]
        name (string)            -- name of placemark (default None)
        visibility (int)         -- whether the feature is shown (default None)
        open (int)               -- whether open or closed in Places (default None)
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
        extrude (int)            -- connect to the ground? (default None)
        tessellate (int)         -- allowed to follow the terrain (default None)
        altitudemode (string)    -- alt use See [AltitudeMode] (default None)
        gxaltitudemode (string)  -- alt use. See [GxAltitudeMode] (default None)
        gxaltitudeoffset         -- offsets feature vertically (default None)
        gxdraworder (int)        -- draw order many linestrings (default None)
        extendeddata ([ExtendedData]) -- extra data (default None)

        """
        super(LineString, self).__init__(**kwargs)
        self._kml['extrude'] = extrude
        self._kml['tessellate'] = tessellate
        self._kml['altitudeMode'] = altitudemode
        self._kml['gx:altitudeMode'] = gxaltitudemode
        self._kml['gx:altitudeOffset'] = gxaltitudeoffset
        self._kml['gx:drawOrder'] = gxdraworder

    @property
    def extrude(self):
        """Connect the LinearRing to the ground, accepts int (0 or 1)."""
        return self._kml['extrude']

    @extrude.setter
    def extrude(self, extrude):
        self._kml['extrude'] = extrude

    @property
    def tessellate(self):
        """Allowe the LinearRing to follow the terrain, accepts int (0 or 1)."""
        return self._kml['tessellate']

    @tessellate.setter
    def tessellate(self, tessellate):
        self._kml['tessellate'] = tessellate

    @property
    def altitudemode(self):
        """
        Specifies how the altitude for the Camera is interpreted.

        Accepts [AltitudeMode] constants.

        """
        return self._kml['altitudeMode']

    @altitudemode.setter
    def altitudemode(self, mode):
        self._kml['altitudeMode'] = mode

    @property
    def gxaltitudemode(self):
        """
        Specifies how the altitude for the Camera is interpreted.

        With the addition of being relative to the sea floor.
        Accepts [GxAltitudeMode] constants.

        """
        return self._kml['gx:altitudeMode']

    @gxaltitudemode.setter
    def gxaltitudemode(self, mode):
        self._kml['gx:altitudeMode'] = mode

    @property
    def gxaltitudeoffset(self):
        """How much to offsets the LinearRing vertically, accepts int."""
        return self._kml['gx:altitudeOffset']

    @gxaltitudeoffset.setter
    def gxaltitudeoffset(self, offset):
        self._kml['gx:altitudeOffset'] = offset

    @property
    def gxdraworder(self):
        """The order to draw the linestring, accepts int."""
        return self._kml['gx:drawOrder']

    @gxdraworder.setter
    def gxdraworder(self, gxdraworder):
        self._kml['gx:drawOrder'] = gxdraworder

    def __str__(self):
        str = '<LineString id="{0}">'.format(self._id)
        str += super(LineString, self).__str__()
        str += "</LineString>"
        return str


class Polygon(Geometry):

    """
    A Polygon is defined by an outer boundary and/or an inner boundary.

    Keyword Arguments:
    name (string)            -- name of placemark (default None)
    visibility (int)         -- whether the feature is shown (default None)
    open (int)               -- whether open or closed in Places (default None)
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
    extrude (int)            -- connect to the ground? (default None)
    tessellate (int)         -- allowed to follow the terrain (default None)
    altitudemode (string)    -- alt use See [AltitudeMode] (default None)
    gxaltitudemode (string)  -- alt use. See [GxAltitudeMode] (default None)
    gxaltitudeoffset         -- offsets feature vertically (default None)
    gxdraworder (int)        -- draw order many linestrings (default None)
    outerboundaryis (tuples) -- list of tuples for outer (default (0.0,0.0,0.0))
    innerboundaryis (tuples) -- list of lists of tuples for inner (default None)
    extendeddata ([ExtendedData]) -- extra data (default None)

    Properties:
    Same as arguments, with the following additional properties:
    style               -- [Style] (default None)
    stylemap            -- [StyleMap] (default None)
    liststyle           -- [ListStyle] (default None)
    balloonstyle        -- [BalloonStyle] (default None)
    iconstyle           -- [IconStyle] (default None)
    labelstyle          -- [LabelStyle] (default None)
    linestyle           -- [LineStyle] (default None)
    polystyle           -- [PolyStyle] (default None)
    placemark           -- [Placemark] (default [Placemark], read-only)

    """

    def __init__(self,
                 extrude=None,
                 tessellate=None,
                 altitudemode=None,
                 gxaltitudemode=None,
                 outerboundaryis=(),
                 innerboundaryis=(), **kwargs):
        """
        Creates a polygon element

        Keyword Arguments:
        name (string)          -- name of placemark (default None)
        visibility (int)       -- whether the feature is shown (default None)
        open (int)             -- whether open or closed in Places (default None)
        atomauthor (string)    -- author of the document (default None)
        atomlink (string)      -- URL containing this KML (default None)
        address (string)       -- standard address (default None)
        xaladdressdetails(string)-- address as xAL (default None)
        phonenumber (string)   -- phone number for Maps mobile (default None)
        snippet ([Snippet])    -- short description of feature (default None)
        description (string)   -- description shown in balloon (default None)
        camera ([Camera])      -- camera that views the scene (default None)
        lookat ([LookAt])      -- camera relative to feature (default None)
        timestamp ([TimeStamp])-- single moment in time (default None)
        timespan ([TimeSpan])  -- period of time (default None)
        region ([Region])      -- bounding box of features (default None)
        extrude (int)          -- connect to the ground? (default None)
        tessellate (int)       -- allowed to follow the terrain (default None)
        altitudemode (string)  -- alt use See [AltitudeMode] (default None)
        gxaltitudemode (string)-- alt use. See [GxAltitudeMode] (default None)
        gxaltitudeoffset       -- offsets feature vertically (default None)
        gxdraworder (int)      -- draw order many linestrings (default None)
        outerboundaryis(tuples)--list of tuples for outer(default (0.0,0.0,0.0))
        innerboundaryis(tuples)--list of lists of tuples for inner(default None)
        extendeddata ([ExtendedData]) -- extra data (default None)

        """
        super(Polygon, self).__init__(**kwargs)
        self._kml['extrude'] = extrude
        self._kml['tessellate'] = tessellate
        self._kml['altitudeMode'] = altitudemode
        self._kml['gx:altitudeMode'] = gxaltitudemode
        self._kml['outerBoundaryIs'] = LinearRing(list(outerboundaryis))
        self._kml['innerBoundaryIs'] = None
        self.innerboundaryis = list(innerboundaryis)

    @property
    def extrude(self):
        """Connect the LinearRing to the ground, accepts int (0 or 1)."""
        return self._kml['extrude']

    @extrude.setter
    def extrude(self, extrude):
        self._kml['extrude'] = extrude

    @property
    def tessellate(self):
        """Allowe the LinearRing to follow the terrain, accepts int (0 or 1)."""
        return self._kml['tessellate']

    @tessellate.setter
    def tessellate(self, tessellate):
        self._kml['tessellate'] = tessellate

    @property
    def altitudemode(self):
        """
        Specifies how the altitude for the Camera is interpreted.

        Accepts [AltitudeMode] constants.

        """
        return self._kml['altitudeMode']

    @altitudemode.setter
    def altitudemode(self, mode):
        self._kml['altitudeMode'] = mode

    @property
    def gxaltitudemode(self):
        """
        Specifies how the altitude for the Camera is interpreted.

        With the addition of being relative to the sea floor.
        Accepts [GxAltitudeMode] constants.

        """
        return self._kml['gx:altitudeMode']

    @gxaltitudemode.setter
    def gxaltitudemode(self, mode):
        self._kml['gx:altitudeMode'] = mode

    @property
    def innerboundaryis(self):
        """
        The inner boundaries.

        Accepts list of list of tuples of floats for multiple boundaries, or a
        list of tuples of floats for a single boundary.

        """
        return self._innerboundaryis

    @innerboundaryis.setter
    def innerboundaryis(self, rings):
        self._innerboundaryis = []
        if not len(rings):
            self._kml['innerBoundaryIs'] = None
        else:
            if type(rings[0]) == type(()):
                rings = [rings]
            self._kml['innerBoundaryIs'] = ''
            for ring in rings:
                self._kml['innerBoundaryIs'] += LinearRing(ring).__str__()
                self._innerboundaryis.append(LinearRing(ring))

    @property
    def outerboundaryis(self):
        """The outer boundary, accepts a list of tuples of floats."""
        return self._kml['outerBoundaryIs']

    @outerboundaryis.setter
    def outerboundaryis(self, coords):
        self._kml['outerBoundaryIs'] = LinearRing(coords)

    def __str__(self):
        str = '<Polygon id="{0}">'.format(self._id)
        str += super(Polygon, self).__str__()
        str += "</Polygon>"
        return str


class MultiGeometry(Geometry):
    """
    A Polygon is defined by an outer boundary and/or an inner boundary.

    Keyword Arguments:
    name (string)            -- name of placemark (default None)
    visibility (int)         -- whether the feature is shown (default None)
    open (int)               -- whether open or closed in Places (default None)
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

    Properties:
    Same as arguments, with the following additional properties:
    style               -- [Style] (default None)
    stylemap            -- [StyleMap] (default None)
    liststyle           -- [ListStyle] (default None)
    balloonstyle        -- [BalloonStyle] (default None)
    iconstyle           -- [IconStyle] (default None)
    labelstyle          -- [LabelStyle] (default None)
    linestyle           -- [LineStyle] (default None)
    polystyle           -- [PolyStyle] (default None)
    placemark           -- [Placemark] (default [Placemark], read-only)

    Public Methods:
    newpoint                   -- Creates a new [Point]
    newlinestring              -- Creates a new [LineString]
    newpolygon                 -- Creates a new [Polygon]
    newgroundoverlay           -- Creates a new [GroundOverlay]
    newscreenoverlay           -- Creates a new [ScreenOverlay]
    newphotooverlay            -- Creates a new [PhotoOverlay]
    newmodel                   -- Creates a new [Model]

    """

    def __init__(self,
                 geometries=(), **kwargs):
        """
        Creates a new multigeometry element.

        Keyword Arguments:
        name (string)            -- name of placemark (default None)
        visibility (int)         -- whether the feature is shown (default None)
        open (int)               -- whether open or closed in Places (default None)
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
        super(MultiGeometry, self).__init__(**kwargs)
        self._geometries = list(geometries)

    def _newfeature(self, cls, **kwargs):
        feat = cls(**kwargs)
        feat._parent = self._placemark
        self._geometries.append(feat)
        return feat

    def newpoint(self, **kwargs):
        """
        Creates a new [Point] and attaches it to this MultiGeometry.

        Returns an instance of [Point] class.

        Keyword Arguments:
        Same as [Point].
        """
        return self._newfeature(Point, **kwargs)

    def newlinestring(self, **kwargs):
        """
        Creates a new [LineString] and attaches it to this MultiGeometry.

        Returns an instance of [LineString] class.

        Keyword Arguments:
        Same as [LineString].
        """
        return self._newfeature(LineString, **kwargs)

    def newpolygon(self, **kwargs):
        """
        Creates a new [Polygon] and attaches it to this MultiGeometry.

        Returns an instance of [Polygon] class.

        Keyword Arguments:
        Same as [Polygon].
        """
        return self._newfeature(Polygon, **kwargs)

    def newgroundoverlay(self, **kwargs):
        """
        Creates a new [GroundOverlay] and attaches it to this MultiGeometry.

        Returns an instance of [GroundOverlay] class.

        Keyword Arguments:
        Same as [GroundOverlay].
        """
        return self._newfeature(GroundOverlay, **kwargs)

    def newscreenoverlay(self, **kwargs):
        """
        Creates a new [ScreenOverlay] and attaches it to this MultiGeometry.

        Returns an instance of [ScreenOverlay] class.

        Keyword Arguments:
        Same as [ScreenOverlay].
        """
        return self._newfeature(ScreenOverlay, **kwargs)

    def newphotooverlay(self, **kwargs):
        """
        Creates a new [PhotoOverlay] and attaches it to this MultiGeometry.

        Returns an instance of [PhotoOverlay] class.

        Keyword Arguments:
        Same as [PhotoOverlay].
        """
        return self._newfeature(PhotoOverlay, **kwargs)

    def newmodel(self, **kwargs):
        """
        Creates a new [Model] and attaches it to this MultiGeometry.

        Returns an instance of [Model] class.

        Keyword Arguments:
        Same as [Model].
        """
        return self._newfeature(Model, **kwargs)

    def __str__(self):
        str = '<MultiGeometry id="{0}">'.format(self._id)
        str += super(MultiGeometry, self).__str__()
        for geom in self._geometries:
            str += geom.__str__()
        str += "</MultiGeometry>"
        return str


class Overlay(Feature):
    """_Base type for image overlays."""
    def __init__(self, color=None,
                       draworder=None,
                       icon=None,
                       **kwargs):
        super(Overlay, self).__init__(**kwargs)
        self._kml['color'] = color
        self._kml['drawOrder'] = draworder
        self._kml['Icon'] = icon

    @property
    def color(self):
        """The color of the overlay, accepts hex string."""
        return self._kml['color']

    @color.setter
    def color(self, color):
        self._kml['color'] = color

    @property
    def draworder(self):
        """The order to draw the overlay, accepts int."""
        return self._kml['drawOrder']

    @draworder.setter
    def draworder(self, draworder):
        self._kml['drawOrder'] = draworder

    @property
    def icon(self):
        """The icon to use for the overlay, accepts [Icon]."""
        if self._kml['Icon'] is None:
            self._kml['Icon'] = Icon()
        return self._kml['Icon']

    @icon.setter
    def icon(self, icon):
        self._kml['Icon'] = icon


class GroundOverlay(Overlay):
    """
    Draws an image overlay draped onto the terrain.

    Keyword Arguments:
    name (string)            -- name of placemark (default None)
    visibility (int)         -- whether the feature is shown (default None)
    open (int)               -- whether open or closed in Places (default None)
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
    color (hex string)       -- string of [Color] constants (default None)
    draworder (int)          -- the order the overlay is drawn (default None)
    icon ([Icon])            -- an icon for the overlay (default None)
    altitude (float)         -- distance above earth's surface  (default None)
    altitudemode (string)    -- alt use See [AltitudeMode] (default None)
    gxaltitudemode (string)  -- alt use. See [GxAltitudeMode] (default None)
    latlonbox ([LatLonBox])  -- position of overlay (default None)
    gxlatlonquad ([GxLatLonQuad])-- position of overlay (default None)
    extendeddata ([ExtendedData]) -- extra data (default None)

    Properties:
    Same as arguments, with the following additional properties:
    style               -- [Style] (default None)
    liststyle           -- [ListStyle] (default None)
    balloonstyle        -- [BalloonStyle] (default None)
    placemark           -- [Placemark] (default [Placemark], read-only)

    """

    def __init__(self, altitude=None,
                       altitudemode=None,
                       gxaltitudemode=None,
                       latlonbox=None,
                       gxlatlonquad=None,
                       **kwargs):
        """
        Creates a groundoverlay element.

        Keyword Arguments:
        name (string)            -- name of placemark (default None)
        visibility (int)         -- whether the feature is shown (default None)
        open (int)               -- whether open or closed in Places (default None)
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
        color (hex string)       -- string of [Color] constants (default None)
        draworder (int)          -- int (default None)
        icon ([Icon])            -- [Icon] (default None)
        altitude (float)         -- distance above earth (default None)
        altitudemode (string)    -- alt use See [AltitudeMode] (default None)
        gxaltitudemode (string)  -- alt use. See [GxAltitudeMode] (default None)
        latlonbox ([LatLonBox])  -- position of overlay (default None)
        gxlatlonquad ([GxLatLonQuad])-- position of overlay (default None)
        extendeddata ([ExtendedData]) -- extra data (default None)

        """
        super(GroundOverlay, self).__init__(**kwargs)
        self._kml['altitude'] = altitude
        self._kml['altitudeMode'] = altitudemode
        self._kml['gx:altitudeMode'] = gxaltitudemode
        self._kml['LatLonBox'] = latlonbox
        self._kml['gx:LatLonQuad'] = gxlatlonquad

    @property
    def altitude(self):
        """Distance above earth surface, accepts float."""
        return self._kml['altitude']

    @altitude.setter
    def altitude(self, altitude):
        self._kml['altitude'] = altitude

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
    def gxaltitudemode(self, gxaltitudemode):
        self._kml['gx:altitudeMode'] = gxaltitudemode

    @property
    def latlonbox(self):
        """
        Specifies where the top, bottom, right, and left sides are.

        Accepts [LatLonBox].

        """
        if self._kml['LatLonBox'] is None:
            self._kml['LatLonBox'] = LatLonBox()
        return self._kml['LatLonBox']

    @latlonbox.setter
    def latlonbox(self, latlonbox):
        self._kml['LatLonBox'] = latlonbox

    @property
    def gxlatlonquad(self):
        """
        Specifies the coordinates of the four corner points of a quadrilateral
        defining the overlay area. Accepts [GxLatLonQuad].

        """
        if self._kml['gx:LatLonQuad'] is None:
            self._kml['gx:LatLonQuad'] = GxLatLonQuad()
        return self._kml['gx:LatLonQuad']

    @gxlatlonquad.setter
    def gxlatlonquad(self, gxlatlonquad):
        self._kml['gx:LatLonQuad'] = gxlatlonquad


class ScreenOverlay(Overlay):
    """
    Draws an image overlay fixed to the screen.

    Keyword Arguments:
    name (string)            -- name of placemark (default None)
    visibility (int)         -- whether the feature is shown (default None)
    open (int)               -- whether open or closed in Places (default None)
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
    color (hex string)       -- string of [Color] constants (default None)
    draworder (int)          -- int (default None)
    icon ([Icon])            -- an icon (default None)
    overlayxy ([OverlayXY])  -- point in overlay image (default None)
    screenxy ([ScreenXY])    -- point on screen (default None)
    rotationxy ([RotationXY])-- screen point to rotate about (default None)
    size ([Size])            -- size of the image(default None)
    rotation (float)         -- rotation of the image (default None)
    extendeddata ([ExtendedData]) -- extra data (default None)

    Properties:
    Same as arguments, with the following additional properties:
    style               -- [Style] (default None)
    liststyle           -- [ListStyle] (default None)
    balloonstyle        -- [BalloonStyle] (default None)
    placemark           -- [Placemark] (default [Placemark], read-only)

    """

    def __init__(self, overlayxy=None,
                       screenxy=None,
                       rotationxy=None,
                       size=None,
                       rotation=None,
                       **kwargs):
        """
        Creates a screenoverlay element.

        Keyword Arguments:
        name (string)            -- name of placemark (default None)
        visibility (int)         -- whether the feature is shown (default None)
        open (int)               -- whether open or closed in Places (default None)
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
        color (hex string)       -- string of [Color] constants (default None)
        draworder (int)          -- int (default None)
        icon ([Icon])            -- an icon (default None)
        overlayxy ([OverlayXY])  -- point in overlay image (default None)
        screenxy ([ScreenXY])    -- point on screen (default None)
        rotationxy ([RotationXY])-- screen point to rotate about (default None)
        size ([Size])            -- size of the image(default None)
        rotation (float)         -- rotation of the image (default None)
        extendeddata ([ExtendedData]) -- extra data (default None)

        """
        super(ScreenOverlay, self).__init__(**kwargs)
        self._kml['rotation'] =rotation
        self._kml['overlayXY_'] = overlayxy
        self._kml['screenXY_'] = screenxy
        self._kml['rotationXY_'] = rotationxy
        self._kml['size_'] = size

    @property
    def rotation(self):
        """Rotation of the overlay, accepts float."""
        return self._kml['rotation']

    @rotation.setter
    def rotation(self, rotation):
        self._kml['rotation'] = rotation

    @property
    def overlayxy(self):
        """
        Point on the overlay image that is mapped to a screen coordinate.

        Specifies a point on (or outside of) the overlay image that is mapped
        to the screen coordinate [ScreenXY], accepts [OverlayXY]
        """
        if self._kml['overlayXY_'] is None:
            self._kml['overlayXY_'] = OverlayXY()
        return self._kml['overlayXY_']

    @overlayxy.setter
    def overlayxy(self, overlayxy):
        self._kml['overlayXY_'] = overlayxy

    @property
    def screenxy(self):
        """
        Point relative to screen origin that the image is mapped to.

        Specifies a point relative to the screen origin that the overlay image
        is mapped to, accepts [ScreenXY].
        
        """
        if self._kml['screenXY_'] is None:
            self._kml['screenXY_'] = ScreenXY()
        return self._kml['screenXY_']

    @screenxy.setter
    def screenxy(self, screenxy):
        self._kml['screenXY_'] = screenxy

    @property
    def rotationxy(self):
        """
        Point relative to the screen about which the overlay is rotated.

        Accepts [RotationXY]
        """
        if self._kml['rotationXY_'] is None:
            self._kml['rotationXY_'] = RotationXY()
        return self._kml['rotationXY_']

    @rotationxy.setter
    def rotationxy(self, rotationxy):
        self._kml['rotationXY_'] = rotationxy

    @property
    def size(self):
        """The size of the image for the screen overlay, accepts [Size]."""
        if self._kml['size_'] is None:
            self._kml['size_'] = Size()
        return self._kml['size_']

    @size.setter
    def size(self, size):
        self._kml['size_'] = size


class PhotoOverlay(Overlay):
    """
    Geographically locate a photograph in Google Earth.

    Keyword Arguments:
    name (string)            -- name of placemark (default None)
    visibility (int)         -- whether the feature is shown (default None)
    open (int)               -- whether open or closed in Places (default None)
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
    color (hex string)       -- string of [Color] constants (default None)
    draworder (int)          -- the order the overlay is drawn (default None)
    icon ([Icon])            -- an icon for the overlay (default None)
    rotation (float)         -- the rotation of the overlay (default None)
    viewvolume ([ViewVolume])-- extent current scene is visible (default None)
    imagepyramid([ImagePyramid])-- hierarchical set of images (default None)
    point ([Point])          -- draws an icon to mark position (default None)
    shape (string)           -- string from [Shape] constants (default None)
    extendeddata ([ExtendedData]) -- extra data (default None)

    Properties:
    Same as arguments, with the following additional properties:
    style               -- [Style] (default None)
    iconstyle           -- [IconStyle] (default None)
    liststyle           -- [ListStyle] (default None)
    balloonstyle        -- [BalloonStyle] (default None)
    placemark           -- [Placemark] (default [Placemark], read-only)

    """

    def __init__(self, rotation=None,
                       viewvolume=None,
                       imagepyramid=None,
                       point=None,
                       shape=None,
                       **kwargs):
        """
        Creates a photooverlay element.

        Keyword Arguments:
        name (string)            -- name of placemark (default None)
        visibility (int)         -- whether the feature is shown (default None)
        open (int)               -- whether open or closed in Places (default None)
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
        color (hex string)       -- string of [Color] constants (default None)
        draworder (int)          -- the order the overlay is drawn (default None)
        icon ([Icon])            -- an icon for the overlay (default None)
        rotation (float)         -- the rotation of the overlay (default None)
        viewvolume ([ViewVolume])-- extent current scene is visible (default None)
        imagepyramid([ImagePyramid])-- hierarchical set of images (default None)
        point ([Point])          -- draws an icon to mark position (default None)
        shape (string)           -- string from [Shape] constants (default None)
        extendeddata ([ExtendedData]) -- extra data (default None)

        """
        super(PhotoOverlay, self).__init__(**kwargs)
        self._kml['rotation'] = rotation
        self._kml['ViewVolume'] = viewvolume
        self._kml['ImagePyramid'] = imagepyramid
        self._kml['point_'] = point
        self._kml['shape'] = shape

    @property
    def rotation(self):
        """Rotation of the overlay, accepts float."""
        return self._kml['rotation']

    @rotation.setter
    def rotation(self, rotation):
        self._kml['rotation'] = rotation

    @property
    def viewvolume(self):
        """How much of the current scene is visible, accepts [ViewVolume]."""
        if self._kml['ViewVolume'] is None:
            self._kml['ViewVolume'] = ViewVolume()
        return self._kml['ViewVolume']

    @viewvolume.setter
    def viewvolume(self, viewvolume):
        self._kml['ViewVolume'] = viewvolume

    @property
    def imagepyramid(self):
        """Hierarchical set of images, accepts [ImagePyramid]."""
        if self._kml['ImagePyramid'] is None:
            self._kml['ImagePyramid'] = ImagePyramid()
        return self._kml['ImagePyramid']

    @imagepyramid.setter
    def imagepyramid(self, imagepyramid):
        self._kml['ImagePyramid'] = imagepyramid

    @property
    def point(self):
        """Draws an icon to mark the position of the overlay,accepts [Point]."""
        if self._kml['point_'] is None:
            self._kml['point_'] = Point()
        return self._kml['point_']

    @point.setter
    def point(self, point):
        self._kml['point_'] = point

    @property
    def shape(self):
        """Shape the photo is drawn, accepts string from [Shape] constants."""
        return self._kml['shape']

    @shape.setter
    def shape(self, shape):
        self._kml['shape'] = shape


class NetworkLink(Feature):
    """
    References a KML file or KMZ archive on a local or remote network.

    Keyword Arguments:
    name (string)            -- name of placemark (default None)
    visibility (int)         -- whether the feature is shown (default None)
    open (int)               -- whether open or closed in Places (default None)
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
    extrude (int)            -- connect to the ground? (default 0)
    altitudemode (string)    -- alt use See [AltitudeMode] (default None)
    gxaltitudemode (string)  -- alt use. See [GxAltitudeMode] (default None)
    refreshvisibility (int)  -- action to be taken on refresh (default None)
    flytoview (int)          -- whether to fly to the view (default None)
    link ([Link])            -- link element (default None)

    Properties:
    Same as arguments.

    """
    
    def __init__(self, refreshvisibility=None,
                       flytoview=None,
                       link=None,
                       **kwargs):
        """
        Creates a NetworkLink Element.

        Keyword Arguments:
        name (string)            -- name of placemark (default None)
        visibility (int)         -- whether the feature is shown (default None)
        open (int)               -- whether open or closed in Places (default None)
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
        extrude (int)            -- connect to the ground? (default None)
        altitudemode (string)    -- alt use See [AltitudeMode] (default None)
        gxaltitudemode (string)  -- alt use. See [GxAltitudeMode] (default None)
        refreshvisibility (int)  -- action to be taken on refresh (default None)
        flytoview (int)          -- whether to fly to the view (default None)
        link ([Link])            -- link element (default None)

        """
        super(NetworkLink, self).__init__(**kwargs)
        self._kml['refreshVisibility'] = refreshvisibility
        self._kml['flyToView'] = flytoview
        self._kml['Link'] = link

    @property
    def refreshvisibility(self):
        """
        How the visibility is affected by a refresh

        A value of 0 leaves the visibility of features within the control of
        the Google Earth user. Set the value to 1 to reset the visibility of
        features each time the NetworkLink is refreshed, accepts int (0 or 1).
         
        """
        return self._kml['refreshVisibility']

    @refreshvisibility.setter
    def refreshvisibility(self, refreshvisibility):
        self._kml['refreshVisibility'] = refreshvisibility

    @property
    def flytoview(self):
        """
        A value of 1 causes Google Earth to fly to the view of the AbstractView.

        Accepts int (0 or 1).

        """
        return self._kml['flyToView']

    @flytoview.setter
    def flytoview(self, flytoview):
        self._kml['flyToView'] = flytoview

    @property
    def link(self):
        """A [Link] class instance, accepts [Link]"""
        if self._kml['Link'] is None:
            self._kml['Link'] = Link()
        return self._kml['Link']

    @link.setter
    def link(self, link):
        self._kml['Link'] = link


class Model(Geometry):
    """
    A 3D object described in a COLLADA file.

    Keyword Arguments:
    name (string)            -- name of placemark (default None)
    visibility (int)         -- whether the feature is shown (default None)
    open (int)               -- whether open or closed in Places (default None)
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
    extrude (int)            -- connect to the ground? (default None)
    altitudemode (string)    -- alt use See [AltitudeMode] (default None)
    gxaltitudemode (string)  -- alt use. See [GxAltitudeMode] (default None)
    location ([Location])    -- coordinates of the origin (default None)
    orientation ([Orientation])-- rotation of a model (default None)
    scale ([Scale])          -- the scale along the axes (default None)
    link ([Link])            -- a [Link] instance (default None)
    resourcemap ([ResourceMap])-- texture mapper (default None)
    extendeddata ([ExtendedData]) -- extra data (default None)

    Properties:
    Same as arguments, with the following additional properties:
    style               -- [Style] (default None)
    stylemap            -- [StyleMap] (default None)
    liststyle           -- [ListStyle] (default None)
    balloonstyle        -- [BalloonStyle] (default None)
    iconstyle           -- [IconStyle] (default None)
    labelstyle          -- [LabelStyle] (default None)
    linestyle           -- [LineStyle] (default None)
    polystyle           -- [PolyStyle] (default None)
    placemark           -- [Placemark] (default [Placemark], read-only)

    """

    def __init__(self,
                 altitudemode=None,
                 gxaltitudemode=None,
                 location=None,
                 orientation=None,
                 scale=None,
                 link=None,
                 resourcemap=None,
                 **kwargs):
        """
        Creates a model element.

        Keyword Arguments:
        name (string)            -- name of placemark (default None)
        visibility (int)         -- whether the feature is shown (default None)
        open (int)               -- whether open or closed in Places (default None)
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
        extrude (int)            -- connect to the ground? (default None)
        altitudemode (string)    -- alt use See [AltitudeMode] (default None)
        gxaltitudemode (string)  -- alt use. See [GxAltitudeMode] (default None)
        location ([Location])    -- coordinates of the origin (default None)
        orientation ([Orientation])-- rotation of a model (default None)
        scale ([Scale])          -- the scale along the axes (default None)
        link ([Link])            -- a [Link] instance (default None)
        resourcemap ([ResourceMap])-- texture mapper (default None)
        extendeddata ([ExtendedData]) -- extra data (default None)

        """
        super(Model, self).__init__(**kwargs)
        self._kml['altitudeMode'] = altitudemode
        self._kml['gx:altitudeMode'] = gxaltitudemode
        self._kml['Location'] = location
        self._kml['Orientation'] = orientation
        self._kml['Scale'] = scale
        self._kml['Link'] = link
        self._kml['ResourceMap'] = resourcemap

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
    def gxaltitudemode(self, gxaltitudemode):
        self._kml['gx:altitudeMode'] = gxaltitudemode

    @property
    def location(self):
        """Position of the origin of the model, accepts [Location]."""
        if self._kml['Location'] is None:
            self._kml['Location'] = Location()
        return self._kml['Location']

    @location.setter
    def location(self, location):
        self._kml['Location'] = location

    @property
    def orientation(self):
        """The rotation on the model, accepts [Orientation]."""
        if self._kml['Orientation'] is None:
            self._kml['Orientation'] = Orientation()
        return self._kml['Orientation']

    @orientation.setter
    def orientation(self, orientation):
        self._kml['Orientation'] = orientation

    @property
    def scale(self):
        """"The scale of the model, accepts [Scale]."""
        if self._kml['Scale'] is None:
            self._kml['Scale'] = Scale()
        return self._kml['Scale']

    @scale.setter
    def scale(self, scale):
        self._kml['Scale'] = scale

    @property
    def link(self):
        """"A [Link] class instance, accepts [Link]."""
        if self._kml['Link'] is None:
            self._kml['Link'] = Link()
        return self._kml['Link']

    @link.setter
    def link(self, link):
        self._kml['Link'] = link

    @property
    def resourcemap(self):
        """Used for mapping textures, accepts [ResourceMap]."""
        if self._kml['ResourceMap'] is None:
            self._kml['ResourceMap'] = ResourceMap()
        return self._kml['ResourceMap']

    @resourcemap.setter
    def resourcemap(self, resourcemap):
        self._kml['ResourceMap'] = resourcemap

    def __str__(self):
        str = '<Model id="{0}">'.format(self._id)
        str += super(Model, self).__str__()
        str += "</Model>"
        return str


class GxTrack(Geometry):
    """
    A track describes how an object moves through the world over a given time period.

    Keyword Arguments:
    name (string)                 -- name of placemark (default None)
    visibility (int)              -- whether the feature is shown (default None)
    open (int)                    -- whether open or closed in Places (default None)
    atomauthor (string)           -- author of the document (default None)
    atomlink (string)             -- URL containing this KML (default None)
    address (string)              -- standard address (default None)
    xaladdressdetails(string)     -- address as xAL (default None)
    phonenumber (string)          -- phone number for Maps mobile (default None)
    snippet ([Snippet])           -- short description of feature (default None)
    description (string)          -- description shown in balloon (default None)
    camera ([Camera])             -- camera that views the scene (default None)
    lookat ([LookAt])             -- camera relative to feature (default None)
    timestamp ([TimeStamp])       -- single moment in time (default None)
    timespan ([TimeSpan])         -- period of time (default None)
    region ([Region])             -- bounding box of features (default None)
    extrude (int)                 -- connect to the ground? (default None)
    altitudemode (string)         -- alt use See [AltitudeMode] (default None)
    gxaltitudemode (string)       -- alt use. See [GxAltitudeMode] (default None)
    extendeddata ([ExtendedData]) -- extra data (default None)

    Properties:
    Same as arguments, with the following additional properties:
    style               -- [Style] (default None)
    stylemap            -- [StyleMap] (default None)
    liststyle           -- [ListStyle] (default None)
    balloonstyle        -- [BalloonStyle] (default None)
    iconstyle           -- [IconStyle] (default None)
    labelstyle          -- [LabelStyle] (default None)
    linestyle           -- [LineStyle] (default None)
    polystyle           -- [PolyStyle] (default None)
    placemark           -- [Placemark] (default [Placemark], read-only)
    whens               -- list of times given (default [])
    angles              -- list of angles given (default [])
    gxcoords            -- list of coords given (default [])

    Public Methods:
    newwhen    -- Attaches new when entry/entries
    newangle   -- Attaches new angle entry/entries
    newgxcoord -- Attaches new gxcoord entry/entries
    newdata    -- Attaches new when, gxcoord and/or angle entry/entries

    """

    def __init__(self,
                 altitudemode=None,
                 gxaltitudemode=None,
                 **kwargs):
        """
        Creates a gx:track element.

        Keyword Arguments:
        name (string)                 -- name of placemark (default None)
        visibility (int)              -- whether the feature is shown (default None)
        open (int)                    -- whether open or closed in Places (default None)
        atomauthor (string)           -- author of the document (default None)
        atomlink (string)             -- URL containing this KML (default None)
        address (string)              -- standard address (default None)
        xaladdressdetails(string)     -- address as xAL (default None)
        phonenumber (string)          -- phone number for Maps mobile (default None)
        snippet ([Snippet])           -- short description of feature (default None)
        description (string)          -- description shown in balloon (default None)
        camera ([Camera])             -- camera that views the scene (default None)
        lookat ([LookAt])             -- camera relative to feature (default None)
        timestamp ([TimeStamp])       -- single moment in time (default None)
        timespan ([TimeSpan])         -- period of time (default None)
        region ([Region])             -- bounding box of features (default None)
        extrude (int)                 -- connect to the ground? (default None)
        altitudemode (string)         -- alt use See [AltitudeMode] (default None)
        gxaltitudemode (string)       -- alt use. See [GxAltitudeMode] (default None)
        location ([Location])         -- coordinates of the origin (default None)
        orientation ([Orientation])   -- rotation of a model (default None)
        scale ([Scale])               -- the scale along the axes (default None)
        link ([Link])                 -- a [Link] instance (default None)
        resourcemap ([ResourceMap])   -- texture mapper (default None)
        extendeddata ([ExtendedData]) -- extra data (default None)

        """
        super(GxTrack, self).__init__(**kwargs)
        self._kml['altitudeMode'] = altitudemode
        self._kml['gx:altitudeMode'] = gxaltitudemode
        self._kml['ExtendedData'] = None
        self.whens = []
        self.gxcoords = []
        self.angles = []

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
    def gxaltitudemode(self, gxaltitudemode):
        self._kml['gx:altitudeMode'] = gxaltitudemode

    def newdata(self, gxcoord, when, angle=None):
        """
        Creates a new gxcoord, when time and angle (if provided).

        This is a convenience method for calling newwhen, newgxcoord and newangle. when and gxcoord are required,
        angle is optional.

        """
        self.newgxcoord(gxcoord)
        self.newwhen(when)
        if angle is not None:
            self.newangle(angle)

    def newwhen(self, when):
        """
        Creates a new when time, accepts string or list of string.

        If one string is given a single when entry is created, but if a list of strings is given, a when entry is
        created for each string in the list.

        """
        if type(when) == list:
            self.whens += when
        else:
            self.whens.append(when)

    def newgxcoord(self, coord):
        """
        Creates a gx:coord, accepts list of one tuples.

        A gxcoord entry is created for every tuple in the list.

        """
        if type(coord) == list:
            for crd in coord:
                coords = Coordinates()
                coords.addcoordinates([crd])
                self.gxcoords.append(coords)
        else:
            coords = Coordinates()
            coords.addcoordinates(list(coord))
            self.gxcoords.append(coords)

    def newangle(self, angle):
        """
        Creates a new angle, accepts float or list of floats.

        If one float is given a single angle entry is created, but if a list of floats is given, a angle entry is
        created for each float in the list.

        """
        if type(angle) == list:
            self.angles += angle
        else:
            self.angles.append(angle)

    @property
    def extendeddata(self):
        """Extra data for the feature."""
        if self._kml['ExtendedData'] is None:
            self._kml['ExtendedData'] = ExtendedData()
        return self._kml['ExtendedData']

    @extendeddata.setter
    def extendeddata(self, extendeddata):
        self._kml['ExtendedData'] = extendeddata

    def __str__(self):
        str = '<gx:Track>'
        for when in self.whens:
            str += "<when>{0}</when>".format(when)
        for angle in self.angles:
            str += "<angle>{0}</angle>".format(angle)
        for gxcoord in self.gxcoords:
            str += "<gx:coord>{0}</gx:coord>".format(gxcoord.__str__().replace(',', ' '))
        str += super(GxTrack, self).__str__()
        str += '</gx:Track>'
        return str



class GxMultiTrack(Geometry):
    """
    A container for grouping gx:tracks.

    Keyword Arguments:
    name (string)            -- name of placemark (default None)
    visibility (int)         -- whether the feature is shown (default None)
    open (int)               -- whether open or closed in Places (default None)
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
    gxinterpolate (int)      -- interpolate values between tracks (default None)
    tracks (list)            -- a list of GxTracks (default ())

    Properties:
    Same as arguments, with the following additional properties:
    style               -- [Style] (default None)
    stylemap            -- [StyleMap] (default None)
    liststyle           -- [ListStyle] (default None)
    balloonstyle        -- [BalloonStyle] (default None)
    iconstyle           -- [IconStyle] (default None)
    labelstyle          -- [LabelStyle] (default None)
    linestyle           -- [LineStyle] (default None)
    polystyle           -- [PolyStyle] (default None)
    placemark           -- [Placemark] (default [Placemark], read-only)

    Public Methods:
    newtrack            -- Creates a [GxTrack]

    """

    def __init__(self,
                 tracks=(), gxinterpolate=None, **kwargs):
        """
        Creates a new gxmultitrack element.

        Keyword Arguments:
        name (string)            -- name of placemark (default None)
        visibility (int)         -- whether the feature is shown (default None)
        open (int)               -- whether open or closed in Places (default None)
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
        gxinterpolate (int)      -- interpolate values between tracks (default None)
        tracks (list)            -- a list of GxTracks (default ())

        """
        super(GxMultiTrack, self).__init__(**kwargs)
        self._kml['gx:interpolate'] = gxinterpolate
        self.tracks = list(tracks)

    def newgxtrack(self, **kwargs):
        """
        Creates a new [GxTrack] and attaches it to this mutlitrack.

        Returns an instance of [GxTrack] class.

        Keyword Arguments:
        Same as [GxTrack], except arguments that are not applicale in a multitrack grouping will be ignored, such as
        name, visibility, open, etc.
        """
        self.tracks.append(GxTrack(**kwargs))
        return self.tracks[-1]

    def __str__(self):
        str = '<gx:MultiTrack id="{0}">'.format(self._id)
        str += super(GxMultiTrack, self).__str__()
        for track in self.tracks:
            str += track.__str__()
        str += "</gx:MultiTrack>"
        return str

