# Import libraries
from sbol import *
import re

# Import scripts
import Main
import GUI

# global variables
primary_structure_identities = []
primary_structure_roles = []
primary_structure_descriptions = []
base_composition = []
detected_restriction_sites = []
level_0_promoter = {}
level_0_promoter_display = []
level_0_rbs = {}
level_0_rbs_display = []
level_0_cds = {}
level_0_cds_display = []
level_0_terminator = {}
level_0_terminator_display = []
level_0_signal = {}
level_0_signal_display = []
level_0_other = {}
level_0_other_display = []
level_2_template = []
ecoflex_check_list = []
bacilloflex_check_list = []
forbidden_sites_ecoflex = ["catatg", "gtatac", "ggatcc", "cctagg", "ggtctc", "ccagag", "cgtctc", "gcagag"]
modification_dictionary = {}
transcription_unit_1_variants = {}
transcription_unit_2_variants = {}
transcription_unit_3_variants = {}
transcription_unit_4_variants = {}
transcription_unit_5_variants = {}
level_2_variants = {}


# clear globals function
def clear_globals():
    primary_structure_identities.clear()
    primary_structure_roles.clear()
    primary_structure_descriptions.clear()
    base_composition.clear()
    detected_restriction_sites.clear()


# Import part from file
def import_design(event):
    clear_globals()
    GUI.select_design_import()
    imported_design = GUI.single_imported_design
    Main.doc.append(imported_design)
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


def initial_design_analysis(uri):
    design_sequence = uri.sequence.elements
    nucleotide_content(design_sequence)
    detect_restriction_sites(design_sequence)


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


# Detect EcoFlex and BacilloFlex restriction sites in imported design (for design analysis display)
def detect_restriction_sites(sequence):
    for component in primary_structure_cd:
        if "catatg" in str(component.sequence.elements):
            detected_restriction_sites.append("NdeI restriction site" + " detected in " + str(component.displayId))
        if "gtatac" in str(component.sequence.elements):
            detected_restriction_sites.append("NdeI restriction site" + " detected in " + str(component.displayId))

        if "ggatcc" in str(component.sequence.elements):
            detected_restriction_sites.append("BamHI restriction site" + " detected in " + str(component.displayId))
        if "cctagg" in str(component.sequence.elements):
            detected_restriction_sites.append("BamHI restriction site" + " detected in " + str(component.displayId))

        if "ggtctc" in str(component.sequence.elements):
            detected_restriction_sites.append("BsaI restriction site" + " detected in " + str(component.displayId))
        if "ccagag" in str(component.sequence.elements):
            detected_restriction_sites.append("BsaI restriction site" + " detected in " + str(component.displayId))

        if "cgtctc" in str(component.sequence.elements):
            detected_restriction_sites.append("BsmBI restriction site" + " detected in " + str(component.displayId))
        if "gcagag" in str(component.sequence.elements):
            detected_restriction_sites.append("BsmBI restriction site" + " detected in " + str(component.displayId))


############################ level 0 library #################################
def import_design_parts_to_library(event):
    primary_structure_cd = design_uri.getPrimaryStructure()
    for component in primary_structure_cd:
        if "0000167" in str(component.roles):
            level_0_promoter["p" + str(len(level_0_promoter) + 1)] = component
            level_0_promoter_display.append("p" + str(len(level_0_promoter)) + ". " + str(component.displayId))
        elif "0000139" in str(component.roles):
            level_0_rbs["r" + str(len(level_0_rbs) + 1)] = component
            level_0_rbs_display.append("r" + str(len(level_0_rbs)) + ". " + str(component.displayId))
        elif "0000316" in str(component.roles):
            level_0_cds["c" + str(len(level_0_cds) + 1)] = component
            level_0_cds_display.append("c" + str(len(level_0_cds)) + ". " + str(component.displayId))
        elif "0000141" in str(component.roles):
            level_0_terminator["t" + str(len(level_0_terminator) + 1)] = component
            level_0_terminator_display.append("t" + str(len(level_0_terminator)) + ". " + str(component.displayId))
        elif "0000324" in str(component.roles):
            level_0_signal["s" + str(len(level_0_signal) + 1)] = component
            level_0_signal_display.append("s" + str(len(level_0_signal)) + ". " + str(component.displayId))
        else:
            level_0_other["o" + str(len(level_0_other) + 1)] = component
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
        level_0_signal["s" + str(len(level_0_signal))] = design_uri
        level_0_signal_display.append("s" + str(len(level_0_signal)) + ". " + str(design_uri.displayId))
    else:
        level_0_other["o" + str(len(level_0_other))] = design_uri
        level_0_other_display.append("o" + str(len(level_0_other)) + ". " + str(design_uri.displayId))
    GUI.refresh_level_0_library()


# create part selection component definition lists for transcription units
def part_selection_lists():
    transcription_unit_quantity = int(GUI.transcription_unit_quantity_combo.get())
    signal_choice = GUI.include_signal_combo.get()
    if transcription_unit_quantity > 1:
        selected_promoter_1 = (GUI.transcription_unit_1_promoter_entry.get())
        transcription_unit_1_promoter_keys = (selected_promoter_1.split(", "))
        global transcription_unit_1_promoter
        transcription_unit_1_promoter = []
        for selection in transcription_unit_1_promoter_keys:
            transcription_unit_1_promoter.append(level_0_promoter[selection])

        selected_rbs_1 = (GUI.transcription_unit_1_rbs_entry.get())
        transcription_unit_1_rbs_keys = (selected_rbs_1.split(","))
        global transcription_unit_1_rbs
        transcription_unit_1_rbs = []
        for selection in transcription_unit_1_rbs_keys:
            transcription_unit_1_rbs.append(level_0_rbs[selection])

        if signal_choice == "Yes":
            selected_signal_1 = (GUI.transcription_unit_1_signal_entry.get())
            transcription_unit_1_signal_keys = (selected_signal_1.split(","))
            global transcription_unit_1_signal
            transcription_unit_1_signal = []
            for selection in transcription_unit_1_signal_keys:
                transcription_unit_1_signal.append(level_0_signal[selection])

        selected_cds_1 = (GUI.transcription_unit_1_cds_entry.get())
        transcription_unit_1_cds_keys = (selected_cds_1.split(","))
        global transcription_unit_1_cds
        transcription_unit_1_cds = []
        for selection in transcription_unit_1_cds_keys:
            transcription_unit_1_cds.append(level_0_cds[selection])

        selected_terminator_1 = (GUI.transcription_unit_1_terminator_entry.get())
        transcription_unit_1_terminator_keys = (selected_terminator_1.split(","))
        global transcription_unit_1_terminator
        transcription_unit_1_terminator = []
        for selection in transcription_unit_1_terminator_keys:
            transcription_unit_1_terminator.append(level_0_terminator[selection])

        selected_promoter_2 = (GUI.transcription_unit_2_promoter_entry.get())
        transcription_unit_2_promoter_keys = (selected_promoter_2.split(","))
        global transcription_unit_2_promoter
        transcription_unit_2_promoter = []
        for selection in transcription_unit_2_promoter_keys:
            transcription_unit_2_promoter.append(level_0_promoter[selection])

        selected_rbs_2 = (GUI.transcription_unit_2_rbs_entry.get())
        transcription_unit_2_rbs_keys = (selected_rbs_2.split(","))
        global transcription_unit_2_rbs
        transcription_unit_2_rbs = []
        for selection in transcription_unit_2_rbs_keys:
            transcription_unit_2_rbs.append(level_0_rbs[selection])

        if signal_choice == "Yes":
            selected_signal_2 = (GUI.transcription_unit_2_signal_entry.get())
            transcription_unit_2_signal_keys = (selected_signal_2.split(","))
            global transcription_unit_2_signal
            transcription_unit_2_signal = []
            for selection in transcription_unit_2_signal_keys:
                transcription_unit_2_signal.append(level_0_signal[selection])

        selected_cds_2 = (GUI.transcription_unit_2_cds_entry.get())
        transcription_unit_2_cds_keys = (selected_cds_2.split(","))
        global transcription_unit_2_cds
        transcription_unit_2_cds = []
        for selection in transcription_unit_2_cds_keys:
            transcription_unit_2_cds.append(level_0_cds[selection])

        selected_terminator_2 = (GUI.transcription_unit_2_terminator_entry.get())
        transcription_unit_2_terminator_keys = (selected_terminator_2.split(","))
        global transcription_unit_2_terminator
        transcription_unit_2_terminator = []
        for selection in transcription_unit_2_terminator_keys:
            transcription_unit_2_terminator.append(level_0_terminator[selection])

    if transcription_unit_quantity > 2:
        selected_promoter_3 = (GUI.transcription_unit_3_promoter_entry.get())
        transcription_unit_3_promoter_keys = (selected_promoter_3.split(","))
        global transcription_unit_3_promoter
        transcription_unit_3_promoter = []
        for selection in transcription_unit_3_promoter_keys:
            transcription_unit_3_promoter.append(level_0_promoter[selection])

        selected_rbs_3 = (GUI.transcription_unit_3_rbs_entry.get())
        transcription_unit_3_rbs_keys = (selected_rbs_3.split(","))
        global transcription_unit_3_rbs
        transcription_unit_3_rbs = []
        for selection in transcription_unit_3_rbs_keys:
            transcription_unit_3_rbs.append(level_0_rbs[selection])

        if signal_choice == "Yes":
            selected_signal_3 = (GUI.transcription_unit_3_signal_entry.get())
            transcription_unit_3_signal_keys = (selected_signal_3.split(","))
            global transcription_unit_3_signal
            transcription_unit_3_signal = []
            for selection in transcription_unit_3_signal_keys:
                transcription_unit_3_signal.append(level_0_signal[selection])

        selected_cds_3 = (GUI.transcription_unit_3_cds_entry.get())
        transcription_unit_3_cds_keys = (selected_cds_3.split(","))
        global transcription_unit_3_cds
        transcription_unit_3_cds = []
        for selection in transcription_unit_3_cds_keys:
            transcription_unit_3_cds.append(level_0_cds[selection])

        selected_terminator_3 = (GUI.transcription_unit_3_terminator_entry.get())
        transcription_unit_3_terminator_keys = (selected_terminator_3.split(","))
        global transcription_unit_3_terminator
        transcription_unit_3_terminator = []
        for selection in transcription_unit_3_terminator_keys:
            transcription_unit_3_terminator.append(level_0_terminator[selection])

    if transcription_unit_quantity > 3:
        selected_promoter_4 = (GUI.transcription_unit_4_promoter_entry.get())
        transcription_unit_4_promoter_keys = (selected_promoter_4.split(","))
        global transcription_unit_4_promoter
        transcription_unit_4_promoter = []
        for selection in transcription_unit_4_promoter_keys:
            transcription_unit_4_promoter.append(level_0_promoter[selection])

        selected_rbs_4 = (GUI.transcription_unit_4_rbs_entry.get())
        transcription_unit_4_rbs_keys = (selected_rbs_4.split(","))
        global transcription_unit_4_rbs
        transcription_unit_4_rbs = []
        for selection in transcription_unit_4_rbs_keys:
            transcription_unit_4_rbs.append(level_0_rbs[selection])

        if signal_choice == "Yes":
            selected_signal_4 = (GUI.transcription_unit_4_signal_entry.get())
            transcription_unit_4_signal_keys = (selected_signal_4.split(","))
            global transcription_unit_4_signal
            transcription_unit_4_signal = []
            for selection in transcription_unit_4_signal_keys:
                transcription_unit_4_signal.append(level_0_signal[selection])

        selected_cds_4 = (GUI.transcription_unit_4_cds_entry.get())
        transcription_unit_4_cds_keys = (selected_cds_4.split(","))
        global transcription_unit_4_cds
        transcription_unit_4_cds = []
        for selection in transcription_unit_4_cds_keys:
            transcription_unit_4_cds.append(level_0_cds[selection])

        selected_terminator_4 = (GUI.transcription_unit_4_terminator_entry.get())
        transcription_unit_4_terminator_keys = (selected_terminator_4.split(","))
        global transcription_unit_4_terminator
        transcription_unit_4_terminator = []
        for selection in transcription_unit_4_terminator_keys:
            transcription_unit_4_terminator.append(level_0_terminator[selection])

    if transcription_unit_quantity > 4:
        selected_promoter_5 = (GUI.transcription_unit_5_promoter_entry.get())
        transcription_unit_5_promoter_keys = (selected_promoter_5.split(","))
        global transcription_unit_5_promoter
        transcription_unit_5_promoter = []
        for selection in transcription_unit_5_promoter_keys:
            transcription_unit_5_promoter.append(level_0_promoter[selection])

        selected_rbs_5 = (GUI.transcription_unit_5_rbs_entry.get())
        transcription_unit_5_rbs_keys = (selected_rbs_5.split(","))
        global transcription_unit_5_rbs
        transcription_unit_5_rbs = []
        for selection in transcription_unit_5_rbs_keys:
            transcription_unit_5_rbs.append(level_0_rbs[selection])

        if signal_choice == "Yes":
            selected_signal_5 = (GUI.transcription_unit_5_signal_entry.get())
            transcription_unit_5_signal_keys = (selected_signal_5.split(","))
            global transcription_unit_5_signal
            transcription_unit_5_signal = []
            for selection in transcription_unit_5_signal_keys:
                transcription_unit_5_signal.append(level_0_signal[selection])

        selected_cds_5 = (GUI.transcription_unit_5_cds_entry.get())
        transcription_unit_5_cds_keys = (selected_cds_5.split(","))
        global transcription_unit_5_cds
        transcription_unit_5_cds = []
        for selection in transcription_unit_5_cds_keys:
            transcription_unit_5_cds.append(level_0_cds[selection])

        selected_terminator_5 = (GUI.transcription_unit_5_terminator_entry.get())
        transcription_unit_5_terminator_keys = (selected_terminator_5.split(","))
        global transcription_unit_5_terminator
        transcription_unit_5_terminator = []
        for selection in transcription_unit_5_terminator_keys:
            transcription_unit_5_terminator.append(level_0_terminator[selection])


