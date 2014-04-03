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

class AltitudeMode(object):
    """
    AltitudeMode constants.

    Constants:
    clamptoground       -- string "clampToGround"
    relativetoground    -- string "relativeToGround"
    absolute            -- string "absolute"

    """
    clamptoground = "clampToGround"
    relativetoground = "relativeToGround"
    absolute = "absolute"


class GxAltitudeMode(object):
    """
    gx:AltitudeMode constants.

    Constants:
    clampToSeaFloor     -- string "clampToSeaFloor"
    relativeToSeaFloor  -- string "relativeToSeaFloor"

    """
    clampToSeaFloor  = "clampToSeaFloor "
    relativeToSeaFloor  = "relativeToSeaFloor "


class ColorMode(object):
    """
    ColorMode constants.

    Constants:
    normal              -- string "normal"
    random              -- string "random"

    """
    normal = "normal"
    random = "random"


class DisplayMode(object):
    """
    DisplayMode constants.

    Constants:
    default             -- string "default"
    hide                -- string "hide"

    """
    default = "default"
    hide = "hide"


class ListItemType(object):
    """
    ListItemType constants.

    Constants:
    check               -- string "check"
    radiofolder         -- string "radioFolder"
    checkoffonly        -- string "checkOffOnly"
    checkhidechildren   -- string "checkHideChildren"

    """
    check = "check"
    radiofolder = "radioFolder"
    checkoffonly = "checkOffOnly"
    checkhidechildren = "checkHideChildren"


class State(object):
    """
    State constants.

    Constants:
    open                -- string "open"
    closed              -- string "closed"
    error               -- string "error"
    fetching0           -- string "fetching0"
    fetching1           -- string "fetching1"
    fetching2           -- string "fetching2"

    """
    open = 'open'
    closed = 'closed'
    error = 'error'
    fetching0 = 'fetching0'
    fetching1 = 'fetching1'
    fetching2 = 'fetching2'


class Units(object):
    """
    Units constants.

    Constants:
    pixel               -- string "pixel"
    fraction            -- string "fraction"
    insetpixels         -- string "insetPixels"

    """
    pixel = 'pixel'
    fraction = 'fraction'
    insetpixels = 'insetPixels'


class Shape(object):
    """
    Shape constants.

    Constants:
    rectangle           -- string "rectangle"
    circle              -- string "circle"
    sphere              -- string "sphere"

    """
    rectangle = 'rectangle'
    circle = 'circle'
    sphere = 'sphere'


class GridOrigin(object):
    """
    GridOrigin constants.

    Constants:
    lowerleft           -- string "lowerLeft"
    upperleft           -- string "upperLeft"

    """
    lowerleft = 'lowerLeft'
    upperleft = 'upperLeft'


class RefreshMode(object):
    """
    RefreshMode constants.

    Constants:
    onchange            -- string "onChange"
    oninterval          -- string "onInterval"
    onexpire            -- string "onExpire"

    """
    onchange = 'onChange'
    oninterval = 'onInterval '
    onexpire = 'onExpire'


class ViewRefreshMode(object):
    """
    ViewRefreshMode constants.

    Constants:
    never               -- string "never"
    onstop              -- string "onStop"
    onrequest           -- string "onRequest"
    onregion            -- string "onRegion"

    """
    never  = 'never '
    onstop  = 'onStop '
    onrequest  = 'onRequest '
    onregion  = 'onRegion '


class Types(object):
    """
    Types constants.

    Constants:
    string           -- string "string"
    int              -- string "int"
    uint             -- string "uint"
    short            -- string "short"
    ushort           -- string "ushort"
    float            -- string "float"
    double           -- string "double"
    bool             -- string "bool"

    """
    string = 'string'
    int = 'int'
    uint = 'uint'
    short = 'short'
    ushort = 'ushort'
    float = 'float'
    double = 'double'
    bool = 'bool'


