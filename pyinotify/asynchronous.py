import asyncore
import pyinotify
import numpy as np

wm = pyinotify.WatchManager()  # Watch Manager
mask = pyinotify.IN_DELETE | pyinotify.IN_CREATE  # watched events

class EventHandler(pyinotify.ProcessEvent):
    def process_IN_CREATE(self, event):
        print("Creating:", event.pathname)

    def process_IN_DELETE(self, event):
        print("Removing:", event.pathname)

notifier = pyinotify.AsyncNotifier(wm, EventHandler())
wdd = wm.add_watch('/SNS/users/j35/test/', mask, rec=True)

asyncore.loop()
