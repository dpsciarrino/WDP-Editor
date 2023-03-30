import tkinter as tk
import sys
import os.path

srcDir = os.path.dirname(__file__)
frameDir = os.path.join(srcDir, "frames")
dialogsDir = os.path.join(frameDir, "dialogs")

sys.path.append(frameDir)
sys.path.append(dialogsDir)

from TreeViewFrame import TreeViewFrame
from MainFrame import MainFrame
from OutputFrame import OutputFrame
from AddTemplatePathDialog import AddTemplatePathDialog

sys.path.remove(dialogsDir)
sys.path.remove(frameDir)


class AppWindow(tk.Tk):
    def __init__(self, app):
        self._app = app

        tk.Tk.__init__(self)
        
        # Set Application Window Properties
        self.winfo_toplevel().title(f"WDP Editor - {self._app.appModel.wdpModel.wdp_filename}")
        self.winfo_toplevel().geometry("1200x600+10+10")

        # Create Menu Bar
        self.menubar = MainMenuBar(self)
        if app.get_templates_folder_path() is not None:
            self.menubar.disable_template_menu()

        # Add Main Frame
        self.mainFrame = MainFrame(self._app, self)

        # Add Tree Frame
        self.treeFrame = TreeViewFrame(self._app, self)

        # Add Output Frame
        self.outputFrame = OutputFrame(self._app, self)
        

        # Configure Grid
        self.grid_columnconfigure(0, minsize=10, weight=1)
        self.grid_columnconfigure(1, minsize=100, weight=2)
        self.grid_columnconfigure(2, minsize=100, weight=1)

        self.grid_rowconfigure(0, minsize=100, weight=2)
        self.grid_rowconfigure(1, minsize=20, weight=0)
        
        # Place Frame onto Grid
        self.treeFrame.grid(row = 0, column = 0, columnspan=1, rowspan=1, sticky="NEWS")
        self.mainFrame.grid(row=0, column=1, columnspan=2, rowspan=1, sticky="NEWS")
        self.outputFrame.grid(row=1, column=0, columnspan=3, rowspan=1, sticky="NEWS")

        # Set Focus on Application Window
        self.after(500, lambda:self.focus_force())

        self.app.initialize_app()
        self.treeFrame.build_tree_view(self.app.get_project_tree())

        self.mainloop()
    
    @property
    def app(self):
        return self._app
    
    def get_current_folder(self):
        if not self.treeFrame.currentSelectedItemID.endswith('.dwg'):
            iid_split: list = self.treeFrame.currentSelectedItemID.split('_')
            if ('root' in iid_split) or ('' in iid_split):
                return []
            else:
                iid_split.remove('dir')
                return iid_split
        return None

    
    def get_current_item_name(self):
        """
        Extracts the currently selected item's name, if the item is a file.
        """
        if self.treeFrame.currentSelectedItemID.endswith('.dwg'):
            iid_split: list = self.treeFrame.currentSelectedItemID.split('_')
            pieces = len(iid_split)
            return iid_split[pieces-1]

        return None
    
    def file_mode(self):
        self.mainFrame.file_mode()
    
    def folder_mode(self):
        self.mainFrame.folder_mode()
    
    def refresh_view(self):
        self.treeFrame.update_current()
    
    def refresh_folder_mode(self):
        self.mainFrame.file_mode()
        self.mainFrame.folder_mode()
        
    def launch_template_path_dialog(self):
        AddTemplatePathDialog(self.mainFrame)

    
    def get_current_item_path(self):
        """
        Extracts the currently selected item's path, if the item is a file.
        """
        drawing_path = None
        iid_split: list = self.treeFrame.currentSelectedItemID.split('_')
        drawing_path = "/"
        for piece in iid_split:
            if piece != self.get_current_item_name() and piece != 'root' and piece != 'dir':
                drawing_path = drawing_path + piece + "/"

        return drawing_path
    
    def kill(self):
        self.winfo_toplevel().destroy()
    
    def exitApp(self):
        self.kill()
    
    def update_main_frame_drawing_info(self, iid):
        # iid is the drawing file name
        iid_split: list = iid.split('_')
        pieces = len(iid_split)
        
        # Get Drawing Name
        drawing_name = iid_split[pieces-1]

        # Get Drawing Path
        drawing_path = "/"
        for piece in iid_split:
            if piece != drawing_name and piece != 'root' and piece != 'dir':
                drawing_path = drawing_path + piece + "/"
            
        # Get the descriptions
        descriptions = self._app.get_drawing_descriptions(drawing_path, drawing_name)

        # Get the section
        section = self._app.get_drawing_section(drawing_path, drawing_name)
        
        # Update Main Frame
        self.mainFrame.update_name_label(drawing_name)
        self.mainFrame.update_section_label(section)
        self.mainFrame.update_path_label(drawing_path)
        self.mainFrame.update_decsription1_label(descriptions[0])
        self.mainFrame.update_description2_label(descriptions[1])
        self.mainFrame.update_description3_label(descriptions[2])
    
    def update_main_frame_folder_info(self, iid):
        self.mainFrame.update_name_label("")
        self.mainFrame.update_section_label("")
        self.mainFrame.update_path_label("")
        self.mainFrame.update_decsription1_label("")
        self.mainFrame.update_description2_label("")
        self.mainFrame.update_description3_label("")
    
    def save(self):
        # Step 1: Retrieve project model
        self._app.save()
    
    def disable_template_menu(self):
        self.menubar.disable_template_menu()

        
    

class MainMenuBar(tk.Menu):
    def __init__(self, appWindow):
        self.menubar = tk.Menu(appWindow)
        appWindow.config(menu=self.menubar)

        # File Menu Definition
        self.fileMenu = tk.Menu(self.menubar, tearoff=0)
        self.fileMenu.add_command(label="Save WDP", command=appWindow.save)
        self.fileMenu.add_command(label="Exit", command=appWindow.exitApp)

        self.menubar.add_cascade(label="File", menu=self.fileMenu)

        # Config Menu Definition
        self.configMenu = tk.Menu(self.menubar, tearoff=0)
        self.configMenu.add_command(label="Add Templates Folder...", command=appWindow.launch_template_path_dialog)

        self.menubar.add_cascade(label="Templates", menu=self.configMenu)
    
    def disable_template_menu(self):
        self.menubar.entryconfig("Templates", state="disabled")