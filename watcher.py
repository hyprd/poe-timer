from tkinter.filedialog import askdirectory
from watchdog.events import PatternMatchingEventHandler
from watchdog.observers.polling import PollingObserver
import time, os

class FileModifiedHandler(PatternMatchingEventHandler):
    def on_modified(self, event):
        new_line = seek_last_line(self.patterns[0])
        if "You have entered" in new_line:
            print(new_line)
        return super().on_modified(event)

def seek_last_line(client):
    with open(client, "rb") as file:
        try:
            file.seek(-2, os.SEEK_END)
            while file.read(1) != b'\n':
                file.seek(-2, os.SEEK_CUR)
        except OSError:
            file.seek(0)
        return file.readline().decode()

def main():
    directory = askdirectory(title = 'Path to client.txt')
    patterns = [directory + '/Client.txt']
    event_handler = FileModifiedHandler(patterns = patterns)
    observer = PollingObserver()
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