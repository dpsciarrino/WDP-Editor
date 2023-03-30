import tkinter as tk
from tkinter import ttk
import os
import sys

frames_dir = os.path.dirname(__file__)
dialogDir = os.path.join(frames_dir, 'dialogs')

sys.path.append(dialogDir)

from ContextDialogs import CreateFolderDialog
from ContextDialogs import DeleteFolderDialog
from ContextDialogs import RenameFolderDialog
from ContextDialogs import DeleteFileDialog
from ContextDialogs import EditAllDescription1Dialog
from ContextDialogs import EditAllDescription2Dialog
from ContextDialogs import CreateFileFromTemplateDialog

sys.path.remove(dialogDir)

class TreeViewFrame(tk.Frame):
    def __init__(self, app, window):
        self._app = app
        self._window = window
        self._tree: ttk.Treeview = None
        self._currentSelectedItemID = None

        tk.Frame.__init__(self, self._window, bg='WHITE', width=250)

        # Root Project File Context Menu
        self.root_context_menu = tk.Menu(self, tearoff=0)
        self.root_context_menu.add_command(label="Create DWG from Template...", command=lambda :self.showDialog(CreateFileFromTemplateDialog))
        self.root_context_menu.add_command(label="Create Folder...", command=lambda:self.showDialog(CreateFolderDialog))

        # First Level Directory Context Menu
        self.first_level_directory_context_menu = tk.Menu(self, tearoff=0)
        self.first_level_directory_context_menu.add_command(label="Create DWG from Template...", command=lambda :self.showDialog(CreateFileFromTemplateDialog))   
        self.first_level_directory_context_menu.add_command(label="Create Folder...", command= lambda : self.showDialog(CreateFolderDialog))
        self.first_level_directory_context_menu.add_separator()
        self.first_level_directory_context_menu.add_command(label="Edit All Description 1...", command=lambda:self.showDialog(EditAllDescription1Dialog))
        self.first_level_directory_context_menu.add_command(label="Edit All Description 2...", command=lambda:self.showDialog(EditAllDescription2Dialog))
        self.first_level_directory_context_menu.add_separator()
        self.first_level_directory_context_menu.add_command(label="Rename Folder...", command = lambda: self.showDialog(RenameFolderDialog))
        self.first_level_directory_context_menu.add_command(label="Delete Folder", command = lambda: self.showDialog(DeleteFolderDialog))
        
        # Second Level Directory Context Menu
        self.second_level_directory_context_menu = tk.Menu(self, tearoff=0)
        self.second_level_directory_context_menu.add_command(label="Create DWG from Template...", command=lambda :self.showDialog(CreateFileFromTemplateDialog))
        self.second_level_directory_context_menu.add_separator()
        self.second_level_directory_context_menu.add_command(label="Edit All Description 1...", command=lambda:self.showDialog(EditAllDescription1Dialog))
        self.second_level_directory_context_menu.add_command(label="Edit All Description 2...", command=lambda:self.showDialog(EditAllDescription2Dialog))
        self.second_level_directory_context_menu.add_separator()
        self.second_level_directory_context_menu.add_command(label="Rename Folder...", command=lambda:self.showDialog(RenameFolderDialog))
        self.second_level_directory_context_menu.add_command(label="Delete Folder", command=lambda: self.showDialog(DeleteFolderDialog))

        # DWG Drawing Context Menu
        self.dwg_context_menu = tk.Menu(self, tearoff=0)
        self.dwg_context_menu.add_command(label="Remove DWG from Project", command=lambda:self.showDialog(DeleteFileDialog))


    @property
    def currentSelectedItemID(self):
        return self._currentSelectedItemID
    
    @currentSelectedItemID.setter
    def currentSelectedItemID(self, value):
        self._currentSelectedItemID = value
    
    @property
    def app(self):
        return self._app
    
    @property
    def window(self):
        return self._window
    
    def update_current(self):
        self._currentSelectedItemID = self._tree.focus()

        if self._currentSelectedItemID.endswith('.dwg'):
            # Drawing Selected
            self._window.update_main_frame_drawing_info(self._currentSelectedItemID)
        else:
            # Folder Selected
            self._window.update_main_frame_folder_info(self._currentSelectedItemID)
    

    
    def showDialog(self, dialog):
        '''
        showDialog(dialog)

        'dialog describes the Class of the tk.Window dialog.

        showDialog creates an instance of 'dialog' and runs it with mainloop()
        '''
        window = dialog(self)
        window.mainloop()

    def tree_click_event(self, event):
        """
        Updates the currently selected item ID when tree view item is clicked.
        """
        self._currentSelectedItemID = self._tree.focus()

        # Updates the MainFrame about the currently selected object's iid
        if self._currentSelectedItemID.endswith('.dwg'):
            self._window.file_mode()
            self._window.update_main_frame_drawing_info(self._currentSelectedItemID)
        else:
            self._window.folder_mode()
            self._window.update_main_frame_folder_info(self._currentSelectedItemID)
        
    def showContextMenu(self, event):
        """
        Handles which context menu to show on right-click in TreeView frame.
        """
        iid = self._tree.identify_row(event.y)

        if iid:
            self._tree.selection_set(iid)
            # Drawing Object
            if iid.endswith(".dwg"):
                self.dwg_context_menu.post(event.x_root, event.y_root)
            # Directory Object
            elif iid.startswith('dir_'):
                # First Level Directory
                if iid.count('_') == 1:
                    self.first_level_directory_context_menu.post(event.x_root, event.y_root)
                # Second Level Directory
                elif iid.count('_') == 2:
                    self.second_level_directory_context_menu.post(event.x_root, event.y_root)
            elif iid == "root":
                self.root_context_menu.post(event.x_root, event.y_root)
            else:
                pass
        else:
            pass

    def build_tree_view(self, project_dir_structure):
        """
        build_tree_view(project_dir_structure)

        Handles the high-level building of the TreeViewFrame's treeview.
        """
        self._tree = ttk.Treeview(self, selectmode='browse')

        # Bindings
        self._tree.bind("<Button-3>", self.showContextMenu)
        self._tree.bind("<Button-1>", self.tree_click_event)
        self._tree.bind('<<TreeviewSelect>>', self.tree_click_event)

        # Set Heading
        self._tree.heading('#0', text='WDP Structure')

        # Populate Tree View
        self.populate_treeview(project_dir_structure)

        # Place Tree View in TreeViewFrame
        self._tree.pack(fill = 'both', expand = True)
    
    def populate_treeview(self, project_dir_structure):
        # Clear all from treeview
        for item in self._tree.get_children():
            self._tree.delete(item)

        # Insert Root
        self._tree.insert("", "end", iid="root", text=f"{self._app.get_wdp_path().name}")

        # Insert Root DWG files
        root_dwgs = project_dir_structure['files']
        self.add_drawings_to_tree(root_dwgs, "root")
        
        # Insert First Level Root Directories
        root_dirs = project_dir_structure['dirs']
        for (first_level_dir_name, first_level_dir) in root_dirs.items():
            # Add First Level Folder to Tree
            #   iid=dir_xxxxx where xxxxx is the name of the folder
            self.add_folder_to_tree(first_level_dir_name, "root")

            # Add Drawings in First Level Folder to Tree
            first_level_folder_dwgs = first_level_dir['files']
            self.add_drawings_to_tree(first_level_folder_dwgs, f"dir_{first_level_dir_name}")

            # Add Second Level Directories
            second_level_dirs = root_dirs[first_level_dir_name]['dirs']
            for (second_level_dir_name, second_level_dir) in second_level_dirs.items():
                # Add Second Level Folder to Tree
                #   iid=dir_xxxxx_yyyyy where xxxxx is the name of the parent folder and yyyyy is the name of the second level folder
                self.add_folder_to_tree(second_level_dir_name, f"dir_{first_level_dir_name}")

                # Add Drawings in Second Level Folder to Tree
                second_level_folder_dwgs = second_level_dir['files']
                self.add_drawings_to_tree(second_level_folder_dwgs, f"dir_{first_level_dir_name}_{second_level_dir_name}")
    
    def add_drawings_to_tree(self, dwg_list: list, folder_iid:str):
        for dwg in dwg_list:
            self._tree.insert(folder_iid, "end", iid=f"{folder_iid}_{dwg['name']}", text=f"{dwg['name']}")
        
    def add_drawing_to_tree(self, drawing, folder_iid:str):
        self._tree.insert(folder_iid, "end", iid=f"{folder_iid}_{drawing['name']}", text=f"{drawing['name']}")
    
    def add_folder_to_tree(self, folder_name: str, parent_iid:str):
        if parent_iid.startswith("dir_"):
            parent_name = parent_iid.split('_')[1]
            new_iid = f"dir_{parent_name}_{folder_name}"
            self._tree.insert(parent_iid, "end", iid=new_iid, text=f"{folder_name}")
            return 0

        self._tree.insert(parent_iid, "end", iid=f"dir_{folder_name}", text=f"{folder_name}")
        return 0
    
    def remove_folder(self, folder_iid):
        self._tree.delete(folder_iid)
        self._tree.selection_set('root')
    
    def rename_folder(self, parent_iid, newFolderName):
        """
        Renames a folder in 'parent_iid' Folder to newFolderName. Updates the name, directory paths, and iid's of the objects.
        """
        children = self._tree.get_children(self._currentSelectedItemID)
        iid_split = self._currentSelectedItemID.split('_')
        old_folder_name = iid_split[len(iid_split)-1]

        # Create a new folder
        new_folder_iid = ""
        if parent_iid != 'root':
            new_folder_iid = parent_iid + '_' + newFolderName
        else:
            new_folder_iid = 'dir_' + newFolderName

        self._tree.insert(parent_iid, "end", iid=new_folder_iid, text=newFolderName)

        for child in children:
            new_child_iid = child.replace(old_folder_name, newFolderName)
            child_split = child.split('_')
            new_child_name = child_split[len(child_split)-1]
            self._tree.insert(new_folder_iid, "end", iid=new_child_iid, text=new_child_name)

            grandchildren = self._tree.get_children(child)
            for grandchild in grandchildren:
                new_grandchild_iid = grandchild.replace(old_folder_name, newFolderName)
                grandchild_split = grandchild.split('_')
                grandchild_name = grandchild_split[len(grandchild_split)-1]
                self._tree.insert(new_child_iid, "end", iid=new_grandchild_iid ,text=grandchild_name)

        self.remove_folder(self._currentSelectedItemID)
    
    def remove_file(self, iid):
        self._tree.delete(iid)
        self._tree.selection_set('root')
    
        