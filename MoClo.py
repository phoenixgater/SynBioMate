# Import libraries
from sbol import *

# Import scripts
import Main
import GUI

# global variables
primary_structure_identities = []
primary_structure_roles = []
primary_structure_descriptions = []
base_composition = []
detected_rfc10_sites = []
level_0_promoter = {}
level_0_promoter_display = []
level_0_rbs = {}
level_0_rbs_display = []
level_0_cds = {}
level_0_cds_display = []
level_0_terminator = {}
level_0_terminator_display = []
level_0_signal_peptide = {}
level_0_signal_peptide_display = []
level_0_other = {}
level_0_other_display = []
level_2_template = []




# clear globals function
def clear_globals():
    primary_structure_identities.clear()
    primary_structure_roles.clear()
    primary_structure_descriptions.clear()
    base_composition.clear()
    detected_rfc10_sites.clear()

# Import part from file
def import_design(event):
    clear_globals()
    GUI.select_design_import()
    imported_design = GUI.single_imported_design
    Main.doc.read(imported_design)
    get_design_uri()
    get_design_primary_structure_identities()
    get_design_roles()
    get_design_descriptions()
    GUI.create_description_button_moclo()
    GUI.create_analysis_button_moclo()
    initial_design_analysis(design_uri)
    GUI.refresh_canvas_moclo()
    GUI.display_assembled_design_moclo(primary_structure_roles)
    GUI.refresh_design_parts_to_library()



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


###################################### sequence analysis #####################################
def initial_design_analysis(uri):
    design_sequence = uri.sequence.elements
    nucleotide_content(design_sequence)
    rfc10_restriction_sites(design_sequence)


# Calculate nucleotide content
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
    a_percentage = "A: " + str(round((a_count / base_count) * 100, 2)) + "%"
    t_percentage = "T: " + str(round((t_count / base_count) * 100, 2)) + "%"
    g_percentage = "G: " + str(round((g_count / base_count) * 100, 2)) + "%"
    c_percentage = "C: " + str(round((c_count / base_count) * 100, 2)) + "%"
    base_composition.extend([a_percentage, t_percentage, g_percentage, c_percentage])


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

############################ level 0 library #################################
def import_design_parts_to_library(event):
    primary_structure_cd = design_uri.getPrimaryStructure()
    for component in primary_structure_cd:
        if "0000167" in str(component.roles):
            level_0_promoter["p" + str(len(level_0_promoter))] = component
            level_0_promoter_display.append("p" + str(len(level_0_promoter)) + ". " + str(component.displayId))
        elif "0000139" in str(component.roles):
            level_0_rbs["r" + str(len(level_0_rbs))] = component
            level_0_rbs_display.append("r" + str(len(level_0_rbs)) + ". " + str(component.displayId))
        elif "0000316" in str(component.roles):
            level_0_cds["c" + str(len(level_0_cds))] = component
            level_0_cds_display.append("c" + str(len(level_0_cds)) + ". " + str(component.displayId))
        elif "0000141" in str(component.roles):
            level_0_terminator["t" + str(len(level_0_terminator))] = component
            level_0_terminator_display.append("t" + str(len(level_0_terminator)) + ". " + str(component.displayId))
        elif "0000324" in str(component.roles):
            level_0_signal_peptide["s" + str(len(level_0_signal_peptide))] = component
            level_0_signal_peptide_display.append("s" + str(len(level_0_signal_peptide)) + ". " + str(component.displayId))
        else:
            level_0_other["o" + str(len(level_0_other))] = component
            level_0_other_display.append("o" + str(len(level_0_other)) + ". " + str(component.displayId))

    GUI.refresh_level_0_library()

# Add level 0 part from file
def import_part_from_file(event):
    GUI.select_design_import()
    imported_design = GUI.single_imported_design
    Main.doc.read(imported_design)
    if len(Main.doc.componentDefinitions) == 1:
        for obj in Main.doc.componentDefinitions:
            design_uri = obj
    if "0000167" in str(design_uri.roles):
        level_0_promoter["p" + str(len(level_0_promoter))] = design_uri
        level_0_promoter_display.append("p" + str(len(level_0_promoter)) + ". " + str(design_uri.displayId))
    elif "0000139" in str(design_uri.roles):
        level_0_rbs["r" + str(len(level_0_rbs))] = design_uri
        level_0_rbs_display.append("r" + str(len(level_0_rbs)) + ". " + str(design_uri.displayId))
    elif "0000316" in str(design_uri.roles):
        level_0_cds["c" + str(len(level_0_cds))] = design_uri
        level_0_cds_display.append("c" + str(len(level_0_cds)) + ". " + str(design_uri.displayId))
    elif "0000141" in str(design_uri.roles):
        level_0_terminator["t" + str(len(level_0_terminator))] = design_uri
        level_0_terminator_display.append("t" + str(len(level_0_terminator)) + ". " + str(design_uri.displayId))
    elif "0000324" in str(design_uri.roles):
        level_0_signal_peptide["s" + str(len(level_0_signal_peptide))] = design_uri
        level_0_signal_peptide_display.append("s" + str(len(level_0_signal_peptide)) + ". " + str(design_uri.displayId))
    else:
        level_0_other["o" + str(len(level_0_other))] = design_uri
        level_0_other_display.append("o" + str(len(level_0_other)) + ". " + str(design_uri.displayId))
    GUI.refresh_level_0_library()

