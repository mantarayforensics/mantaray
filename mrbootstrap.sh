#!/bin/sh
SUDO_USER=$USER

usage() {
	echo "MantaRay Boostrap Script"
	echo
	echo "usage"
	echo
	echo "h - print this message"
	echo "s - install the skin"
	echo "i - install the tools"
	exit 0
}

update_and_install(){
	## Update
	sudo apt-get update && sudo apt-get upgrade -y  || { echo "Upgrade command failed - Is dpkg locked? Please re-run the bootsrap script"; exit 1; }

	## Add Repositories
	sudo apt-add-repository -y ppa:mantaray/stable
	sudo apt-add-repository -y ppa:sift/stable

	## Stop popup windows
	sudo gsettings set org.gnome.desktop.media-handling automount false && sudo gsettings set org.gnome.desktop.media-handling automount-open false

	## Update and Upgrade
	sudo apt-get update && sudo apt-get upgrade -y || { echo "Upgrade command failed - Is dpkg locked? Please re-run the bootsrap script"; exit 1; }

	## Create mount directories
	for NUM in 1 2 3 4 5
	do
		if [ ! -d /mnt/windows_mount$NUM ]; then
			sudo mkdir -p /mnt/windows_mount$NUM
		fi
		if [ ! -d /mnt/ewf$NUM ]; then
			sudo mkdir -p /mnt/ewf$NUM
		fi
	done

	for NUM in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30
	do
		if [ ! -d /mnt/shadow/vss$NUM ]; then
			sudo mkdir -p /mnt/shadow/vss$NUM
		fi
		if [ ! -d /mnt/shadow_mount/vss$NUM ]; then
			sudo mkdir -p /mnt/shadow_mount/vss$NUM
		fi
	done

	## Install packages
	sudo apt-get -y install mantaray python-pip git || { echo "Install command failed - Is dpkg locked? Please re-run the bootsrap script"; exit 1; }

	## Install pip requirements
	sudo pip install rekall
	sudo pip install docopt
	sudo pip install python-evtx
	sudo pip install python-registry

	## Install icons on sidebar
	sudo -u $SUDO_USER dconf write /desktop/unity/launcher/favorites "['nautilus.desktop', 'gnome-terminal.desktop', 'MantaRay.desktop', 'firefox.desktop', 'gnome-screenshot.desktop', 'gcalctool.desktop', 'gedit.desktop']"

	## Place icon on Desktop
	cp /usr/share/applications/MantaRay.desktop /home/$SUDO_USER/Desktop
	chmod +x /home/$SUDO_USER/Desktop/MantaRay.desktop

	## Convert rr plugins
	sudo dos2unix -ascii /usr/share/regripper/*

	## Link binaries
	if [ ! -L /usr/bin/mount_ewf.py ] && [ ! -e /usr/bin/mount_ewf.py ]; then
		sudo ln -s /usr/bin/ewfmount /usr/bin/mount_ewf.py
	fi
	if [ ! -L /usr/bin/vol.py ]; then
		sudo ln -s /usr/bin/vol /usr/bin/vol.py
	fi
	if [ ! -L /usr/bin/log2timeline ]; then
		sudo ln -s /usr/bin/log2timeline_legacy /usr/bin/log2timeline
	fi

	## Git other needed files
	sudo git clone https://github.com/sans-dfir/sift-files /tmp/sift-files
	cd /tmp/sift-files
	sudo bash install.sh
	sudo rm -r -f /tmp/sift-files
}

install_theme(){

	## Install background for theme
	sudo -u $SUDO_USER gsettings set org.gnome.desktop.background picture-uri file:///usr/share/mantaray/images/Mantaray_Logo_Template_Full_Screen.gif

	sudo gsettings set com.canonical.unity-greeter background file:///usr/share/mantaray/images/Mantaray_Logo_Template_Full_Screen.gif

	## Chage Hostname
	OLD_HOSTNAME=$(hostname)
	sudo sed -i "s/$OLD_HOSTNAME/mantaray/g" /etc/hosts
	sudo sed -i "s/$OLD_HOSTNAME/mantaray/g" /etc/hostname
	sudo hostname mantaray

}

SKIN=0
INSTALL=0

while getopts ":hvsi" opt
do
case "${opt}" in
    h ) usage; exit 1;;
    v ) echo "$0 -- Version 20140524"; exit 0 ;;
    s ) SKIN=1 ;;
    i ) INSTALL=1 ;;
    \?) echo
        echoerror "Option does not exist: $OPTARG"
        usage
        exit 1
        ;;
esac
done

if [ "$INSTALL" -eq 1 ]; then
	update_and_install
	if [ "$SKIN" -eq 1 ]; then
		install_theme
	fi

	echo "Completed installation."
	echo "Please restart your machine in order to complete installation"
	echo "Run: sudo reboot"
fi

