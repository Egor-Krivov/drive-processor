import sys
import datetime
from os.path import abspath, relpath, join, exists, dirname
from os import makedirs

import pyinotify


class EventHandler(pyinotify.ProcessEvent):
    def my_init(self, raw_path: str, processed_path: str, process: callable,
                log: callable):
        log('Processing folders:\n\tfrom:{}\n\tto:{}'.
            format(raw_path, processed_path))
        self.__raw_path = abspath(raw_path)
        self.__processed_path = abspath(processed_path)
        self.__process = process
        self.__log = log

    def process_IN_CREATE(self, event):
        self.__process_file(event.pathname)

    def process_IN_MOVED_TO(self, event):
        self.__process_file(event.pathname)

    def process_IN_DELETE(self, event):
        self.__delete_file(event.pathname)

    def process_IN_MOVED_FROM(self, event):
        self.__delete_file(event.pathname)

    def __process_file(self, path):
        log = self.__log
        new_path = join(self.__processed_path, relpath(path, self.__raw_path))
        new_path = abspath(new_path)
        new_path_dir = dirname(new_path)
        if not exists(new_path_dir):
            makedirs(new_path_dir)
        log('processing:\n\tfrom:{}\n\tto:{}'.format(path, new_path))
        self.__process(path, new_path)
        log('is complete')

    def __delete_file(self, path):
        log = self.__log
        log('file {} was deleted'.format(path))


def monitor_folder(raw_path: str, processed_path: str, process: callable,
                  logfile: object=sys.stdout):
    """Monitor 'raw_path' for new files. Each of new files are processed with
    'process' function [process(path_in, path_out)] and placed in
    'processed_path' folder, preserving structure.

    Parameters
    ----------
    raw_path:
        Path to the folder to monitor.

    processed_path:
        Path to the folder to place processed files.

    process: Callable(path_in, path_out)
        Function, that process file in 'path_in' and place result to path_out

    logfile: object
        Opened logfile. If None, there is no logging.
    """
    if logfile is not None:
        time = datetime.datetime.now

        def log(*args):
            print(*(time(), *args), flush=True, file=logfile)
    else:
        def log(*args):
            pass
    log('Monitor drive started')
    wm = pyinotify.WatchManager()  # Watch Manager

    # pevent parameter helps not to process directories
    handler = EventHandler(raw_path=raw_path, processed_path=processed_path,
                           process=process, log=log, pevent=lambda x: x.dir)
    notifier = pyinotify.Notifier(wm, handler)

    mask = pyinotify.IN_CREATE | pyinotify.IN_MOVED_TO
    mask |= pyinotify.IN_DELETE | pyinotify.IN_MOVED_FROM
    wdd = wm.add_watch(raw_path, mask, rec=True, auto_add=True)

    # endless loop
    notifier.loop()
