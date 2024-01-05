from tkinter.filedialog import askdirectory
from watchdog.events import PatternMatchingEventHandler
from watchdog.observers.polling import PollingObserver
from datetime import datetime
from collections import deque

import logging
import tkinter as tk
import time

window = tk.Tk()
window.attributes('-topmost', True)

instance_label = tk.Label(window, text="(current instance)")
instance_label.pack()

time_label = tk.Label(window, text="(timer)")
time_label.pack()   
    
client = ''
current_instance = ''
timestamp = ''
timer_started = False
stopwatch_time = 0

def timer():
    global stopwatch_time
    stopwatch_time += 1
    time_label.configure(text = stopwatch_time)
    time_label.after(1000, timer)
    
class FileModifiedHandler(PatternMatchingEventHandler):
    def on_modified(self, event):
        global client, current_instance, timer_started, stopwatch_time, timestamp
        with open(client, encoding='utf-8') as file:
            client_contents = deque(file, 2)
        # The watchdog poller sometimes skips over the instance transition string. Deque for the 
        # last two lines will capture it properly.
        for i in range(2):    
            if "You have entered" in client_contents[i] and client_contents[i] != current_instance:
                current_instance = client_contents[i]
                current_instance_formatted = client_contents[i].partition('entered ')[2].replace('.', '').strip()
                stopwatch_time = 0
                if not timer_started:
                    timer_started = True
                    timestamp = datetime.now()
                    timer()
                elif timer_started:
                    timer_started = False
                    elapsed = str(datetime.now() - timestamp)
                    logging.info("Entered %s for %s", current_instance_formatted, elapsed)
                instance_label['text'] = current_instance_formatted
            else:
                continue
               
def main():
    global client
    directory = askdirectory(title = 'Path to client.txt')
    patterns = [directory + '/Client.txt']
    client = patterns[0]
    event_handler = FileModifiedHandler(patterns = patterns)
    observer = PollingObserver()
    observer.schedule(event_handler, directory)
    observer.start()
    logging.basicConfig(filename = 'times.log', filemode = 'a', datefmt = '%H:%M:%S', format='[%(asctime)s] %(message)s', level = logging.INFO)
    window.mainloop()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
if __name__ == '__main__':
    main()
    