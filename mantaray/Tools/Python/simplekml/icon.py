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

class Link(Kmlable):
    """
    Defines an image associated with an Icon style or overlay.

    Keyword Arguments:
    href (string)            -- target url (default None)
    refreshmode (string)     -- one of [RefreshMode] constants (default None)
    refreshinterval (float)  -- time between refreshes (default None)
    viewrefreshmode (string) -- one of [ViewRefreshMode] constants(default None)
    viewrefreshtime (float)  -- time to refresh after camera stop (default None)
    viewboundscale (float)   -- extent to request (default None)
    viewformat (string)      -- query string format (default None)
    httpquery (string)       -- extra info for query string (default None)

    Properties:
    Same as arguments.

    """

    def __init__(self,
                 href=" ",
                 refreshmode=None,
                 refreshinterval=None,
                 viewrefreshmode=None,
                 viewrefreshtime=None,
                 viewboundscale=None,
                 viewformat=None,
                 httpquery=None):
        """
        Creates a link element.

        Keyword Arguments:
        href (string)           -- target url (default None)
        refreshmode (string)    -- one of [RefreshMode] constants (default None)
        refreshinterval (float) -- time between refreshes (default None)
        viewrefreshmode (string)-- [ViewRefreshMode] constants(default None)
        viewrefreshtime (float) -- time to refresh after camera (default None)
        viewboundscale (float)  -- extent to request (default None)
        viewformat (string)     -- query string format (default None)
        httpquery (string)      -- extra info for query string (default None)

        """
        super(Link, self).__init__()
        self._kml["href"] = href
        self._kml["refreshMode"] = refreshmode
        self._kml["refreshInterval"] = refreshinterval
        self._kml["viewRefreshMode"] = viewrefreshmode
        self._kml["viewRefreshTime"] = viewrefreshtime
        self._kml["viewBoundScale"] = viewboundscale
        self._kml["viewFormat"] = viewformat
        self._kml["httpQuery"] = httpquery
        
    @property
    def href(self):
        """Target url, accepts string."""
        return self._kml['href']
    
    @href.setter
    def href(self, href):
        self._kml['href'] = href

    @property
    def refreshmode(self):
        """Type of refresh, accepts string of [RefreshMode] constants."""
        return self._kml['refreshMode']

    @refreshmode.setter
    def refreshmode(self, refreshmode):
        self._kml['refreshMode'] = refreshmode

    @property
    def refreshinterval(self):
        """Time between refreshed, accepts float."""
        return self._kml['refreshInterval']

    @refreshinterval.setter
    def refreshinterval(self, refreshinterval):
        self._kml['refreshInterval'] = refreshinterval

    @property
    def viewrefreshmode(self):
        """Camera specific refresh, accepts [ViewRefreshMode] constants."""
        return self._kml['viewRefreshMode']

    @viewrefreshmode.setter
    def viewrefreshmode(self, viewrefreshmode):
        self._kml['viewRefreshMode'] = viewrefreshmode

    @property
    def viewrefreshtime(self):
        """Camera specific refresh time, accepts float."""
        return self._kml['viewRefreshTime']

    @viewrefreshtime.setter
    def viewrefreshtime(self, viewrefreshtime):
        self._kml['viewRefreshTime'] = viewrefreshtime

    @property
    def viewboundscale(self):
        """Extent to request from server, accepts float."""
        return self._kml['viewBoundScale']

    @viewboundscale.setter
    def viewboundscale(self, viewboundscale):
        self._kml['viewBoundScale'] = viewboundscale

    @property
    def viewformat(self):
        """Format of the query string, accepts string."""
        return self._kml['viewFormat']

    @viewformat.setter
    def viewformat(self, viewformat):
        self._kml['viewFormat'] = viewformat

    @property
    def httpquery(self):
        """Extra information to append to the query string, accepts string."""
        return self._kml['httpQuery']

    @httpquery.setter
    def httpquery(self, httpquery):
        self._kml['httpQuery'] = httpquery


