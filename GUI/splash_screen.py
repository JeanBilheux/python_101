from tkinter import *

splash_width = 500
splash_height = 500


splash_root = Tk()

# find the screen size
screen_width = splash_root.winfo_screenwidth()
screen_height = splash_root.winfo_screenheight()

left_position = int(screen_width/2 - splash_width/2)
top_position = int(screen_height/2 - splash_height/2)

splash_root.title("Jupyter notebooks is starting ...")
splash_root.overrideredirect(True) # hide the title bar
splash_root.geometry(f'{splash_width}x{splash_height}+{left_position}+{top_position}')
splash_root.iconbitmap('logo.png')
splash_label = Label(splash_root, text="Splash screen", font=("Helvetica",  18))
splash_label.pack(pady=20)

bg = PhotoImage(file="logo.png")
my_label = Label(splash_root, image=bg)
my_label.place(x=0, y=0, relwidth=1, relheight=1)

# splash screen timer
splash_root.after(3000, splash_root.destroy)

splash_root.mainloop()
