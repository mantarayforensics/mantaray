==================================
Using Volatility 2.3
==================================

The most basic volatility commands are constructed as shown below. Replace --plugin with the name of the plugin to use, --image with the file path to your memory image, and --profile with the name of the profile (such as Win7SP1x64). 

::

  $ python vol.py [plugin] -f [image] --profile=[profile] 

Here is an example: 

::

  $ python vol.py pslist -f /path/to/memory.img --profile=Win7SP1x64
  
For everything beyond this example, such as controlling the output format, listing the available plugins and profiles, or supplying plugin-specific options, see the rest of the text below. 

===== 
Global Options 
=====

There are several command-line options that are global (i.e. they apply to all plugins). This section is for folks who are new to Volatility or anyone who wants to become more familiar with what functionality can be tweaked. 

===== 
Displaying Help 
=====

You can display the main help menu by passing -h or --help on command-line. This shows the global options and lists the plugins available to the currently specified profile. If you do not specify a profile, you'll be working with the default, WinXPSP2x86, thus you'll only see plugins that are valid for that operating system and architecture (for example, you won't see linux plugins or windows plugins that only work on Vista). To specify a profile other than the default, see Selecting a Profile below. Developer note: to restrict plugins per profile, see the [PluginInterface22#Restricting_Plugins_Per_Profile Restricting Plugins Per Profile] page. 

The remainder of this section will discuss the various options in greater detail. 

::

  $ python vol.py -h
  Volatile Systems Volatility Framework 2.3

  Usage: Volatility - A memory forensics analysis platform.

  Options:
    -h, --help            list all available options and their default values.
                          Default values may be set in the configuration file
                          (/etc/volatilityrc)
    --conf-file=/Users/Michael/.volatilityrc
                          User based configuration file
    -d, --debug           Debug volatility
    --plugins=PLUGINS     Additional plugin directories to use (colon separated)
    --info                Print information about all registered objects
    --cache-directory=/Users/Michael/.cache/volatility
                          Directory where cache files are stored
    --cache               Use caching
    --tz=TZ               Sets the timezone for displaying timestamps
    -f FILENAME, --filename=FILENAME
                          Filename to use when opening an image
    --profile=WinXPSP2x86
                          Name of the profile to load
    -l LOCATION, --location=LOCATION
                          A URN location from which to load an address space
    -w, --write           Enable write support
    --use-old-as          Use the legacy address spaces
    --dtb=DTB             DTB Address
    --output=text         Output in this format (format support is module
                          specific)
    --output-file=OUTPUT_FILE
                          write output in this file
    -v, --verbose         Verbose information
    -k KPCR, --kpcr=KPCR  Specify a specific KPCR address
    -g KDBG, --kdbg=KDBG  Specify a specific KDBG virtual address

          Supported Plugin Commands:

                  apihooks        Detect API hooks in process and kernel memory
                  bioskbd         Reads the keyboard buffer from Real Mode memory
                  callbacks       Print system-wide notification routines
                  cmdscan         Extract command history by scanning for _COMMAND_HISTORY
                  connections     Print list of open connections [Windows XP and 2003 Only]
  [snip]

===== 
Selecting a Profile 
===== 

Volatility needs to know what type of system your memory dump came from, so it knows which data structures, algorithms, and symbols to use. A default profile of WinXPSP2x86 is set internally, so if you're analyzing a Windows XP SP2 x86 memory dump, you do not need to supply --profile at all. However, for all others, you must specify the proper profile name. 

Note: If you do not know what type of system the memory dump is from, use the [http://code.google.com/p/volatility/wiki/CommandReference23#imageinfo imageinfo] or [http://code.google.com/p/volatility/wiki/CommandReference23#kdbgscan kdbgscan] plugins for a suggestion. These plugins are Windows-only. 

If you want to see a list of supported profile names, do the following:

::

  $ python vol.py --info

  [snip]

  Profiles
  --------
  VistaSP0x64     - A Profile for Windows Vista SP0 x64
  VistaSP0x86     - A Profile for Windows Vista SP0 x86
  VistaSP1x64     - A Profile for Windows Vista SP1 x64
  VistaSP1x86     - A Profile for Windows Vista SP1 x86
  VistaSP2x64     - A Profile for Windows Vista SP2 x64
  VistaSP2x86     - A Profile for Windows Vista SP2 x86
  Win2003SP0x86   - A Profile for Windows 2003 SP0 x86
  Win2003SP1x64   - A Profile for Windows 2003 SP1 x64
  Win2003SP1x86   - A Profile for Windows 2003 SP1 x86
  Win2003SP2x64   - A Profile for Windows 2003 SP2 x64
  Win2003SP2x86   - A Profile for Windows 2003 SP2 x86
  Win2008R2SP0x64 - A Profile for Windows 2008 R2 SP0 x64
  Win2008R2SP1x64 - A Profile for Windows 2008 R2 SP1 x64
  Win2008SP1x64   - A Profile for Windows 2008 SP1 x64
  Win2008SP1x86   - A Profile for Windows 2008 SP1 x86
  Win2008SP2x64   - A Profile for Windows 2008 SP2 x64
  Win2008SP2x86   - A Profile for Windows 2008 SP2 x86
  Win7SP0x64      - A Profile for Windows 7 SP0 x64
  Win7SP0x86      - A Profile for Windows 7 SP0 x86
  Win7SP1x64      - A Profile for Windows 7 SP1 x64
  Win7SP1x86      - A Profile for Windows 7 SP1 x86
  WinXPSP1x64     - A Profile for Windows XP SP1 x64
  WinXPSP2x64     - A Profile for Windows XP SP2 x64
  WinXPSP2x86     - A Profile for Windows XP SP2 x86
  WinXPSP3x86     - A Profile for Windows XP SP3 x86


=====
Alternatives to Command Line Options  
===== 

If you're about to enter a lengthy engagement and don't want to type the path to your memory dump and the corresponding profile name each time, there are two alternatives: environment variables and configuration files. If an option is not supplied on command-line, Volatility will try to get it from an environment variable and if that fails - from a configuration file. 

Note also that to avoid confusion, the (-h/--help) option also lists the current value of each parameter so you can easily check what value is being used (from the environment or the config files). 

=====
Environment Variables
===== 

On a Linux or OS X system you can set options by exporting them in your shell, as shown below:

::

  $ export VOLATILITY_PROFILE=Win7SP0x86
  $ export VOLATILITY_LOCATION=file:///tmp/myimage.img
  $ ./vol.py pslist
  $ ./vol.py files


=====
Configuration Files
=====

Configuration files are typically "volatilityrc" in the current directory or ~/.volatilityrc (user's home directory), or at user specified path (using the --conf-file option). An example of the file contents is shown below: 

::

  [DEFAULT]
  PROFILE=Win7SP0x86
  LOCATION=file:///tmp/myimage.img

===== 
Enabling Debug Messages 
=====

If something isn't happening in Volatility the way you'd expect, try running the command with -d/--debug. This will enable the printing of debug messages to standard error. If you *really* need to debug Volatility (as in using pdb debugger), then add -d -d -d to your commands. 

===== 
Using the Cache 
===== 

The cache allows Volatility to store arbitrary objects and constants for later retrieval. This can include, DTB, KDBG, or KPCR addresses, entire x86 page translation tables, or even hibernation decompression data structures. To enable use of the cache, add --cache to your commands. This feature pickles (serializes) the data in files on your disk, so if you want to choose the location of cache files, use --cache-directory. For more information, see the caching system page in the developer guide for your release version.

=====
Setting the Timezone 
===== 

Timestamps extracted from memory can either be in system-local time, or in Universal Time Coordinates (UTC).  If they're in UTC, Volatility can be instructed to display them in a time zone of the analyst's choosing.  To choose a timezone, use one of the standard timezone names (such as Europe/London, US/Eastern or most [http://en.wikipedia.org/wiki/List_of_tz_database_time_zones Olson timezones]) with the --tz=TIMEZONE flag.  Volatility attempts to use  [http://pytz.sourceforge.net/ pytz] if installed, otherwise it uses [http://docs.python.org/2/library/time.html#time.tzset tzset]. 

Please note that specifying a timezone will not affect how system-local times are displayed.  If you identify a time that you know is UTC-based, please file it as an issue in the issue tracker.

By default the `_EPROCESS` `CreateTime` and `ExitTime` timestamps are in UTC.  Below is output from Volatility with `pytz` installed:

::

  $ python vol.py -f win7.vmem --profile=Win7SP1x86 pslist
  Volatile Systems Volatility Framework 2.3_alpha
  Offset(V)  Name                    PID   PPID   Thds     Hnds   Sess  Wow64 Start                          Exit                          
  ---------- -------------------- ------ ------ ------ -------- ------ ------ ------------------------------ ------------------------------
  0x84133630 System                    4      0     93      420 ------      0 2011-10-20 15:25:11 UTC+0000                                 
  0x852add40 smss.exe                276      4      4       29 ------      0 2011-10-20 15:25:11 UTC+0000                                 
  0x851d9530 csrss.exe               364    356      9      560      0      0 2011-10-20 15:25:15 UTC+0000                                 
  0x859c8530 wininit.exe             404    356      7       88      0      0 2011-10-20 15:25:16 UTC+0000                                 
  0x859cf530 csrss.exe               416    396     10      236      1      0 2011-10-20 15:25:16 UTC+0000
  [snip]                      


Below is output from the same sample using the `--tz=America/Chicago` option to get Central Standard Time:

::

  $ python vol.py -f win7.vmem --profile=Win7SP1x86 pslist --tz=America/Chicago
  Volatile Systems Volatility Framework 2.3_alpha
  Offset(V)  Name                    PID   PPID   Thds     Hnds   Sess  Wow64 Start                          Exit                          
  ---------- -------------------- ------ ------ ------ -------- ------ ------ ------------------------------ ------------------------------
  0x84133630 System                    4      0     93      420 ------      0 2011-10-20 10:25:11 CDT-0500                                 
  0x852add40 smss.exe                276      4      4       29 ------      0 2011-10-20 10:25:11 CDT-0500                                 
  0x851d9530 csrss.exe               364    356      9      560      0      0 2011-10-20 10:25:15 CDT-0500                                 
  0x859c8530 wininit.exe             404    356      7       88      0      0 2011-10-20 10:25:16 CDT-0500                                 
  0x859cf530 csrss.exe               416    396     10      236      1      0 2011-10-20 10:25:16 CDT-0500  
  [snip] 


Below is the same output above, but without the `pytz` library installed:

::

  $ python2.6 vol.py -f win7.vmem --profile=Win7SP1x86 pslist --tz=America/Chicago
  Volatile Systems Volatility Framework 2.3_alpha
  Offset(V)  Name                    PID   PPID   Thds     Hnds   Sess  Wow64 Start                          Exit                          
  ---------- -------------------- ------ ------ ------ -------- ------ ------ ------------------------------ ------------------------------
  0x84133630 System                    4      0     93      420 ------      0 2011-10-20 10:25:11 CDT                                      
  0x852add40 smss.exe                276      4      4       29 ------      0 2011-10-20 10:25:11 CDT                                      
  0x851d9530 csrss.exe               364    356      9      560      0      0 2011-10-20 10:25:15 CDT                                      
  0x859c8530 wininit.exe             404    356      7       88      0      0 2011-10-20 10:25:16 CDT                                      
  0x859cf530 csrss.exe               416    396     10      236      1      0 2011-10-20 10:25:16 CDT      
  [snip]                                 

=====
Setting the DTB 
===== 

The DTB (Directory Table Base) is what Volatility uses to translate virtual addresses to physical addresses. By default, a kernel DTB is used (from the Idle/System process). If you want to use a different process's DTB when accessing data, supply the address to --dtb=ADDRESS. 

=====
Setting the KDBG Address 
===== 

*This is a Windows-only option*

Volatility scans for the KDDEBUGGER_DATA64 structure using hard-coded signatures "KDBG" and a series of sanity checks. These signatures are not critical for the operating system to function properly, thus malware can overwrite them in attempt to throw off tools that *do* rely on the signature. Additionally, in some cases there may be more than one KDDEBUGGER_DATA64 (for example if you apply a major OS update and don't reboot), which can cause confusion and lead to incorrect process and module listings, among other problems. If you know the address add KDDEBUGGER_DATA64, you can specify it with --kdbg=ADDRESS and this override the automated scans. For more information, see the [http://code.google.com/p/volatility/wiki/CommandReference23#kdbgscan kdbgscan] plugin. 

=====
Setting the KPCR Address
=====

*This is a Windows-only option*

There is one KPCR (Kernel Processor Control Region) for each CPU on a system. Some Volatility plugins display per-processor information. Thus if you want to display data for a specific CPU, for example CPU 3 instead of CPU 1, you can pass the address of that CPU's KPCR with --kpcr=ADDRESS. To locate the KPCRs for all CPUs, see the [http://code.google.com/p/volatility/wiki/CommandReference23#kpcrscan kpcrscan] plugin. Also note that starting in Volatility 2.2, many of the plugins such as [http://code.google.com/p/volatility/wiki/CommandReference23#idt idt] and [http://code.google.com/p/volatility/wiki/CommandReference23#gdt gdt] automatically iterate through the list of KPCRs.

=====
Enabling Write Support
===== 

Write support in Volatility should be used with caution. Therefore, to actually enable it, you must not only type --write on command-line but you must type a "password" in response to a question that you'll be prompted with. In most cases you will not want to use write support since it can lead to corruption or modification of data in your memory dump. However, special cases exist that make this feature really interesting. For example, you could cleanse a live system of certain malware by writing to RAM over firewire, or you could break into a locked workstation by patching bytes in the winlogon DLLs. 

=====
Specifying Additional Plugin Directories
=====

Volatility's plugin architecture can load plugin files from multiple directories at once. In the Volatility source code, most plugins are located in volatility/plugins. However, there is another directory (volatility/contrib) which is reserved for contributions from third party developers, or weakly supported plugins that simply aren't enabled by default. To access these plugins you just type --plugins=contrib/plugins on command-line. It also enables you to create a separate directory of your own plugins that you can manage without having to add/remove/modify files in the core volatility directories. 

*Note:* the parameter to --plugins can also be a zip file containing the plugins such as --plugins=myplugins.zip. _Due to the way plugins are loaded, the external plugins directory or zip file must be specified before any plugin-specific arguments (including the name of the plugin)._  Example:

::

  $ python vol.py --plugins=contrib/plugins -f XPSP3x86.vmem timeliner 


=====
Choosing an Output Format
=====

By default, plugins use text renderers to standard output.  If you want to redirect to a file, you can of course use the console's redirection (i.e. > out.txt) or you could use --output-file=out.txt. The reason you can also choose --output=FORMAT is for allowing plugins to also render output as HTML, JSON, SQL, or whatever you choose. However, there are no plugins with those alternate output formats pre-configured for use, so you'll need to add a function named render_html, render_json, render_sql, respectively to each plugin before using --output=HTML. 

=====
Plugin Specific Options
=====

Many plugins accept arguments of their own, which are independent of the global options.  To see the list of available options, type both the plugin name and -h/--help on command-line. 

::

  $ python vol.py dlllist -h


=====
Using Volatility as a Library
===== 

Although its possible to use Volatility as a library, we hope to support it better in the future. Currently, if you need to import volatility from one of your other python scripts, you can use the following example code:

::

  $ python
  >>> import volatility.conf as conf
  >>> import volatility.registry as registry
  >>> registry.PluginImporter()
  <volatility.registry.PluginImporter object at 0x7f9608f3ac10>
  >>> config = conf.ConfObject()
  >>> import volatility.commands as commands
  >>> import volatility.addrspace as addrspace
  >>> registry.register_global_options(config, commands.Command)
  >>> registry.register_global_options(config, addrspace.BaseAddressSpace)
  >>> config.parse_options()
  >>> config.PROFILE="WinXPSP2x86"
  >>> config.LOCATION = "file:///media/memory/private/image.dmp"
  >>> import volatility.plugins.taskmods as taskmods
  >>> p = taskmods.PSList(config)
  >>> for process in p.calculate():
  ...   print process
  ... 