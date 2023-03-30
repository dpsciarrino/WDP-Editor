import os
import sys
import tkinter as tk
from pathlib import Path

from gui.app_gui import AppWindow
from gui.provide_wdp_dialog import ProvideWDPWindow

from model.wdp_util import convert_project_to_wdp, extract_intro_lines, save_wdp_file

srcDir = os.path.dirname(__file__)
modelDir = os.path.join(srcDir, 'model')

# Retrieve relevant classes
sys.path.append(modelDir)
from app_model import AppModel
sys.path.remove(modelDir)

class Application:
    '''
    Application

    Encapsulates global application.
    '''
    def __init__(self) -> None:
        # Source Directory
        self._srcDir = os.path.dirname(os.path.abspath(__file__))

        # App Directory
        self._appDir = os.path.dirname(self._srcDir)

        self._appModel = AppModel()

        # Global Variables
        self._kill_request = False

        # WDP Data
        self._wdp_path: Path = None
        self._template_path: Path = None

        self._outputManager = OutputManager(self)

    
    @property
    def srcDir(self):
        return self._srcDir
    
    @property
    def appDir(self):
        return self._appDir
    
    @property
    def appModel(self):
        return self._appModel
    
    @property
    def outputManager(self):
        return self._outputManager
    
    @property
    def wdp_path(self):
        return self._wdp_path
    
    @wdp_path.setter
    def wdp_path(self, value: Path):
        self._wdp_path = value
    
    @property
    def template_path(self):
        return self._template_path
    
    @template_path.setter
    def template_path(self, value):
        self._template_path = value

    def kill(self):
        """
        kill()

        Used by Provide_WDP_Dialog window to cancel application.
        """
        self._kill_request = True
    
    def get_kill_request(self):
        """
        get_kill_request()

        Used in Main to cancel application if kill_request is set.
        """
        return self._kill_request
    
    def get_wdp_path(self):
        return self._wdp_path
    
    def get_templates_folder_path(self):
        return self._template_path
    
    def get_project_tree(self):
        return self.appModel.wdpModel.project_tree
    
    def get_template_drawings(self):
        if self.appModel.templateModel != None:
            return self.appModel.templateModel.possible_templates
        
        return []
    
    def initialize_app(self):
        """
        Handles application initialization functions.
        """
        self.outputManager.broadcast("Initializing application.")

        self.outputManager.broadcast(f"WDP File Path:")
        self.outputManager.broadcast(f"\t{self.get_wdp_path()}")
        self.outputManager.broadcast(f"Templates Folder Path:")
        if self.get_templates_folder_path() is None:
            self.outputManager.broadcast("\tNo templates folder assigned. If needed, select a template folder. See 'Templates' menu.")
            self.outputManager.broadcast("\tTemplate folders must have at least one DWG file to use as potential template.")
        else:
            self.outputManager.broadcast(f"\t{self.get_templates_folder_path()}")
    
    def get_drawing_descriptions(self, drawing_path, drawing_name):
        """
        Given a path and a drawing naming, returns the drawing descriptions in a 3-tuple.
        """
        return self.appModel.wdpModel.get_descriptions(drawing_path, drawing_name)
    
    def edit_description(self, number, new_description, drawing_path, drawing_name):
        """
        Given a drawing name and drawing path, change the description <number> to <new_description>
        """
        return self.appModel.wdpModel.edit_description(number, new_description, drawing_path, drawing_name)
    
    def edit_section(self, new_section, drawing_path, drawing_name):
        """
        Given a section string, drawing name, and drawing path, change the section to <new_section>
        """
        return self.appModel.wdpModel.edit_section(new_section, drawing_path, drawing_name)
    
    def get_drawing_section(self, drawing_path, drawing_name):
        """
        Given the drawing name, return the drawing section.
        """
        return self.appModel.wdpModel.get_section(drawing_path, drawing_name)
    
    def create_folder(self, newFolderName, parentFolder):
        """
        Given a new folder name and parent folder, creates a new folder in the project tree.
        """
        return self.appModel.wdpModel.create_folder(newFolderName, parentFolder)
    
    def delete_folder(self, keep, folder_path):
        """
        Given a folder path, deletes the folder at the end of the path. If keep is True, all files in folder are moved to parent.
        """
        return self.appModel.wdpModel.delete_folder(keep, folder_path)
    
    def rename_folder(self, folder_path, new_folder_name):
        """
        Given a current folder path, change the name of the folder to new_folder_name.
        """
        return self.appModel.wdpModel.rename_folder(folder_path, new_folder_name)
    
    def remove_dwg(self, dwg_iid):
        """
        Given the ID of a DWG file, remove it from the application.
        """
        return self.appModel.wdpModel.remove_file(dwg_iid)
    
    def editAllDescription1(self, folder_iid, newDescription):
        """
        Provides a wrapper for editing Description 1 field in Model
        """
        return self.appModel.wdpModel.editAllDescription1(folder_iid, newDescription)

    def editAllDescription2(self, folder_iid, newDescription):
        """
        Provides a wrapper for editing Description 2 field in Model
        """
        return self.appModel.wdpModel.editAllDescription2(folder_iid, newDescription)
    
    def create_dwg(self, file_iid, template_file):
        """
        Creates DWG file based on Template File and adds to Model.
        """

        # Create the file
        contents = ""
        with open(template_file, 'rb') as fr:
            contents = fr.read()
        fr.close()

        iid_split = file_iid.split('_')
        file_name = iid_split[len(iid_split)-1]
        wdp_folder = self.wdp_path.parent
        new_file_path = wdp_folder / file_name

        with open(new_file_path, 'wb') as fw:
            fw.write(contents)
        fw.close()

        # Add drawing to Model
        self._appModel.wdpModel.add_dwg(file_iid)
    
    def save(self):
        """
        save()

        Saves current configuration to WDP file.
            Step 1: Retrieve project model from appModel
            Step 2: Build the lines to add to WDP file
            Step 3: Copy the first portion of the WDP file
            Step 4: Append the lines from project model
            Step 5: Save to file.
        """
        # Step 1: Retrieve project model from app   and   Step 2: Build the lines to add to WDP file
        wdp_project_lines = convert_project_to_wdp(self.get_project_tree())

        # Step 3: Copy the first portion of working WDP file
        wdp_intro_lines = extract_intro_lines(self.get_wdp_path())

        # Step 4: Append the lines from project model
        wdp_lines = wdp_intro_lines + wdp_project_lines

        # Step 5: Save content to file
        success = save_wdp_file(self.get_wdp_path(), wdp_lines)

        if success == 0:
            self._outputManager.broadcast("WDP File Saved.")
            


