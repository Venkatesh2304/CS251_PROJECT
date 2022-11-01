import threading
import queue
import time 
q = queue.Queue()

def worker():
    while True:
        item = q.get()
        print(f'Working on {item}')
        print(f'Finished {item}')
        time.sleep(1)
        q.task_done()

# Turn-on the worker thread.
threading.Thread(target=worker, daemon=True).start()

# Send thirty task requests to the worker.
for item in range(30):
    q.put(item)


# Block until all tasks are done.
q.join()
for item in range(40,50) : 
     q.put(item)
for i in range(20) : 
    print(i)
q.join()
print('All work completed')