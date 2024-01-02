from tkinter.filedialog import askdirectory
from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer
import time

class FileModifiedHandler(PatternMatchingEventHandler):
    def on_modified(self, event):
        print("File was modified.")
        return super().on_modified(event)

def main():
    directory = askdirectory(title = 'Path to client.txt')
    patterns = [directory + '/Client.txt']
    event_handler = FileModifiedHandler(patterns = patterns)
    observer = Observer()
    observer.schedule(event_handler, directory, recursive = True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    
    
if __name__ == '__main__':
    main()