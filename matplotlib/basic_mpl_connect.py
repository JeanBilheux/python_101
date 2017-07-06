from __future__ import print_function
import matplotlib.pyplot as plt
import numpy as np

def process_key(event):
    print("Key:", event.key)

def process_button(event):
    print("Button:", event.x, event.y, event.xdata, event.ydata, event.button)

def resize_figure(event):
    print("Resizing figure")
    
def closing_figure(event):
    print("Closing figure")

def entering_figure(event):
    print("Entering figure")

def leaving_figure(event):
    print("Leaving figure")

fig, ax = plt.subplots(1, 1)
x = np.arange(10)
y = np.cos(x)
ax.scatter(x,y)
fig.canvas.mpl_connect('key_press_event', process_key) #not working
fig.canvas.mpl_connect('button_press_event', process_button) 
fig.canvas.mpl_connect('resize_event', resize_figure)  #not working
fig.canvas.mpl_connect('close_event', closing_figure)
fig.canvas.mpl_connect('figure_enter_event', entering_figure)
fig.canvas.mpl_connect('figure_leave_event', leaving_figure)

plt.show()
