#!/usr/bin/env python

##########################COPYRIGHT INFORMATION############################
# Copyright (C) 2014, Chapin Bryce, webmaster@mantarayforensics.com		  #
#                                                                         #
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
#########################COPYRIGHT INFORMATION#############################

__author__ = 'cbryce'

import subprocess
import threading
import argparse
import time
import datetime
import os
import sys
import vol_get_pids
import easygui


def run_pid_plugin(fin, profile, plug, out, count, plugins, pid, dump_plugin):
    """
    Will run a volatility plugin for a PID within a thread.

    ::NOTE::
    * --plugins= must precede -f in command for the profiles to be loaded correctly
    """
    cmd = "vol.py -f " + fin + " --profile=" + profile + " " + plug + " -p " + pid

    if plug in dump_plugin:
        dump_path = out + "/" + pid + "/" + plug + "/"
        os.makedirs(dump_path)
        cmd += " --dump-dir=" + dump_path

    cmd += " --output-file=" + out + plug + ".txt"

    subprocess.call(cmd, shell=True, stderr=ERRFILE)
    status = str("[Thread " + str(datetime.datetime.now()) + "] Completed PID " + pid + " " + plug + ", " + str(count) + " of " + str(len(plugins)-1))
    print(status)
    OUTFILE.write(status)


def run_plugin(fin, profile, plug, out, count, plugins, dump_plugin):
    """
    Will run a volatility plugin within a thread.

    ::NOTE::
    * --plugins= must precede -f in command for the profiles to be loaded correctly
    """
    cmd = "vol.py -f " + fin + " --profile=" + profile + " " + plug

    if plug in dump_plugin:
        dump_path = out + "/" + plug + "/"
        os.makedirs(dump_path)
        cmd = cmd + " --dump-dir=" + dump_path

    cmd = cmd + " --output-file=" + out + plug + ".txt"

    subprocess.call([cmd], shell=True, stderr=ERRFILE)
    status = str("[Thread " + str(datetime.datetime.now()) + "] Completed " + plug + ", " + str(count) + " of " + str(len(plugins)-1))
    print(status)
    OUTFILE.write(status)


