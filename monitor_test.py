import datetime
from shutil import copyfile

from monitor import monitor_folder

if __name__ == '__main__':
    raw_path = '/media/data/Dropbox/raw'
    processed_path = '/media/data/Dropbox/processed'

    with open('log_' + str(datetime.datetime.now()), 'w') as logfile:
        monitor_folder(raw_path, processed_path, copyfile, logfile)