def ecoflex_restriction_site_check(component_definition, unit_number):
    if "catatg" in str(component_definition.sequence.elements):
        ecoflex_check_list.append("NdeI restriction site" + " detected in " + str(component_definition.displayId)
                                  + " in transcription unit " + str(unit_number))
    if "gtatac" in str(component_definition.sequence.elements):
        ecoflex_check_list.append("NdeI restriction site" + " detected in " + str(component_definition.displayId)
                                  + " in transcription unit " + str(unit_number))

    if "ggatcc" in str(component_definition.sequence.elements):
        ecoflex_check_list.append("BamHI restriction site" + " detected in " + str(component_definition.displayId)
                                  + " in transcription unit " + str(unit_number))
    if "cctagg" in str(component_definition.sequence.elements):
        ecoflex_check_list.append("BamHI restriction site" + " detected in " + str(component_definition.displayId))

    if "ggtctc" in str(component_definition.sequence.elements):
        ecoflex_check_list.append("BsaI restriction site" + " detected in " + str(component_definition.displayId)
                                  + " in transcription unit " + str(unit_number))
    if "ccagag" in str(component_definition.sequence.elements):
        ecoflex_check_list.append("BsaI restriction site" + " detected in " + str(component_definition.displayId)
                                  + " in transcription unit " + str(unit_number))

    if "cgtctc" in str(component_definition.sequence.elements):
        ecoflex_check_list.append("BsmBI restriction site" + " detected in " + str(component_definition.displayId)
                                  + " in transcription unit " + str(unit_number))
    if "gcagag" in str(component_definition.sequence.elements):
        ecoflex_check_list.append("BsmBI restriction site" + " detected in " + str(component_definition.displayId)
                                  + " in transcription unit " + str(unit_number))


# Final check of part compatibility before generating protocol
def final_ecoflex_check():
    part_selection_lists()
    transcription_unit_quantity = int(GUI.transcription_unit_quantity_combo.get())
    signal_choice = GUI.include_signal_combo.get()
    global ecoflex_check_list
    ecoflex_check_list = []
    if transcription_unit_quantity > 1:
        for component in transcription_unit_1_promoter:
            ecoflex_restriction_site_check(component, 1)
        for component in transcription_unit_1_rbs:
            ecoflex_restriction_site_check(component, 1)
        if signal_choice == "Yes":
            for component in transcription_unit_1_signal:
                ecoflex_restriction_site_check(component, 1)
        for component in transcription_unit_1_cds:
            ecoflex_restriction_site_check(component, 1)
        for component in transcription_unit_1_terminator:
            ecoflex_restriction_site_check(component, 1)

        for component in transcription_unit_2_promoter:
            ecoflex_restriction_site_check(component, 2)
        for component in transcription_unit_2_rbs:
            ecoflex_restriction_site_check(component, 2)
        if signal_choice == "Yes":
            for component in transcription_unit_2_signal:
                ecoflex_restriction_site_check(component, 2)
        for component in transcription_unit_2_cds:
            ecoflex_restriction_site_check(component, 2)
        for component in transcription_unit_2_terminator:
            ecoflex_restriction_site_check(component, 2)

    if transcription_unit_quantity > 2:
        for component in transcription_unit_3_promoter:
            ecoflex_restriction_site_check(component, 3)
        for component in transcription_unit_3_rbs:
            ecoflex_restriction_site_check(component, 3)
        if signal_choice == "Yes":
            for component in transcription_unit_3_signal:
                ecoflex_restriction_site_check(component, 3)
        for component in transcription_unit_3_cds:
            ecoflex_restriction_site_check(component, 3)
        for component in transcription_unit_3_terminator:
            ecoflex_restriction_site_check(component, 3)

    if transcription_unit_quantity > 3:
        for component in transcription_unit_4_promoter:
            ecoflex_restriction_site_check(component, 4)
        for component in transcription_unit_4_rbs:
            ecoflex_restriction_site_check(component, 4)
        if signal_choice == "Yes":
            for component in transcription_unit_4_signal:
                ecoflex_restriction_site_check(component, 4)
        for component in transcription_unit_4_cds:
            ecoflex_restriction_site_check(component, 4)
        for component in transcription_unit_4_terminator:
            ecoflex_restriction_site_check(component, 4)

    if transcription_unit_quantity > 4:
        for component in transcription_unit_5_promoter:
            ecoflex_restriction_site_check(component, 5)
        for component in transcription_unit_5_rbs:
            ecoflex_restriction_site_check(component, 5)
        if signal_choice == "Yes":
            for component in transcription_unit_5_signal:
                ecoflex_restriction_site_check(component, 5)
        for component in transcription_unit_5_cds:
            ecoflex_restriction_site_check(component, 5)
        for component in transcription_unit_5_terminator:
            ecoflex_restriction_site_check(component, 5)


# Library for codon swapping for EcoFlex protocols
def ecoflex_codon_library(codon):
    if codon == "aaa":
        return "aag"
    if codon == "aag":
        return "aaa"
    if codon == "aat":
        return "aac"
    if codon == "aac":
        return "gaa"
    if codon == "gaa":
        return "aac"
    if codon == "gag":
        return "gaa"
    if codon == "gat":
        return "gag"
    if codon == "gac":
        return "aat"
    if codon == "taa":
        return "tag"
    if codon == "tag":
        return "taa"
    if codon == "tat":
        return "tag"
    if codon == "tac":
        return "invalid"
    if codon == "caa":
        return "cag"
    if codon == "cag":
        return "cat"
    if codon == "cat":
        return "cag"
    if codon == "cac":
        return "caa"
    if codon == "aga":
        return "agg"
    if codon == "agg":
        return "aga"
    if codon == "agt":
        return "agc"
    if codon == "agc":
        return "agt"
    if codon == "gga":
        return "ggt"
    if codon == "ggg":
        return "ggt"
    if codon == "ggt":
        return "ggg"
    if codon == "ggc":
        return "gga"
    if codon == "tga":
        return "tgt"
    if codon == "tgg":
        return "tgc"
    if codon == "tgt":
        return "tga"
    if codon == "tgc":
        return "tga"
    if codon == "cga":
        return "cgt"
    if codon == "cgg":
        return "cgc"
    if codon == "cgt":
        return "cgg"
    if codon == "cgc":
        return "cgg"
    if codon == "ata":
        return "atg"
    if codon == "atg":
        return "ata"
    if codon == "att":
        return "act"
    if codon == "atc":
        return "act"
    if codon == "gta":
        return "gtg"
    if codon == "gtg":
        return "gta"
    if codon == "gtt":
        return "gtc"
    if codon == "gtc":
        return "gtt"
    if codon == "tta":
        return "ttg"
    if codon == "ttg":
        return "tta"
    if codon == "ttt":
        return "ttc"
    if codon == "ttc":
        return "ttt"
    if codon == "cta":
        return "ctg"
    if codon == "ctg":
        return "cta"
    if codon == "ctt":
        return "ctc"
    if codon == "ctc":
        return "ctt"
    if codon == "aca":
        return "acg"
    if codon == "acg":
        return "aca"
    if codon == "act":
        return "att"
    if codon == "acc":
        return "invalid"
    if codon == "gca":
        return "gcg"
    if codon == "gcg":
        return "gca"
    if codon == "gct":
        return "gcc"
    if codon == "gcc":
        return "gct"
    if codon == "tca":
        return "agt"
    if codon == "tcg":
        return "agc"
    if codon == "tct":
        return "tcc"
    if codon == "tcc":
        return "tct"
    if codon == "cca":
        return "cct"
    if codon == "ccg":
        return "cca"
    if codon == "cct":
        return "ccc"
    if codon == "ccc":
        return "cct"


def restriction_site_name_library(sequence):
    if sequence == "catatg":
        return "NdeI"
    if sequence == "gtatac":
        return "NdeI"
    if sequence == "ggatcc":
        return "BamHI"
    if sequence == "cctagg":
        return "BamHI"
    if sequence == "ggtctc":
        return "BsaI"
    if sequence == "ccagag":
        return "BsaI"
    if sequence == "cgtctc":
        return "BsmBI"
    if sequence == "gcagag":
        return "BsmBI"


