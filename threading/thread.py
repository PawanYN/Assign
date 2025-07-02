import threading
import time
from concurrent.futures import ThreadPoolExecutor


def worker(number):
    print(f"calculating the result for number {number}")
    print("")
    time.sleep(2)
    return number**2

pool=ThreadPoolExecutor(2)
work1=pool.submit(worker,7)
work2=pool.submit(worker,9)
work3=pool.submit(worker,5)
work4=pool.submit(worker,5)
work5=pool.submit(worker,8)
work6=pool.submit(worker,5)
work7=pool.submit(worker,11)
work8=pool.submit(worker,4)
work9=pool.submit(worker,6)
print("Hare krishna")
print("Hare krishna")


if work3.done():
    print(work3.result())
else:
    print("No result yet")
    
time.sleep(5)
if work3.done():
    print(work3.result())
    

# def worker():
    
#     time.sleep(2)
#     print("done")

# t1=threading.Thread(target=worker)
# t1.start()

# t2=threading.Thread(target=worker)
# t2.start()

# t3=threading.Thread(target=worker)
# t3.start()

# t4=threading.Thread(target=worker)
# t4.start()