class Icon(Link):
    """
    Defines an image associated with an Icon style or overlay.

    Keyword Arguments:
    href (string)            -- target url (default None)
    refreshmode (string)     -- one of [RefreshMode] constants (default None)
    refreshinterval (float)  -- time between refreshes (default None)
    viewrefreshmode (string) -- one of [ViewRefreshMode] constants(default None)
    viewrefreshtime (float)  -- time to refresh after camera stop (default None)
    viewboundscale (float)   -- extent to request (default None)
    viewformat (string)      -- query string format (default None)
    httpquery (string)       -- extra info for query string (default None)
    gxx (int)                -- x position of icon palette (default None)
    gxy (int)                -- y position of icon palette (default None)
    gxh (int)                -- height of icon palette (default None)
    gxw (int)                -- width of icon palette (default None)

    Properties:
    Same as arguments.

    """

    def __init__(self,
                 gxx=None,
                 gxy=None,
                 gxw=None,
                 gxh=None,
                 **kwargs):
        """
        Creates a icon element.

        Keyword Arguments:
        href (string)            -- target url (default None)
        refreshmode (string)     -- one of [RefreshMode] constants (default None)
        refreshinterval (float)  -- time between refreshes (default None)
        viewrefreshmode (string) -- one of [ViewRefreshMode] constants(default None)
        viewrefreshtime (float)  -- time to refresh after camera stop (default None)
        viewboundscale (float)   -- extent to request (default None)
        viewformat (string)      -- query string format (default None)
        httpquery (string)       -- extra info for query string (default None)
        gxx (int)                -- x position of icon palette (default None)
        gxy (int)                -- y position of icon palette (default None)
        gxh (int)                -- height of icon palette (default None)
        gxw (int)                -- width of icon palette (default None)

        """
        super(Icon, self).__init__(**kwargs)
        self._kml["gx:x"] = gxx
        self._kml["gx:y"] = gxy
        self._kml["gx:w"] = gxw
        self._kml["gx:h"] = gxh
        
    @property
    def gxx(self):
        """x position of icon palette, accpets int."""
        return self._kml['gx:x']

    @gxx.setter
    def gxx(self, gxx):
        self._kml['gx:x'] = gxx

    @property
    def gxy(self):
        """y position of icon palette, accpets int."""
        return self._kml['gx:y']

    @gxy.setter
    def gxy(self, gxy):
        self._kml['gx:y'] = gxy

    @property
    def gxw(self):
        """Width of icon palette, accpets int."""
        return self._kml['gx:w']

    @gxw.setter
    def gxw(self, gxw):
        self._kml['gx:w'] = gxw

    @property
    def gxh(self):
        """Height of icon palette, accpets int."""
        return self._kml['gx:h']

    @gxh.setter
    def gxh(self, gxh):
        self._kml['gx:h'] = gxh



class ItemIcon(Kmlable):
    """
    Defines an image associated with an Icon style or overlay.

    Keyword Arguments:
    href (string)  -- URL of the image (default None)
    state (string) -- string from [State] constants (default None)

    Properties:
    Same as arguments.

    """

    def __init__(self, state=None, href=None):
        """
        Creates a itemicon element.

        Keyword Arguments:
        href (string)  -- URL of the image (default None)
        state (string) -- string from [State] constants (default None)

        """
        super(ItemIcon, self).__init__()
        self._kml["href"] = href
        self._kml["state"] = state

    @property
    def href(self):
        """URL of the image used in List View for Feature, accepts string."""
        return self._kml['href']

    @href.setter
    def href(self, href):
        self._kml['href'] = href

    @property
    def state(self):
        """Current state of the link, accepts string from [State] constants."""
        return self._kml['state']

    @state.setter
    def state(self, state):
        self._kml['state'] = state