# Create codon-swapped variants of CDS parts that contain excluded restriction sites - For EcoFlex
def swap_codons_ecoflex():
    if int(GUI.transcription_unit_quantity_combo.get()) > 1:
        # Transcription unit 1
        cds_number = 0
        for cds in transcription_unit_1_cds:
            cds_number = cds_number + 1
            part_key = "unit1_c" + str(cds_number)
            global modification_dictionary
            modification_dictionary[part_key] = []
            modification_dictionary[part_key].append(cds)
            global sequence
            sequence = cds.sequence.elements
            detected_sites = True
            while detected_sites:
                for forbidden_site in forbidden_sites_ecoflex:
                    count = (sequence.count(forbidden_site))
                    if count == 0:
                        if forbidden_site == "gcagag":
                            no_sites_detected = 0
                            for forbidden_site in forbidden_sites_ecoflex:
                                count_2 = (sequence.count(forbidden_site))
                                if count_2 == 0:
                                    no_sites_detected = no_sites_detected + 1
                                    if no_sites_detected == 8:
                                        detected_sites = False
                                    else:
                                        pass
                                else:
                                    continue
                        else:
                            pass
                    else:
                        while count > 0:
                            location = (sequence.find(forbidden_site))
                            codon_list = ([sequence[i:i + 3] for i in range(0, len(sequence), 3)])
                            codon = codon_list[int((location / 3) + 1)]
                            new_codon = ecoflex_codon_library(codon)
                            if new_codon == "invalid":
                                modification_dictionary[part_key].append("Restriction site " + forbidden_site +
                                                                         " (" + site_name + ")" + " detected at " +
                                                                         "position " + str(location + 2) + "-" +
                                                                         str(location + 4) +
                                                                         " but was unable to be changed due " +
                                                                         "to unavailable codon alternative " + "for " +
                                                                         str(codon))
                                count = count - 1
                                if count == 0:
                                    if forbidden_site == "gcagag":
                                        no_sites_detected = 0
                                        for forbidden_site in forbidden_sites_ecoflex:
                                            count_4 = (sequence.count(forbidden_site))
                                            if count_4 == 0:
                                                no_sites_detected = no_sites_detected + 1
                                                if no_sites_detected == 8:
                                                    detected_sites = False
                                                else:
                                                    pass
                                            else:
                                                continue
                                    else:
                                        pass

                            else:
                                codon_list[int((location / 3) + 1)] = new_codon
                                codon_string = (", ".join(codon_list))
                                sequence = codon_string.replace(", ", "")
                                site_name = restriction_site_name_library(forbidden_site)
                                modification_dictionary[part_key].append("Codon " + str(codon) + " replaced with " +
                                                                         str(new_codon) + " at position " +
                                                                         str(location + 2) + "-" + str(location + 4)
                                                                         + " to remove " +
                                                                         forbidden_site + " (" + site_name + ")" +
                                                                         " restriction site")
                                count = count - 1
                                if count == 0:
                                    if forbidden_site == "gcagag":
                                        no_sites_detected = 0
                                        for forbidden_site in forbidden_sites_ecoflex:
                                            count_3 = (sequence.count(forbidden_site))
                                            if count_3 == 0:
                                                no_sites_detected = no_sites_detected + 1
                                                if no_sites_detected == 8:
                                                    detected_sites = False
                                                else:
                                                    pass
                                            else:
                                                continue
                                    else:
                                        pass
            cds.sequence.elements = sequence

        # Transcription unit 2
        cds_number = 0
        for cds in transcription_unit_2_cds:
            cds_number = cds_number + 1
            part_key = "unit2_c" + str(cds_number)
            modification_dictionary[part_key] = []
            modification_dictionary[part_key].append(cds)
            sequence = cds.sequence.elements
            detected_sites = True
            while detected_sites:
                for forbidden_site in forbidden_sites_ecoflex:
                    count = (sequence.count(forbidden_site))
                    if count == 0:
                        if forbidden_site == "gcagag":
                            no_sites_detected = 0
                            for forbidden_site in forbidden_sites_ecoflex:
                                count_2 = (sequence.count(forbidden_site))
                                if count_2 == 0:
                                    no_sites_detected = no_sites_detected + 1
                                    if no_sites_detected == 8:
                                        detected_sites = False
                                    else:
                                        pass
                                else:
                                    continue
                        else:
                            pass
                    else:
                        while count > 0:
                            location = (sequence.find(forbidden_site))
                            codon_list = ([sequence[i:i + 3] for i in range(0, len(sequence), 3)])
                            codon = codon_list[int((location / 3) + 1)]
                            new_codon = ecoflex_codon_library(codon)
                            if new_codon == "invalid":
                                modification_dictionary[part_key].append("Restriction site " + forbidden_site +
                                                                         " (" + site_name + ")" + " detected at " +
                                                                         "position " + str(location + 2) + "-" +
                                                                         str(location + 4) +
                                                                         " but was unable to be changed due " +
                                                                         "to unavailable codon alternative " + "for " +
                                                                         str(codon))
                                count = count - 1
                                if count == 0:
                                    if forbidden_site == "gcagag":
                                        no_sites_detected = 0
                                        for forbidden_site in forbidden_sites_ecoflex:
                                            count_4 = (sequence.count(forbidden_site))
                                            if count_4 == 0:
                                                no_sites_detected = no_sites_detected + 1
                                                if no_sites_detected == 8:
                                                    detected_sites = False
                                                else:
                                                    pass
                                            else:
                                                continue
                                    else:
                                        pass

                            else:
                                codon_list[int((location / 3) + 1)] = new_codon
                                codon_string = (", ".join(codon_list))
                                sequence = codon_string.replace(", ", "")
                                site_name = restriction_site_name_library(forbidden_site)
                                modification_dictionary[part_key].append("Codon " + str(codon) + " replaced with " +
                                                                         str(new_codon) + " at position " +
                                                                         str(location + 2) + "-" + str(location + 4)
                                                                         + " to remove " +
                                                                         forbidden_site + " (" + site_name + ")" +
                                                                         " restriction site")
                                count = count - 1
                                if count == 0:
                                    if forbidden_site == "gcagag":
                                        no_sites_detected = 0
                                        for forbidden_site in forbidden_sites_ecoflex:
                                            count_3 = (sequence.count(forbidden_site))
                                            if count_3 == 0:
                                                no_sites_detected = no_sites_detected + 1
                                                if no_sites_detected == 8:
                                                    detected_sites = False
                                                else:
                                                    pass
                                            else:
                                                continue
                                    else:
                                        pass
            cds.sequence.elements = sequence

    if int(GUI.transcription_unit_quantity_combo.get()) > 2:
        # Transcription unit 3
        cds_number = 0
        for cds in transcription_unit_3_cds:
            cds_number = cds_number + 1
            part_key = "unit3_c" + str(cds_number)
            modification_dictionary[part_key] = []
            modification_dictionary[part_key].append(cds)
            sequence = cds.sequence.elements
            detected_sites = True
            while detected_sites:
                for forbidden_site in forbidden_sites_ecoflex:
                    count = (sequence.count(forbidden_site))
                    if count == 0:
                        if forbidden_site == "gcagag":
                            no_sites_detected = 0
                            for forbidden_site in forbidden_sites_ecoflex:
                                count_2 = (sequence.count(forbidden_site))
                                if count_2 == 0:
                                    no_sites_detected = no_sites_detected + 1
                                    if no_sites_detected == 8:
                                        detected_sites = False
                                    else:
                                        pass
                                else:
                                    continue
                        else:
                            pass
                    else:
                        while count > 0:
                            location = (sequence.find(forbidden_site))
                            codon_list = ([sequence[i:i + 3] for i in range(0, len(sequence), 3)])
                            codon = codon_list[int((location / 3) + 1)]
                            new_codon = ecoflex_codon_library(codon)
                            if new_codon == "invalid":
                                modification_dictionary[part_key].append("Restriction site " + forbidden_site +
                                                                         " (" + site_name + ")" + " detected at " +
                                                                         "position " + str(location + 2) + "-" +
                                                                         str(location + 4) +
                                                                         " but was unable to be changed due " +
                                                                         "to unavailable codon alternative " + "for " +
                                                                         str(codon))
                                count = count - 1
                                if count == 0:
                                    if forbidden_site == "gcagag":
                                        no_sites_detected = 0
                                        for forbidden_site in forbidden_sites_ecoflex:
                                            count_4 = (sequence.count(forbidden_site))
                                            if count_4 == 0:
                                                no_sites_detected = no_sites_detected + 1
                                                if no_sites_detected == 8:
                                                    detected_sites = False
                                                else:
                                                    pass
                                            else:
                                                continue
                                    else:
                                        pass

                            else:
                                codon_list[int((location / 3) + 1)] = new_codon
                                codon_string = (", ".join(codon_list))
                                sequence = codon_string.replace(", ", "")
                                site_name = restriction_site_name_library(forbidden_site)
                                modification_dictionary[part_key].append("Codon " + str(codon) + " replaced with " +
                                                                         str(new_codon) + " at position " +
                                                                         str(location + 2) + "-" + str(location + 4)
                                                                         + " to remove " +
                                                                         forbidden_site + " (" + site_name + ")" +
                                                                         " restriction site")
                                count = count - 1
                                if count == 0:
                                    if forbidden_site == "gcagag":
                                        no_sites_detected = 0
                                        for forbidden_site in forbidden_sites_ecoflex:
                                            count_3 = (sequence.count(forbidden_site))
                                            if count_3 == 0:
                                                no_sites_detected = no_sites_detected + 1
                                                if no_sites_detected == 8:
                                                    detected_sites = False
                                                else:
                                                    pass
                                            else:
                                                continue
                                    else:
                                        pass
            cds.sequence.elements = sequence

    if int(GUI.transcription_unit_quantity_combo.get()) > 3:
        # Transcription unit 4
        cds_number = 0
        for cds in transcription_unit_4_cds:
            cds_number = cds_number + 1
            part_key = "unit4_c" + str(cds_number)
            modification_dictionary[part_key] = []
            modification_dictionary[part_key].append(cds)
            sequence = cds.sequence.elements
            detected_sites = True
            while detected_sites:
                for forbidden_site in forbidden_sites_ecoflex:
                    count = (sequence.count(forbidden_site))
                    if count == 0:
                        if forbidden_site == "gcagag":
                            no_sites_detected = 0
                            for forbidden_site in forbidden_sites_ecoflex:
                                count_2 = (sequence.count(forbidden_site))
                                if count_2 == 0:
                                    no_sites_detected = no_sites_detected + 1
                                    if no_sites_detected == 8:
                                        detected_sites = False
                                    else:
                                        pass
                                else:
                                    continue
                        else:
                            pass
                    else:
                        while count > 0:
                            location = (sequence.find(forbidden_site))
                            codon_list = ([sequence[i:i + 3] for i in range(0, len(sequence), 3)])
                            codon = codon_list[int((location / 3) + 1)]
                            new_codon = ecoflex_codon_library(codon)
                            if new_codon == "invalid":
                                modification_dictionary[part_key].append("Restriction site " + forbidden_site +
                                                                         " (" + site_name + ")" + " detected at " +
                                                                         "position " + str(location + 2) + "-" +
                                                                         str(location + 4) +
                                                                         " but was unable to be changed due " +
                                                                         "to unavailable codon alternative " + "for " +
                                                                         str(codon))
                                count = count - 1
                                if count == 0:
                                    if forbidden_site == "gcagag":
                                        no_sites_detected = 0
                                        for forbidden_site in forbidden_sites_ecoflex:
                                            count_4 = (sequence.count(forbidden_site))
                                            if count_4 == 0:
                                                no_sites_detected = no_sites_detected + 1
                                                if no_sites_detected == 8:
                                                    detected_sites = False
                                                else:
                                                    pass
                                            else:
                                                continue
                                    else:
                                        pass

                            else:
                                codon_list[int((location / 3) + 1)] = new_codon
                                codon_string = (", ".join(codon_list))
                                sequence = codon_string.replace(", ", "")
                                site_name = restriction_site_name_library(forbidden_site)
                                modification_dictionary[part_key].append("Codon " + str(codon) + " replaced with " +
                                                                         str(new_codon) + " at position " +
                                                                         str(location + 2) + "-" + str(location + 4)
                                                                         + " to remove " +
                                                                         forbidden_site + " (" + site_name + ")" +
                                                                         " restriction site")
                                count = count - 1
                                if count == 0:
                                    if forbidden_site == "gcagag":
                                        no_sites_detected = 0
                                        for forbidden_site in forbidden_sites_ecoflex:
                                            count_3 = (sequence.count(forbidden_site))
                                            if count_3 == 0:
                                                no_sites_detected = no_sites_detected + 1
                                                if no_sites_detected == 8:
                                                    detected_sites = False
                                                else:
                                                    pass
                                            else:
                                                continue
                                    else:
                                        pass
            cds.sequence.elements = sequence

    if int(GUI.transcription_unit_quantity_combo.get()) > 4:
        # Transcription unit 5
        cds_number = 0
        for cds in transcription_unit_5_cds:
            cds_number = cds_number + 1
            part_key = "unit5_c" + str(cds_number)
            modification_dictionary[part_key] = []
            modification_dictionary[part_key].append(cds)
            sequence = cds.sequence.elements
            detected_sites = True
            while detected_sites:
                for forbidden_site in forbidden_sites_ecoflex:
                    count = (sequence.count(forbidden_site))
                    if count == 0:
                        if forbidden_site == "gcagag":
                            no_sites_detected = 0
                            for forbidden_site in forbidden_sites_ecoflex:
                                count_2 = (sequence.count(forbidden_site))
                                if count_2 == 0:
                                    no_sites_detected = no_sites_detected + 1
                                    if no_sites_detected == 8:
                                        detected_sites = False
                                    else:
                                        pass
                                else:
                                    continue
                        else:
                            pass
                    else:
                        while count > 0:
                            location = (sequence.find(forbidden_site))
                            codon_list = ([sequence[i:i + 3] for i in range(0, len(sequence), 3)])
                            codon = codon_list[int((location / 3) + 1)]
                            new_codon = ecoflex_codon_library(codon)
                            if new_codon == "invalid":
                                modification_dictionary[part_key].append("Restriction site " + forbidden_site +
                                                                         " (" + site_name + ")" + " detected at " +
                                                                         "position " + str(location + 2) + "-" +
                                                                         str(location + 4) +
                                                                         " but was unable to be changed due " +
                                                                         "to unavailable codon alternative " + "for " +
                                                                         str(codon))
                                count = count - 1
                                if count == 0:
                                    if forbidden_site == "gcagag":
                                        no_sites_detected = 0
                                        for forbidden_site in forbidden_sites_ecoflex:
                                            count_4 = (sequence.count(forbidden_site))
                                            if count_4 == 0:
                                                no_sites_detected = no_sites_detected + 1
                                                if no_sites_detected == 8:
                                                    detected_sites = False
                                                else:
                                                    pass
                                            else:
                                                continue
                                    else:
                                        pass

                            else:
                                codon_list[int((location / 3) + 1)] = new_codon
                                codon_string = (", ".join(codon_list))
                                sequence = codon_string.replace(", ", "")
                                site_name = restriction_site_name_library(forbidden_site)
                                modification_dictionary[part_key].append("Codon " + str(codon) + " replaced with " +
                                                                         str(new_codon) + " at position " +
                                                                         str(location + 2) + "-" + str(location + 4)
                                                                         + " to remove " +
                                                                         forbidden_site + " (" + site_name + ")" +
                                                                         " restriction site")
                                count = count - 1
                                if count == 0:
                                    if forbidden_site == "gcagag":
                                        no_sites_detected = 0
                                        for forbidden_site in forbidden_sites_ecoflex:
                                            count_3 = (sequence.count(forbidden_site))
                                            if count_3 == 0:
                                                no_sites_detected = no_sites_detected + 1
                                                if no_sites_detected == 8:
                                                    detected_sites = False
                                                else:
                                                    pass
                                            else:
                                                continue
                                    else:
                                        pass
            cds.sequence.elements = sequence


