import pyinotify

from processor import process


class EventHandler(pyinotify.ProcessEvent):
    def process_IN_CREATE(self, event):
        print("Creating:", event.pathname)

    def process_IN_DELETE(self, event):
        print("Removing:", event.pathname)

    def process_IN_MOVED_TO(self, event):
        print("Moved to:", event)


wm = pyinotify.WatchManager()  # Watch Manager
mask = pyinotify.IN_DELETE | pyinotify.IN_CREATE | pyinotify.IN_MOVED_TO

handler = EventHandler()
notifier = pyinotify.Notifier(wm, handler)
wdd = wm.add_watch('/media/data/Dropbox/test', mask, rec=True, auto_add=True)

notifier.loop()