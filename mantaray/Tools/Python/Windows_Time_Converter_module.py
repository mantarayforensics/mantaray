
##########################COPYRIGHT INFORMATION############################
# Copyright (C) 2014 webmaster@mantarayforensics.com 					  #
# This program is free software: you can redistribute it and/or modify    #
# it under the terms of the GNU General Public License as published by    #
# the Free Software Foundation, either version 3 of the License, or       #
# (at your option) any later version.                                     #
#                                                                         #
# This program is distributed in the hope that it will be useful,         #
# but WITHOUT ANY WARRANTY; without even the implied warranty of          #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the           #
# GNU General Public License for more details.                            #
#                                                                         #
# You should have received a copy of the GNU General Public License       #
# along with this program.  If not, see http://www.gnu.org/licenses/.     #
##########################COPYRIGHT INFORMATION############################

import datetime

def Windows_Time_Converter_module(dt):
    print(dt)
    microseconds = int(dt, 16) / 10
    seconds, microseconds = divmod(microseconds, 1000000)
    days, seconds = divmod(seconds, 86400)

    #return datetime.datetime(1601, 1, 1) + datetime.timedelta(days, seconds, microseconds)
    time = datetime.datetime(1601, 1, 1) + datetime.timedelta(days, seconds, microseconds)
    #print(time)
    #print format(getFiletime(time), '%a, %d %B %Y %H:%M:%S %Z')

    return time
