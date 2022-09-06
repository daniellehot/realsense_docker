from multiprocessing import shared_memory
import numpy as np
import time

existing_shm = shared_memory.SharedMemory(name='shared_space')
c = existing_shm.buf
try:
    while True:
        print(c)
        time.sleep(1.0)
except KeyboardInterrupt:
    print('interrupted!')
    existing_shm.close()
    #existing_shm.unlink()