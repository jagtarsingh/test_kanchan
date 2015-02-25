# Copyright (C) 2006-2013 Wyplay, All Rights Reserved.
# This source code and any compilation or derivative thereof is the
# proprietary information of Wyplay and is confidential in nature.
# Under no circumstances is this software to be exposed to or placed under
# an Open Source License of any type without the expressed written permission
# of Wyplay.


from wyvas import Canvas, Text, Window, Image
import commands
from peewee.notifier import loop, events_watch
from mal.input import init
import os
import time
import subprocess

init(['stdin'])

global display

def initGraphics():
    global display
    resolution = (1280,720)
    display = Canvas(resolution, 25)

    mytext = Text(font="Wyplay", size=24)
    mytext.set_text("Press 'd' keyboard key to show browsers when finished to launch")
    display.add_child(mytext)
    mytext.move(10, 600)

    mytext = Text(font="Wyplay", size=24)
    mytext.set_text("Press 't' keyboard key to switch focus between wybar and background web site")
    display.add_child(mytext)
    mytext.move(10, 650)

global focused_window
global window1
global window2
global browser_wybar_cmdline
global browser_background_cmdline
global browser_background_pid
global browser_wybar_pid

focused_window = None
window1 = None
window2 = None
browser_wybar_cmdline = ["WebkitLauncher", "-t", "http://web-request-qualif.abx1012-corev2.wyplay.com/simple-renderer/bar.php?imei=20110301&product=WBD002240AA&sn=112233445566&version=001.005.00000.0000000033&lang=en&wstester=true"]
#browser_background_cmdline = ["WebkitLauncher", "-t","http://172.16.10.141/geo"]
browser_background_cmdline = ["WebkitLauncher", "-t","http://web-request-qualif.abx1012-corev2.wyplay.com/apps/rssreader/public/video?rss=video_geo"]
browser_background_pid = 0
browser_wybar_pid = 0

def launchProcess(commandline):
    return subprocess.Popen(commandline)

def launchProcesses():
    global browser_wybar_cmdline
    global browser_background_cmdline
    global browser_background_pid
    global browser_wybar_pid
    p = launchProcess(browser_background_cmdline)
    browser_background_pid = p.pid
    p = launchProcess(browser_wybar_cmdline)
    browser_wybar_pid = p.pid

def grabProcesses():
    global display
    global focused_window
    global window1
    global window2
    global browser_background_pid
    global browser_wybar_pid
    process_name="WebkitLauncher"
    use_pidof = False
    if use_pidof:
        result = commands.getoutput('pidof %s' % process_name)
        print "result = %s" % result
        result = result.split()
    else:
        result = [browser_background_pid, browser_wybar_pid]

    width = 1280
    height = 720
    x = 0
    y = 0
    for pid in result:
        print "pid = ", pid
        win = Window(int(pid))
        display.add_child(win)
        win.move(x, y)
        win.set_volume(width, height)
        #x = x + width / 3 + 10
        #y = y + height / 3
        #x = x + 450
        #y = y + 50
        if window1 == None:
            window1 = win
        elif window2 == None:
            window2 = win
    if window2 <> None:
        focused_window = window2
        focused_window.set_focus()
    if window2 <> None:
        print "TRASNPARENNN"
        #window2.set_color(a=128)
        window2.set_blend(1)

    #myimage = Image()
    #myimage.load(url="http://backtooriginal.files.wordpress.com/2011/04/toto.jpg")
    #display.add_child(myimage)
    #myimage.move(300, 100)
    #myimage.set_volume(400, 100)
    #myimage.set_color(a=180)


def switch_focus():
    global focused_window
    global window1
    global window2
    print "switch_focus"
    print "focused_window = ", focused_window
    print "window1 = ", window1
    print "window2 = ", window2
    if focused_window == window1:
        focused_window = window2
    elif focused_window == window2:
        focused_window = window1
    else:
        focused_window = None
    if focused_window <> None:
        print "set_focus"
        focused_window.set_focus()

def send_event(event_name):
    global focused_window
    print "send_event ", event_name
    if focused_window <> None:
        print "OK"
        focused_window.send_event(key=event_name, status="press")

def got_event(ev):
    if ev.name == "DEBUG":
        grabProcesses()
    elif ev.name == "TOGGLE_MENU":
        switch_focus()
    elif ev.name == "LEFT":
        send_event("CURSOR_LEFT")
    elif ev.name == "RIGHT":
        send_event("CURSOR_RIGHT")
    elif ev.name == "UP":
        send_event("CURSOR_UP")
    elif ev.name == "DOWN":
        send_event("CURSOR_DOWN")
    elif ev.name == "SELECT":
        send_event("ENTER")
    #elif ev.name == "PREVIOUS":
    #    launchProcesses()
    else:
        print "Event = ", ev
    """
    elif ev.name == "short_DEBUG":
        print "Received : short_DEBUG"
    else:
        print "Event = ", ev
    """


initGraphics()
launchProcesses()

events_watch(got_event)

print "Begin loop"

loop()

