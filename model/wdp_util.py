from pathlib import Path

class Drawing:
    """
    Class: Drawing

    Describes a drawing within the WDP project file.
    """
    def __init__(self, dwg_obj) -> None:
        self._name: str = dwg_obj['name']
        self._section: str = dwg_obj['section']
        self._description1: str = dwg_obj['description1']
        self._description2: str = dwg_obj['description2']
        self._description3: str = dwg_obj['description3']
        self._directory: str = dwg_obj['directory']

    def __repr__(self):
        return f"\nName:\t\t\t{self._name}\nSection:\t\t{self._section}\nDescription1:\t\t{self._description1}\nDescription2:\t\t{self._description2}\nDescription3:\t\t{self._description3}\nDirectory:\t\t{self._directory}\n"
    
    @property
    def name(self):
        return self._name
    
    @property
    def section(self):
        return self._section
    
    @property
    def description1(self):
        return self._description1

    @property
    def description2(self):
        return self._description2
    
    @property
    def description3(self):
        return self._description3
    
    @property
    def directory(self):
        return self._directory
    
    def to_json(self) -> dict:
        return {"name":self.name,"section":self.section, "directory":self.directory, "description1":self.description1,"description2":self.description2, "description3":self.description3}

    def to_wdp_format(self) -> str:
        return "This is wdp format"



def get_wdp_lines(wdp_filepath: Path):
    """
    get_wdp_lines(wdp_filepath)

    Returns the lines in the WDP file that are relevant for the application.
    """
    relevant_lines= []
    with open(wdp_filepath, 'r') as fd:
        lines = fd.readlines()

        for line in lines:
            if line.startswith('=') or line.endswith('.dwg\n'):
                relevant_lines.append(line.strip())
    fd.close()

    return relevant_lines

def get_drawings_and_empty_subdirectories(relevant_lines: list):
    """
    get_drawings_and_empty_subdirectories(relevant_lines)

    Takes in a portion of WDP file returned by get_wdp_lines() and returns:
    1. a list of Drawing objects
    2. a list of empty subdirectories in the WDP file
    """
    current_dwg_object = {"name":None, "section":"", "description1": "", "description2": "", "description3": "", "directory": ""}

    drawings = []
    empty_subdirectories = []

    def reset_dwg_object():
        return {"name":None, "section":"", "description1": "", "description2": "", "description3": "", "directory": ""}

    description_number = 1
    for line in relevant_lines:
        # Project Path Directory line
        if line[:9] == "=====SUB=":
            if "[Empty]" in line:
                empty_subdirectories.append(line[9:-7])
                current_dwg_object = reset_dwg_object()
                description_number = 1
            
            current_dwg_object['directory'] = line[9:]
        # Description line
        elif line[:3] == "===":
            if description_number == 1: current_dwg_object['description1'] = line[3:]
            if description_number == 2: current_dwg_object['description2'] = line[3:]
            if description_number == 3: current_dwg_object['description3'] = line[3:]
            description_number += 1
        # Section Line
        elif line[:1] == "=":
            current_dwg_object['section'] = line[1:]
            
        # Drawing File line
        elif line[-4:] == '.dwg':
            current_dwg_object['name'] = line

            # Drawing file is last to be read before saving drawing object
            drawings.append(Drawing(current_dwg_object))
            current_dwg_object = reset_dwg_object()
            description_number = 1
    
    return drawings, empty_subdirectories

def subdirectory_exists(subdirectory, tree):
    """
    subdirectory_exists(subdirectory, tree)

    Checks if a subdirectory exists in the tree.
    Limited to two levels (RIO1/SCHEMATIC for example)
    """
    # If subdirectory is None, we are at root
    if subdirectory == None or subdirectory == '':
        return True
    
    # Set current directory as root.
    current = tree['dirs']

    # Test whether subdirectory exists at the root level
    if subdirectory.count('/') == 0:
        try:
            current[subdirectory]
        except KeyError as e:
            return False
        
    # Test whether subdirectory exists at the second level
    if subdirectory.count('/') == 1:
        folders = subdirectory.split('/')
        try:
            current[folders[0]]['dirs'][folders[1]]
        except KeyError as e:
            return False
    
    return True


def add_subdirectory_to_tree(subdirectory, root):
    """
    add_subdirectory_to_tree(subdirectory, root)

    Adds the subdirectory path to the tree.
    """

    # First-level folder
    if subdirectory.count('/') == 0:
        root['dirs'][subdirectory] = {
            'dirs':{},
            'files':[]
        }
    
    # Second-level folder
    else:
        folders = subdirectory.split('/')
        # First level does not exists
        if not subdirectory_exists(folders[0], root):
            # Add first level
            root['dirs'][folders[0]] = {
                'dirs': {},
                'files': []
            }
            # Add second level
            root['dirs'][folders[0]]['dirs'][folders[1]] = {
                'dirs': {},
                'files': []
            }
        else:
            # Add second level
            root['dirs'][folders[0]]['dirs'][folders[1]] = {
                'dirs': {},
                'files': []
            }

