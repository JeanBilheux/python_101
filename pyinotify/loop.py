import pyinotify
import numpy as np

# Instanciate a new WatchManager (will be used to store watches).
wm = pyinotify.WatchManager()
# Associate this WatchManager with a Notifier (will be used to report and
# process events).
notifier = pyinotify.Notifier(wm)
# Add a new watch on /tmp for ALL_EVENTS.
wm.add_watch('/SNS/users/j35/test/', pyinotify.ALL_EVENTS)
# Loop forever and handle events.
notifier.loop()

for i in np.arange(5):
    print(f"{i =}")
    
