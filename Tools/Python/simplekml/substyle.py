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

from simplekml.base import Kmlable, HotSpot
from simplekml.constants import *
from simplekml.icon import Icon, ItemIcon

class ColorStyle(Kmlable):
    """_A base class for geometry styles."""

    def __init__(self, color=None, colormode=ColorMode.normal):
        super(ColorStyle, self).__init__()
        self._kml["color"] = color
        self._kml["colorMode"] = colormode

    @property
    def color(self):
        """Hex string representing a color, accepts string."""
        return self._kml['color']

    @color.setter
    def color(self, color):
        self._kml['color'] = color

    @property
    def colormode(self):
        """How the color is to be used, string from [ColorMode] constants."""
        return self._kml["colorMode"]

    @colormode.setter
    def colormode(self, colormode):
        self._kml["colorMode"] = colormode


class LineStyle(ColorStyle):
    """
    Specifies the drawing style for all line geometry.

    Keyword Arguments:
    color (string)         -- string of KML hex value (default None)
    colormode (string)     -- string [ColorMode] constants (default "normal")
    width (float)          -- width of the line (default None)
    gxoutercolor (string)  -- string [ColorMode] constants (default "normal")
    gxouterwidth (float)   -- width of the line (default None)
    gxphysicalwidth (float)-- physical width (default None)

    Properties:
    Same as arguments.

    """

    def __init__(self,
                 width=None,
                 gxoutercolor=None,
                 gxouterwidth=None,
                 gxphysicalwidth=None,
                 **kwargs):
        """
        Creates a linestyle element.

        Keyword Arguments:
        color (string)         -- string of KML hex value (default None)
        colormode (string)     -- string [ColorMode] constants(default "normal")
        width (float)          -- width of the line (default None)
        gxoutercolor (string)  -- string [ColorMode] constants(default "normal")
        gxouterwidth (float)   -- width of the line (default None)
        gxphysicalwidth (float)-- physical width (default None)

        """
        super(LineStyle, self).__init__(**kwargs)
        self._kml["width"] = width
        self._kml["gx:outerColor"] = gxoutercolor
        self._kml["gx:outerWidth"] = gxouterwidth
        self._kml["gx:physicalWidth"] = gxphysicalwidth

    @property
    def width(self):
        """Width of the line, accepts float."""
        return self._kml['width']

    @width.setter
    def width(self, width):
        self._kml['width'] = width

    @property
    def gxoutercolor(self):
        """Outer color of the line, accepts string."""
        return self._kml["gx:outerColor"]

    @gxoutercolor.setter
    def gxoutercolor(self, gxoutercolor):
        self._kml["gx:outerColor"] = gxoutercolor

    @property
    def gxouterwidth(self):
        """Outer width of the line, accepts float."""
        return self._kml["gx:outerWidth"]

    @gxouterwidth.setter
    def gxouterwidth(self, gxouterwidth):
        self._kml["gx:outerWidth"] = gxouterwidth

    @property
    def gxphysicalwidth(self):
        """Physical width of the line, accepts float."""
        return self._kml["gx:physicalWidth"]

    @gxphysicalwidth.setter
    def gxphysicalwidth(self, gxphysicalwidth):
        self._kml["gx:physicalWidth"] = gxphysicalwidth


class PolyStyle(ColorStyle):
    """
    Specifies the drawing style for all polygons.

    Keyword Arguments:
    color (string)      -- string of KML hex value (default None)
    colormode (string)  -- string [ColorMode] constants(default "normal")
    fill (int)          -- filled polygon 1 or 0 (default 1)
    outline (int)       -- outlined polygon 1 or 0 (default 1)

    Properties:
    Same as arguments.

    """

    def __init__(self, fill=1, outline=1, **kwargs):
        """
        Creates a poltstyle element.

        Keyword Arguments:
        color (string)      -- string of KML hex value (default None)
        colormode (string)  -- string [ColorMode] constants(default "normal")
        fill (int)          -- filled polygon 1 or 0 (default 1)
        outline (int)       -- outlined polygon 1 or 0 (default 1)

        """
        super(PolyStyle, self).__init__(**kwargs)
        self._kml["fill"] = fill
        self._kml["outline"] = outline

    @property
    def fill(self):
        """Must the polygon be filled, accepts int of 0 or 1."""
        return self._kml['fill']

    @fill.setter
    def fill(self, fill):
        self._kml['fill'] = fill

    @property
    def outline(self):
        """Must the polygon be outlined, accepts int of 0 or 1."""
        return self._kml['outline']

    @outline.setter
    def outline(self, outline):
        self._kml['outline'] = outline


class IconStyle(ColorStyle):
    """
    Specifies how icons for point Placemarks are drawn.

    Keyword Arguments:
    color (string)      -- string of KML hex value (default None)
    colormode (string)  -- string [ColorMode] constants(default "normal")
    scale (float)       -- size of the icon (default 1)
    heading (float)     -- rotation of the icon (default 0)
    icon ([Icon])       -- the [Icon] (default [Icon])
    hotspot ([Hotspot]) -- the [HotSpot] (default None)

    Properties:
    Same as arguments.

    """

    def __init__(self, scale=1, heading=0, icon=None, hotspot=None, **kwargs):
        """
        Creates a iconstyle element.

        Keyword Arguments:
        color (string)      -- string of KML hex value (default None)
        colormode (string)  -- string [ColorMode] constants(default "normal")
        scale (float)       -- size of the icon (default 1)
        heading (float)     -- rotation of the icon (default 0)
        icon ([Icon])       -- the [Icon] (default [Icon])
        hotspot ([Hotspot]) -- the [HotSpot] (default None)

        """
        super(IconStyle, self).__init__(**kwargs)
        if icon is None:
            icon = Icon(href="http://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png")
        self._kml["scale"] = scale
        self._kml["heading"] = heading
        self._kml["Icon"] = icon
        self._kml["hotspot_"] = hotspot

    @property
    def scale(self):
        """Size of the icon, accepts float."""
        return self._kml['scale']

    @scale.setter
    def scale(self, scale):
        self._kml['scale'] = scale

    @property
    def heading(self):
        """Rotation of the icon, accepts float."""
        return self._kml['heading']

    @heading.setter
    def heading(self, heading):
        self._kml['heading'] = heading

    @property
    def icon(self):
        """The actual [Icon] to be displayed, accepts [Icon]."""
        return self._kml["Icon"]

    @icon.setter
    def icon(self, icon):
        self._kml["Icon"] = icon

    @property
    def hotspot(self):
        """Anchor position inside of the icon, accepts [HotSpot]."""
        if self._kml["hotspot_"] is None:
            self._kml["hotspot_"] = HotSpot()
        return self._kml["hotspot_"]

    @hotspot.setter
    def hotspot(self, hotspot):
        self._kml["hotspot_"] = hotspot


