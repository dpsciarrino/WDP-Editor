import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from pathlib import Path

class AddTemplatePathDialog(tk.Tk):
    def __init__(self, parentFrame):
        self._app = parentFrame.app
        self._window = parentFrame.window
        self._parentFrame = parentFrame

        self._template_path = None

        tk.Tk.__init__(self)
        self.winfo_toplevel().title("Add Template Path")
        self.winfo_toplevel().geometry("700x150+500+200")
        f = tk.Frame(self, bg='white')

        # Label
        self.label = tk.Label(f, bg='white', fg='black', text="Browse for Template Folder:")

        self.message_string2 = tk.Label(self, text="", bg="white", fg="black")
        self.success_string2 = tk.Label(self, text="", bg="white", fg="green")

        # Template Drawings Directory Widgets
        self.locate_template_directory_entry = tk.Entry(self, width=70, borderwidth=2)
        self.locate_template_directory_entry.insert(0, "")
        self.locate_template_directory_button = tk.Button(self, text="...", height=1, width=1, command= lambda: self.openTemplateDirectoryBrowser(self.locate_template_directory_entry, self.message_string2, self.success_string2))

        self.label.place(x=28, y=10, relx=0, rely=0, anchor='nw')
        self.locate_template_directory_entry.place(x=135, y=32, relx=0, rely=0, anchor='nw')
        self.locate_template_directory_button.place(x=560, y=30, relx=0, rely=0, anchor='nw')

        # Button
        self.okButton = ttk.Button(f, text="OK", width=10, command= lambda: self.add_template_path())
        self.okButton.place(x = 210, y = 95, anchor='nw')

        # Close Button
        self.closeButton = ttk.Button(f, text="Cancel", width=10, command= self.kill)
        self.closeButton.place(x = 450, y = 95, anchor='nw')

        self.success_string2.place(x=135, y=70, relx=0, rely=0, anchor='nw')
        self.message_string2.place(x=137, y=70, relx=0, rely=0, anchor='nw')

        f.pack(fill = 'both', expand=1)
        self.after(500, lambda: self.focus_force())
    
    @property
    def template_path(self):
        return self._template_path
    
    @template_path.setter
    def template_path(self, value):
        self._template_path = value
    
    def openTemplateDirectoryBrowser(self, entrybox, message_label: tk.Label, success_label: tk.Label):
        """
        Opens File Explorer to locate template directory.
        """
        directoryName = filedialog.askdirectory(initialdir="/", title="Select Template Directory")
        self.focus_force()
        self.grab_set()
        entrybox.delete(0, 'end')
        message_label.config(text="")
        success_label.config(text="")
        entrybox.insert(0, directoryName)

        # Check if a DWG file is in the working directory
        dwg_files = sorted(Path(directoryName).glob('*.dwg'))
        if len(dwg_files) == 0:
            message_label.config(text="No DWG files found...")
            return -1
        
        success_label.config(text=f"DWG Template Files Found")

        self.template_path = Path(directoryName)

        return 0
    
    def add_template_path(self):
        self._window.app.template_path = self.template_path
        self._app.appModel.store_possible_templates(self.template_path)
        self._window.disable_template_menu()
        self.kill()
        return None
        
    def kill(self):
        self.winfo_toplevel().destroy()