def main(fin, profile, num_thread, out, pid_enabled, dump_enabled):
    global OUTFILE
    global ERRFILE


    out = out + 'Volatility/'
    os.makedirs(out)

    # Set Logfile & Error Log
    log_file = out + "/Volatility_logfile.txt"
    OUTFILE = open(log_file, 'w')
    log_file = out + "/Volatility_errors_logfile.txt"
    ERRFILE = open(log_file, 'w')

    if profile.startswith("Win"):
        plugins = ["kpcrscan","atoms","atomscan","auditpol","bigpools","bioskbd","callbacks","clipboard","cmdline",
                   "cmdscan","connections","connscan","consoles","crashinfo","deskscan","devicetree","dlllist","dlldump",
                   "driverirp","driverscan","dumpfiles","dumpcerts","envars","eventhooks","evtlogs","filescan","gahti",
                   "gditimers","gdt","getservicesids","getsids","handles","hibinfo","hivelist",
                   "hivescan","hpakextract","hpakinfo","idt","iehistory","imageinfo","impscan","joblinks","kdbgscan",
                   "ldrmodules","limeinfo","machoinfo","malfind","mbrparser","memmap","memdump","messagehooks","mftparser","modscan",
                   "moddump","modules","multiscan","mutantscan","netscan","notepad","objtypescan","patcher","poolpeek","pooltracker",
                   "printkey","privs","pslist","psscan","pstree","psxview","procmon","screenshot","sessions",
                   "shellbags","shimcache","sockets","sockscan","ssdt","strings","svcscan","symlinkscan","thrdscan","threads",
                   "timeliner","timers","truecryptmaster","truecryptpassphrase","truecryptsummary","unloadedmodules",
                   "userassist","userhandles","vaddump","vadinfo","vadtree","vadwalk","vboxinfo","verinfo","vmwareinfo","windows",
                   "wintree","wndscan","yarascan"]

        pid_plugins = ["dlllist", "envars", "getsids", "handles", "iehistory", "impscan", "joblinks", "ldrmodules",
                       "malfind", "memmap", "notepad", "privs", "pslist", "strings", "threads", "userhandles", "vadinfo",
                       "vadtree", "vadwalk", "yarascan", "dumpfiles", "dumpcerts", ""]

        plugins_dump = ["dlldump", "dumpfiles", "dumpcerts", "evtlogs", "malfind", "memdump", "mftparser", "moddump",
                        "notepad", "procdump", "screenshot", "truecryptmaster", "vaddump", "verinfo", "yarascan"]
        """
        Extra features to add in the future:
        dumpcerts: --ssl uses openssl for parsing | --physical to scan deallocated space
        dumpfiles: --summary-file=FILE for output | --filter to select type (see docs)
        evtlogs: --save-evt to save as .evt file
        mftparser: --nocheck to include entries with NULL timestamps
        patcher: -x XML input to patch binaries
        pooltracker: --whitelist to eliminate known files | --show-free to show unallocated tags
        printkey: --key=KEY to print a reg key , sub keys, and values
        procdump: -m to carve as a memory sample instead of exe/disk | -u to bypass sanity checks when creating disk image
        psxview: -R apply known good rules
        screenshot: --show-unallocated to skip unallocated (test)
        shellbags: --machine=NAME will add name to header
        strings: --string-file=FILE to output in strings format | --scan to scan with PSScan for PIDs
        threads: -L to list all available tags
        timeliner: --output=XLSX,MACTIME (only xlsxl if openpyxl is installed) | --hive=HIVE to gather timestamps from | --user=USER to gather timestamps from | --machine=NAME to add to header | --type=EvtLog,IEHistory,ImageDate,LoadTime,Process,Shimcache,Socket,Symlink,Thread,TimeDateStamp,Userassist,_CMHIVE,_CM_KEY_BODY,_HBASE_BLOCK | --highlight=HIGHLIGT will highlight specified malicious items
        callbacks: -V scan virtual space instead of phsycial
        bigpools: -t TAG to find
        poolpeek: needs --tag to find
        malfind: needs `-y` to be specified
        impscan: needs `--base` to be specified
        """

    elif profile.startswith("Lin"):
        # removed linux_volshell
        plugins = ["linux_apihooks","linux_arp","linux_banner","linux_bash","linux_bash_env","linux_bash_hash",
                   "linux_check_afinfo","linux_check_creds","linux_check_evt_arm","linux_check_fop","linux_check_idt",
                   "linux_check_inline_kernel","linux_check_modules","linux_check_syscall","linux_check_syscall_arm",
                   "linux_check_tty","linux_cpuinfo","linux_dentry_cache","linux_dmesg","linux_dump_map","linux_elfs",
                   "linux_enumerate_files","linux_find_file","linux_hidden_modules","linux_ifconfig",
                   "linux_iomem","linux_kernel_opened_files","linux_keyboard_notifiers","linux_ldrmodules",
                   "linux_library_list","linux_librarydump","linux_list_raw","linux_lsmod","linux_lsof","linux_malfind",
                   "linux_memmap","linux_moddump","linux_mount","linux_mount_cache","linux_netfilter","linux_netstat",
                   "linux_pidhashtable","linux_pkt_queues","linux_plthook","linux_proc_maps","linux_proc_maps_rb",
                   "linux_procdump","linux_process_hollow","linux_psaux","linux_psenv","linux_pslist",
                   "linux_pslist_cache","linux_pstree","linux_psxview","linux_recover_filesystem","linux_route_cache",
                   "linux_sk_buff_cache","linux_slabinfo","linux_strings","linux_threads","linux_tmpfs",
                   "linux_truecrypt_passphrase","linux_vma_cache","linux_yarascan"]

        pid_plugins = ["linux_apihooks", "linux_bash", "linux_bash_env", "linux_bash_hash", "linux_check_creds",
                       "linux_dump_map", "linux_elfs", "linux_ldrmodules", "linux_library_list", "linux_library_dump",
                       "linux_lsof", "linux_malfind", "linux_memmap", "linux_netstat", "linux_pidhashtable",
                       "linux_pkt_queues", "linux_proc_maps", "linux_proc_maps_rb", "linux_procdump",
                       "linux_process_hollow", "linux_psaux", "linux_psenv", "linux_pslist", "linux_pslist_cache",
                       "linux_pstree", "linux_strings", "linux_threads", "linux_truecrypt_passphrase"]

        plugins_dump = ["linux_dump_map", "linux_library_dump", "linux_moddump", "linux_pkt_queues", "linux_procdump",
                        "linux_recover_filesystem", "linux_sk_buff_cache", "linux_yarascan"]
        """
        Extra Features to research in future:
        linux_vma_cache: -u show unallocated
        linux_tmpfs: -S SB super block to process | -L list available superblocks
        linux_strings: -S STRING_FILE file output in string format | -S use psscan if no offest provided | -o HEX offset of Physical addr
        linux_sk_buff_cache: -u show unallocated
        linux_route_cache: -R resolve DNS of remote IP
        linux_pslist_cache: -u show unallocated
        linux_process_hollow: -P PATH to known good file
        linux_plthook: -a display all PLT slots
        linux_pkt_queues: -U ignore unix sockets
        linux_netstat: -U ignore unix sockets
        linux_mount_cache: -u show unallocated
        linux_moddump: -r REGEX | -i ignore case
        linux_lsmod: -T show section addresses | -P show module parameters | -c IDC file to be created for module
        linux_info_regs: Broken and removed from list
        linux_find_file: -L list all files cached in memory | -i INODE to extract
        linux_dentry_cache: -u show unallocated
        linux_check_fop: -i INODE to check
        linux_apihooks: -a Check all functions, including those with PLT hooks
        linux_bash_hash: -A scann all processes
        linux_bash: -A scan all processes, not just those named in bash | -P print unallocated entries | -H HISTORY_LIST
        """

    elif profile.startswith("Mac"):
        # removed mac_volshell
        plugins = ["mac_adium", "mac_apihooks","mac_apihooks_kernel","mac_arp","mac_bash","mac_bash_env",
                   "mac_bash_hash","mac_calendar","mac_check_mig_table","mac_check_syscall_shadow",
                   "mac_check_syscalls","mac_check_sysctl","mac_check_trap_table","mac_contacts","mac_dead_procs",
                   "mac_dead_sockets","mac_dead_vnodes","mac_dmesg","mac_dump_file","mac_dump_maps","mac_dyld_maps",
                   "mac_find_aslr_shift","mac_ifconfig","mac_ip_filters","mac_keychaindump","mac_ldrmodules",
                   "mac_librarydump","mac_list_files","mac_list_sessions","mac_list_zones","mac_lsmod",
                   "mac_lsmod_iokit","mac_lsmod_kext_map","mac_lsof","mac_machine_info","mac_malfind",
                   "mac_memdump","mac_moddump","mac_mount","mac_netstat","mac_network_conns",
                   "mac_notifiers","mac_pgrp_hash_table","mac_pid_hash_table","mac_print_boot_cmdline","mac_proc_maps",
                   "mac_procdump","mac_psaux","mac_pslist","mac_pstree","mac_psxview","mac_recover_filesystem",
                   "mac_route","mac_socket_filters","mac_strings","mac_tasks","mac_trustedbsd","mac_version",
                   "mac_yarascan"]

        pid_plugins = ["mac_proc_maps", "mac_adium", "mac_api_hooks", "mac_bash", "mac_bash_env", "mac_bash_hash",
                       "mac_calendar", "mac_contacts", "mac_dead_procs", "mac_dead_sockets", "mac_dead_vnodes",
                       "mac_dump_maps", "mac_dyld_maps", "mac_keychaindump", "mac_ldrmodules", "mac_librarydump",
                       "mac_list_sessions", "mac_lsof", "mac_memdump", "mac_netstat", "mac_pgrp_hash_table",
                       "mac_pid_hash_table", "mac_procdump", "mac_psaux", "mac_pslist", "mac_pstree", "mac_strings",
                       "mac_tasks"]

        plugins_dump = ["mac_adium", "mac_dump_maps", "mac_librarydump", "mac_malfind", "mac_memdump", "mac_moddump"
                        "mac_procdump", "mac_recover_filesystem", "mac_yarascan"]
        """
        Extra Features to research in future:
        mac_yara: Has a lot of features about yara info
        mac_strings: -S STRING_FILE file output in string format | -S use psscan if no offest provided | -o HEX offset of Physical addr
        mac_moddump: -r DUmp matching REGEX | -i Ignore case in matches
        mac_keychaindump: use chainbreaker to open related keychain files
        mac_trustedbsd: -a ADDR, show info on VAD at or containing this address
        mac_socket_filters: -a ADDR, show info on VAD at or containing this address
        mac_notifiers: -a ADDR, show info on VAD at or containing this address
        mac_lsmod: -a ADDR, show info on VAD at or containing this address
        mac_ip_filters: -a ADDR, show info on VAD at or containing this address
        mac_dump_file: -q FILE_OFFSET, virtual addr of vnode structure from mac_list_files | -O OUTFILE, output file path
        mac_bash: -A scan all processes, not just those named in bash | -P print unallocated entries
        mac_bash_hash: -A scan all processes, not just those named in bash
        mac_check_syscalls: -i Path to unistd_{32,64}.h from the target machine
        """

    else:
        print("Invalid Profile Selected")
        OUTFILE.write("Invalid Profile Selected")
        sys.exit(1)

    # Remove all plugins for dump if it is disabled so they cannot match and run.
    if not dump_enabled:
        plugins_dump = []

    start = datetime.datetime.now()

    #"""
    for count, plug in enumerate(plugins):
        while 1:
            if threading.activeCount() <= num_thread:
                status = str("[Thread " + str(datetime.datetime.now()) + "] Starting plugin " + plug)
                print(status)
                OUTFILE.flush()
                OUTFILE.write(status)
                t = threading.Thread(target=run_plugin, args=[fin, profile, plug, out, count, plugins, plugins_dump])
                t.start()
                break
            else:
                time.sleep(4)
    #"""

    pids_to_process = vol_get_pids.get_pids(fin, profile)

    if pid_enabled:
        for proc in pids_to_process:
            try:
                pid = int(proc["pid"])
                forward = 1
            except:
                print('Could not parse PID: ' + proc["pid"])
                OUTFILE.write('Could not parse PID: ' + proc["pid"])
                forward = 0
            if forward:
                path_out = out + "/PID/" + proc["name"] + "_" + str(pid) + "/"
                os.makedirs(path_out)

                for count, pid_plug in enumerate(pid_plugins):
                    while 1:
                        if threading.activeCount() <= num_thread:
                            status = str("[Thread " + str(datetime.datetime.now()) + "] Starting PID " + str(pid) + " plugin " + pid_plug)
                            print(status)
                            OUTFILE.write(status)
                            t = threading.Thread(target=run_pid_plugin, args=[fin, profile, pid_plug, path_out, count, pid_plugins, str(pid), plugins_dump])
                            t.start()
                            break
                        else:
                            time.sleep(4)

    while 1:
        if threading.activeCount() == 1:
            status = str("[Main " + str(datetime.datetime.now()) + "] Completed")
            print(status)
            OUTFILE.write(status)
            status = str("[Main " + str(datetime.datetime.now()) + "] Runtime: " + str(datetime.datetime.now()-start))
            print(status)
            OUTFILE.write(status)
            OUTFILE.close()
            break
        else:
            if time.time() % 60 == 0:  # Wait 2 minutes to prompt the user that threads are still running
                status = str("[Main " + str(datetime.datetime.now()) + "] waiting for " + str(threading.activeCount()-1) + " threads to finish")
                print(status)
                OUTFILE.write(status)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Volley24 is a tool used at the command line and with the MantaRay Suite for processing memory images in Volatility 2.4", epilog="Copyright Chapin Bryce, 2014 webmaster@mantarayforensics.com")
    parser.add_argument('-P', help="Enable processing of a specific PID across plugins", action="store_true")
    parser.add_argument('-d', help="Enable plugins to dump data from memory images", action="store_true")
    parser.add_argument('-t', help="Specify the number of threads to run", required=True, type=int)
    parser.add_argument('fin', help='Memory Image')
    parser.add_argument('-p', metavar='PROFILE', help='Volatility Profile Name (Using Volatility Syntax)', required=True)
    parser.add_argument('out', help='Output Directory')
    args = parser.parse_args()
    fin = args.fin
    profile = args.p
    num_thread = args.t
    out = args.out
    if not os.path.exists(out):
        os.makedirs(out)
    if not out.endswith("/") or out.endswith("\\"):
        out = out + "/"
    main(fin, profile, num_thread, out, args.P, args.d)