class LabelStyle(ColorStyle):
    """
    Specifies how the name of a Feature is drawn.

    Keyword Arguments:
    color (string)      -- string of KML hex value (default None)
    colormode (string)  -- string [ColorMode] constants(default "normal")
    scale (float)       -- size of the icon (default 1)

    Properties:
    Same as arguments.

    """

    def __init__(self, scale=1, **kwargs):
        """
        Creates a labelstyle element.

        Keyword Arguments:
        color (string)      -- string of KML hex value (default None)
        colormode (string)  -- string [ColorMode] constants(default "normal")
        scale (float)       -- size of the icon (default 1)

        """
        super(LabelStyle, self).__init__(**kwargs)
        self._kml["scale"] = scale

    @property
    def scale(self):
        """Size of the icon, accepts float."""
        return self._kml['scale']

    @scale.setter
    def scale(self, scale):
        self._kml['scale'] = scale


class BalloonStyle(Kmlable):
    """
    Specifies the content and layout of the description balloon.

    Keyword Arguments:
    bgcolor (string)     -- background color hex value (default None)
    textcolor (string)   -- text color  hex value (default None)
    text (string)        -- the actual text (default None)
    displaymode (string) -- string [DisplayMode] constants (default "default")

    Properties:
    Same as arguments.

    """

    def __init__(self,
                 bgcolor=None,
                 textcolor=None,
                 text=None,
                 displaymode=DisplayMode.default):
        """
        Creates a balloonstyle element.

        Keyword Arguments:
        bgcolor (string)     -- background color hex value (default None)
        textcolor (string)   -- text color  hex value (default None)
        text (string)        -- the actual text (default None)
        displaymode (string) -- string [DisplayMode] constants (default "default")

        """
        super(BalloonStyle, self).__init__()
        self._kml["bgColor"] = bgcolor
        self._kml["textColor"] = textcolor
        self._kml["text"] = text
        self._kml["displayMode"] = displaymode

    @property
    def bgcolor(self):
        """Background color of the balloon, accepts hex string."""
        return self._kml["bgColor"]

    @bgcolor.setter
    def bgcolor(self, bgcolor):
        self._kml["bgColor"] = bgcolor

    @property
    def textcolor(self):
        """Text color in the balloon, accepts hex string."""
        return self._kml["textColor"]

    @textcolor.setter
    def textcolor(self, textcolor):
        self._kml["textColor"] = textcolor

    @property
    def text(self):
        """The actual text that will appear in the balloon, accepts string."""
        return self._kml['text']

    @text.setter
    def text(self, text):
        self._kml['text'] = text

    @property
    def displaymode(self):
        """How the balloon is tyo be displayed, accepts string from [DisplayMode] constants."""
        return self._kml["displayMode"]
    
    
    @displaymode.setter
    def displaymode(self, displaymode):
        self._kml["displayMode"] = displaymode


class ListStyle(Kmlable):
    """
    Specifies the display of the elements style in the navigation bar.

    Keyword Arguments:
    listitemtype (string) -- string from [ListItemType] constants (default "check")
    bgcolor (string)      -- background color hex value (default None)
    itemicon ([ItemIcon]) -- an [ItemIcon] instance (default None)

    Properties:
    Same as arguments.

    """

    def __init__(self,
                 listitemtype=ListItemType.check,
                 bgcolor=None,
                 itemicon=None):
        """
        Creates a liststyle element.

        Keyword Arguments:
        listitemtype (string) -- string from [ListItemType] constants (default "check")
        bgcolor (string)      -- background color hex value (default None)
        itemicon ([ItemIcon]) -- an [ItemIcon] instance (default None)

        """
        super(ListStyle, self).__init__()
        self._kml["listItemType"] = listitemtype
        self._kml["bgColor"] = bgcolor
        self._kml["ItemIcon"] = itemicon

    @property
    def itemicon(self):
        """An instance of an [ItemIcon] class, accepts [ItemIcon]."""
        if self._kml["ItemIcon"] is None:
            self._kml["ItemIcon"] = ItemIcon()
        return self._kml["ItemIcon"]

    @itemicon.setter
    def itemicon(self, itemicon):
        self._kml["ItemIcon"] = itemicon

    @property
    def listitemtype(self):
        """How an item is diaplyed, accepts string from [ListItemType] constants."""
        return self._kml["listItemType"]

    @listitemtype.setter
    def listitemtype(self, listitemtype):
        self._kml["listItemType"] = listitemtype

    @property
    def bgcolor(self):
        """The background color of the item, accepts a hex string."""
        return self._kml["bgColor"]

    @bgcolor.setter
    def bgcolor(self, bgcolor):
        self._kml["bgColor"] = bgcolor