def add_drawing(drawing, tree):
    """
    Adds a drawing to a treeview object.
    """
    # Add drawing to root
    if drawing.directory == None or drawing.directory == '':
        tree['files'].append(drawing.to_json())
    
    # Add drawing to first level directory
    elif drawing.directory.count('/') == 0:
        tree['dirs'][drawing.directory]['files'].append(drawing.to_json())

    # Add drawing to second level directory
    elif drawing.directory.count('/') == 1:
        folders = drawing.directory.split('/')
        tree['dirs'][folders[0]]['dirs'][folders[1]]['files'].append(drawing.to_json())

def add_drawing_to_tree(drawing: Drawing, tree):
    """
    Wrapper function for adding a drawing object to a treeview object.
    """
    if not subdirectory_exists(drawing.directory, tree):
        add_subdirectory_to_tree(drawing.directory, tree)

    add_drawing(drawing, tree)


def get_project_directory_structure(drawings, empty_subdirectories) -> dict:
    """
    get_project_directory_structure(drawings, empty_subdirectories)

    Returns a JSON-like project directory structure as dict.
    """
    tree:dict = {
        'dirs':{},
        'files':[]
    }

    # Add drawings to directory structure
    for drawing in drawings:
        add_drawing_to_tree(drawing, tree)
    
    # Add remaining subdirectories
    for empty_subdirectory in empty_subdirectories:
        add_subdirectory_to_tree(empty_subdirectory, tree)
    
    return tree

def drawing_object_to_text(drawing: Drawing):
    """
    Returns the text representation of a Drawing object.
    """
    lines = []
    
    # Add section
    if drawing.section != "":
        lines.append(f"={drawing.section}")

    # Add Descriptions 
    if drawing.description1 != "":
        lines.append(f"==={drawing.description1}")
    if drawing.description2 != "":
        if drawing.description1 == "":
            lines.append("===")
        lines.append(f"==={drawing.description2}")
    if drawing.description3 != "":
        if drawing.description1 == "" and drawing.description2 == "":
            lines.append("===")
            lines.append("===")
        if drawing.description2 == "":
            lines.append("===")

        lines.append(f"==={drawing.description3}")
    
    # Add Folder Path Directory
    if drawing.directory != "":
        lines.append(f"=====SUB={drawing.directory}")
    
    # Add drawing file name
    lines.append(f"{drawing.name}")

    content = ""
    for line in lines:
        content = content + line + "\n"
    
    return content

def convert_project_to_wdp(project_directory: dict):
    """
    Expects project_tree from app.

    Must have at minimum the following structure:
    {
        "dirs":{}
        "files":[]
    }
    """
    content = ""

    # First Level Files
    for file in project_directory['files']:
        dwg = Drawing(file)
        content += drawing_object_to_text(dwg)
    
    for key, _ in project_directory['dirs'].items():
        # Check if sub-directory is empty
        num_of_dirs = len(project_directory['dirs'][key]['dirs'])
        num_of_files = len(project_directory['dirs'][key]['files'])
        if num_of_dirs == 0 and num_of_files == 0:
            content += f"=====SUB={key}[Empty]\n"

        # Add files to WDP file
        for second_level_file in project_directory['dirs'][key]['files']:
            dwg = Drawing(second_level_file)
            content += drawing_object_to_text(dwg)
        
        # Go to next subdirectory
        for key2, _ in project_directory['dirs'][key]['dirs'].items():
            # Check if sub-directory is empty
            num_of_dirs = len(project_directory['dirs'][key]['dirs'][key2]['dirs'])
            num_of_files = len(project_directory['dirs'][key]['dirs'][key2]['files'])
            if num_of_dirs == 0 and num_of_files == 0:
                content += f"=====SUB={key}/{key2}[Empty]\n"

            # Add files to WDP file
            for third_level_file in project_directory['dirs'][key]['dirs'][key2]['files']:
                dwg = Drawing(third_level_file)
                content += drawing_object_to_text(dwg)
        

    return content

def extract_intro_lines(wdp_path: Path):
    """
    Extracts the intro lines of a WDP file, everything before the directory structure definition.
    """
    intro = ""
    try:
        with open(wdp_path, 'r') as fd:
            lines = fd.readlines()

            for line in lines:
                if not line.startswith('=') and not line.endswith('.dwg\n'):
                    intro += line

    except Exception as e:
        print(e.args)
    finally:
        fd.close()

    return intro

def save_wdp_file(wdp_path: Path, wdp_contents: str):
    """
    Saves to WDP file
    """
    try:
        with open(wdp_path, 'w') as fd:
            fd.write(wdp_contents)
        
    except Exception as e:
        print(e.args)
        return -1
    finally:
        fd.close()
    
    return 0