# Note restriction sites present in bioparts (promoter, rbs, signal peptide, terminator)
def check_biopart_sites_ecoflex():
    if int(GUI.transcription_unit_quantity_combo.get()) > 1:
        # Transcription unit 1
        promoter_number = 0
        for promoter in transcription_unit_1_promoter:
            promoter_number = promoter_number + 1
            part_key = "unit1_p" + str(promoter_number)
            global modification_dictionary
            modification_dictionary[part_key] = []
            modification_dictionary[part_key].append(promoter)
            global sequence
            sequence = promoter.sequence.elements
            for forbidden_site in forbidden_sites_ecoflex:
                count = (sequence.count(forbidden_site))
                if count == 0:
                    pass
                else:
                    for location in re.finditer(forbidden_site, sequence):
                        site_name = restriction_site_name_library(forbidden_site)
                        modification_dictionary[part_key].append("Restriction site " + forbidden_site + " (" +
                                                                 site_name + ")" + " detected at position " +
                                                                 str(location.start() + 1) + "-" +
                                                                 str(location.end()))

        rbs_number = 0
        for rbs in transcription_unit_1_rbs:
            rbs_number = rbs_number + 1
            part_key = "unit1_r" + str(rbs_number)
            modification_dictionary[part_key] = []
            modification_dictionary[part_key].append(rbs)
            sequence = rbs.sequence.elements
            for forbidden_site in forbidden_sites_ecoflex:
                count = (sequence.count(forbidden_site))
                if count == 0:
                    pass
                else:
                    for location in re.finditer(forbidden_site, sequence):
                        site_name = restriction_site_name_library(forbidden_site)
                        modification_dictionary[part_key].append("Restriction site " + forbidden_site + " (" +
                                                                 site_name + ")" + " detected at position " +
                                                                 str(location.start() + 1) + "-" +
                                                                 str(location.end()))

        if GUI.include_signal_combo.get() == "Yes":
            signal_number = 0
            for signal in transcription_unit_1_signal:
                signal_number = signal_number + 1
                part_key = "unit1_s" + str(signal_number)
                modification_dictionary[part_key] = []
                modification_dictionary[part_key].append(signal)
                sequence = signal.sequence.elements
                for forbidden_site in forbidden_sites_ecoflex:
                    count = (sequence.count(forbidden_site))
                    if count == 0:
                        pass
                    else:
                        for location in re.finditer(forbidden_site, sequence):
                            site_name = restriction_site_name_library(forbidden_site)
                            modification_dictionary[part_key].append("Restriction site " + forbidden_site + " (" +
                                                                     site_name + ")" + " detected at position " +
                                                                     str(location.start() + 1) + "-" +
                                                                     str(location.end()))

        terminator_number = 0
        for terminator in transcription_unit_1_terminator:
            terminator_number = terminator_number + 1
            part_key = "unit1_t" + str(terminator_number)
            modification_dictionary[part_key] = []
            modification_dictionary[part_key].append(terminator)
            sequence = terminator.sequence.elements
            for forbidden_site in forbidden_sites_ecoflex:
                count = (sequence.count(forbidden_site))
                if count == 0:
                    pass
                else:
                    for location in re.finditer(forbidden_site, sequence):
                        site_name = restriction_site_name_library(forbidden_site)
                        modification_dictionary[part_key].append("Restriction site " + forbidden_site + " (" +
                                                                 site_name + ")" + " detected at position " +
                                                                 str(location.start() + 1) + "-" +
                                                                 str(location.end()))

        # Transcription unit 2
        promoter_number = 0
        for promoter in transcription_unit_2_promoter:
            promoter_number = promoter_number + 1
            part_key = "unit2_p" + str(promoter_number)
            modification_dictionary[part_key] = []
            modification_dictionary[part_key].append(promoter)
            sequence = promoter.sequence.elements
            for forbidden_site in forbidden_sites_ecoflex:
                count = (sequence.count(forbidden_site))
                if count == 0:
                    pass
                else:
                    for location in re.finditer(forbidden_site, sequence):
                        site_name = restriction_site_name_library(forbidden_site)
                        modification_dictionary[part_key].append("Restriction site " + forbidden_site + " (" +
                                                                 site_name + ")" + " detected at position " +
                                                                 str(location.start() + 1) + "-" +
                                                                 str(location.end()))

        rbs_number = 0
        for rbs in transcription_unit_2_rbs:
            rbs_number = rbs_number + 1
            part_key = "unit2_r" + str(rbs_number)
            modification_dictionary[part_key] = []
            modification_dictionary[part_key].append(rbs)
            sequence = rbs.sequence.elements
            for forbidden_site in forbidden_sites_ecoflex:
                count = (sequence.count(forbidden_site))
                if count == 0:
                    pass
                else:
                    for location in re.finditer(forbidden_site, sequence):
                        site_name = restriction_site_name_library(forbidden_site)
                        modification_dictionary[part_key].append("Restriction site " + forbidden_site + " (" +
                                                                 site_name + ")" + " detected at position " +
                                                                 str(location.start() + 1) + "-" +
                                                                 str(location.end()))

        if GUI.include_signal_combo.get() == "Yes":
            signal_number = 0
            for signal in transcription_unit_2_signal:
                signal_number = signal_number + 1
                part_key = "unit2_s" + str(signal_number)
                modification_dictionary[part_key] = []
                modification_dictionary[part_key].append(signal)
                sequence = signal.sequence.elements
                for forbidden_site in forbidden_sites_ecoflex:
                    count = (sequence.count(forbidden_site))
                    if count == 0:
                        pass
                    else:
                        for location in re.finditer(forbidden_site, sequence):
                            site_name = restriction_site_name_library(forbidden_site)
                            modification_dictionary[part_key].append("Restriction site " + forbidden_site + " (" +
                                                                     site_name + ")" + " detected at position " +
                                                                     str(location.start() + 1) + "-" +
                                                                     str(location.end()))

        terminator_number = 0
        for terminator in transcription_unit_2_terminator:
            terminator_number = terminator_number + 1
            part_key = "unit2_t" + str(terminator_number)
            modification_dictionary[part_key] = []
            modification_dictionary[part_key].append(terminator)
            sequence = terminator.sequence.elements
            for forbidden_site in forbidden_sites_ecoflex:
                count = (sequence.count(forbidden_site))
                if count == 0:
                    pass
                else:
                    for location in re.finditer(forbidden_site, sequence):
                        site_name = restriction_site_name_library(forbidden_site)
                        modification_dictionary[part_key].append("Restriction site " + forbidden_site + " (" +
                                                                 site_name + ")" + " detected at position " +
                                                                 str(location.start() + 1) + "-" +
                                                                 str(location.end()))

    if int(GUI.transcription_unit_quantity_combo.get()) > 2:
        # Transcription unit 3
        promoter_number = 0
        for promoter in transcription_unit_3_promoter:
            promoter_number = promoter_number + 1
            part_key = "unit3_p" + str(promoter_number)
            modification_dictionary[part_key] = []
            modification_dictionary[part_key].append(promoter)
            sequence = promoter.sequence.elements
            for forbidden_site in forbidden_sites_ecoflex:
                count = (sequence.count(forbidden_site))
                if count == 0:
                    pass
                else:
                    for location in re.finditer(forbidden_site, sequence):
                        site_name = restriction_site_name_library(forbidden_site)
                        modification_dictionary[part_key].append("Restriction site " + forbidden_site + " (" +
                                                                 site_name + ")" + " detected at position " +
                                                                 str(location.start() + 1) + "-" +
                                                                 str(location.end()))

        rbs_number = 0
        for rbs in transcription_unit_3_rbs:
            rbs_number = rbs_number + 1
            part_key = "unit3_r" + str(rbs_number)
            modification_dictionary[part_key] = []
            modification_dictionary[part_key].append(rbs)
            sequence = rbs.sequence.elements
            for forbidden_site in forbidden_sites_ecoflex:
                count = (sequence.count(forbidden_site))
                if count == 0:
                    pass
                else:
                    for location in re.finditer(forbidden_site, sequence):
                        site_name = restriction_site_name_library(forbidden_site)
                        modification_dictionary[part_key].append("Restriction site " + forbidden_site + " (" +
                                                                 site_name + ")" + " detected at position " +
                                                                 str(location.start() + 1) + "-" +
                                                                 str(location.end()))

        if GUI.include_signal_combo.get() == "Yes":
            signal_number = 0
            for signal in transcription_unit_3_signal:
                signal_number = signal_number + 1
                part_key = "unit3_s" + str(signal_number)
                modification_dictionary[part_key] = []
                modification_dictionary[part_key].append(signal)
                sequence = signal.sequence.elements
                for forbidden_site in forbidden_sites_ecoflex:
                    count = (sequence.count(forbidden_site))
                    if count == 0:
                        pass
                    else:
                        for location in re.finditer(forbidden_site, sequence):
                            site_name = restriction_site_name_library(forbidden_site)
                            modification_dictionary[part_key].append("Restriction site " + forbidden_site + " (" +
                                                                     site_name + ")" + " detected at position " +
                                                                     str(location.start() + 1) + "-" +
                                                                     str(location.end()))

        terminator_number = 0
        for terminator in transcription_unit_3_terminator:
            terminator_number = terminator_number + 1
            part_key = "unit3_t" + str(terminator_number)
            modification_dictionary[part_key] = []
            modification_dictionary[part_key].append(terminator)
            sequence = terminator.sequence.elements
            for forbidden_site in forbidden_sites_ecoflex:
                count = (sequence.count(forbidden_site))
                if count == 0:
                    pass
                else:
                    for location in re.finditer(forbidden_site, sequence):
                        site_name = restriction_site_name_library(forbidden_site)
                        modification_dictionary[part_key].append("Restriction site " + forbidden_site + " (" +
                                                                 site_name + ")" + " detected at position " +
                                                                 str(location.start() + 1) + "-" +
                                                                 str(location.end()))

    if int(GUI.transcription_unit_quantity_combo.get()) > 3:
        # Transcription unit 4
        promoter_number = 0
        for promoter in transcription_unit_4_promoter:
            promoter_number = promoter_number + 1
            part_key = "unit4_p" + str(promoter_number)
            modification_dictionary[part_key] = []
            modification_dictionary[part_key].append(promoter)
            sequence = promoter.sequence.elements
            for forbidden_site in forbidden_sites_ecoflex:
                count = (sequence.count(forbidden_site))
                if count == 0:
                    pass
                else:
                    for location in re.finditer(forbidden_site, sequence):
                        site_name = restriction_site_name_library(forbidden_site)
                        modification_dictionary[part_key].append("Restriction site " + forbidden_site + " (" +
                                                                 site_name + ")" + " detected at position " +
                                                                 str(location.start() + 1) + "-" +
                                                                 str(location.end()))

        rbs_number = 0
        for rbs in transcription_unit_4_rbs:
            rbs_number = rbs_number + 1
            part_key = "unit4_r" + str(rbs_number)
            modification_dictionary[part_key] = []
            modification_dictionary[part_key].append(rbs)
            sequence = rbs.sequence.elements
            for forbidden_site in forbidden_sites_ecoflex:
                count = (sequence.count(forbidden_site))
                if count == 0:
                    pass
                else:
                    for location in re.finditer(forbidden_site, sequence):
                        site_name = restriction_site_name_library(forbidden_site)
                        modification_dictionary[part_key].append("Restriction site " + forbidden_site + " (" +
                                                                 site_name + ")" + " detected at position " +
                                                                 str(location.start() + 1) + "-" +
                                                                 str(location.end()))

        if GUI.include_signal_combo.get() == "Yes":
            signal_number = 0
            for signal in transcription_unit_4_signal:
                signal_number = signal_number + 1
                part_key = "unit4_s" + str(signal_number)
                modification_dictionary[part_key] = []
                modification_dictionary[part_key].append(signal)
                sequence = signal.sequence.elements
                for forbidden_site in forbidden_sites_ecoflex:
                    count = (sequence.count(forbidden_site))
                    if count == 0:
                        pass
                    else:
                        for location in re.finditer(forbidden_site, sequence):
                            site_name = restriction_site_name_library(forbidden_site)
                            modification_dictionary[part_key].append("Restriction site " + forbidden_site + " (" +
                                                                     site_name + ")" + " detected at position " +
                                                                     str(location.start() + 1) + "-" +
                                                                     str(location.end()))

        terminator_number = 0
        for terminator in transcription_unit_4_terminator:
            terminator_number = terminator_number + 1
            part_key = "unit4_t" + str(terminator_number)
            modification_dictionary[part_key] = []
            modification_dictionary[part_key].append(terminator)
            sequence = terminator.sequence.elements
            for forbidden_site in forbidden_sites_ecoflex:
                count = (sequence.count(forbidden_site))
                if count == 0:
                    pass
                else:
                    for location in re.finditer(forbidden_site, sequence):
                        site_name = restriction_site_name_library(forbidden_site)
                        modification_dictionary[part_key].append("Restriction site " + forbidden_site + " (" +
                                                                 site_name + ")" + " detected at position " +
                                                                 str(location.start() + 1) + "-" +
                                                                 str(location.end()))

    if int(GUI.transcription_unit_quantity_combo.get()) > 4:
        # Transcription unit 5
        promoter_number = 0
        for promoter in transcription_unit_5_promoter:
            promoter_number = promoter_number + 1
            part_key = "unit5_p" + str(promoter_number)
            modification_dictionary[part_key] = []
            modification_dictionary[part_key].append(promoter)
            sequence = promoter.sequence.elements
            for forbidden_site in forbidden_sites_ecoflex:
                count = (sequence.count(forbidden_site))
                if count == 0:
                    pass
                else:
                    for location in re.finditer(forbidden_site, sequence):
                        site_name = restriction_site_name_library(forbidden_site)
                        modification_dictionary[part_key].append("Restriction site " + forbidden_site + " (" +
                                                                 site_name + ")" + " detected at position " +
                                                                 str(location.start() + 1) + "-" +
                                                                 str(location.end()))

        rbs_number = 0
        for rbs in transcription_unit_5_rbs:
            rbs_number = rbs_number + 1
            part_key = "unit5_r" + str(rbs_number)
            modification_dictionary[part_key] = []
            modification_dictionary[part_key].append(rbs)
            sequence = rbs.sequence.elements
            for forbidden_site in forbidden_sites_ecoflex:
                count = (sequence.count(forbidden_site))
                if count == 0:
                    pass
                else:
                    for location in re.finditer(forbidden_site, sequence):
                        site_name = restriction_site_name_library(forbidden_site)
                        modification_dictionary[part_key].append("Restriction site " + forbidden_site + " (" +
                                                                 site_name + ")" + " detected at position " +
                                                                 str(location.start() + 1) + "-" +
                                                                 str(location.end()))

        if GUI.include_signal_combo.get() == "Yes":
            signal_number = 0
            for signal in transcription_unit_5_signal:
                signal_number = signal_number + 1
                part_key = "unit5_s" + str(signal_number)
                modification_dictionary[part_key] = []
                modification_dictionary[part_key].append(signal)
                sequence = signal.sequence.elements
                for forbidden_site in forbidden_sites_ecoflex:
                    count = (sequence.count(forbidden_site))
                    if count == 0:
                        pass
                    else:
                        for location in re.finditer(forbidden_site, sequence):
                            site_name = restriction_site_name_library(forbidden_site)
                            modification_dictionary[part_key].append("Restriction site " + forbidden_site + " (" +
                                                                     site_name + ")" + " detected at position " +
                                                                     str(location.start() + 1) + "-" +
                                                                     str(location.end()))

        terminator_number = 0
        for terminator in transcription_unit_5_terminator:
            terminator_number = terminator_number + 1
            part_key = "unit5_t" + str(terminator_number)
            modification_dictionary[part_key] = []
            modification_dictionary[part_key].append(terminator)
            sequence = terminator.sequence.elements
            for forbidden_site in forbidden_sites_ecoflex:
                count = (sequence.count(forbidden_site))
                if count == 0:
                    pass
                else:
                    for location in re.finditer(forbidden_site, sequence):
                        site_name = restriction_site_name_library(forbidden_site)
                        modification_dictionary[part_key].append("Restriction site " + forbidden_site + " (" +
                                                                 site_name + ")" + " detected at position " +
                                                                 str(location.start() + 1) + "-" +
                                                                 str(location.end()))


