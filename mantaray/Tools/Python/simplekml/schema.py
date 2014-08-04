from simplekml.base import Kmlable

class SimpleField(Kmlable):
    """
    Custom field, forms part of a schema.

    Keyword Arguments:
    name (string)        -- name of field (required)
    type (string)        -- type of field (default "string")
    displayname (string) -- alternative name (default None)

    Properties:
    Same as arguments.

    """

    def __init__(self, name=None, type='string', displayname=None):
        """
        Creates a simplefield.

        Keyword Arguments:
        name (string)        -- name of field (default None)
        type (string)        -- base type of field (default "string")
        displayname (string) -- alternative name (default None)
        """
        super(SimpleField, self).__init__()
        self._kml['name'] = name
        self._kml['type'] = type
        self._kml['displayName'] = displayname

    @property
    def name(self):
        """Name of field, accepts string."""
        return self._kml['name']

    @name.setter
    def name(self, name):
        self._kml['name'] = name

    @property
    def type(self):
        """Type of field, accepts string from [Types] constants."""
        return self._kml['type']

    @type.setter
    def type(self, type):
        self._kml['type'] = type

    @property
    def displayname(self):
        """Pretty name of field that is shown in google earth, accepts string."""
        return self._kml['displayName']

    @displayname.setter
    def displayname(self, displayname):
        self._kml['displayName'] = displayname

    def __str__(self):
        str = '<SimpleField type="{0}" name="{1}">'.format(self.type, self.name)
        if self.displayname is not None:
            str += '<displayName>{0}</displayName>'.format(self.displayname)
        str += '</SimpleField>'
        return str


class GxSimpleArrayField(SimpleField):
    """
    Custom array field for gx:track, forms part of a schema.

    Keyword Arguments:
    name (string)        -- name of field (required)
    type (string)        -- type of field (default "string")
    displayname (string) -- alternative name (default None)

    Properties:
    Same as arguments.

    """

    def __init__(self, name=None, type='string', displayname=None):
        """
        Creates a gx:simplearrayfield.

        Keyword Arguments:
        name (string)        -- name of field (default None)
        type (string)        -- base type of field (default "string")
        displayname (string) -- alternative name (default None)
        """
        super(GxSimpleArrayField, self).__init__(name, type, displayname)

    def __str__(self):
        str = '<gx:SimpleArrayField type="{0}" name="{1}">'.format(self.type, self.name)
        if self.displayname is not None:
            str += '<displayName>{0}</displayName>'.format(self.displayname)
        str += '</gx:SimpleArrayField>'
        return str


class SimpleData(Kmlable):
    """
    Data of a schema.

    Keyword Arguments:
    name (string)              -- name of field from schema (required)
    value (int, float, string) -- value of field (default None)

    Properties:
    Same as arguments.

    """

    def __init__(self, name, value):
        """
        Creates simpledata.

        Keyword Arguments:
        name (string)              -- name of field from schema (required)
        value (int, float, string) -- value of field (required)
        """
        super(SimpleData, self).__init__()
        self._kml['name'] = name
        self._kml['value'] = value

    @property
    def name(self):
        """Name of field, accepts string."""
        return self._kml['name']

    @name.setter
    def name(self, name):
        self._kml['name'] = name

    @property
    def value(self):
        """Value of field, accepts int, float or string."""
        return self._kml['value']

    @value.setter
    def value(self, value):
        self._kml['value'] = value

    def __str__(self):
        str = '<SimpleData name="{0}">{1}</SimpleData>'.format(self.name, self.value)
        return str


