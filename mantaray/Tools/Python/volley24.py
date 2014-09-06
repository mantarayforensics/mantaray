#!/usr/bin/env python

#########################COPYRIGHT INFORMATION############################
#Copyright (C) 2014, Chapin Bryce, webmaster@mantarayforensics.com		 #
#                                                                        #
#This program is free software: you can redistribute it and/or modify    #
#it under the terms of the GNU General Public License as published by    #
#the Free Software Foundation, either version 3 of the License, or       #
#(at your option) any later version.                                     #
#                                                                        #
#This program is distributed in the hope that it will be useful,         #
#but WITHOUT ANY WARRANTY; without even the implied warranty of          #
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the           #
#GNU General Public License for more details.                            #
#                                                                        #
#You should have received a copy of the GNU General Public License       #
#along with this program.  If not, see http://www.gnu.org/licenses/.     #
#########################COPYRIGHT INFORMATION############################

__author__ = 'cbryce'

import subprocess
import threading
import argparse
import time
import datetime
import os
import sys
import vol_get_pids


def run_pid_plugin(fin, profile, plug, out, count, plugins, pid, profile_path):
    """
    Will run a volatility plugin for a PID within a thread.

    ::NOTE::
    * --plugins= must precede -f in command for the profiles to be loaded correctly
    """
    subprocess.call(["vol --plugins='" + profile_path + "' -f " + fin + " --profile=" + profile + " " + plug + " -p " + pid + " --output-file=" + out +
                     plug + ".txt"], shell=True)
    print "[Thread ", datetime.datetime.now(), "] Completed PID " + pid + " " + plug + ", ", count, " of ", \
        len(plugins)-1


def run_plugin(fin, profile, plug, out, count, plugins, profile_path):
    """
    Will run a volatility plugin within a thread.

    ::NOTE::
    * --plugins= must precede -f in command for the profiles to be loaded correctly
    """
    subprocess.call(["vol --plugins=" + profile_path + " -f " + fin + "  --profile=" + profile + " " + plug + " > " + out + plug + ".txt"],
                    shell=True)
    print "[Thread ", datetime.datetime.now(), "] Completed " + plug + ", ", count, " of ", len(plugins)-1


