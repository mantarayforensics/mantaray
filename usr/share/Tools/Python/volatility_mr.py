#!/usr/bin/env python3
# This program runs Volatility 2.3 modules against either a RAM image or decompressed hiberfil.sys file

#import modules
import os
from os.path import join
import re
import io
import sys
import string
import subprocess

from easygui import *
from check_for_folder import *


def volatility_mr (case_number, root_folder_path, evidence, profile_to_use):
    print ("The case_name is: " + case_number)
    print ("The output folder is: " + root_folder_path)
    print ("The evidence to process is: " + evidence)

    #create output folder path
    folder_path = root_folder_path + "/" + "Volatility"
    check_for_folder (folder_path, "NONE")

    #open a log file for output
    log_file = folder_path + "/Volatility_logfile.txt"
    outfile = open (log_file, 'wt+')

    Image_Path = evidence

    #add quotes to image path in case of spaces
    quoted_path = "'" + Image_Path + "'"

    #allow user to use pre-selected profile name
    if profile_to_use == "NOPROFILESELECTED":

        #run first volatility command to get image type
        print ("Checking RAM image for imageinfo information...This may take a few minutes....\n")
        imageinfo = subprocess.check_output (["vol -f " + quoted_path + " imageinfo"], shell=True,
                                             universal_newlines=True)
        print ("The value of imageinfo is: " + imageinfo)
        outfile.write ("The value of imageinfo is: " + imageinfo)

        #have user specify the image type
        profile_type = enterbox (msg="Please Enter the profile to use", title='Profile Type', default='', strip=True,
                                 image=None, root=None)

        print ("Profile selected: " + profile_type)

    else:
        print ("Using profile " + profile_to_use)
        profile_type = profile_to_use

    #run kdbgscan
    print (
        "\n\n[1 of 40] Running kdbgscan.\nSee Volatility Commands reference data ("
        "/usr/share/mantaray/docs/VolatilityUsage23.rst) for more information\n")
    kdbgscan_command = "vol --profile=" + profile_type + " -f " + quoted_path + " kdbgscan > " + "'" + folder_path + \
                       "/" + case_number + "_kdbgscan.txt" + "'"
    subprocess.call ([kdbgscan_command], shell=True)

    #run kprcscan
    #print("Running kprcscan.\nSee Volatility Commands reference data (
    # /usr/share/mantaray/docs/VolatilityUsage23.rst) for more information\n")
    #kprcscan_command = "vol --profile=" + profile_type + " -f " + quoted_path + " kprcscan > " + "'"+folder_path +
    # "/" + case_number + "_kprcscan.txt"+"'"
    #subprocess.call([kprcscan_command], shell=True)

    #run pslist
    print (
        "\n\n[2 of 40] Running pslist.\nSee Volatility Commands reference data ("
        "/usr/share/mantaray/docs/VolatilityUsage23.rst) for more information\n")
    pslist_command = "vol --profile=" + profile_type + " -f " + quoted_path + " pslist > " + "'" + folder_path + "/" \
                     + case_number + "_pslist.txt" + "'"
    subprocess.call ([pslist_command], shell=True)

    #run pstree
    print (
        "\n\n[3 of 40] Running pstree.\nSee Volatility Commands reference data ("
        "/usr/share/mantaray/docs/VolatilityUsage23.rst) for more information\n")
    pstree_command = "vol --profile=" + profile_type + " -f " + quoted_path + " pstree > " + "'" + folder_path + "/" \
                     + case_number + "_pstree.txt" + "'"
    subprocess.call ([pstree_command], shell=True)

    #run psscan
    print (
        "\n\n[4 of 40] Running psscan.\nSee Volatility Commands reference data ("
        "/usr/share/mantaray/docs/VolatilityUsage23.rst) for more information\n")
    psscan_command = "vol --profile=" + profile_type + " -f " + quoted_path + " psscan > " + "'" + folder_path + "/" \
                     + case_number + "_psscan.txt" + "'"
    subprocess.call ([psscan_command], shell=True)

    #run dlllist
    print (
        "\n\n[5 of 40] Running dlllist.\nSee Volatility Commands reference data ("
        "/usr/share/mantaray/docs/VolatilityUsage23.rst) for more information\n")
    dlllist_command = "vol --profile=" + profile_type + " -f " + quoted_path + " dlllist > " + "'" + folder_path + \
                      "/" + case_number + "_dlllist.txt" + "'"
    subprocess.call ([dlllist_command], shell=True)

    #run handles
    print (
        "\n\n[6 of 40] Running handles.\nSee Volatility Commands reference data ("
        "/usr/share/mantaray/docs/VolatilityUsage23.rst) for more information\n")
    handles_command = "vol --profile=" + profile_type + " -f " + quoted_path + " handles > " + "'" + folder_path + \
                      "/" + case_number + "_handles.txt" + "'"
    subprocess.call ([handles_command], shell=True)

    #run getsids
    print (
        "\n\n[7 of 40] Running getsids.\nSee Volatility Commands reference data ("
        "/usr/share/mantaray/docs/VolatilityUsage23.rst) for more information\n")
    getsids_command = "vol --profile=" + profile_type + " -f " + quoted_path + " getsids > " + "'" + folder_path + \
                      "/" + case_number + "_getsids.txt" + "'"
    subprocess.call ([getsids_command], shell=True)

    #run verinfo
    #print("Running verinfo.\nSee Volatility Commands reference data (/usr/share/mantaray/docs/VolatilityUsage23.rst)
    #  for more information\n")
    #verinfo_command = "vol --profile=" + profile_type + " -f " + quoted_path + " verinfo > " + "'"+folder_path + "/"
    # + case_number + "_verinfo.txt"+"'"
    #subprocess.call([verinfo_command], shell=True)

    #run modules
    print (
        "\n\n[8 of 40] Running modules.\nSee Volatility Commands reference data ("
        "/usr/share/mantaray/docs/VolatilityUsage23.rst) for more information\n")
    modules_command = "vol --profile=" + profile_type + " -f " + quoted_path + " modules > " + "'" + folder_path + \
                      "/" + case_number + "_modules.txt" + "'"
    subprocess.call ([modules_command], shell=True)

    #run modscan
    print (
        "\n\n[9 of 40] Running modscan.\nSee Volatility Commands reference data ("
        "/usr/share/mantaray/docs/VolatilityUsage23.rst) for more information\n")
    modscan_command = "vol --profile=" + profile_type + " -f " + quoted_path + " modscan > " + "'" + folder_path + \
                      "/" + case_number + "_modscan.txt" + "'"
    subprocess.call ([modscan_command], shell=True)

    #run moddump
    #mkdir for moddump
    os.mkdir (folder_path + "/moddump/")
    print (
        "\n\n[10 of 40] Running moddump.\nSee Volatility Commands reference data ("
        "/usr/share/mantaray/docs/VolatilityUsage23.rst) for more information\n")
    moddump_command = "vol --profile=" + profile_type + " -f " + quoted_path + " moddump -D " + "'" + folder_path + \
                      "/moddump/" + "'" + " > " + "'" + folder_path + "/" + case_number + "_moddump.txt" + "'"
    subprocess.call ([moddump_command], shell=True)

    #run ssdt
    print (
        "\n\n[11 of 40] Running ssdt.\nSee Volatility Commands reference data ("
        "/usr/share/mantaray/docs/VolatilityUsage23.rst) for more information\n")
    ssdt_command = "vol --profile=" + profile_type + " -f " + quoted_path + " ssdt > " + "'" + folder_path + "/" + \
                   case_number + "_ssdt.txt" + "'"
    subprocess.call ([ssdt_command], shell=True)

    #run driverscan
    print (
        "\n\n[12 of 40] Running driverscan.\nSee Volatility Commands reference data ("
        "/usr/share/mantaray/docs/VolatilityUsage23.rst) for more information\n")
    driverscan_command = "vol --profile=" + profile_type + " -f " + quoted_path + " driverscan > " + "'" + \
                         folder_path + "/" + case_number + "_driverscan.txt" + "'"
    subprocess.call ([driverscan_command], shell=True)

    #run modscan
    print (
        "\n\n[13 of 40] Running modscan.\nSee Volatility Commands reference data ("
        "/usr/share/mantaray/docs/VolatilityUsage23.rst) for more information\n")
    modscan_command = "vol --profile=" + profile_type + " -f " + quoted_path + " modscan > " + "'" + folder_path + \
                      "/" + case_number + "_modscan.txt" + "'"
    subprocess.call ([modscan_command], shell=True)

    #run filescan
    print (
        "\n\n[14 of 40] Running filescan.\nSee Volatility Commands reference data ("
        "/usr/share/mantaray/docs/VolatilityUsage23.rst) for more information\n")
    filescan_command = "vol --profile=" + profile_type + " -f " + quoted_path + " filescan > " + "'" + folder_path + \
                       "/" + case_number + "_filescan.txt" + "'"
    subprocess.call ([filescan_command], shell=True)

    #run mutantscan
    print (
        "\n\n[15 of 40] Running mutantscan.\nSee Volatility Commands reference data ("
        "/usr/share/mantaray/docs/VolatilityUsage23.rst) for more information\n")
    mutantscan_command = "vol --profile=" + profile_type + " -f " + quoted_path + " mutantscan > " + "'" + \
                         folder_path + "/" + case_number + "_mutantscan.txt" + "'"
    subprocess.call ([mutantscan_command], shell=True)

    #run symlinkscan
    print (
        "\n\n[16 of 40] Running symlinkscan.\nSee Volatility Commands reference data ("
        "/usr/share/mantaray/docs/VolatilityUsage23.rst) for more information\n")
    symlinkscan_command = "vol --profile=" + profile_type + " -f " + quoted_path + " symlinkscan > " + "'" + \
                          folder_path + "/" + case_number + "_symlinkscan.txt" + "'"
    subprocess.call ([symlinkscan_command], shell=True)

    #run thrdscan
    print (
        "\n\n[17 of 40] Running thrdscan.\nSee Volatility Commands reference data ("
        "/usr/share/mantaray/docs/VolatilityUsage23.rst) for more information\n")
    thrdscan_command = "vol --profile=" + profile_type + " -f " + quoted_path + " thrdscan > " + "'" + folder_path + \
                       "/" + case_number + "_thrdscan.txt" + "'"
    subprocess.call ([thrdscan_command], shell=True)

    #run connections
    print (
        "\n\n[18 of 40] Running connections.\nSee Volatility Commands reference data ("
        "/usr/share/mantaray/docs/VolatilityUsage23.rst) for more information\n")
    connections_command = "vol --profile=" + profile_type + " -f " + quoted_path + " connections > " + "'" + \
                          folder_path + "/" + case_number + "_connections.txt" + "'"
    subprocess.call ([connections_command], shell=True)

    #run sockets
    print (
        "\n\n[19 of 40] Running sockets.\nSee Volatility Commands reference data ("
        "/usr/share/mantaray/docs/VolatilityUsage23.rst) for more information\n")
    sockets_command = "vol --profile=" + profile_type + " -f " + quoted_path + " sockets > " + "'" + folder_path + \
                      "/" + case_number + "_sockets.txt" + "'"
    subprocess.call ([sockets_command], shell=True)

    #run sockscan
    print (
        "\n\n[20 of 40] Running sockscan.\nSee Volatility Commands reference data ("
        "/usr/share/mantaray/docs/VolatilityUsage23.rst) for more information\n")
    sockscan_command = "vol --profile=" + profile_type + " -f " + quoted_path + " sockscan > " + "'" + folder_path + \
                       "/" + case_number + "_sockscan.txt" + "'"
    subprocess.call ([sockscan_command], shell=True)

    #run netscan
    print (
        "\n\n[21 of 40] Running netscan.\nSee Volatility Commands reference data ("
        "/usr/share/mantaray/docs/VolatilityUsage23.rst) for more information\n")
    netscan_command = "vol --profile=" + profile_type + " -f " + quoted_path + " netscan > " + "'" + folder_path + \
                      "/" + case_number + "_netscan.txt" + "'"
    subprocess.call ([netscan_command], shell=True)

    #run hivescan
    print (
        "\n\n[22 of 40] Running hivescan.\nSee Volatility Commands reference data ("
        "/usr/share/mantaray/docs/VolatilityUsage23.rst) for more information\n")
    hivescan_command = "vol --profile=" + profile_type + " -f " + quoted_path + " hivescan > " + "'" + folder_path + \
                       "/" + case_number + "_hivescan.txt" + "'"
    subprocess.call ([hivescan_command], shell=True)

    #run hivelist
    print (
        "\n\n[23 of 40] Running hivelist.\nSee Volatility Commands reference data ("
        "/usr/share/mantaray/docs/VolatilityUsage23.rst) for more information\n")
    hivelist_command = "vol --profile=" + profile_type + " -f " + quoted_path + " hivelist > " + "'" + folder_path + \
                       "/" + case_number + "_hivelist.txt" + "'"
    subprocess.call ([hivelist_command], shell=True)

    #run userassist
    print (
        "\n\n[24 of 40] Running userassist.\nSee Volatility Commands reference data ("
        "/usr/share/mantaray/docs/VolatilityUsage23.rst) for more information\n")
    userassist_command = "vol --profile=" + profile_type + " -f " + quoted_path + " userassist > " + "'" + \
                         folder_path + "/" + case_number + "_userassist.txt" + "'"
    subprocess.call ([userassist_command], shell=True)

    #run svcscan
    print (
        "\n\n[25 of 40] Running svcscan.\nSee Volatility Commands reference data ("
        "/usr/share/mantaray/docs/VolatilityUsage23.rst) for more information\n")
    svcscan_command = "vol --profile=" + profile_type + " -f " + quoted_path + " svcscan > " + "'" + folder_path + \
                      "/" + case_number + "_svcscan.txt" + "'"
    subprocess.call ([svcscan_command], shell=True)

    #run ldrmodules
    print (
        "\n\n[26 of 40] Running ldrmodules.\nSee Volatility Commands reference data ("
        "/usr/share/mantaray/docs/VolatilityUsage23.rst) for more information\n")
    ldrmodules_command = "vol --profile=" + profile_type + " -f " + quoted_path + " ldrmodules > " + "'" + \
                         folder_path + "/" + case_number + "_ldrmodules.txt" + "'"
    subprocess.call ([ldrmodules_command], shell=True)

    #run idt
    #print("Running idt.\nSee Volatility Commands reference data (/usr/share/mantaray/docs/VolatilityUsage23.rst) for
    #  more information\n")
    #idt_command = "vol idt -f " + quoted_path + "  > " + "'"+folder_path + "/" + case_number + "_idt.txt"+"'"
    #subprocess.call([idt_command], shell=True)

    #run gdt
    print (
        "\n\n[27 of 40] Running gdt.\nSee Volatility Commands reference data ("
        "/usr/share/mantaray/docs/VolatilityUsage23.rst) for more information\n")
    gdt_command = "vol gdt -f " + quoted_path + "  > " + "'" + folder_path + "/" + case_number + "_gdt.txt" + "'"
    subprocess.call ([gdt_command], shell=True)

    #run callbacks
    print (
        "\n\n[28 of 40] Running callbacks.\nSee Volatility Commands reference data ("
        "/usr/share/mantaray/docs/VolatilityUsage23.rst) for more information\n")
    callbacks_command = "vol -f " + quoted_path + " callbacks > " + "'" + folder_path + "/" + case_number + \
                        "_callbacks.txt" + "'"
    subprocess.call ([callbacks_command], shell=True)

    #run devicetree
    print (
        "\n\n[29 of 40] Running devicetree.\nSee Volatility Commands reference data ("
        "/usr/share/mantaray/docs/VolatilityUsage23.rst) for more information\n")
    devicetree_command = "vol -f " + quoted_path + " devicetree > " + "'" + folder_path + "/" + case_number + \
                         "_devicetree.txt" + "'"
    subprocess.call ([devicetree_command], shell=True)

    #VistaSP0x86run psxview
    print (
        "\n\n[30 of 40] Running psxview.\nSee Volatility Commands reference data ("
        "/usr/share/Manta_Ray/docs/VolatilityUsage23.html) for more information\n")
    psxview_command = "vol -f " + quoted_path + " psxview > " + "'" + folder_path + "/" + case_number + \
                      "_psxview.txt" + "'"
    subprocess.call ([psxview_command], shell=True)

    #run privs
    print (
        "\n\n[31 of 40] Running privs.\nSee Volatility Commands reference data ("
        "/usr/share/Manta_Ray/docs/VolatilityUsage23.rst) for more information\n")
    privs_command = "vol --profile=" + profile_type + " -f " + quoted_path + " privs > " + "'" + folder_path + "/" + \
                    case_number + "_privs.txt" + "'"
    subprocess.call ([privs_command], shell=True)

    #run iehistory
    print (
        "\n\n[32 of 40] Running devicetree.\nSee Volatility Commands reference data ("
        "/usr/share/Manta_Ray/docs/VolatilityUsage23.rst) for more information\n")
    iehistory_command = "vol --profile=" + profile_type + " -f " + quoted_path + " iehistory > " + "'" + folder_path \
                        + "/" + case_number + "_iehistory.txt" + "'"
    subprocess.call ([iehistory_command], shell=True)

    #run unloadedmodules
    print (
        "\n\n[33 of 40] Running unloadedmodules.\nSee Volatility Commands reference data ("
        "/usr/share/Manta_Ray/docs/VolatilityUsage23.rst) for more information\n")
    unloadedmodules_command = "vol --profile=" + profile_type + " -f " + quoted_path + " unloadedmodules > " + "'" + \
                              folder_path + "/" + case_number + "_unloadedmodules.txt" + "'"
    subprocess.call ([unloadedmodules_command], shell=True)

    #run shellbags
    print (
        "\n\n[34 of 40] Running shellbags.\nSee Volatility Commands reference data ("
        "/usr/share/Manta_Ray/docs/VolatilityUsage23.rst) for more information\n")
    shellbags_command = "vol -f " + quoted_path + " shellbags > " + "'" + folder_path + "/" + case_number + \
                        "_shellbags.txt" + "'"
    subprocess.call ([shellbags_command], shell=True)

    #run vboxinfo
    print (
        "\n\n[35 of 40] Running vboxinfo.\nSee Volatility Commands reference data ("
        "/usr/share/Manta_Ray/docs/VolatilityUsage23.rst) for more information\n")
    vboxinfo_command = "vol --profile=" + profile_type + " -f " + quoted_path + " vboxinfo > " + "'" + folder_path + \
                       "/" + case_number + "_vboxinfo.txt" + "'"
    subprocess.call ([vboxinfo_command], shell=True)

    #run vmwareinfo
    print (
        "\n\n[36 of 40] Running vmwareinfo.\nSee Volatility Commands reference data ("
        "/usr/share/Manta_Ray/docs/VolatilityUsage23.rst) for more information\n")
    vmwareinfo_command = "vol -f " + quoted_path + " vmwareinfo > " + "'" + folder_path + "/" + case_number + \
                         "_vmwareinfo.txt" + "'"
    subprocess.call ([vmwareinfo_command], shell=True)

    #run hpakinfo
    print (
        "\n\n[37 of 40] Running hpakinfo.\nSee Volatility Commands reference data ("
        "/usr/share/Manta_Ray/docs/VolatilityUsage23.rst) for more information\n")
    hpakinfo_command = "vol --profile=" + profile_type + " -f " + quoted_path + " hpakinfo > " + "'" + folder_path + \
                       "/" + case_number + "_hpakinfo.txt" + "'"
    subprocess.call ([hpakinfo_command], shell=True)

    #run hpakextract
    #	print("Running hpakextract.\nSee Volatility Commands reference data (
    # /usr/share/Manta_Ray/docs/VolatilityUsage23.rst) for more information\n")
    #	hpakextract_command = "vol --profile=" + profile_type + " -f " + quoted_path + " hpakextract > " +
    # "'"+folder_path + "/" + case_number + "_hpakextract.txt"+"'"
    #	subprocess.call([hpakextract_command], shell=True)

    #run mbrparser
    print (
        "\n\n[38 of 40] Running mbrparser.\nSee Volatility Commands reference data ("
        "/usr/share/Manta_Ray/docs/VolatilityUsage23.rst) for more information\n")
    mbrparser_command = "vol --profile=" + profile_type + " -f " + quoted_path + " mbrparser > " + "'" + folder_path \
                        + "/" + case_number + "_mbrparser.txt" + "'"
    subprocess.call ([mbrparser_command], shell=True)

    #run mftparser
    print (
        "\n\n[39 of 40] Running mftparser.\nSee Volatility Commands reference data ("
        "/usr/share/Manta_Ray/docs/VolatilityUsage23.rst) for more information\n")
    mftparser_command = "vol --profile=" + profile_type + " -f " + quoted_path + " mftparser > " + "'" + folder_path \
                        + "/" + case_number + "_mftparser.txt" + "'"
    subprocess.call ([mftparser_command], shell=True)

    #run timeliner
    print (
        "\n\n[40 of 40] Running timeliner.\nSee Volatility Commands reference data ("
        "/usr/share/Manta_Ray/docs/VolatilityUsage23.rst) for more information\n")
    timeliner_command = "vol --profile=" + profile_type + " -f " + quoted_path + " timeliner > " + "'" + folder_path \
                        + "/" + case_number + "_timeliner.txt" + "'"
    subprocess.call ([timeliner_command], shell=True)

    #run dumpcerts
    #print("Running dumpcerts.\nSee Volatility Commands reference data (
    # /usr/share/Manta_Ray/docs/VolatilityUsage23.rst) for more information\n")
    #dumpcerts_command = "vol --profile=" + profile_type + " -f " + quoted_path + " dumpcerts > " + "'"+folder_path + "/" + case_number + "_dumpcerts.txt"+"'"
    #subprocess.call([dumpcerts_command], shell=True)


    #run dumpfiles
    #try:
    #	os.mkdir(folder_path + "/dumpfiles")
    #	print("Running dumpfiles.\nSee Volatility Commands reference data (/usr/share/Manta_Ray/docs/VolatilityUsage23.rst) for more information\n")
    #	dumpfiles_command = "vol --profile=" + profile_type + " -f " + quoted_path + " dumpfiles --dump-dir " + "'"+folder_path + "/dumpfiles"+"'"
    #	subprocess.call([dumpfiles_command], shell=True)
    #except:
    #	print("Dumpdirs failed. Please report to MantaRay Forums at MantaRayForensics.com")
    #	outfile.write("\n#######\nDumpdirs failed. Please report to MantaRay Forums at MantaRayForensics.com\n#######\n")


    #run timers
    #print("Running timers.\nSee Volatility Commands reference data (/usr/share/mantaray/docs/VolatilityUsage23.rst) for more information\n")
    #timers_command = "vol --profile=" + profile_type + " -f " + quoted_path + " timers > " + "'"+folder_path + "/" + case_number + "_timers.txt"+"'"
    #subprocess.call([timers_command], shell=True)

    #close outfile
    outfile.close ()

    #change dir into output folder
    os.chdir (folder_path)

    #run unix2dos on text files
    unix2dos_command = "sudo unix2dos *.txt"
    subprocess.call ([unix2dos_command], shell=True)

