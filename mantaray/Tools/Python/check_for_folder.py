# check to see if folder exists.  If it does then add the date, if not then create it

import os
import datetime


def check_for_folder (path, outfile):
    if not os.path.exists (path):
        os.makedirs (path)
        #print("Just created folder: " + path)
        if (outfile != "NONE"):
            outfile.write ("\nJust created output folder: " + path + "\n")
        folder = path
    else:
        print ("\nOutput folder: " + path + " already exists - appending date/time.")
        #get datetime
        now = datetime.datetime.now ()
        os.makedirs (path + "_" + now.strftime ("%Y-%m-%d_%H_%M_%S"))
        if (outfile != "NONE"):
            outfile.write ("Just created output folder: " + path + "_" + now.strftime ("%Y-%m-%d_%H_%M_%S"))
        folder = path + "_" + now.strftime ("%Y-%m-%d_%H_%M_%S")

    return folder
