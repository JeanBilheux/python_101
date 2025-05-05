# Notifier example from tutorial
#
# See: http://github.com/seb-m/pyinotify/wiki/Tutorial
#
import pyinotify

wm = pyinotify.WatchManager()  # Watch Manager
mask = pyinotify.IN_DELETE | pyinotify.IN_CREATE  # watched events

class EventHandler(pyinotify.ProcessEvent):
    def process_IN_CREATE(self, event):
        print("Creating:", event.pathname)

    def process_IN_DELETE(self, event):
        print("Removing:", event.pathname)

handler = EventHandler()
notifier = pyinotify.Notifier(wm, handler, timeout=100000)
wdd = wm.add_watch('/SNS/users/j35/test', mask, rec=True)

# def quick_check(notifier):
#             assert notifier._timeout is not None, 'Notifier must be constructed with a short timeout'
#             notifier.process_events()
#             while notifier.check_events():  #loop in case more events appear while we are processing
#                   notifier.read_events()
#                   notifier.process_events()

# quick_check(notifier)

notifier.loop()


for i in np.arange(10):
    print(f"{i =}")
