import os
import sys
from pathlib import Path

cur_path = sys.path[0]

file = open(
    '{}/.local/share/applications/prime-run-selector.desktop'.format(Path.home()), 'w+')
file.write('''[Desktop Entry]
Name= Prime Run Selector
Comment= Simple GUI App for execute any app with prime-run command
Exec= prime-run-selector
Icon= {}/icon/icon.png
Terminal=false
Type=Application
StartupNotify=true'''.format(cur_path))
file.close()

os.system("echo -e '#! /bin/bash\nexec env DISPLAY=$DISPLAY python {}/prime-run-selector.py' | sudo tee /usr/bin/prime-run-selector".format(cur_path))
os.system("sudo chmod +x /usr/bin/prime-run-selector")

print('----------------------\ninstalled successfully\n----------------------')
