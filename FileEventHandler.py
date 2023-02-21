import os
from watchdog.events import FileSystemEventHandler
from FileEvent import FileEvent


class FileEventHandler(FileSystemEventHandler):
    def __init__(self, fileEventQueue):
        self.fileEventQueue = fileEventQueue

    # @staticmethod
    # def on_any_event(event):
    #     if event.event_type == 'moved':
    #         print('%s  %s  %s' % (event.event_type, event.src_path, event.dest_path))
    #     else:
    #         print('%s  %s' % (event.event_type, event.src_path))

    def filter_event(self, event):
        if event.is_directory:
            return 1
        if event.src_path.endswith('.TMP') or event.src_path.endswith('~tmp'):
            return 1
        return 0

    def on_moved(self, event):
        if event.dest_path.endswith('.TMP') or self.filter_event(event):
            return None

        self.fileEventQueue.put(FileEvent('moved', event.src_path, event.dest_path))

    def on_created(self, event):
        if self.filter_event(event):
            return None

        self.fileEventQueue.put(FileEvent('created', event.src_path))


    def on_deleted(self, event):
        if self.filter_event(event):
            return None

        self.fileEventQueue.put(FileEvent('deleted', event.src_path))


