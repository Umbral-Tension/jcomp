

import os
import json
import subprocess
import shlex
from jtools.jconsole import test, ptest

display_server = os.environ['XDG_SESSION_TYPE'].casefold() # wayland or x11
if display_server == 'wayland':
    import window_manager.wm_wayland as wm
else:
    import window_manager.wm_xorg as wm


basedir = os.path.dirname(__file__)
with open(os.path.join(basedir, '../../resources/paths.json')) as fp:
    paths = json.load(fp)


def open(name, *args):
    """"
    Open a program/website or switch to it if it already exists. 

    @param name: one of the programs or websites named in resources/paths.json
    """
    name = name.casefold()
    try:
        exec_cmd = paths[name]['exec_cmd']
        if display_server == 'wayland':
            window_title = paths[name]['wayland_window_title']
        else:
            window_title = paths[name]['window_title']
    except KeyError:
        os.system(f'zenity --warning --text="{name} not found in the file paths.json" --title="window_manager.py"')
        return
    
    # Activate the program window if it's already running
    if wm.win_exists(window_title):
        wm.win_activate(window_title)
        return

    # Single website opening
    if exec_cmd.casefold().startswith('http'):
        browser = paths['firefox']['exec_cmd']
        exec_cmd = f'{browser} {exec_cmd}'
    
    os.system(exec_cmd + ' &')