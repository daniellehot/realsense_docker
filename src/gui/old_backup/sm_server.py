import tkinter as tk
from tkinter import ttk
from multiprocessing import shared_memory
import numpy as np

# https://stackoverflow.com/questions/72754287/python-shared-memory-how-can-i-put-the-random-integer-into-the-shared-memory-bl
# https://docs.python.org/3/library/multiprocessing.shared_memory.html

save_flag = 0
arr = np.ndarray(1)
print(arr.nbytes)

try:
    shm = shared_memory.SharedMemory(create = True, name="shared_space", size=arr.nbytes)
except:
    shm = shared_memory.SharedMemory(create = False, name="shared_space", size=arr.nbytes)

shm_arr = np.ndarray(arr.shape, dtype=arr.dtype, buffer=shm.buf)


def save_data():
    arr[0] += 1
    shm_arr = arr
    print(shm_arr)

# root window
root = tk.Tk()
root.geometry('300x200')
root.resizable(False, False)
root.title('Button Demo')

# exit button
save_button = ttk.Button(
    root,
    text='Save',
    command=save_data
)

save_button.pack(
    ipadx=5,
    ipady=5,
    expand=True
)

try:
    root.mainloop()
except KeyboardInterrupt:
    shm.close()
    shm.unlink()
    root.quit()