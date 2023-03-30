import tkinter as tk
from tkinter import ttk 

class EditDescription1Dialog(tk.Tk):
    def __init__(self, mainFrame):
        self._app = mainFrame.app
        self._window = mainFrame.window
        self._currentItemPath = mainFrame.get_current_item_path()
        self._currentItemName = mainFrame.get_current_item_name()

        tk.Tk.__init__(self)
        self.winfo_toplevel().title("Edit Description 1")
        self.winfo_toplevel().geometry("350x150+500+200")
        f = tk.Frame(self, bg='white')

        # Label
        self.label = tk.Label(f, bg='white', fg='black', text="Description 1:")
        self.label.place(x = 10, y = 10, anchor='nw')

        # Text Input
        self.entry = tk.Entry(f, bg='white', fg='black', borderwidth=2, width=53)
        self.entry.place(x = 10, y = 50, anchor='nw')

        # Button
        self.okButton = ttk.Button(f, text="OK", width=10, command= lambda: self.editDescription1())
        self.okButton.place(x = 60, y = 100, anchor='nw')

        # Close Button
        self.closeButton = ttk.Button(f, text="Cancel", width=10, command= self.kill)
        self.closeButton.place(x = 200, y = 100, anchor='nw')

        f.pack(fill = 'both', expand=1)
        self.after(500, lambda: self.focus_force())
    
    def editDescription1(self):
        self._app.edit_description(1, self.entry.get(), self._currentItemPath, self._currentItemName)
        self._window.refresh_view()
        self.kill()
        
    def kill(self):
        self.winfo_toplevel().destroy()
    

class EditDescription2Dialog(tk.Tk):
    def __init__(self, mainFrame):
        self._app = mainFrame.app
        self._window = mainFrame.window
        self._currentItemPath = mainFrame.get_current_item_path()
        self._currentItemName = mainFrame.get_current_item_name()

        tk.Tk.__init__(self)
        self.winfo_toplevel().title("Edit Description 2")
        self.winfo_toplevel().geometry("350x150+500+200")
        f = tk.Frame(self, bg='white')

        # Label
        self.label = tk.Label(f, bg='white', fg='black', text="Description 2:")
        self.label.place(x = 10, y = 10, anchor='nw')

        # Text Input
        self.entry = tk.Entry(f, bg='white', fg='black', borderwidth=2, width=53)
        self.entry.place(x = 10, y = 50, anchor='nw')

        # Button
        self.okButton = ttk.Button(f, text="OK", width=10, command= lambda: self.editDescription2())
        self.okButton.place(x = 60, y = 100, anchor='nw')

        # Close Button
        self.closeButton = ttk.Button(f, text="Cancel", width=10, command= self.kill)
        self.closeButton.place(x = 200, y = 100, anchor='nw')

        f.pack(fill = 'both', expand=1)
        self.after(500, lambda: self.focus_force())
    
    def editDescription2(self):
        self._app.edit_description(2, self.entry.get(), self._currentItemPath, self._currentItemName)
        self._window.refresh_view()
        self.kill()

    def kill(self):
        self.winfo_toplevel().destroy()
    


class EditDescription3Dialog(tk.Tk):
    def __init__(self, mainFrame):
        self._app = mainFrame.app
        self._window = mainFrame.window
        self._currentItemPath = mainFrame.get_current_item_path()
        self._currentItemName = mainFrame.get_current_item_name()

        tk.Tk.__init__(self)
        self.winfo_toplevel().title("Edit Description 3")
        self.winfo_toplevel().geometry("350x150+500+200")
        f = tk.Frame(self, bg='white')

        # Label
        self.label = tk.Label(f, bg='white', fg='black', text="Description 3:")
        self.label.place(x = 10, y = 10, anchor='nw')

        # Text Input
        self.entry = tk.Entry(f, bg='white', fg='black', borderwidth=2, width=53)
        self.entry.place(x = 10, y = 50, anchor='nw')

        # Button
        self.okButton = ttk.Button(f, text="OK", width=10, command= lambda: self.editDescription3())
        self.okButton.place(x = 60, y = 100, anchor='nw')

        # Close Button
        self.closeButton = ttk.Button(f, text="Cancel", width=10, command= self.kill)
        self.closeButton.place(x = 200, y = 100, anchor='nw')

        f.pack(fill = 'both', expand=1)
        self.after(500, lambda: self.focus_force())
    
    def editDescription3(self):
        self._app.edit_description(3, self.entry.get(), self._currentItemPath, self._currentItemName)
        self._window.refresh_view()
        self.kill()

    def kill(self):
        self.winfo_toplevel().destroy()
    







class EditSectionDialog(tk.Tk):
    def __init__(self, mainFrame):
        self._app = mainFrame.app
        self._window = mainFrame.window
        self._currentItemPath = mainFrame.get_current_item_path()
        self._currentItemName = mainFrame.get_current_item_name()

        tk.Tk.__init__(self)
        self.winfo_toplevel().title("Edit Section")
        self.winfo_toplevel().geometry("350x150+500+200")
        f = tk.Frame(self, bg='white')

        # Label
        self.label = tk.Label(f, bg='white', fg='black', text="Section:")
        self.label.place(x = 10, y = 10, anchor='nw')

        # Text Input
        self.entry = tk.Entry(f, bg='white', fg='black', borderwidth=2, width=53)
        self.entry.place(x = 10, y = 50, anchor='nw')

        # Button
        self.okButton = ttk.Button(f, text="OK", width=10, command= lambda: self.edit_section())
        self.okButton.place(x = 60, y = 100, anchor='nw')

        # Close Button
        self.closeButton = ttk.Button(f, text="Cancel", width=10, command= self.kill)
        self.closeButton.place(x = 200, y = 100, anchor='nw')

        f.pack(fill = 'both', expand=1)
        self.after(500, lambda: self.focus_force())
    
    def edit_section(self):
        self._app.edit_section(self.entry.get(), self._currentItemPath, self._currentItemName)
        self._window.refresh_view()
        self.kill()
        
    def kill(self):
        self.winfo_toplevel().destroy()