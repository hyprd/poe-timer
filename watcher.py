from tkinter.filedialog import askdirectory
from watchdog.events import PatternMatchingEventHandler
from watchdog.observers.polling import PollingObserver

import tkinter as tk
import time, os

timer_started = False
start = 0
elapsed_time = 0

window = tk.Tk()
timeLabel = tk.Label(window, text="text")
timeLabel.pack()
t = 0
halt_timer = False

class FileModifiedHandler(PatternMatchingEventHandler):
    def on_modified(self, event):
        global elapsed_time, start, timer_started, halt_timer
        new_line = seek_last_line(self.patterns[0])
        if "You have entered" in new_line:
            if not timer_started:
                halt_timer = False
                print('Timer started')
                tick()
                start = time.perf_counter()
                timer_started = True
                
            elif timer_started:
                print('Timer finished')
                elapsed_time = round(time.perf_counter() - start, 2)
                print(elapsed_time)
                timer_started = False
                halt_timer = True
                
        return super().on_modified(event)

def tick():
    global t
    global halt_timer
    t += 1
    timeLabel['text'] = t
    if not halt_timer:
        timeLabel.after(1000, tick)

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
    observer.schedule(event_handler, directory)
    observer.start()
    window.mainloop()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
if __name__ == '__main__':
    main()