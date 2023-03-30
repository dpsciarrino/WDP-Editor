# WDP-Editor
Provides a relatively easy way to edit WDP project files used in AutoCAD Electrical.

## Purpose

AutoCAD Electrical makes it difficult to quickly and efficiently modify certain drawing-level fields. Including:
- Description 1
- Description 2
- Description 3
- Section

Out of necessity, and to save time, I created this WDP Editor GUI to better manage these project files.

## Features
1. Reading and Viewing WDP files as a Treeview.
2. Path and Folder management up to 3 levels.
  2.1. Includes renaming, creating, deleting, and reading project folders.
3. Managing DWG filenames, sections, and where they reside in the folder structure.
4. Ability to edit the Description 1 field for every DWG in a specific folder.
5. Ability to edit the Description 2 field for every DWG in a specific folder.
6. Creates a backup copy of WDP upon opening main application, so you can revert changes if something goes wrong.
  6.1. Backup file is called <name-of-wdp-file>.wdp-backup and resides in the project directory
7. Saves changes to WDP file.

## Using WDP Editor

### Running WDP Editor

Run WDP Editor by cloning this repository, navigating to it, and running the run.py file.

```
python run.py
```
or
```
python3 run.py
```

### Initial Setup

You will be prompted to provide two directories: a Working Directory and a Template Directory.

#### The Working Directory

The Working Directory holds the .WDP file you'd like to edit. This is the same folder AutoCAD Electrical uses to store all it's project-specific files. As such, there may be other files present, like .DWG files and other project-specific files.

When you select the Working Directory, WDP Editor automatically senses whether or not it sees a WDP file in the directory and will prompt you accordingly.

#### The Template Directory

The Template Directory is optional. WDP Editor allows you to add new DWG files and can use other DWGs as templates. This is the directory where those "template" drawings are stored.

When you select the Template Directory, WDP Editor automatically senser whether or not it sees a DWG file in the directory and will prompt you accordingly.




