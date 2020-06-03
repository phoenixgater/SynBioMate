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
    test_function()


# Retrieve objects in doc
def objects_in_doc():
    dictionary_doc = [obj for obj in Main.doc]
    return dictionary_doc

def test_function():
    construct_cd = Main.doc.componentDefinitions
    for x in construct_cd:
        print(len(x.components))


    '''uri_list = []
    for obj in Main.doc:
        uri_list.append(obj)
    print(uri_list)
    for TopLevel in uri_list:
        print(TopLevel.ComponentDefinition)
        cd_list = (Main.doc.getComponentDefinition(str(TopLevel)))
        print(cd_list.sequences)'''



    '''part1 = Main.doc.getComponentDefinition(str(uri_list[0]))
    print(len(part1.components))'''






