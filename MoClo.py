# Import libraries
from sbol import *

# Import scripts
import Main
import GUI


# Import part from file
def import_design():
    GUI.select_design_import()
    imported_design = GUI.single_imported_design
    print(imported_design)
