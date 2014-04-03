import os

from simplekml import *

kml = Kml(name='5_overlays')

# GroundOverlay
ground = kml.newgroundoverlay(name='GroundOverlay Test')
ground.icon.href = 'resources/smile.png'
ground.gxlatlonquad.coords = [(18.410524,-33.903972),(18.411429,-33.904171),(18.411757,-33.902944),(18.410850,-33.902767)]
# or
#ground.latlonbox.north = -33.902828
#ground.latlonbox.south = -33.904104
#ground.latlonbox.east =  18.410684
#ground.latlonbox.west =  18.411633
#ground.latlonbox.rotation = -14

# ScreenOverlay
screen = kml.newscreenoverlay(name='ScreenOverlay Test')
screen.icon.href = 'resources/simplekml-logo.png'
screen.overlayxy = OverlayXY(x=0,y=1,xunits=Units.fraction,yunits=Units.fraction)
screen.screenxy = ScreenXY(x=15,y=15,xunits=Units.pixel,yunits=Units.insetpixels)
screen.size.x = -1
screen.size.y = -1
screen.size.xunits = Units.fraction
screen.size.yunits = Units.fraction

# PhotoOverlay
photo = kml.newphotooverlay(name='PhotoOverlay Test')
photo.camera = Camera(longitude=18.410858, latitude=-33.904446, altitude=50, altitudemode=AltitudeMode.clamptoground)
photo.point.coords = [(18.410858,-33.90444)]
photo.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/shapes/camera.png'
photo.icon.href = 'resources/stadium.jpg'
photo.viewvolume = ViewVolume(-25,25,-15,15,1)

kml.save(os.path.splitext(__file__)[0] + ".kml")
kml.savekmz(os.path.splitext(__file__)[0] + ".kmz")