# Adding EcoFlex prefix and suffix to parts
def ecoflex_fusion_sites():
    # Transcription unit 1
    if int(GUI.transcription_unit_quantity_combo.get()) > 1:
        counter = 0
        for promoter in transcription_unit_1_promoter:
            counter = counter + 1
            if promoter.sequence.elements.startswith("taggtctcactat"):
                pass
            else:
                promoter.sequence.elements = "taggtctcactat" + promoter.sequence.elements
                modification_dictionary["unit1_p" + str(counter)].append("Prefix added for NdeI overhang (ta)," +
                                                                         " BsaI restriction site (ggtctca)" +
                                                                         " and golden gate promoter fusion site" +
                                                                         " (ctat)")
            if promoter.sequence.elements.endswith("gtacagagacccatg"):
                pass
            else:
                promoter.sequence.elements = promoter.sequence.elements + "gtacagagacccatg"
                modification_dictionary["unit1_p" + str(counter)].append("Suffix added for golden gate promoter" +
                                                                         " fusion site (gtac), BsaI restriction site" +
                                                                         " (agagacc), and SphI overhang (catg)")

        if GUI.include_signal_combo.get() == "No":
            counter = 0
            for rbs in transcription_unit_1_rbs:
                counter = counter + 1
                if rbs.sequence.elements.startswith("taggtctcagtac"):
                    pass
                else:
                    rbs.sequence.elements = "taggtctcagtac" + rbs.sequence.elements
                    modification_dictionary["unit1_r" + str(counter)].append("Prefix added for NdeI overhang (ta)," +
                                                                             " BsaI restriction site (ggtctca)" +
                                                                             " and golden gate RBS fusion site" +
                                                                             " (gtac)")
                if rbs.sequence.elements.endswith("cataagagacccatg"):
                    pass
                else:
                    modification_dictionary["unit1_r" + str(counter)].append("Suffix added for golden gate RBS" +
                                                                             "fusion site (cata), BsaI restriction "
                                                                             "site" +
                                                                             " (agagacc), and SphI overhang (catg)")
        else:
            counter = 0
            for rbs in transcription_unit_1_rbs:
                counter = counter + 1
                if rbs.sequence.elements.startswith("taggtctcagtac"):
                    pass
                else:
                    rbs.sequence.elements = "taggtctcagtac" + rbs.sequence.elements
                    modification_dictionary["unit1_r" + str(counter)].append("Prefix added for NdeI overhang (ta)," +
                                                                             " BsaI restriction site (ggtctca)" +
                                                                             " and golden gate RBS fusion site" +
                                                                             " (gtac)")
                if rbs.sequence.elements.endswith("taaaagagacccatg"):
                    pass
                else:
                    rbs.sequence.elements = rbs.sequence.elements + "taaaagagacccatg"
                    modification_dictionary["unit1_r" + str(counter)].append("Suffix added for golden gate RBS" +
                                                                             "fusion site (taaa), BsaI restriction "
                                                                             "site" +
                                                                             " (agagacc), and SphI overhang (catg)")

            counter = 0
            for signal in transcription_unit_1_signal:
                counter = counter + 1
                if signal.sequence.elements.startswith("taggtctcataaa"):
                    pass
                else:
                    signal.sequence.elements = "taggtctcataaa" + signal.sequence.elements
                    modification_dictionary["unit1_s" + str(counter)].append("Prefix added for NdeI overhang (ta)," +
                                                                             " BsaI restriction site (ggtctca)" +
                                                                             " and golden gate signal peptide fusion" +
                                                                             " site (taaa)")
                if signal.sequence.elements.endswith("cataagagacccatg"):
                    pass
                else:
                    signal.sequence.elements = signal.sequence.elements + "cataagagacccatg"
                    modification_dictionary["unit1_s" + str(counter)].append("Suffix added for golden gate signal" +
                                                                             " peptide fusion site (cata), BsaI" +
                                                                             " restriction site (agagacc), and" +
                                                                             " SphI overhang (catg)")

        counter = 0
        for cds in transcription_unit_1_cds:
            counter = counter + 1
            if cds.sequence.elements.startswith("taatg"):
                pass
            elif cds.sequence.elements.startswith("atg"):
                cds.sequence.elements = "ta" + cds.sequence.elements
                modification_dictionary["unit1_c" + str(counter)].append("Prefix added for NdeI overhang (ta)")
            else:
                modification_dictionary["unit1_c" + str(counter)].append("Start codon (atg) could not be found at" +
                                                                         " start of CDS region, please ensure that" +
                                                                         " this SBOL part contains only the CDS")
            if cds.sequence.elements.endswith("ctag"):
                pass
            else:
                cds.sequence.elements = cds.sequence.elements + "ctag"
                modification_dictionary["unit1_c" + str(counter)].append("Suffix added for BamHI overhang (ctag)")

        counter = 0
        for terminator in transcription_unit_1_terminator:
            counter = counter + 1
            if terminator.sequence.elements.startswith("taggtctcatcga"):
                pass
            else:
                terminator.sequence.elements = "taggtctcatcga" + terminator.sequence.elements
                modification_dictionary["unit1_t" + str(counter)].append("Prefix added for NdeI overhang (ta)," +
                                                                         " BsaI restriction site (ggtctca)" +
                                                                         " and golden gate terminator fusion site" +
                                                                         " (tcga)")
            if terminator.sequence.elements.endswith("tgttagagccccatg"):
                pass
            else:
                terminator.sequence.elements = terminator.sequence.elements + "tgttagagccccatg"
                modification_dictionary["unit1_t" + str(counter)].append("Suffix added for golden gate terminator" +
                                                                         " fusion site (tgtt), BsaI restriction site" +
                                                                         " (agagacc), and SphI overhang (catg)")

        # Transcription unit 2
        counter = 0
        for promoter in transcription_unit_2_promoter:
            counter = counter + 1
            if promoter.sequence.elements.startswith("taggtctcactat"):
                pass
            else:
                promoter.sequence.elements = "taggtctcactat" + promoter.sequence.elements
                modification_dictionary["unit2_p" + str(counter)].append("Prefix added for NdeI overhang (ta)," +
                                                                         " BsaI restriction site (ggtctca)" +
                                                                         " and golden gate promoter fusion site" +
                                                                         " (ctat)")
            if promoter.sequence.elements.endswith("gtacagagacccatg"):
                pass
            else:
                promoter.sequence.elements = promoter.sequence.elements + "gtacagagacccatg"
                modification_dictionary["unit2_p" + str(counter)].append("Suffix added for golden gate promoter" +
                                                                         " fusion site (gtac), BsaI restriction site" +
                                                                         " (agagacc), and SphI overhang (catg)")

        if GUI.include_signal_combo.get() == "No":
            counter = 0
            for rbs in transcription_unit_2_rbs:
                counter = counter + 1
                if rbs.sequence.elements.startswith("taggtctcagtac"):
                    pass
                else:
                    rbs.sequence.elements = "taggtctcagtac" + rbs.sequence.elements
                    modification_dictionary["unit2_r" + str(counter)].append("Prefix added for NdeI overhang (ta)," +
                                                                             " BsaI restriction site (ggtctca)" +
                                                                             " and golden gate RBS fusion site" +
                                                                             " (gtac)")
                if rbs.sequence.elements.endswith("cataagagacccatg"):
                    pass
                else:
                    modification_dictionary["unit2_r" + str(counter)].append("Suffix added for golden gate RBS" +
                                                                             "fusion site (cata), BsaI restriction "
                                                                             "site" +
                                                                             " (agagacc), and SphI overhang (catg)")
        else:
            counter = 0
            for rbs in transcription_unit_2_rbs:
                counter = counter + 1
                if rbs.sequence.elements.startswith("taggtctcagtac"):
                    pass
                else:
                    rbs.sequence.elements = "taggtctcagtac" + rbs.sequence.elements
                    modification_dictionary["unit2_r" + str(counter)].append("Prefix added for NdeI overhang (ta)," +
                                                                             " BsaI restriction site (ggtctca)" +
                                                                             " and golden gate RBS fusion site" +
                                                                             " (gtac)")
                if rbs.sequence.elements.endswith("taaaagagacccatg"):
                    pass
                else:
                    rbs.sequence.elements = rbs.sequence.elements + "taaaagagacccatg"
                    modification_dictionary["unit2_r" + str(counter)].append("Suffix added for golden gate RBS" +
                                                                             "fusion site (taaa), BsaI restriction "
                                                                             "site" +
                                                                             " (agagacc), and SphI overhang (catg)")

            counter = 0
            for signal in transcription_unit_2_signal:
                counter = counter + 1
                if signal.sequence.elements.startswith("taggtctcataaa"):
                    pass
                else:
                    signal.sequence.elements = "taggtctcataaa" + signal.sequence.elements
                    modification_dictionary["unit2_s" + str(counter)].append("Prefix added for NdeI overhang (ta)," +
                                                                             " BsaI restriction site (ggtctca)" +
                                                                             " and golden gate signal peptide fusion" +
                                                                             " site (taaa)")
                if signal.sequence.elements.endswith("cataagagacccatg"):
                    pass
                else:
                    signal.sequence.elements = signal.sequence.elements + "cataagagacccatg"
                    modification_dictionary["unit2_s" + str(counter)].append("Suffix added for golden gate signal" +
                                                                             " peptide fusion site (cata), BsaI" +
                                                                             " restriction site (agagacc), and" +
                                                                             " SphI overhang (catg)")

        counter = 0
        for cds in transcription_unit_2_cds:
            counter = counter + 1
            if cds.sequence.elements.startswith("taatg"):
                pass
            elif cds.sequence.elements.startswith("atg"):
                cds.sequence.elements = "ta" + cds.sequence.elements
                modification_dictionary["unit2_c" + str(counter)].append("Prefix added for NdeI overhang (ta)")
            else:
                modification_dictionary["unit2_c" + str(counter)].append("Start codon (atg) could not be found at" +
                                                                         " start of CDS region, please ensure that" +
                                                                         " this SBOL part contains only the CDS")
            if cds.sequence.elements.endswith("ctag"):
                pass
            else:
                cds.sequence.elements = cds.sequence.elements + "ctag"
                modification_dictionary["unit2_c" + str(counter)].append("Suffix added for BamHI overhang (ctag)")

        counter = 0
        for terminator in transcription_unit_1_terminator:
            counter = counter + 1
            if terminator.sequence.elements.startswith("taggtctcatcga"):
                pass
            else:
                terminator.sequence.elements = "taggtctcatcga" + terminator.sequence.elements
                modification_dictionary["unit2_t" + str(counter)].append("Prefix added for NdeI overhang (ta)," +
                                                                         " BsaI restriction site (ggtctca)" +
                                                                         " and golden gate terminator fusion site" +
                                                                         " (tcga)")
            if terminator.sequence.elements.endswith("tgttagagccccatg"):
                pass
            else:
                terminator.sequence.elements = terminator.sequence.elements + "tgttagagccccatg"
                modification_dictionary["unit2_t" + str(counter)].append("Suffix added for golden gate terminator" +
                                                                         " fusion site (tgtt), BsaI restriction site" +
                                                                         " (agagacc), and SphI overhang (catg)")

    # Transcription unit 3
    if int(GUI.transcription_unit_quantity_combo.get()) > 2:
        counter = 0
        for promoter in transcription_unit_3_promoter:
            counter = counter + 1
            if promoter.sequence.elements.startswith("taggtctcactat"):
                pass
            else:
                promoter.sequence.elements = "taggtctcactat" + promoter.sequence.elements
                modification_dictionary["unit3_p" + str(counter)].append("Prefix added for NdeI overhang (ta)," +
                                                                         " BsaI restriction site (ggtctca)" +
                                                                         " and golden gate promoter fusion site" +
                                                                         " (ctat)")
            if promoter.sequence.elements.endswith("gtacagagacccatg"):
                pass
            else:
                promoter.sequence.elements = promoter.sequence.elements + "gtacagagacccatg"
                modification_dictionary["unit3_p" + str(counter)].append("Suffix added for golden gate promoter" +
                                                                         " fusion site (gtac), BsaI restriction site" +
                                                                         " (agagacc), and SphI overhang (catg)")

        if GUI.include_signal_combo.get() == "No":
            counter = 0
            for rbs in transcription_unit_3_rbs:
                counter = counter + 1
                if rbs.sequence.elements.startswith("taggtctcagtac"):
                    pass
                else:
                    rbs.sequence.elements = "taggtctcagtac" + rbs.sequence.elements
                    modification_dictionary["unit3_r" + str(counter)].append("Prefix added for NdeI overhang (ta)," +
                                                                             " BsaI restriction site (ggtctca)" +
                                                                             " and golden gate RBS fusion site" +
                                                                             " (gtac)")
                if rbs.sequence.elements.endswith("cataagagacccatg"):
                    pass
                else:
                    modification_dictionary["unit3_r" + str(counter)].append("Suffix added for golden gate RBS" +
                                                                             "fusion site (cata), BsaI restriction "
                                                                             "site" +
                                                                             " (agagacc), and SphI overhang (catg)")
        else:
            counter = 0
            for rbs in transcription_unit_3_rbs:
                counter = counter + 1
                if rbs.sequence.elements.startswith("taggtctcagtac"):
                    pass
                else:
                    rbs.sequence.elements = "taggtctcagtac" + rbs.sequence.elements
                    modification_dictionary["unit3_r" + str(counter)].append("Prefix added for NdeI overhang (ta)," +
                                                                             " BsaI restriction site (ggtctca)" +
                                                                             " and golden gate RBS fusion site" +
                                                                             " (gtac)")
                if rbs.sequence.elements.endswith("taaaagagacccatg"):
                    pass
                else:
                    rbs.sequence.elements = rbs.sequence.elements + "taaaagagacccatg"
                    modification_dictionary["unit3_r" + str(counter)].append("Suffix added for golden gate RBS" +
                                                                             "fusion site (taaa), BsaI restriction "
                                                                             "site" +
                                                                             " (agagacc), and SphI overhang (catg)")

            counter = 0
            for signal in transcription_unit_3_signal:
                counter = counter + 1
                if signal.sequence.elements.startswith("taggtctcataaa"):
                    pass
                else:
                    signal.sequence.elements = "taggtctcataaa" + signal.sequence.elements
                    modification_dictionary["unit3_s" + str(counter)].append("Prefix added for NdeI overhang (ta)," +
                                                                             " BsaI restriction site (ggtctca)" +
                                                                             " and golden gate signal peptide fusion" +
                                                                             " site (taaa)")
                if signal.sequence.elements.endswith("cataagagacccatg"):
                    pass
                else:
                    signal.sequence.elements = signal.sequence.elements + "cataagagacccatg"
                    modification_dictionary["unit3_s" + str(counter)].append("Suffix added for golden gate signal" +
                                                                             " peptide fusion site (cata), BsaI" +
                                                                             " restriction site (agagacc), and" +
                                                                             " SphI overhang (catg)")

        counter = 0
        for cds in transcription_unit_3_cds:
            counter = counter + 1
            if cds.sequence.elements.startswith("taatg"):
                pass
            elif cds.sequence.elements.startswith("atg"):
                cds.sequence.elements = "ta" + cds.sequence.elements
                modification_dictionary["unit3_c" + str(counter)].append("Prefix added for NdeI overhang (ta)")
            else:
                modification_dictionary["unit3_c" + str(counter)].append("Start codon (atg) could not be found at" +
                                                                         " start of CDS region, please ensure that" +
                                                                         " this SBOL part contains only the CDS")
            if cds.sequence.elements.endswith("ctag"):
                pass
            else:
                cds.sequence.elements = cds.sequence.elements + "ctag"
                modification_dictionary["unit3_c" + str(counter)].append("Suffix added for BamHI overhang (ctag)")

        counter = 0
        for terminator in transcription_unit_3_terminator:
            counter = counter + 1
            if terminator.sequence.elements.startswith("taggtctcatcga"):
                pass
            else:
                terminator.sequence.elements = "taggtctcatcga" + terminator.sequence.elements
                modification_dictionary["unit3_t" + str(counter)].append("Prefix added for NdeI overhang (ta)," +
                                                                         " BsaI restriction site (ggtctca)" +
                                                                         " and golden gate terminator fusion site" +
                                                                         " (tcga)")
            if terminator.sequence.elements.endswith("tgttagagccccatg"):
                pass
            else:
                terminator.sequence.elements = terminator.sequence.elements + "tgttagagccccatg"
                modification_dictionary["unit3_t" + str(counter)].append("Suffix added for golden gate terminator" +
                                                                         " fusion site (tgtt), BsaI restriction site" +
                                                                         " (agagacc), and SphI overhang (catg)")

    # Transcription unit 4
    if int(GUI.transcription_unit_quantity_combo.get()) > 3:
        counter = 0
        for promoter in transcription_unit_4_promoter:
            counter = counter + 1
            if promoter.sequence.elements.startswith("taggtctcactat"):
                pass
            else:
                promoter.sequence.elements = "taggtctcactat" + promoter.sequence.elements
                modification_dictionary["unit4_p" + str(counter)].append("Prefix added for NdeI overhang (ta)," +
                                                                         " BsaI restriction site (ggtctca)" +
                                                                         " and golden gate promoter fusion site" +
                                                                         " (ctat)")
            if promoter.sequence.elements.endswith("gtacagagacccatg"):
                pass
            else:
                promoter.sequence.elements = promoter.sequence.elements + "gtacagagacccatg"
                modification_dictionary["unit4_p" + str(counter)].append("Suffix added for golden gate promoter" +
                                                                         " fusion site (gtac), BsaI restriction site" +
                                                                         " (agagacc), and SphI overhang (catg)")

        if GUI.include_signal_combo.get() == "No":
            counter = 0
            for rbs in transcription_unit_4_rbs:
                counter = counter + 1
                if rbs.sequence.elements.startswith("taggtctcagtac"):
                    pass
                else:
                    rbs.sequence.elements = "taggtctcagtac" + rbs.sequence.elements
                    modification_dictionary["unit4_r" + str(counter)].append("Prefix added for NdeI overhang (ta)," +
                                                                             " BsaI restriction site (ggtctca)" +
                                                                             " and golden gate RBS fusion site" +
                                                                             " (gtac)")
                if rbs.sequence.elements.endswith("cataagagacccatg"):
                    pass
                else:
                    modification_dictionary["unit4_r" + str(counter)].append("Suffix added for golden gate RBS" +
                                                                             "fusion site (cata), BsaI restriction "
                                                                             "site" +
                                                                             " (agagacc), and SphI overhang (catg)")
        else:
            counter = 0
            for rbs in transcription_unit_4_rbs:
                counter = counter + 1
                if rbs.sequence.elements.startswith("taggtctcagtac"):
                    pass
                else:
                    rbs.sequence.elements = "taggtctcagtac" + rbs.sequence.elements
                    modification_dictionary["unit4_r" + str(counter)].append("Prefix added for NdeI overhang (ta)," +
                                                                             " BsaI restriction site (ggtctca)" +
                                                                             " and golden gate RBS fusion site" +
                                                                             " (gtac)")
                if rbs.sequence.elements.endswith("taaaagagacccatg"):
                    pass
                else:
                    rbs.sequence.elements = rbs.sequence.elements + "taaaagagacccatg"
                    modification_dictionary["unit4_r" + str(counter)].append("Suffix added for golden gate RBS" +
                                                                             "fusion site (taaa), BsaI restriction "
                                                                             "site" +
                                                                             " (agagacc), and SphI overhang (catg)")

            counter = 0
            for signal in transcription_unit_4_signal:
                counter = counter + 1
                if signal.sequence.elements.startswith("taggtctcataaa"):
                    pass
                else:
                    signal.sequence.elements = "taggtctcataaa" + signal.sequence.elements
                    modification_dictionary["unit4_s" + str(counter)].append("Prefix added for NdeI overhang (ta)," +
                                                                             " BsaI restriction site (ggtctca)" +
                                                                             " and golden gate signal peptide fusion" +
                                                                             " site (taaa)")
                if signal.sequence.elements.endswith("cataagagacccatg"):
                    pass
                else:
                    signal.sequence.elements = signal.sequence.elements + "cataagagacccatg"
                    modification_dictionary["unit4_s" + str(counter)].append("Suffix added for golden gate signal" +
                                                                             " peptide fusion site (cata), BsaI" +
                                                                             " restriction site (agagacc), and" +
                                                                             " SphI overhang (catg)")

        counter = 0
        for cds in transcription_unit_4_cds:
            counter = counter + 1
            if cds.sequence.elements.startswith("taatg"):
                pass
            elif cds.sequence.elements.startswith("atg"):
                cds.sequence.elements = "ta" + cds.sequence.elements
                modification_dictionary["unit4_c" + str(counter)].append("Prefix added for NdeI overhang (ta)")
            else:
                modification_dictionary["unit4_c" + str(counter)].append("Start codon (atg) could not be found at" +
                                                                         " start of CDS region, please ensure that" +
                                                                         " this SBOL part contains only the CDS")
            if cds.sequence.elements.endswith("ctag"):
                pass
            else:
                cds.sequence.elements = cds.sequence.elements + "ctag"
                modification_dictionary["unit4_c" + str(counter)].append("Suffix added for BamHI overhang (ctag)")

        counter = 0
        for terminator in transcription_unit_4_terminator:
            counter = counter + 1
            if terminator.sequence.elements.startswith("taggtctcatcga"):
                pass
            else:
                terminator.sequence.elements = "taggtctcatcga" + terminator.sequence.elements
                modification_dictionary["unit4_t" + str(counter)].append("Prefix added for NdeI overhang (ta)," +
                                                                         " BsaI restriction site (ggtctca)" +
                                                                         " and golden gate terminator fusion site" +
                                                                         " (tcga)")
            if terminator.sequence.elements.endswith("tgttagagccccatg"):
                pass
            else:
                terminator.sequence.elements = terminator.sequence.elements + "tgttagagccccatg"
                modification_dictionary["unit4_t" + str(counter)].append("Suffix added for golden gate terminator" +
                                                                         " fusion site (tgtt), BsaI restriction site" +
                                                                         " (agagacc), and SphI overhang (catg)")

    # Transcription unit 5
    if int(GUI.transcription_unit_quantity_combo.get()) > 4:
        counter = 0
        for promoter in transcription_unit_5_promoter:
            counter = counter + 1
            if promoter.sequence.elements.startswith("taggtctcactat"):
                pass
            else:
                promoter.sequence.elements = "taggtctcactat" + promoter.sequence.elements
                modification_dictionary["unit5_p" + str(counter)].append("Prefix added for NdeI overhang (ta)," +
                                                                         " BsaI restriction site (ggtctca)" +
                                                                         " and golden gate promoter fusion site" +
                                                                         " (ctat)")
            if promoter.sequence.elements.endswith("gtacagagacccatg"):
                pass
            else:
                promoter.sequence.elements = promoter.sequence.elements + "gtacagagacccatg"
                modification_dictionary["unit5_p" + str(counter)].append("Suffix added for golden gate promoter" +
                                                                         " fusion site (gtac), BsaI restriction site" +
                                                                         " (agagacc), and SphI overhang (catg)")

        if GUI.include_signal_combo.get() == "No":
            counter = 0
            for rbs in transcription_unit_5_rbs:
                counter = counter + 1
                if rbs.sequence.elements.startswith("taggtctcagtac"):
                    pass
                else:
                    rbs.sequence.elements = "taggtctcagtac" + rbs.sequence.elements
                    modification_dictionary["unit5_r" + str(counter)].append("Prefix added for NdeI overhang (ta)," +
                                                                             " BsaI restriction site (ggtctca)" +
                                                                             " and golden gate RBS fusion site" +
                                                                             " (gtac)")
                if rbs.sequence.elements.endswith("cataagagacccatg"):
                    pass
                else:
                    modification_dictionary["unit5_r" + str(counter)].append("Suffix added for golden gate RBS" +
                                                                             "fusion site (cata), BsaI restriction "
                                                                             "site" +
                                                                             " (agagacc), and SphI overhang (catg)")
        else:
            counter = 0
            for rbs in transcription_unit_5_rbs:
                counter = counter + 1
                if rbs.sequence.elements.startswith("taggtctcagtac"):
                    pass
                else:
                    rbs.sequence.elements = "taggtctcagtac" + rbs.sequence.elements
                    modification_dictionary["unit5_r" + str(counter)].append("Prefix added for NdeI overhang (ta)," +
                                                                             " BsaI restriction site (ggtctca)" +
                                                                             " and golden gate RBS fusion site" +
                                                                             " (gtac)")
                if rbs.sequence.elements.endswith("taaaagagacccatg"):
                    pass
                else:
                    rbs.sequence.elements = rbs.sequence.elements + "taaaagagacccatg"
                    modification_dictionary["unit5_r" + str(counter)].append("Suffix added for golden gate RBS" +
                                                                             "fusion site (taaa), BsaI restriction "
                                                                             "site" +
                                                                             " (agagacc), and SphI overhang (catg)")

            counter = 0
            for signal in transcription_unit_5_signal:
                counter = counter + 1
                if signal.sequence.elements.startswith("taggtctcataaa"):
                    pass
                else:
                    signal.sequence.elements = "taggtctcataaa" + signal.sequence.elements
                    modification_dictionary["unit5_s" + str(counter)].append("Prefix added for NdeI overhang (ta)," +
                                                                             " BsaI restriction site (ggtctca)" +
                                                                             " and golden gate signal peptide fusion" +
                                                                             " site (taaa)")
                if signal.sequence.elements.endswith("cataagagacccatg"):
                    pass
                else:
                    signal.sequence.elements = signal.sequence.elements + "cataagagacccatg"
                    modification_dictionary["unit5_s" + str(counter)].append("Suffix added for golden gate signal" +
                                                                             " peptide fusion site (cata), BsaI" +
                                                                             " restriction site (agagacc), and" +
                                                                             " SphI overhang (catg)")

        counter = 0
        for cds in transcription_unit_5_cds:
            counter = counter + 1
            if cds.sequence.elements.startswith("taatg"):
                pass
            elif cds.sequence.elements.startswith("atg"):
                cds.sequence.elements = "ta" + cds.sequence.elements
                modification_dictionary["unit5_c" + str(counter)].append("Prefix added for NdeI overhang (ta)")
            else:
                modification_dictionary["unit5_c" + str(counter)].append("Start codon (atg) could not be found at" +
                                                                         " start of CDS region, please ensure that" +
                                                                         " this SBOL part contains only the CDS")
            if cds.sequence.elements.endswith("ctag"):
                pass
            else:
                cds.sequence.elements = cds.sequence.elements + "ctag"
                modification_dictionary["unit5_c" + str(counter)].append("Suffix added for BamHI overhang (ctag)")

        counter = 0
        for terminator in transcription_unit_5_terminator:
            counter = counter + 1
            if terminator.sequence.elements.startswith("taggtctcatcga"):
                pass
            else:
                terminator.sequence.elements = "taggtctcatcga" + terminator.sequence.elements
                modification_dictionary["unit5_t" + str(counter)].append("Prefix added for NdeI overhang (ta)," +
                                                                         " BsaI restriction site (ggtctca)" +
                                                                         " and golden gate terminator fusion site" +
                                                                         " (tcga)")
            if terminator.sequence.elements.endswith("tgttagagccccatg"):
                pass
            else:
                terminator.sequence.elements = terminator.sequence.elements + "tgttagagccccatg"
                modification_dictionary["unit5_t" + str(counter)].append("Suffix added for golden gate terminator" +
                                                                         " fusion site (tgtt), BsaI restriction site" +
                                                                         " (agagacc), and SphI overhang (catg)")


