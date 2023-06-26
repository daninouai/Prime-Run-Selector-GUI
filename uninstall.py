import os
from pathlib import Path

file_path = '{}/.local/share/applications/prime-run-selector.desktop'.format(Path.home())

if os.path.exists(file_path):
    os.remove(file_path)
    print('----------------------\ndesktop entry removed\n----------------------')
else:
    print('----------------------\ndesktop entry not found!\n----------------------')
