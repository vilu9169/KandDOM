import threading
import time

def wait_and_hi(index):
    #time.sleep(1)
    print("hi", index)

threads = [threading.Thread(target=wait_and_hi, args=[x]) for x in range(50000)]

start = time.time()

for thread in threads:
    thread.start()


for thread in threads:
    thread.join()



print("done in", time.time() - start, "seconds")