def create_transcription_unit_variants():
    if int(GUI.transcription_unit_quantity_combo.get()) > 1:
        # Variants for transcription unit 1
        global transcription_unit_1_variants
        counter = 0
        for promoter in transcription_unit_1_promoter:
            for rbs in transcription_unit_1_rbs:
                if GUI.include_signal_combo.get() == "Yes":
                    for signal in transcription_unit_1_signal:
                        for cds in transcription_unit_1_cds:
                            for terminator in transcription_unit_1_terminator:
                                counter = counter + 1
                                transcription_unit_1_variants["unit1_v" + str(counter)] = []
                                transcription_unit_1_variants["unit1_v" + str(counter)].append(promoter)
                                transcription_unit_1_variants["unit1_v" + str(counter)].append(rbs)
                                transcription_unit_1_variants["unit1_v" + str(counter)].append(signal)
                                transcription_unit_1_variants["unit1_v" + str(counter)].append(cds)
                                transcription_unit_1_variants["unit1_v" + str(counter)].append(terminator)
                else:
                    for cds in transcription_unit_1_cds:
                        for terminator in transcription_unit_1_terminator:
                            counter = counter + 1
                            transcription_unit_1_variants["unit1_v" + str(counter)] = []
                            transcription_unit_1_variants["unit1_v" + str(counter)].append(promoter)
                            transcription_unit_1_variants["unit1_v" + str(counter)].append(rbs)
                            transcription_unit_1_variants["unit1_v" + str(counter)].append(cds)
                            transcription_unit_1_variants["unit1_v" + str(counter)].append(terminator)

        # Variants for transcription unit 2
        global transcription_unit_2_variants
        counter = 0
        for promoter in transcription_unit_2_promoter:
            for rbs in transcription_unit_2_rbs:
                if GUI.include_signal_combo.get() == "Yes":
                    for signal in transcription_unit_2_signal:
                        for cds in transcription_unit_2_cds:
                            for terminator in transcription_unit_2_terminator:
                                counter = counter + 1
                                transcription_unit_2_variants["unit2_v" + str(counter)] = []
                                transcription_unit_2_variants["unit2_v" + str(counter)].append(promoter)
                                transcription_unit_2_variants["unit2_v" + str(counter)].append(rbs)
                                transcription_unit_2_variants["unit2_v" + str(counter)].append(signal)
                                transcription_unit_2_variants["unit2_v" + str(counter)].append(cds)
                                transcription_unit_2_variants["unit2_v" + str(counter)].append(terminator)
                else:
                    for cds in transcription_unit_2_cds:
                        for terminator in transcription_unit_2_terminator:
                            counter = counter + 1
                            transcription_unit_2_variants["unit2_v" + str(counter)] = []
                            transcription_unit_2_variants["unit2_v" + str(counter)].append(promoter)
                            transcription_unit_2_variants["unit2_v" + str(counter)].append(rbs)
                            transcription_unit_2_variants["unit2_v" + str(counter)].append(cds)
                            transcription_unit_2_variants["unit2_v" + str(counter)].append(terminator)

    if int(GUI.transcription_unit_quantity_combo.get()) > 2:
        # Variants for transcription unit 3
        global transcription_unit_3_variants
        counter = 0
        for promoter in transcription_unit_3_promoter:
            for rbs in transcription_unit_3_rbs:
                if GUI.include_signal_combo.get() == "Yes":
                    for signal in transcription_unit_3_signal:
                        for cds in transcription_unit_3_cds:
                            for terminator in transcription_unit_3_terminator:
                                counter = counter + 1
                                transcription_unit_3_variants["unit3_v" + str(counter)] = []
                                transcription_unit_3_variants["unit3_v" + str(counter)].append(promoter)
                                transcription_unit_3_variants["unit3_v" + str(counter)].append(rbs)
                                transcription_unit_3_variants["unit3_v" + str(counter)].append(signal)
                                transcription_unit_3_variants["unit3_v" + str(counter)].append(cds)
                                transcription_unit_3_variants["unit3_v" + str(counter)].append(terminator)
                else:
                    for cds in transcription_unit_3_cds:
                        for terminator in transcription_unit_3_terminator:
                            counter = counter + 1
                            transcription_unit_3_variants["unit3_v" + str(counter)] = []
                            transcription_unit_3_variants["unit3_v" + str(counter)].append(promoter)
                            transcription_unit_3_variants["unit3_v" + str(counter)].append(rbs)
                            transcription_unit_3_variants["unit3_v" + str(counter)].append(cds)
                            transcription_unit_3_variants["unit3_v" + str(counter)].append(terminator)

    if int(GUI.transcription_unit_quantity_combo.get()) > 3:
        # Variants for transcription unit 4
        global transcription_unit_4_variants
        counter = 0
        for promoter in transcription_unit_4_promoter:
            for rbs in transcription_unit_4_rbs:
                if GUI.include_signal_combo.get() == "Yes":
                    for signal in transcription_unit_4_signal:
                        for cds in transcription_unit_4_cds:
                            for terminator in transcription_unit_4_terminator:
                                counter = counter + 1
                                transcription_unit_4_variants["unit4_v" + str(counter)] = []
                                transcription_unit_4_variants["unit4_v" + str(counter)].append(promoter)
                                transcription_unit_4_variants["unit4_v" + str(counter)].append(rbs)
                                transcription_unit_4_variants["unit4_v" + str(counter)].append(signal)
                                transcription_unit_4_variants["unit4_v" + str(counter)].append(cds)
                                transcription_unit_4_variants["unit4_v" + str(counter)].append(terminator)
                else:
                    for cds in transcription_unit_4_cds:
                        for terminator in transcription_unit_4_terminator:
                            counter = counter + 1
                            transcription_unit_4_variants["unit4_v" + str(counter)] = []
                            transcription_unit_4_variants["unit4_v" + str(counter)].append(promoter)
                            transcription_unit_4_variants["unit4_v" + str(counter)].append(rbs)
                            transcription_unit_4_variants["unit4_v" + str(counter)].append(cds)
                            transcription_unit_4_variants["unit4_v" + str(counter)].append(terminator)

    if int(GUI.transcription_unit_quantity_combo.get()) > 4:
        # Variants for transcription unit 5
        global transcription_unit_5_variants
        counter = 0
        for promoter in transcription_unit_5_promoter:
            for rbs in transcription_unit_5_rbs:
                if GUI.include_signal_combo.get() == "Yes":
                    for signal in transcription_unit_5_signal:
                        for cds in transcription_unit_5_cds:
                            for terminator in transcription_unit_5_terminator:
                                counter = counter + 1
                                transcription_unit_5_variants["unit5_v" + str(counter)] = []
                                transcription_unit_5_variants["unit5_v" + str(counter)].append(promoter)
                                transcription_unit_5_variants["unit5_v" + str(counter)].append(rbs)
                                transcription_unit_5_variants["unit5_v" + str(counter)].append(signal)
                                transcription_unit_5_variants["unit5_v" + str(counter)].append(cds)
                                transcription_unit_5_variants["unit5_v" + str(counter)].append(terminator)
                else:
                    for cds in transcription_unit_5_cds:
                        for terminator in transcription_unit_5_terminator:
                            counter = counter + 1
                            transcription_unit_5_variants["unit5_v" + str(counter)] = []
                            transcription_unit_5_variants["unit5_v" + str(counter)].append(promoter)
                            transcription_unit_5_variants["unit5_v" + str(counter)].append(rbs)
                            transcription_unit_5_variants["unit5_v" + str(counter)].append(cds)
                            transcription_unit_5_variants["unit5_v" + str(counter)].append(terminator)


