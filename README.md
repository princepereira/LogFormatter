# LogFormatter
Description: SublimeText3 Plugin to format the structured logs
Author: Prince Pereira
Date: 30-07-2019

1. Install required packages
==============================

wget https://download.sublimetext.com/sublime_text_3_build_3207_x64.tar.bz2
tar xvf sublime_text_3_build_3207_x64.tar.bz2
sudo mv sublime_text_3 /opt/sublime_text
cp /opt/sublime_text/sublime_text.desktop $HOME/Desktop/.
sudo apt-get -y install python3-pip
sudo pip3 install pysftp
sudo pip3 install texttable

# Start sublime text by clicking desktop icon

# Install 'Package Control' in SublimeText by:
#	- Open console by "ctrl+`" shortcut or the View > Show Console
#	- Copy the below code to console and press Enter

#==============================================================>>>>>>>>

import urllib.request,os,hashlib; h = '6f4c264a24d933ce70df5dedcf1dcaee' + 'ebe013ee18cced0ef93d5f746d80ef60'; pf = 'Package Control.sublime-package'; ipp = sublime.installed_packages_path(); urllib.request.install_opener( urllib.request.build_opener( urllib.request.ProxyHandler()) ); by = urllib.request.urlopen( 'http://packagecontrol.io/' + pf.replace(' ', '%20')).read(); dh = hashlib.sha256(by).hexdigest(); print('Error validating download (got %s instead of %s), please try manual install' % (dh, h)) if dh != h else open(os.path.join( ipp, pf), 'wb' ).write(by)

#<<<<<<<<==============================================================

# Restart sublime text again
# Check the installation directory of pip packages. Eg: /usr/local/lib/python3.5/dist-packages/
# Update 'pip-path.txt' in the project path accordingly
# Move the current project to '~/.config/sublime-text-3/Packages/LogFormatter' directory



2. Running the project
=============================

# Press "ctrl+`" for reloading the project whenever any changes are made
# Press "alt+enter" for loading the configuration file where we can provide the options or preferences.
#	- Press "shift+enter" for new line
#	- Press "enter" for saving the preferences
# Open the logs in a window and run the log formatting functionality by "alt+p"