def create_protocol_directory(event):
    chassis_choice = GUI.chassis_selection_combo.get()
    transcription_unit_quantity = GUI.transcription_unit_quantity_combo.get()
    signal_peptide_choice = GUI.include_signal_peptide_combo.get()
    primer_selection = GUI.primer_selection_combo.get()
    liquid_handler_choice = GUI.liquid_handler_combo.get()
    part_selection_lists()
    if chassis_choice == "E. coli":
        from EcoFlex_Protocol import create_protocol
        create_protocol()

# create part selection component definition lists
def part_selection_lists():
    transcription_unit_quantity = int(GUI.transcription_unit_quantity_combo.get())
    signal_peptide_choice = GUI.include_signal_peptide_combo.get()
    if transcription_unit_quantity > 1:
        #### Transcription unit 1 ####
        selected_promoters_1 = (GUI.transcription_unit_1_promoter_entry.get())
        transcription_unit_1_promoters = (selected_promoters_1.split(","))
        print(transcription_unit_1_promoters)

        selected_rbs_1 = (GUI.transcription_unit_1_rbs_entry.get())
        transcription_unit_1_rbs = (selected_rbs_1.split(","))

        if signal_peptide_choice == "Yes":
            selected_signal_1 = (GUI.transcription_unit_1_signal_entry.get())
            transcription_unit_1_rbs = (selected_signal_1.split(","))

        selected_cds_1 = (GUI.transcription_unit_1_cds_entry.get())
        transcription_unit_1_rbs = (selected_cds_1.split(","))

        selected_terminator_1 = (GUI.transcription_unit_1_terminator_entry.get())
        transcription_unit_1_terminator = (selected_terminator_1.split(","))

        #### Transcription unit 2 ####
        selected_promoters_2 = (GUI.transcription_unit_2_promoter_entry.get())
        transcription_unit_2_promoters = (selected_promoters_2.split(","))

        selected_rbs_2 = (GUI.transcription_unit_2_rbs_entry.get())
        transcription_unit_2_rbs = (selected_rbs_2.split(","))

        if signal_peptide_choice == "Yes":
            selected_signal_2 = (GUI.transcription_unit_2_signal_entry.get())
            transcription_unit_2_rbs = (selected_signal_2.split(","))

        selected_cds_2 = (GUI.transcription_unit_2_cds_entry.get())
        transcription_unit_2_rbs = (selected_cds_2.split(","))

        selected_terminator_2 = (GUI.transcription_unit_2_terminator_entry.get())
        transcription_unit_2_terminator = (selected_terminator_2.split(","))

    if transcription_unit_quantity > 2:
        #### Transcription unit 3 ####
        selected_promoters_3 = (GUI.transcription_unit_3_promoter_entry.get())
        transcription_unit_3_promoters = (selected_promoters_3.split(","))
        print(transcription_unit_3_promoters)

        selected_rbs_3 = (GUI.transcription_unit_3_rbs_entry.get())
        transcription_unit_3_rbs = (selected_rbs_3.split(","))

        if signal_peptide_choice == "Yes":
            selected_signal_3 = (GUI.transcription_unit_3_signal_entry.get())
            transcription_unit_3_rbs = (selected_signal_3.split(","))

        selected_cds_3 = (GUI.transcription_unit_3_cds_entry.get())
        transcription_unit_3_rbs = (selected_cds_3.split(","))

        selected_terminator_3 = (GUI.transcription_unit_3_terminator_entry.get())
        transcription_unit_3_terminator = (selected_terminator_3.split(","))

    if transcription_unit_quantity > 3:
        #### Transcription unit 4 ####
        selected_promoters_4 = (GUI.transcription_unit_4_promoter_entry.get())
        transcription_unit_4_promoters = (selected_promoters_4.split(","))
        print(transcription_unit_4_promoters)

        selected_rbs_4 = (GUI.transcription_unit_4_rbs_entry.get())
        transcription_unit_4_rbs = (selected_rbs_4.split(","))

        if signal_peptide_choice == "Yes":
            selected_signal_4 = (GUI.transcription_unit_4_signal_entry.get())
            transcription_unit_4_rbs = (selected_signal_4.split(","))

        selected_cds_4 = (GUI.transcription_unit_4_cds_entry.get())
        transcription_unit_4_rbs = (selected_cds_4.split(","))

        selected_terminator_4 = (GUI.transcription_unit_4_terminator_entry.get())
        transcription_unit_4_terminator = (selected_terminator_4.split(","))

    if transcription_unit_quantity > 4:
        #### Transcription unit 5 ####
        selected_promoters_5 = (GUI.transcription_unit_5_promoter_entry.get())
        transcription_unit_5_promoters = (selected_promoters_5.split(","))
        print(transcription_unit_5_promoters)

        selected_rbs_5 = (GUI.transcription_unit_5_rbs_entry.get())
        transcription_unit_5_rbs = (selected_rbs_5.split(","))

        if signal_peptide_choice == "Yes":
            selected_signal_5 = (GUI.transcription_unit_5_signal_entry.get())
            transcription_unit_5_rbs = (selected_signal_5.split(","))

        selected_cds_5 = (GUI.transcription_unit_5_cds_entry.get())
        transcription_unit_5_rbs = (selected_cds_5.split(","))

        selected_terminator_5 = (GUI.transcription_unit_5_terminator_entry.get())
        transcription_unit_5_terminator = (selected_terminator_5.split(","))










