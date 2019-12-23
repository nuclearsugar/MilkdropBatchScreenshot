#!/usr/bin/env python

import os
import shutil
import sys
import time
import win32con

from pywinauto.application import Application
from os.path import join as pjoin

INPUT_DELAY = 0.25
WINAMP_BASE_DIR = pjoin("C:\\", "Program Files (x86)", "Winamp")
WINAMP_MILKDROP_DIR = pjoin(WINAMP_BASE_DIR, "Plugins", "Milkdrop2")

WINAMP_EXE = pjoin(WINAMP_BASE_DIR, "winamp.exe")
PRESETS_DIR = pjoin(WINAMP_MILKDROP_DIR, "presets")
PRESETS_TODO_DIR = pjoin(PRESETS_DIR, "TODO")
PRESETS_DONE_DIR = pjoin(PRESETS_DIR, "DONE")
PRESETS_PRIOR_DIR = pjoin(PRESETS_DIR, "PRIOR")
PRESETS_SCREENSHOTS_DIR = pjoin(PRESETS_DIR, "SCREENSHOTS")

##
## Winamp shortcuts
##
# b - next song
# z - previous song
# x - play
# v - stop
# ctrl-shift-k - show visualizer
# alt-l - library


# Raw events, vs type_keys, for shortcuts required for some reason
def send_raw_key(window, key, delay=INPUT_DELAY):
    if len(key) != 1:
        raise Exception("Key must be of length 1: " + key)
    window.post_message(win32con.WM_KEYDOWN, ord(key), 0x002D0001)
    time.sleep(delay)
    print "posted", key, "down"
    window.post_message(win32con.WM_KEYUP, ord(key), 0xC02D0001)
    time.sleep(delay)
    print "posted", key, "up"

def type_keys(window, keys, delay=INPUT_DELAY):
    window.type_keys(keys)
    time.sleep(delay)
    print "typed", keys


def move_existing_presets():
    prior_dir_exists = False
    # Move any existing presets to backup location
    moved_count = 0
    for f in os.listdir(PRESETS_DIR):
        if f.endswith(".milk"):
            if not prior_dir_exists:
                if os.path.exists(PRESETS_PRIOR_DIR):
                    prior_dir_exists = True
                else:
                    os.mkdir(PRESETS_PRIOR_DIR)
            shutil.move(pjoin(PRESETS_DIR, f), pjoin(PRESETS_PRIOR_DIR, f))
            moved_count += 1
    if moved_count > 0:
        print "Moved", moved_count, "existing presets into", PRESETS_PRIOR_DIR 


# Sanity check expected directories
for p in (WINAMP_EXE, PRESETS_TODO_DIR, PRESETS_DONE_DIR):
    if not os.path.exists(p):
        print "Path does not exists:", p
        sys.exit(1)

move_existing_presets()

if not os.path.exists(PRESETS_SCREENSHOTS_DIR):
    os.mkdir(PRESETS_SCREENSHOTS_DIR)

# Input presets
todo_presets = []
for p in os.listdir(PRESETS_TODO_DIR):
    todo_presets.append(p)

print "Found", len(todo_presets), "TODO presets"

for pi,p in enumerate(todo_presets):
    print "Capturing preset (%d/%d): %s" % (pi+1, len(todo_presets), p)
    shutil.move(pjoin(PRESETS_TODO_DIR, p), pjoin(PRESETS_DIR, p))

    # Run winamp
    app = Application().start(WINAMP_EXE)
    main_window = app.top_window()
    time.sleep(INPUT_DELAY)
    
    while True:
        # Show visualizer: ctrl-shift-k
        type_keys(main_window, "^+k")
        time.sleep(INPUT_DELAY)
        
        # Find MilkDrop via window name/caption (hacky but it works)
        vis_window = app.top_window()
        if vis_window.exists():
            break
    
    # Play song: x
    time.sleep(INPUT_DELAY)
    send_raw_key(main_window, "X")

    # TODO: Check for "open url" window (where is ctrl-l coming from?)
    
    # Three screenshots
    for i in range(1,4):
        # Wait
        time.sleep(2)
        # Screenshot
        suffix = "_screenshot" + str(i)
        print suffix
        full_name = pjoin(PRESETS_SCREENSHOTS_DIR, p + suffix + ".png")
        vis_window.capture_as_image().save(full_name)
    
    # Hide visualizer to clear: alt-l
    # alt (i.e. "%") is sometimes flaky so "Open files" window pops up, close it and retry
    #while True:
    #    type_keys(main_window, "%l")
    #    open_files = app.open_files
    #    if open_files.exists():
    #        open_files.close()
    #        time.sleep(INPUT_DELAY*2)
    #    else:
    #        break
    
    # Kill app
    # Force kill
    app.kill()
    # Exit: Alt-F4
    #type_keys(main_window, "%{F4}")

    # Move to done
    shutil.move(pjoin(PRESETS_DIR, p), pjoin(PRESETS_DONE_DIR, p))
    print

