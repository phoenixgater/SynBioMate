# Import libraries
from sbol import *

# Import scripts
import Main
import GUI

# Global variables
primary_structure_identities = []
primary_structure_roles = []
primary_structure_descriptions = []
primary_structure_component_definitions = []
detected_rfc10_sites = []
base_composition = []

############################### Importing Design ###################################

# Import design
def import_design(event):
    GUI.select_design_import()
    imported_design = GUI.single_imported_design
    print(imported_design)
    Main.doc.read(imported_design)
    get_design_uri()
    get_design_primary_structure_identities()
    get_design_roles()
    GUI.display_canvas_pg()
    GUI.display_assembled_design_pg(primary_structure_roles)
    get_design_descriptions()
    GUI.create_description_button_pg()
    initial_design_analysis()
    GUI.create_analysis_button_pg()



# Isolate URI of main design
def get_design_uri():
    sub_component_quantity = []
    try:
        for obj in Main.doc.componentDefinitions:
            sub_component_quantity.append(len(obj.components))
    except LookupError:
        pass
    for obj in Main.doc.componentDefinitions:
        if len(obj.components) == max(sub_component_quantity):
            global design_uri
            design_uri = obj

# Create list of identities of the parts in the design
def get_design_primary_structure_identities():
    global primary_structure_cd
    primary_structure_cd = design_uri.getPrimaryStructure()
    for components in primary_structure_cd:
        primary_structure_identities.append(str(components.displayId))
    print(primary_structure_identities)

# Create list of roles of the parts in the design
def get_design_roles():
    primary_structure_cd = design_uri.getPrimaryStructure()
    for components in primary_structure_cd:
        if "SO" in str(components.roles):
            primary_structure_roles.append(str(components.roles))
        else:
            primary_structure_roles.append("None")

# Create list of descriptions of the parts in the design
def get_design_descriptions():
    primary_structure_cd = design_uri.getPrimaryStructure()
    for components in primary_structure_cd:
        primary_structure_descriptions.append(components.description)



############################ Design initial analysis ###################################
def initial_design_analysis():
    design_sequence = design_uri.sequence.elements
    nucleotide_content(design_sequence)
    rfc10_restriction_sites(design_sequence)

#Calculate nucleotide content
def nucleotide_content(sequence):
    a_count = 0
    t_count = 0
    g_count = 0
    c_count = 0
    for base in str(sequence):
        if base == "a":
            a_count = a_count + 1
        elif base == "t":
            t_count = t_count + 1
        elif base == "c":
            c_count = c_count + 1
        elif base == "g":
            g_count = g_count + 1
    base_count = len(str(sequence))
    a_percentage = "A: " + str(round((a_count/base_count)*100, 2)) + "%"
    t_percentage = "T: " + str(round((t_count/base_count)*100, 2)) + "%"
    g_percentage = "G: " + str(round((g_count/base_count)*100, 2)) + "%"
    c_percentage = "C: " + str(round((c_count/base_count)*100, 2)) + "%"
    base_composition.extend([a_percentage, t_percentage, g_percentage, c_percentage])
    print(base_composition)

def rfc10_restriction_sites(sequence):
    for component in primary_structure_cd:
        print(component.sequence.elements)
        if "gaattc" in str(component.sequence.elements):
            detected_rfc10_sites.append("EcoRI restriction site" + " detected in " + str(component.displayId))
        if "gcggccgc" in str(component.sequence.elements):
            detected_rfc10_sites.append("NotI restriction site " + "detected in " + str(component.displayId))
        if "tctaga" in str(component.sequence.elements):
            detected_rfc10_sites.append("XbaI restriction site " + "detected in " + str(component.displayId))
        if "tctag" in str(component.sequence.elements):
            detected_rfc10_sites.append("XbaI CDS restriction site " + "detected in " + str(component.displayId))
        if "actagt" in str(component.sequence.elements):
            detected_rfc10_sites.append("SpeI restriction site " + "detected in " + str(component.displayId))
        if "ctgcag" in str(component.sequence.elements):
            detected_rfc10_sites.append("PstI restriction site " + "detected in " + str(component.displayId))


print(detected_rfc10_sites)