class Color(object):
    """
    Color constants (HTML and CSS) and converters.

    Constants:
    See HTML and CSS standard colors for full list. All constants are lowercase.

    Class Methods:
    rgb(r, g, b, a) -- Convert rgba to GE hex value.
    hex(hstr)       -- Convert hex (without alpha) to GE hex value.
    hexa(hstr)      -- Changes the alpha value of the given Google Earth hex value.
    changealpha(alpha, gehex) -- Changes the alpha value of the given Google Earth hex value.

    """

    @classmethod
    def rgb(cls, r, g, b, a=255):
        """
        Convert rgba to GE hex value.

        Keyword Arguments:
        r (int) -- red
        g (int) -- green
        b (int) -- blue
        a (int) -- alpha (default 255)

        """
        return '%0.2x%0.2x%0.2x%0.2x' % (a, b, g, r)


    @classmethod
    def hex(cls, hstr):
        """
        Convert hex (without alpha) to GE hex value.

        Keyword Arguments:
        hstr (string) -- hex string without alpha value

        """
        return "ff{0}".format(hstr[::-1])


    @classmethod
    def hexa(cls, hstr):
        """
        Convert hex (with alpha) to GE hex value.

        Keyword Arguments:
        hstr (string) -- hex string with alpha value

        """
        return hstr[::-1]

    @classmethod
    def changealpha(cls, alpha, gehex):
        """
        Changes the alpha value of the given Google Earth hex value.

        Keyword Arguments:
        alpha (string) -- aplha hex string
        gehex (string) -- Google Earth hex string

        """
        return alpha + gehex[2:]

    aliceblue = 'fffff8f0'
    antiquewhite = 'ffd7ebfa'
    aqua = 'ffffff00'
    aquamarine = 'ffd4ff7f'
    azure = 'fffffff0'
    beige = 'ffdcf5f5'
    bisque = 'ffc4e4ff'
    black = 'ff000000'
    blanchedalmond = 'ffcdebff'
    blue = 'ffff0000'
    blueviolet = 'ffe22b8a'
    brown = 'ff2a2aa5'
    burlywood = 'ff87b8de'
    cadetblue = 'ffa09e5f'
    chartreuse = 'ff00ff7f'
    chocolate = 'ff1e69d2'
    coral = 'ff507fff'
    cornflowerblue = 'ffed9564'
    cornsilk = 'ffdcf8ff'
    crimson = 'ff3c14dc'
    cyan = 'ffffff00'
    darkblue = 'ff8b0000'
    darkcyan = 'ff8b8b00'
    darkgoldenrod = 'ff0b86b8'
    darkgray = 'ffa9a9a9'
    darkgrey = 'ffa9a9a9'
    darkgreen = 'ff006400'
    darkkhaki = 'ff6bb7bd'
    darkmagenta = 'ff8b008b'
    darkolivegreen = 'ff2f6b55'
    darkorange = 'ff008cff'
    darkorchid = 'ffcc3299'
    darkred = 'ff00008b'
    darksalmon = 'ff7a96e9'
    darkseagreen = 'ff8fbc8f'
    darkslateblue = 'ff8b3d48'
    darkslategray = 'ff4f4f2f'
    darkslategrey = 'ff4f4f2f'
    darkturquoise = 'ffd1ce00'
    darkviolet = 'ffd30094'
    deeppink = 'ff9314ff'
    deepskyblue = 'ffffbf00'
    dimgray = 'ff696969'
    dimgrey = 'ff696969'
    dodgerblue = 'ffff901e'
    firebrick = 'ff2222b2'
    floralwhite = 'fff0faff'
    forestgreen = 'ff228b22'
    fuchsia = 'ffff00ff'
    gainsboro = 'ffdcdcdc'
    ghostwhite = 'fffff8f8'
    gold = 'ff00d7ff'
    goldenrod = 'ff20a5da'
    gray = 'ff808080'
    grey = 'ff808080'
    green = 'ff008000'
    greenyellow = 'ff2fffad'
    honeydew = 'fff0fff0'
    hotpink = 'ffb469ff'
    indianred = 'ff5c5ccd'
    indigo = 'ff82004b'
    ivory = 'fff0ffff'
    khaki = 'ff8ce6f0'
    lavender = 'fffae6e6'
    lavenderblush = 'fff5f0ff'
    lawngreen = 'ff00fc7c'
    lemonchiffon = 'ffcdfaff'
    lightblue = 'ffe6d8ad'
    lightcoral = 'ff8080f0'
    lightcyan = 'ffffffe0'
    lightgoldenrodyellow = 'ffd2fafa'
    lightgray = 'ffd3d3d3'
    lightgrey = 'ffd3d3d3'
    lightgreen = 'ff90ee90'
    lightpink = 'ffc1b6ff'
    lightsalmon = 'ff7aa0ff'
    lightseagreen = 'ffaab220'
    lightskyblue = 'ffface87'
    lightslategray = 'ff998877'
    lightslategrey = 'ff998877'
    lightsteelblue = 'ffdec4b0'
    lightyellow = 'ffe0ffff'
    lime = 'ff00ff00'
    limegreen = 'ff32cd32'
    linen = 'ffe6f0fa'
    magenta = 'ffff00ff'
    maroon = 'ff000080'
    mediumaquamarine = 'ffaacd66'
    mediumblue = 'ffcd0000'
    mediumorchid = 'ffd355ba'
    mediumpurple = 'ffd87093'
    mediumseagreen = 'ff71b33c'
    mediumslateblue = 'ffee687b'
    mediumspringgreen = 'ff9afa00'
    mediumturquoise = 'ffccd148'
    mediumvioletred = 'ff8515c7'
    midnightblue = 'ff701919'
    mintcream = 'fffafff5'
    mistyrose = 'ffe1e4ff'
    moccasin = 'ffb5e4ff'
    navajowhite = 'ffaddeff'
    navy = 'ff800000'
    oldlace = 'ffe6f5fd'
    olive = 'ff008080'
    olivedrab = 'ff238e6b'
    orange = 'ff00a5ff'
    orangered = 'ff0045ff'
    orchid = 'ffd670da'
    palegoldenrod = 'ffaae8ee'
    palegreen = 'ff98fb98'
    paleturquoise = 'ffeeeeaf'
    palevioletred = 'ff9370d8'
    papayawhip = 'ffd5efff'
    peachpuff = 'ffb9daff'
    peru = 'ff3f85cd'
    pink = 'ffcbc0ff'
    plum = 'ffdda0dd'
    powderblue = 'ffe6e0b0'
    purple = 'ff800080'
    red = 'ff0000ff'
    rosybrown = 'ff8f8fbc'
    royalblue = 'ffe16941'
    saddlebrown = 'ff13458b'
    salmon = 'ff7280fa'
    sandybrown = 'ff60a4f4'
    seagreen = 'ff578b2e'
    seashell = 'ffeef5ff'
    sienna = 'ff2d52a0'
    silver = 'ffc0c0c0'
    skyblue = 'ffebce87'
    slateblue = 'ffcd5a6a'
    slategray = 'ff908070'
    slategrey = 'ff908070'
    snow = 'fffafaff'
    springgreen = 'ff7fff00'
    steelblue = 'ffb48246'
    tan = 'ff8cb4d2'
    teal = 'ff808000'
    thistle = 'ffd8bfd8'
    tomato = 'ff4763ff'
    turquoise = 'ffd0e040'
    violet = 'ffee82ee'
    wheat = 'ffb3def5'
    white = 'ffffffff'
    whitesmoke = 'fff5f5f5'
    yellow = 'ff00ffff'
    yellowgreen = 'ff32cd9a'

        