class GxSimpleArrayData(Kmlable):
    """
    Data of a [GxSimpleArrayField].

    Keyword Arguments:
    name (string) -- name of array field from schema (required)
    values (list) -- values of the array field (default None)

    Properties:
    Same as arguments.

    Public Methods:
    newvalue            -- Adds a value to the gxsimpledarraydata
    """

    def __init__(self, name, values=None):
        """
        Creates gxsimplearraydata.

        Keyword Arguments:
        name (string) -- name of field from schema (required)
        values (list) -- values of the array field (default None)
        """
        super(GxSimpleArrayData, self).__init__()
        self._kml['name'] = name
        self.values = []
        if values is not None:
            self.values += values

    @property
    def name(self):
        """Name of field, accepts string."""
        return self._kml['name']

    @name.setter
    def name(self, name):
        self._kml['name'] = name

    def newvalue(self, value):
        """Adds a value to the gxsimpledarraydata."""
        self.values.append(value)

    def __str__(self):
        str = '<gx:SimpleArrayData name="{0}">'.format(self.name)
        for value in self.values:
            str += "<gx:value>{0}</gx:value>".format(value)
        str += "</gx:SimpleArrayData>"
        return str



class Schema(Kmlable):
    """
    Custom KML schema that is used to add custom data to KML Features.

    Keyword Arguments:
    name (string) -- name of schema (default None)

    Properties:
    Same as arguments, with the following additional properties:
    id                   -- unique id of the schema
    simplefields         -- returns a list of [SimpleField]s
    gxsimplearrayfields  -- returns a list of [GxSimpleArrayFields]s

    Public Methods:
    newsimplefield            -- Creates a [SimpleField]
    newgxsimplearrayfield     -- Creates a [GxSimpleArrayField]

    """

    _id = 0
    def __init__(self, name=None):
        """
        Creates a schema.

        Keyword Arguments:
        name (string) -- name of schema (default None)
        """
        self._id = "schema_{0}".format(Schema._id + 1)
        Schema._id += 1
        super(Schema, self).__init__()
        self._kml['name'] = name
        self.simplefields = []
        self.gxsimplearrayfields = []

    @property
    def id(self):
        """Unique id of the schema."""
        return self._id

    @property
    def name(self):
        """Name of schema, accepts string."""
        return self._kml['name']

    @name.setter
    def name(self, name):
        self._kml['name'] = name

    def newsimplefield(self, name, type, displayname=None):
        """
        Creates a new [SimpleField] and attaches it to this schema.

        Returns an instance of [SimpleField] class.

        Keyword Arguments:
        name (string)        -- name of simplefield (required)
        type (string)        -- type of field (required)
        displayname (string) -- pretty name that will be displayed (default None)
        """
        self.simplefields.append(SimpleField(name, type, displayname))
        return self.simplefields[-1]

    def newgxsimplearrayfield(self, name, type, displayname=None):
        """
        Creates a new [GxSimpleArrayField] and attaches it to this schema.

        Returns an instance of [GxSimpleArrayField] class.

        Keyword Arguments:
        name (string)        -- name of simplefield (required)
        type (string)        -- type of field (required)
        displayname (string) -- pretty name that will be displayed (default None)
        """
        self.gxsimplearrayfields.append(GxSimpleArrayField(name, type, displayname))
        return self.gxsimplearrayfields[-1]

    def __str__(self):
        str = '<Schema name="{0}" id="{1}">'.format(self.name, self._id)
        for field in self.simplefields:
            str += field.__str__()
        for field in self.gxsimplearrayfields:
            str += field.__str__()
        str += '</Schema>'
        return str