class OutputManager:
    """
    Class for user action log.
    """
    def __init__(self, app):
        self._app = app
        self._textBox = None
        self._scrollbar = None

    @property
    def app(self):
        return self._app
    
    @property
    def textBox(self):
        return self._textBox
    
    @property
    def scrollbar(self):
        return self._scrollbar
    
    def generateTextBox(self, frameRef):
        """
        Builds the Output Log textbox layout for view object.
        """
        self._textBox = tk.Text(frameRef, height=7, width = 100)
        self._textBox.config(state = 'disabled')

        self._scrollbar = tk.Scrollbar(frameRef, command = self._textBox.yview)
        self._textBox['yscrollcommand'] = self._scrollbar.set
        
        return self._textBox
    
    def broadcast(self, text):
        """
        Handler for broadcasting user actions to frontend textbox on GUI.
        """
        self._textBox.config(state='normal')
        text = text + '\n'
        self._textBox.insert(tk.END, text)
        self._textBox.config(state='disabled')
        self._textBox.yview_moveto(1)
        
    
def save_backup_wdp(path: Path):
    """
    Saves a backup file of the WDP file.
    """
    backup_path = str(path) + "-backup"

    contents = ""
    try:
        with open(path, 'r') as fd:
            contents = fd.read()
        fd.close()
    except Exception as e:
        print(e.args)
        return -1

    try:
        with open(backup_path, 'w') as fp:
            fp.write(contents)
        fp.close()
    except Exception as e:
        print(e.args)
        return -2

    return 0
    

if __name__ == '__main__':
	#start application
    app = Application()

    # Provide WDP File Path
    ProvideWDPWindow(app)

    # WDP File Path Valid
    if (app.wdp_path != None) and (app.get_kill_request() == False):
        # Save Copy of working WDP file
        save_backup_wdp(app.wdp_path)

        wdp_model = app.appModel.parse_wdp_file(app.wdp_path)

        # Valid WDP File
        if wdp_model != None:
            # Compute template files, if any
            if app.template_path != None:
                app.appModel.store_possible_templates(app.template_path)
                
            AppWindow(app)