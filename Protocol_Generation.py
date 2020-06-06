# Import libraries
from sbol import *

# Import scripts
import Main
import GUI

# Global variables
doc_cd_list = []
sub_component_quantity = []
construct_components_list = []
roles_2 = []
part_roles_list = []
part_names = []
construct_name = str

# Import construct
def import_construct(event):
    GUI.select_construct_import()
    imported_construct = GUI.single_imported_construct
    print(imported_construct)
    Main.doc.read(imported_construct)
    isolate_design_()
    detect_roles()
    isolate_part_names()
    GUI.display_construct_GUI(part_roles_list)


# Retrieve objects in doc
def objects_in_doc():
    dictionary_doc = [obj for obj in Main.doc]
    return dictionary_doc


# Isolating the component definition of the construct design in pySBOL doc
def isolate_design_():
    doc_cd = Main.doc.componentDefinitions
    for componentdefinitions in doc_cd:
        doc_cd_list.append(componentdefinitions)
        sub_component_quantity.append(len(componentdefinitions.components))
    for componentdefinitions in doc_cd_list:
        if len(componentdefinitions.components) == max(sub_component_quantity):
            global construct_cd
            construct_cd = componentdefinitions


# Retrieving SO identifiers of parts in construct design
def detect_roles():
    global part_roles
    for component_definition in construct_cd.getPrimaryStructure():
        construct_components_list.append(component_definition)
    for x in construct_components_list:
        roles_2.append(x.roles)
    for y in roles_2:
        for x in y:
            if "SO" in str(x):
                part_roles_list.append(x)

def isolate_part_names():
    for parts in (construct_components_list):
        parts_2 = str(parts).replace("https://synbiohub.org/public/igem/", " ")
        parts_3 = parts_2.replace("/1", " ")
        part_names.append(parts_3)



