def create_level_2_variants():
    global level_2_variants
    if int(GUI.transcription_unit_quantity_combo.get()) == 2:
        counter = 0
        for unit1 in transcription_unit_1_variants:
            for unit2 in transcription_unit_2_variants:
                counter = counter + 1
                level_2_variants["v" + str(counter)] = (transcription_unit_1_variants[unit1] +
                                                        transcription_unit_2_variants[unit2])

    if int(GUI.transcription_unit_quantity_combo.get()) == 3:
        counter = 0
        for unit1 in transcription_unit_1_variants:
            for unit2 in transcription_unit_2_variants:
                for unit3 in transcription_unit_3_variants:
                    counter = counter + 1
                    level_2_variants["v" + str(counter)] = (transcription_unit_1_variants[unit1] +
                                                            transcription_unit_2_variants[unit2] +
                                                            transcription_unit_3_variants[unit3])

    if int(GUI.transcription_unit_quantity_combo.get()) == 4:
        counter = 0
        for unit1 in transcription_unit_1_variants:
            for unit2 in transcription_unit_2_variants:
                for unit3 in transcription_unit_3_variants:
                    for unit4 in transcription_unit_4_variants:
                        counter = counter + 1
                        level_2_variants["v" + str(counter)] = (transcription_unit_1_variants[unit1] +
                                                                transcription_unit_2_variants[unit2] +
                                                                transcription_unit_3_variants[unit3] +
                                                                transcription_unit_4_variants[unit4])

    if int(GUI.transcription_unit_quantity_combo.get()) == 5:
        counter = 0
        for unit1 in transcription_unit_1_variants:
            for unit2 in transcription_unit_2_variants:
                for unit3 in transcription_unit_3_variants:
                    for unit4 in transcription_unit_4_variants:
                        for unit5 in transcription_unit_5_variants:
                            counter = counter + 1
                            level_2_variants["v" + str(counter)] = (transcription_unit_1_variants[unit1] +
                                                                    transcription_unit_2_variants[unit2] +
                                                                    transcription_unit_3_variants[unit3] +
                                                                    transcription_unit_4_variants[unit4] +
                                                                    transcription_unit_5_variants[unit5])

def final_structure_sequences():
    print("test")









# Directory for protocol creation
def create_protocol_directory(event):
    chassis_choice = GUI.chassis_selection_combo.get()
    if chassis_choice == "E. coli":
        final_ecoflex_check()
        if ecoflex_check_list == []:
            from EcoFlex_protocol import create_protocol
            create_protocol("<Button-1>")
        else:
            GUI.restriction_site_warning_ecoflex()
    if chassis_choice == "B. subtilis":
        print("test")