class Data(Kmlable):
    """
    Data of extended data used to add custom data to KML Features.

    Keyword Arguments:
    schemaurl (string) -- url of a schema (default None)
    """

    def __init__(self, name=None, value=None, displayname=None):
        """
        Creates a data element.

        Keyword Arguments:
        name (string)            -- name of the data (default None)
        value (int, float,string)-- value of the data (default None)
        displayname (string)     -- pretty name that will be displayed (default None)
        """
        super(Data, self).__init__()
        self._kml['name'] = name
        self._kml['value'] = value
        self._kml['displayName'] = displayname

    @property
    def name(self):
        """Data name, accepts string."""
        return self._kml['name']

    @name.setter
    def name(self, name):
        self._kml['name'] = name

    @property
    def value(self):
        """Data value, accepts string."""
        return self._kml['value']

    @value.setter
    def value(self, value):
        self._kml['value'] = value

    @property
    def displayname(self):
        """The name that is displayed to the user, accepts string."""
        return self._kml['displayName']

    @displayname.setter
    def displayname(self, displayname):
        self._kml['displayName'] = displayname

    def __str__(self):
        str = '<Data name="{0}">'.format(self.name)
        if self._kml['value'] is not None:
            str += "<value>{0}</value>".format(self._kml['value'])
        if self._kml['displayName'] is not None:
            str += "<displayName>{0}</displayName>".format(self._kml['displayName'])
        str += '</Data>'
        return str



class SchemaData(Kmlable):
    """
    Data of a schema that is used to add custom data to KML Features.

    Keyword Arguments:
    schemaurl (string) -- url of a schema (default None)
    """

    _id = 0
    def __init__(self, schemaurl=None):
        """
        Creates a schema.

        Keyword Arguments:
        name (string) -- name of schema (required)
        """
        super(SchemaData, self).__init__()
        self.simpledatas = []
        self.gxsimplearraydatas = []

    @property
    def schemaurl(self):
        """Schema url, accepts string."""
        return '#{0}'.format(self._kml['schemaUrl'])

    @schemaurl.setter
    def schemaurl(self, schemaurl):
        self._kml['schemaUrl'] = schemaurl

    def newsimpledata(self, name, value):
        """
        Creates a new [SimpleData] and attaches it to this schemadata.

        Returns an instance of [SimpleData] class.

        Keyword Arguments:
        name (string)                     -- name of simplefield (required)
        value (int, float, string)        -- value of field (required)
        """
        self.simpledatas.append(SimpleData(name, value))
        return self.simpledatas[-1]

    def newgxsimplearraydata(self, name, value):
        """
        Creates a new [GxSimpleArrayData] and attaches it to this schemadata.

        Returns an instance of [GxSimpleArrayData] class.

        Keyword Arguments:
        name (string)                     -- name of gx:simplearrayfield (required)
        value (int, float, string)        -- value of field (required)
        """
        self.gxsimplearraydatas.append(GxSimpleArrayData(name, value))
        return self.gxsimplearraydatas[-1]

    def __str__(self):
        str = '<SchemaData schemaUrl="{0}">'.format(self.schemaurl)
        for field in self.simpledatas:
            str += field.__str__()
        for field in self.gxsimplearraydatas:
            str += field.__str__()
        str += '</SchemaData>'
        return str



class ExtendedData(Kmlable):
    """
    Data of a schema that is used to add custom data to KML Features.

    Keyword Arguments:
    schemaurl (string) -- url of a schema (default None)
    """

    def __init__(self):
        """
        Creates an extendeddata.
        """
        super(ExtendedData, self).__init__()
        self._kml['schemaData_'] = None
        self.datas = []

    @property
    def schemadata(self):
        """Extra data for the feature."""
        if self._kml['schemaData_'] is None:
            self._kml['schemaData_'] = SchemaData()
        return self._kml['schemaData_']

    @schemadata.setter
    def schemadata(self, schemadata):
        self._kml['schemaData_'] = schemadata

    def newdata(self, name, value, displayname=None):
        """
        Creates a new [Data] and attaches it to this schemadata.

        Returns an instance of [Data] class.

        Keyword Arguments:
        name (string)             -- name of simplefield (required)
        value (int, float, string)-- value of field (required)
        displayname (string)      -- pretty name that will be displayed (default None)
        """
        self.datas.append(Data(name, value, displayname))
        return self.datas[-1]

    def __str__(self):
        str = ''
        for data in self.datas:
            str += data.__str__()
        if self._kml['schemaData_'] is not None:
            str += self._kml['schemaData_'].__str__()
        return str