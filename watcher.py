from tkinter.filedialog import askdirectory
from watchdog.events import PatternMatchingEventHandler
from watchdog.observers.polling import PollingObserver

import tkinter as tk
import time
from collections import deque

window = tk.Tk()
window.attributes('-topmost', True)

instance_label = tk.Label(window, text="(current instance)")
instance_label.pack()

time_label = tk.Label(window, text="(timer)")
time_label.pack()   
    
client = ''
current_instance = ''
timer_started = False
elapsed_time = 0
start_time = 0
stopwatch_time = 0

def timer():
    global stopwatch_time
    stopwatch_time += 1
    time_label.configure(text = stopwatch_time)
    time_label.after(1000, timer)
    
class FileModifiedHandler(PatternMatchingEventHandler):
    def on_modified(self, event):
        global client, current_instance, elapsed_time, start_time, timer_started, stopwatch_time
        with open(client, encoding='utf-8') as file:
            client_contents = deque(file, 2)
        # The watchdog poller sometimes skips over the instance transition string. Deque for the 
        # last two lines will capture it properly.
        for i in range(2):    
            if "You have entered" in client_contents[i] and client_contents[i] != current_instance:
                current_instance = client_contents[i]
                stopwatch_time = 0
                if not timer_started:
                    timer_started = True
                    start_time = time.perf_counter()
                    timer()
                elif timer_started:
                    timer_started = False
                    elapsed_time = time.perf_counter() - start_time
                
                instance_label['text'] = client_contents[i].partition('entered ')[2].replace('.', '')
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
    
    window.mainloop()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
if __name__ == '__main__':
    main()
    