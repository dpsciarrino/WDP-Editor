import tkinter as tk
from tkinter import filedialog
from pathlib import Path

class ProvideWDPWindow(tk.Tk):
    def __init__(self, app):
        self._app = app
        tk.Tk.__init__(self)
        self._frame = ProvideWDPFrame(self)

        # Window Properties
        self.winfo_toplevel().geometry("600x250")
        self.winfo_toplevel().title("WDP Editor - Link WDP File")
        self.resizable(0,0)

        self.mainloop()
    
    @property
    def app(self):
        return self._app
    
    def kill(self):
        self.winfo_toplevel().destroy()
    
class ProvideWDPFrame(tk.Frame):
    def __init__(self, wdpWindow):
        self._wdpWindow = wdpWindow

        # Frame Properties
        tk.Frame.__init__(self, wdpWindow, bg='white', width="600", height="250")

        # Message String Widget
        self.message_string = tk.Label(self, text="", bg="white", fg="red")
        self.success_string = tk.Label(self, text="", bg="white", fg="green")
        self.message_string2 = tk.Label(self, text="", bg="white", fg="black")
        self.success_string2 = tk.Label(self, text="", bg="white", fg="green")

        # Locate Working Directory Widgets
        locate_working_directory_label = tk.Label(self, text="Working Directory:", bg="white", fg="black")
        self.locate_working_directory_entry = tk.Entry(self, width=70, borderwidth=2)
        self.locate_working_directory_entry.insert(0, "")
        self.locate_working_directory_button = tk.Button(self, text="...", height=1, width=1, command = lambda : self.openWorkingDirectoryBrowser(self.locate_working_directory_entry, self.message_string, self.success_string))

        # Template Drawings Directory Widgets
        locate_template_directory_label = tk.Label(self, text="Template Directory:", bg="white", fg="black")
        self.locate_template_directory_entry = tk.Entry(self, width=70, borderwidth=2)
        self.locate_template_directory_entry.insert(0, "")
        self.locate_template_directory_button = tk.Button(self, text="...", height=1, width=1, command= lambda: self.openTemplateDirectoryBrowser(self.locate_template_directory_entry, self.message_string2, self.success_string2))

        # Navigation Buttons
        okButton = tk.Button(self, text="OK", height=2, width=10, command=self.okButtonListener)
        cancelButton = tk.Button(self, text="Exit", height=2, width=10, command=self.closeButtonListener)

        # Widget Placement
        locate_working_directory_label.place(x=30, y=20, relx=0, anchor='nw')
        self.locate_working_directory_entry.place(x=135, y=22, relx=0, rely=0, anchor='nw')
        self.locate_working_directory_button.place(x=560, y=20, relx=0, rely=0, anchor='nw')
        self.success_string.place(x=135,y=50,relx=0, rely=0, anchor='nw')
        self.message_string.place(x=137,y=50,relx=0, rely=0, anchor='nw')

        locate_template_directory_label.place(x=28, y=100, relx=0, rely=0, anchor='nw')
        self.locate_template_directory_entry.place(x=135, y=102, relx=0, rely=0, anchor='nw')
        self.locate_template_directory_button.place(x=560, y=100, relx=0, rely=0, anchor='nw')
        self.success_string2.place(x=135, y=130, relx=0, rely=0, anchor='nw')
        self.message_string2.place(x=137, y=130, relx=0, rely=0, anchor='nw')

        okButton.place(x=180, y=150, relx=0, rely=0, anchor='nw')
        cancelButton.place(x=380, y=150, relx=0, rely=0, anchor='nw')

        # Place Frame
        self.place(relx=0.5, rely=0.5, anchor='center')
    
    def openWorkingDirectoryBrowser(self, entrybox, message_label: tk.Label, success_label: tk.Label):
        """
        Opens File Explorer to locate current working directory.
        """
        directoryName = filedialog.askdirectory(initialdir="/", title="Select Working Directory")
        self.focus_force()
        self.grab_set()
        entrybox.delete(0, 'end')
        message_label.config(text="")
        success_label.config(text="")
        entrybox.insert(0, directoryName)

        # Check if a WDP file is in the working directory
        wdp_files = sorted(Path(directoryName).glob('*.wdp'))
        if len(wdp_files) != 1:
            message_label.config(text="No WDP file found.")
            return -1
        
        wdp_filepath = wdp_files[0]
        if not Path.is_file(wdp_filepath):
            message_label.config(text="More than one WDP file found...")
            return -1
        
        success_label.config(text=f"WDP Found: {wdp_filepath.name}")
        self._wdpWindow.app.wdp_path = wdp_filepath

        return 0
    
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
        self._wdpWindow.app.template_path = Path(directoryName)

        return 0
    
    def okButtonListener(self):
        self._wdpWindow.kill()
    
    def closeButtonListener(self):
        self._wdpWindow.app.kill()
        self._wdpWindow.kill()


