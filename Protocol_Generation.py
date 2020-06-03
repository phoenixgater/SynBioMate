# Import libraries
from sbol import *

# Import scripts
import Main
import GUI


# Import construct
def import_construct(event):
    GUI.select_construct_import()
    imported_construct = GUI.single_imported_construct
    print(imported_construct)
    Main.doc.read(imported_construct)
    GUI.objects_in_doc_display_protocol()


# Retrieve objects in doc
def objects_in_doc():
    dictionary_doc = [obj for obj in Main.doc]
    return dictionary_doc

