# Import libraries
from sbol import *

# Import scripts
import Main
import GUI

#Global variables
construct_cd_list = []
sub_component_quantity = []

# Import construct
def import_construct(event):
    GUI.select_construct_import()
    imported_construct = GUI.single_imported_construct
    print(imported_construct)
    Main.doc.read(imported_construct)
    GUI.objects_in_doc_display_protocol()
    isolate_design_()
    design_analysis()


# Retrieve objects in doc
def objects_in_doc():
    dictionary_doc = [obj for obj in Main.doc]
    return dictionary_doc


#Isolating the component definition of the construct design
def isolate_design_():
    construct_cd = Main.doc.componentDefinitions
    for componentdefinitions in construct_cd:
        construct_cd_list.append(componentdefinitions)
        sub_component_quantity.append(len(componentdefinitions.components))
    for componentdefinitions in construct_cd_list:
        if len(componentdefinitions.components) == max(sub_component_quantity):
            global construct_design
            construct_design = componentdefinitions

def design_analysis():
    for component_definition in construct_design.getPrimaryStructure():
        print(component_definition.identity)



