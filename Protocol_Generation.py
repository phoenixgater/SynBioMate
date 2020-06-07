# Import libraries
from sbol import *

# Import scripts
import Main
import GUI

# Global variables
doc_cd_list = []
sub_component_quantity = []
design_components_list = []
roles_2 = []
part_roles_list = []
part_names = []
part_descriptions = []
design_name = str


############################### Importing Design ###################################

# Import design
def import_design(event):
    GUI.select_design_import()
    imported_design = GUI.single_imported_design
    print(imported_design)
    Main.doc.read(imported_design)
    isolate_design_()
    detect_roles()
    isolate_part_names()
    GUI.display_design_GUI(part_roles_list)
    isolate_part_descriptions()
    GUI.create_description_button()


# Isolating the component definition of the design in pySBOL doc
def isolate_design_():
    doc_cd = Main.doc.componentDefinitions
    for componentdefinitions in doc_cd:
        doc_cd_list.append(componentdefinitions)
        sub_component_quantity.append(len(componentdefinitions.components))
    for componentdefinitions in doc_cd_list:
        if len(componentdefinitions.components) == max(sub_component_quantity):
            global design_cd
            design_cd = componentdefinitions


# Retrieving SO identifiers of parts in design
def detect_roles():
    global part_roles
    for component_definition in design_cd.getPrimaryStructure():
        design_components_list.append(component_definition)
    for x in design_components_list:
        roles_2.append(x.roles)
    for y in roles_2:
        for x in y:
            if "SO" in str(x):
                part_roles_list.append(x)


# Isolating part names
def isolate_part_names():
    for parts in (design_components_list):
        parts_2 = str(parts).replace("https://synbiohub.org/public/igem/", " ")
        parts_3 = parts_2.replace("/1", " ")
        part_names.append(parts_3)


# Isolation part descriptions
def isolate_part_descriptions():
    for parts in design_components_list:
        part_descriptions.append(parts.description)

############################ Design initial analysis ###################################