def main(fin, profile, num_thread, out):
    if profile.__contains__("x64"):
        profile_path = "/usr/share/mantaray/volatility_profiles/x64"
    elif profile.__contains__("x86"):
        profile_path = "/usr/share/mantaray/volatility_profiles/x86/"
    else:
        print "Invalid Profile"
        sys.exit(1)

    if profile.startswith("Win"):
        plugins = ["kpcrscan","atoms","atomscan","auditpol","bigpools","bioskbd","callbacks","clipboard","cmdline",
                   "cmdscan","connections","connscan","consoles","crashinfo","deskscan","devicetree","dlllist",
                   "driverirp","driverscan","envars","eventhooks","evtlogs","filescan","gahti",
                   "gditimers","gdt","getservicesids","getsids","handles","hibinfo","hivelist",
                   "hivescan","hpakextract","hpakinfo","idt","iehistory","imageinfo","impscan","joblinks","kdbgscan",
                   "ldrmodules","limeinfo","machoinfo","malfind","mbrparser","memmap","messagehooks","mftparser","modscan",
                   "modules","multiscan","mutantscan","netscan","notepad","objtypescan","patcher","poolpeek","pooltracker",
                   "printkey","privs","pslist","psscan","pstree","psxview","screenshot","sessions",
                   "shellbags","shimcache","sockets","sockscan","ssdt","strings","svcscan","symlinkscan","thrdscan","threads",
                   "timeliner","timers","truecryptmaster","truecryptpassphrase","truecryptsummary","unloadedmodules",
                   "userassist","userhandles","vadinfo","vadtree","vadwalk","vboxinfo","verinfo","vmwareinfo","windows",
                   "wintree","wndscan","yarascan"]

        # poolpeek needs --tag to find
        # malfind needs `-y` to be specified
        # impscan needs `--base` to be specified

        pid_plugins = ["dlllist", "envars", "getsids", "handles", "iehistory", "impscan", "joblinks", "ldrmodules",
                       "malfind", "memmap", "notepad", "privs", "pslist", "strings", "threads", "userhandles", "vadinfo",
                       "vadtree", "vadwalk", "yarascan"]

    elif profile.startswith("Lin"):
        plugins = ["linux_apihooks","linux_arp","linux_banner","linux_bash","linux_bash_env","linux_bash_hash",
                   "linux_check_afinfo","linux_check_creds","linux_check_evt_arm","linux_check_fop","linux_check_idt",
                   "linux_check_inline_kernel","linux_check_modules","linux_check_syscall","linux_check_syscall_arm",
                   "linux_check_tty","linux_cpuinfo","linux_dentry_cache","linux_dmesg","linux_dump_map","linux_elfs",
                   "linux_enumerate_files","linux_find_file","linux_hidden_modules","linux_ifconfig","linux_info_regs",
                   "linux_iomem","linux_kernel_opened_files","linux_keyboard_notifiers","linux_ldrmodules",
                   "linux_library_list","linux_librarydump","linux_list_raw","linux_lsmod","linux_lsof","linux_malfind",
                   "linux_memmap","linux_moddump","linux_mount","linux_mount_cache","linux_netfilter","linux_netstat",
                   "linux_pidhashtable","linux_pkt_queues","linux_plthook","linux_proc_maps","linux_proc_maps_rb",
                   "linux_procdump","linux_process_hollow","linux_psaux","linux_psenv","linux_pslist",
                   "linux_pslist_cache","linux_pstree","linux_psxview","linux_recover_filesystem","linux_route_cache",
                   "linux_sk_buff_cache","linux_slabinfo","linux_strings","linux_threads","linux_tmpfs",
                   "linux_truecrypt_passphrase","linux_vma_cache","linux_volshell","linux_yarascan"]
        pid_plugins = ["linux_lsof", "linux_memmap", "linux_proc_maps", "linux_netstat", "linux_yarascan"]

    elif profile.startswith("Mac"):
        plugins = ["mac_adium","mac_apihooks","mac_apihooks_kernel","mac_arp","mac_bash","mac_bash_env",
                   "mac_bash_hash","mac_calendar","mac_check_mig_table","mac_check_syscall_shadow",
                   "mac_check_syscalls","mac_check_sysctl","mac_check_trap_table","mac_contacts","mac_dead_procs",
                   "mac_dead_sockets","mac_dead_vnodes","mac_dmesg","mac_dump_file","mac_dump_maps","mac_dyld_maps",
                   "mac_find_aslr_shift","mac_ifconfig","mac_ip_filters","mac_keychaindump","mac_ldrmodules",
                   "mac_librarydump","mac_list_files","mac_list_sessions","mac_list_zones","mac_lsmod",
                   "mac_lsmod_iokit","mac_lsmod_kext_map","mac_lsof","mac_machine_info","mac_malfind",
                   "mac_memdump","mac_moddump","mac_mount","mac_netstat","mac_network_conns","mac_notesapp",
                   "mac_notifiers","mac_pgrp_hash_table","mac_pid_hash_table","mac_print_boot_cmdline","mac_proc_maps",
                   "mac_procdump","mac_psaux","mac_pslist","mac_pstree","mac_psxview","mac_recover_filesystem",
                   "mac_route","mac_socket_filters","mac_strings","mac_tasks","mac_trustedbsd","mac_version",
                   "mac_volshell","mac_yarascan"]
        pid_plugins = ["mac_proc_maps"]

    else:
        print "Invalid Profile Selected"
        sys.exit(1)

    start = datetime.datetime.now()

    for count, plug in enumerate(plugins):
        while 1:
            if threading.activeCount() <= num_thread:
                print "[Thread ", datetime.datetime.now(), "] Starting plugin " + plug
                t = threading.Thread(target=run_plugin, args=[fin, profile, plug, out, count, plugins, profile_path])
                t.start()
                break
            else:
                time.sleep(4)

    pids_to_process = vol_get_pids.get_pids(fin, profile)

    for proc in pids_to_process:
        try:
            pid = int(proc["PID"])
            forward = 1
        except:
            print 'Could not parse PID: ' + proc["PID"]
            forward = 0
        if forward:
            path_out = out + "/PID/" + proc["Name"] + "_" + str(pid) + "/"
            os.makedirs(path_out)

            for count, pid_plug in enumerate(pid_plugins):
                while 1:
                    if threading.activeCount() <= num_thread:
                        print "[Thread ", datetime.datetime.now(), "] Starting PID " + str(pid) + " plugin " + pid_plug
                        t = threading.Thread(target=run_pid_plugin, args=[fin, profile, pid_plug, path_out, count, pid_plugins, str(pid), profile_path])
                        t.start()
                        break
                    else:
                        time.sleep(4)

    while 1:
        if threading.activeCount() == 1:
            print "[Main ", datetime.datetime.now(), "] Completed"
            print "[Main ", datetime.datetime.now(), "] Runtime: ", datetime.datetime.now()-start
            break
        else:
            if time.time() % 120 == 0:  # Wait 2 minutes to prompt the user that threads are still running
                print "[Main ", datetime.datetime.now(), "] waiting for ", threading.activeCount()-1, " threads to finish"

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('fin')
    parser.add_argument('profile')
    # parser.add_argument('-p', help="Enable processing of a specific PID across plugins")
    parser.add_argument('-t', help="Specify the number of threads to run", required=True, type=int)
    parser.add_argument('out')
    args = parser.parse_args()
    fin = args.fin
    profile = args.profile
    num_thread = args.t
    out = args.out
    main(fin, profile, num_thread, out)
