try: #python3 imports
	import tkinter as tk
except ImportError: #python3 failed, try python2 imports
	import Tkinter as tk

class Main(tk.Frame):
	def __init__(self, master):
		tk.Frame.__init__(self, master)
		
		lbl = tk.Label(self, text="this is the main frame")
		lbl.pack()
		
		btn = tk.Button(self, text='click me', command=self.popup)
		btn.pack()
	
	def popup(self):
		Popup(self)
		
class Popup(tk.Toplevel):
	def __init__(self, master):
		tk.Toplevel.__init__(self, master)
		
		lbl = tk.Label(self, text="this is the popup")
		lbl.pack()
		
		btn = tk.Button(self, text="OK", command=self.destroy)
		btn.pack()
		
		self.transient(master) #set to be on top of the main window
		self.grab_set() #hijack all commands from the master (clicks on the main window are ignored)
		master.wait_window(self) #pause anything on the main window until this one closes (optional)

def main():
	root = tk.Tk()
	window = Main(root)
	window.pack()
	root.mainloop()

if __name__ == '__main__':
	main()