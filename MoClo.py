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
level_0_rbs = {}
level_0_cds = {}
level_0_terminator = {}
level_0_signal = {}
level_0_other = {}
level_2_template = []
ecoflex_check_list = []
doc = Document()
forbidden_sites_ecoflex = ["catatg", "gtatac", "ggatcc", "cctagg", "ggtctc", "ccagag", "cgtctc", "gcagag", "ctctgg",
                           "gagacc", "ctctgc", "gagacg", "gcatgc", "cgtacg"]
modification_dictionary = {}
transcription_unit_1_variants = {}
transcription_unit_2_variants = {}
transcription_unit_3_variants = {}
transcription_unit_4_variants = {}
transcription_unit_5_variants = {}


# clear globals function
def clear_globals():
    primary_structure_identities.clear()
    primary_structure_roles.clear()
    primary_structure_descriptions.clear()
    base_composition.clear()
    detected_restriction_sites.clear()


# Import SBOL part(s) from file
def import_design(event):
    global primary_structure_cd
    global primary_structure_cd_string
    global design_uri
    doc2 = Document()
    clear_globals()
    GUI.select_design_import()
    imported_design = GUI.single_imported_design
    doc2.read(imported_design)

    # Detecting whether the imported file contains a design, or a single part
    design_detected = False
    for component in doc2.componentDefinitions:
        try:
            component.getPrimaryStructure()
            design_detected = True
        except LookupError:
            pass

    # If design is not detected, it will next detect whether any sub-components are present for the single part
    if not design_detected:
        sub_components_detected = False
        for component in doc2.componentDefinitions:
            if len(component.components) == 0:
                pass
            else:
                sub_components_detected = True

        # If sub-components are detected, the uri for the top-level part will be isolated
        if sub_components_detected:
            sub_component_quantity = []
            try:
                for component in doc2.componentDefinitions:
                    sub_component_quantity.append(len(component.components))
            except LookupError:
                pass
            for component in doc2.componentDefinitions:
                if len(component.components) == max(sub_component_quantity):
                    part_uri = component
                    part_uri_string = str(part_uri)
                    doc.append(imported_design)
                    import_single_part_to_library(part_uri_string)

        # If no sub components are detected, it will be checked that the imported file contains only a single part
        if not sub_components_detected:
            if len(doc2.componentDefinitions) == 1:
                for component in doc2.componentDefinitions:
                    part_uri = component
                    part_uri_string = str(part_uri)
                    doc.append(imported_design)
                    import_single_part_to_library(part_uri_string)
            else:
                print("ERROR PLACEHOLDER")

    # If a primary structure is detected, the contents of the file will be assumed to encode a genetic design
    elif design_detected:
        # Identifying and isolating the component definition of the design
        primary_structure_count = 0
        for component_definition in doc2.componentDefinitions:
            try:
                component_definition.getPrimaryStructure()
                design_uri = component_definition
                primary_structure_count += 1
            except LookupError:
                pass
        if primary_structure_count > 1:
            print("Multiple primary structures detected error")
        else:
            # Retrieving the component definitions of the parts contained within the design
            primary_structure_cd = design_uri.getPrimaryStructure()
            primary_structure_cd_string = []
            for components in primary_structure_cd:
                primary_structure_identities.append(str(components.displayId))
                primary_structure_cd_string.append(str(components))

            # Retrieving the roles of the parts in the design
            for component in primary_structure_cd:
                if "SO" in str(component.roles):
                    primary_structure_roles.append(str(component.roles))
                else:
                    primary_structure_roles.append("None")

            # Retrieving the descriptions of the parts in the design
            for component in primary_structure_cd:
                primary_structure_descriptions.append(component.description)

            # Create GUI button that allows display of part descriptions
            GUI.create_description_button_moclo()

            # Create analysis button for parts in GUI
            GUI.create_analysis_button_moclo()

            # Initial design analysis for imported design
            design_sequence = design_uri.sequence.elements
            nucleotide_content(design_sequence)
            detect_restriction_sites(design_sequence)

            doc.append(imported_design)
            doc2 = Document
            GUI.refresh_canvas_moclo()
            GUI.display_assembled_design_moclo(primary_structure_roles)
            GUI.refresh_design_parts_to_library()






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

        if "gcatgc" in str(component.sequence.elements):
            detected_restriction_sites.append("SphI restriction site" + " detected in " + str(component.displayId))
        if "cgtacg" in str(component.sequence.elements):
            detected_restriction_sites.append("SphI restriction site" + " detected in " + str(component.displayId))

        if "ggatcc" in str(component.sequence.elements):
            detected_restriction_sites.append("BamHI restriction site" + " detected in " + str(component.displayId))
        if "cctagg" in str(component.sequence.elements):
            detected_restriction_sites.append("BamHI restriction site" + " detected in " + str(component.displayId))

        if "ggtctc" in str(component.sequence.elements):
            detected_restriction_sites.append("BsaI restriction site" + " detected in " + str(component.displayId))
        if "ccagag" in str(component.sequence.elements):
            detected_restriction_sites.append("BsaI restriction site" + " detected in " + str(component.displayId))
        if "ctctgg" in str(component.sequence.elements):
            detected_restriction_sites.append("BsaI restriction site" + "detected in " + str(component.displayId))
        if "gagacc" in str(component.sequence.elements):
            detected_restriction_sites.append("BsaI restriction site" + "detected in " + str(component.displayId))

        if "cgtctc" in str(component.sequence.elements):
            detected_restriction_sites.append("BsmBI restriction site" + " detected in " + str(component.displayId))
        if "gcagag" in str(component.sequence.elements):
            detected_restriction_sites.append("BsmBI restriction site" + " detected in " + str(component.displayId))
        if "ctctgc" in str(component.sequence.elements):
            detected_restriction_sites.append("BsmBI restriction site" + " detected in " + str(component.displayId))
        if "gagacg" in str(component.sequence.elements):
            detected_restriction_sites.append("BsmBI restriction site" + " detected in " + str(component.displayId))


############################ level 0 library #################################
def import_design_parts_to_library(event):
    global primary_structure_cd_string
    for component_cd in primary_structure_cd_string:
        component = doc.getComponentDefinition(component_cd)
        previously_added = False
        if "0000167" in str(component.roles):
            for key in level_0_promoter:
                if str(level_0_promoter[key]) == str(component):
                    previously_added = True
            if not previously_added:
                level_0_promoter["p" + str(len(level_0_promoter) + 1)] = component

        elif "0000139" in str(component.roles):
            for key in level_0_rbs:
                if str(level_0_rbs[key]) == str(component):
                    previously_added = True
            if not previously_added:
                level_0_rbs["r" + str(len(level_0_rbs) + 1)] = component

        elif "0000316" in str(component.roles):
            for key in level_0_cds:
                if str(level_0_cds[key]) == str(component):
                    previously_added = True
            if not previously_added:
                level_0_cds["c" + str(len(level_0_cds) + 1)] = component

        elif "0000141" in str(component.roles):
            for key in level_0_terminator:
                if str(level_0_terminator[key]) == str(component):
                    previously_added = True
            if not previously_added:
                level_0_terminator["t" + str(len(level_0_terminator) + 1)] = component

        elif "0000324" in str(component.roles):
            for key in level_0_signal:
                if str(level_0_signal[key]) == str(component):
                    previously_added = True
            if not previously_added:
                level_0_signal["s" + str(len(level_0_signal) + 1)] = component

        else:
            for key in level_0_other:
                if str(level_0_other[key]) == str(component):
                    previously_added = True
            if not previously_added:
                level_0_other["o" + str(len(level_0_other) + 1)] = component

    GUI.refresh_level_0_library()


# Import a single part into the level 0 library
def import_single_part_to_library(component_definition_string):
    component = doc.getComponentDefinition(component_definition_string)
    previously_added = False
    if "0000167" in str(component.roles):
        for key in level_0_promoter:
            if str(level_0_promoter[key]) == str(component):
                previously_added = True
        if not previously_added:
            level_0_promoter["p" + str(len(level_0_promoter) + 1)] = component

    elif "0000139" in str(component.roles):
        for key in level_0_rbs:
            if str(level_0_rbs[key]) == str(component):
                previously_added = True
        if not previously_added:
            level_0_rbs["r" + str(len(level_0_rbs) + 1)] = component

    elif "0000316" in str(component.roles):
        for key in level_0_cds:
            if str(level_0_cds[key]) == str(component):
                previously_added = True
        if not previously_added:
            level_0_cds["c" + str(len(level_0_cds) + 1)] = component

    elif "0000141" in str(component.roles):
        for key in level_0_terminator:
            if str(level_0_terminator[key]) == str(component):
                previously_added = True
        if not previously_added:
            level_0_terminator["t" + str(len(level_0_terminator) + 1)] = component

    elif "0000324" in str(component.roles):
        for key in level_0_signal:
            if str(level_0_signal[key]) == str(component):
                previously_added = True
        if not previously_added:
            level_0_signal["s" + str(len(level_0_signal) + 1)] = component

    else:
        for key in level_0_other:
            if str(level_0_other[key]) == str(component):
                previously_added = True
        if not previously_added:
            level_0_other["o" + str(len(level_0_other) + 1)] = component
    GUI.refresh_level_0_library()


# Move parts in level 0 library to different part types
def move_parts_in_library(event):
    global level_0_promoter
    global level_0_rbs
    global level_0_signal
    global level_0_cds
    global level_0_terminator
    global level_0_other
    part_key = GUI.part_to_move_entry.get()
    cd_list = []

    if part_key in level_0_promoter:
        component = level_0_promoter.pop(part_key)
        for dict_key in level_0_promoter:
            cd_list.append(level_0_promoter[dict_key])
        level_0_promoter = {}
        for component_definition in cd_list:
            level_0_promoter["p" + str(len(level_0_promoter) + 1)] = component_definition

    if part_key in level_0_rbs:
        component = level_0_rbs.pop(part_key)
        for dict_key in level_0_rbs:
            cd_list.append(level_0_rbs[dict_key])
        level_0_rbs = {}
        for component_definition in cd_list:
            level_0_rbs["r" + str(len(level_0_rbs) + 1)] = component_definition

    if part_key in level_0_signal:
        component = level_0_signal.pop(part_key)
        for dict_key in level_0_signal:
            cd_list.append(level_0_signal[dict_key])
        level_0_signal = {}
        for component_definition in cd_list:
            level_0_signal["s" + str(len(level_0_signal) + 1)] = component_definition

    if part_key in level_0_cds:
        component = level_0_cds.pop(part_key)
        for dict_key in level_0_cds:
            cd_list.append(level_0_cds[dict_key])
        level_0_cds = {}
        for component_definition in cd_list:
            level_0_cds["c" + str(len(level_0_cds) + 1)] = component_definition

    if part_key in level_0_terminator:
        component = level_0_terminator.pop(part_key)
        for dict_key in level_0_terminator:
            cd_list.append(level_0_terminator[dict_key])
        level_0_terminator = {}
        for component_definition in cd_list:
            level_0_terminator["t" + str(len(level_0_terminator) + 1)] = component_definition

    if part_key in level_0_other:
        component = level_0_other.pop(part_key)
        for dict_key in level_0_other:
            cd_list.append(level_0_other[dict_key])
        level_0_other = {}
        for component_definition in cd_list:
            level_0_other["o" + str(len(level_0_other) + 1)] = component_definition

    destination_group = GUI.destination_library_select.get()
    if destination_group == "Promoter (p)":
        new_key = "p" + str(len(level_0_promoter) + 1)
        level_0_promoter[new_key] = component
    if destination_group == "RBS (r)":
        new_key = "r" + str(len(level_0_rbs) + 1)
        level_0_rbs[new_key] = component
    if destination_group == "Signal peptide (s)":
        new_key = "s" + str(len(level_0_signal) + 1)
        level_0_signal[new_key] = component
    if destination_group == "Coding region (c)":
        new_key = "c" + str(len(level_0_cds) + 1)
        level_0_cds[new_key] = component
    if destination_group == "Terminator (t)":
        new_key = "t" + str(len(level_0_terminator) + 1)
        level_0_terminator[new_key] = component
    if destination_group == "Other (o)":
        new_key = "o" + str(len(level_0_other) + 1)
        level_0_other[new_key] = component

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
        transcription_unit_1_rbs_keys = (selected_rbs_1.split(", "))
        global transcription_unit_1_rbs
        transcription_unit_1_rbs = []
        for selection in transcription_unit_1_rbs_keys:
            transcription_unit_1_rbs.append(level_0_rbs[selection])

        if signal_choice == "Yes":
            selected_signal_1 = (GUI.transcription_unit_1_signal_entry.get())
            transcription_unit_1_signal_keys = (selected_signal_1.split(", "))
            global transcription_unit_1_signal
            transcription_unit_1_signal = []
            for selection in transcription_unit_1_signal_keys:
                transcription_unit_1_signal.append(level_0_signal[selection])

        selected_cds_1 = (GUI.transcription_unit_1_cds_entry.get())
        transcription_unit_1_cds_keys = (selected_cds_1.split(", "))
        global transcription_unit_1_cds
        transcription_unit_1_cds = []
        for selection in transcription_unit_1_cds_keys:
            transcription_unit_1_cds.append(level_0_cds[selection])

        selected_terminator_1 = (GUI.transcription_unit_1_terminator_entry.get())
        transcription_unit_1_terminator_keys = (selected_terminator_1.split(", "))
        global transcription_unit_1_terminator
        transcription_unit_1_terminator = []
        for selection in transcription_unit_1_terminator_keys:
            transcription_unit_1_terminator.append(level_0_terminator[selection])

        selected_promoter_2 = (GUI.transcription_unit_2_promoter_entry.get())
        transcription_unit_2_promoter_keys = (selected_promoter_2.split(", "))
        global transcription_unit_2_promoter
        transcription_unit_2_promoter = []
        for selection in transcription_unit_2_promoter_keys:
            transcription_unit_2_promoter.append(level_0_promoter[selection])

        selected_rbs_2 = (GUI.transcription_unit_2_rbs_entry.get())
        transcription_unit_2_rbs_keys = (selected_rbs_2.split(", "))
        global transcription_unit_2_rbs
        transcription_unit_2_rbs = []
        for selection in transcription_unit_2_rbs_keys:
            transcription_unit_2_rbs.append(level_0_rbs[selection])

        if signal_choice == "Yes":
            selected_signal_2 = (GUI.transcription_unit_2_signal_entry.get())
            transcription_unit_2_signal_keys = (selected_signal_2.split(", "))
            global transcription_unit_2_signal
            transcription_unit_2_signal = []
            for selection in transcription_unit_2_signal_keys:
                transcription_unit_2_signal.append(level_0_signal[selection])

        selected_cds_2 = (GUI.transcription_unit_2_cds_entry.get())
        transcription_unit_2_cds_keys = (selected_cds_2.split(", "))
        global transcription_unit_2_cds
        transcription_unit_2_cds = []
        for selection in transcription_unit_2_cds_keys:
            transcription_unit_2_cds.append(level_0_cds[selection])

        selected_terminator_2 = (GUI.transcription_unit_2_terminator_entry.get())
        transcription_unit_2_terminator_keys = (selected_terminator_2.split(", "))
        global transcription_unit_2_terminator
        transcription_unit_2_terminator = []
        for selection in transcription_unit_2_terminator_keys:
            transcription_unit_2_terminator.append(level_0_terminator[selection])

    if transcription_unit_quantity > 2:
        selected_promoter_3 = (GUI.transcription_unit_3_promoter_entry.get())
        transcription_unit_3_promoter_keys = (selected_promoter_3.split(", "))
        global transcription_unit_3_promoter
        transcription_unit_3_promoter = []
        for selection in transcription_unit_3_promoter_keys:
            transcription_unit_3_promoter.append(level_0_promoter[selection])

        selected_rbs_3 = (GUI.transcription_unit_3_rbs_entry.get())
        transcription_unit_3_rbs_keys = (selected_rbs_3.split(", "))
        global transcription_unit_3_rbs
        transcription_unit_3_rbs = []
        for selection in transcription_unit_3_rbs_keys:
            transcription_unit_3_rbs.append(level_0_rbs[selection])

        if signal_choice == "Yes":
            selected_signal_3 = (GUI.transcription_unit_3_signal_entry.get())
            transcription_unit_3_signal_keys = (selected_signal_3.split(", "))
            global transcription_unit_3_signal
            transcription_unit_3_signal = []
            for selection in transcription_unit_3_signal_keys:
                transcription_unit_3_signal.append(level_0_signal[selection])

        selected_cds_3 = (GUI.transcription_unit_3_cds_entry.get())
        transcription_unit_3_cds_keys = (selected_cds_3.split(", "))
        global transcription_unit_3_cds
        transcription_unit_3_cds = []
        for selection in transcription_unit_3_cds_keys:
            transcription_unit_3_cds.append(level_0_cds[selection])

        selected_terminator_3 = (GUI.transcription_unit_3_terminator_entry.get())
        transcription_unit_3_terminator_keys = (selected_terminator_3.split(", "))
        global transcription_unit_3_terminator
        transcription_unit_3_terminator = []
        for selection in transcription_unit_3_terminator_keys:
            transcription_unit_3_terminator.append(level_0_terminator[selection])

    if transcription_unit_quantity > 3:
        selected_promoter_4 = (GUI.transcription_unit_4_promoter_entry.get())
        transcription_unit_4_promoter_keys = (selected_promoter_4.split(", "))
        global transcription_unit_4_promoter
        transcription_unit_4_promoter = []
        for selection in transcription_unit_4_promoter_keys:
            transcription_unit_4_promoter.append(level_0_promoter[selection])

        selected_rbs_4 = (GUI.transcription_unit_4_rbs_entry.get())
        transcription_unit_4_rbs_keys = (selected_rbs_4.split(", "))
        global transcription_unit_4_rbs
        transcription_unit_4_rbs = []
        for selection in transcription_unit_4_rbs_keys:
            transcription_unit_4_rbs.append(level_0_rbs[selection])

        if signal_choice == "Yes":
            selected_signal_4 = (GUI.transcription_unit_4_signal_entry.get())
            transcription_unit_4_signal_keys = (selected_signal_4.split(", "))
            global transcription_unit_4_signal
            transcription_unit_4_signal = []
            for selection in transcription_unit_4_signal_keys:
                transcription_unit_4_signal.append(level_0_signal[selection])

        selected_cds_4 = (GUI.transcription_unit_4_cds_entry.get())
        transcription_unit_4_cds_keys = (selected_cds_4.split(", "))
        global transcription_unit_4_cds
        transcription_unit_4_cds = []
        for selection in transcription_unit_4_cds_keys:
            transcription_unit_4_cds.append(level_0_cds[selection])

        selected_terminator_4 = (GUI.transcription_unit_4_terminator_entry.get())
        transcription_unit_4_terminator_keys = (selected_terminator_4.split(", "))
        global transcription_unit_4_terminator
        transcription_unit_4_terminator = []
        for selection in transcription_unit_4_terminator_keys:
            transcription_unit_4_terminator.append(level_0_terminator[selection])

    if transcription_unit_quantity > 4:
        selected_promoter_5 = (GUI.transcription_unit_5_promoter_entry.get())
        transcription_unit_5_promoter_keys = (selected_promoter_5.split(", "))
        global transcription_unit_5_promoter
        transcription_unit_5_promoter = []
        for selection in transcription_unit_5_promoter_keys:
            transcription_unit_5_promoter.append(level_0_promoter[selection])

        selected_rbs_5 = (GUI.transcription_unit_5_rbs_entry.get())
        transcription_unit_5_rbs_keys = (selected_rbs_5.split(", "))
        global transcription_unit_5_rbs
        transcription_unit_5_rbs = []
        for selection in transcription_unit_5_rbs_keys:
            transcription_unit_5_rbs.append(level_0_rbs[selection])

        if signal_choice == "Yes":
            selected_signal_5 = (GUI.transcription_unit_5_signal_entry.get())
            transcription_unit_5_signal_keys = (selected_signal_5.split(", "))
            global transcription_unit_5_signal
            transcription_unit_5_signal = []
            for selection in transcription_unit_5_signal_keys:
                transcription_unit_5_signal.append(level_0_signal[selection])

        selected_cds_5 = (GUI.transcription_unit_5_cds_entry.get())
        transcription_unit_5_cds_keys = (selected_cds_5.split(", "))
        global transcription_unit_5_cds
        transcription_unit_5_cds = []
        for selection in transcription_unit_5_cds_keys:
            transcription_unit_5_cds.append(level_0_cds[selection])

        selected_terminator_5 = (GUI.transcription_unit_5_terminator_entry.get())
        transcription_unit_5_terminator_keys = (selected_terminator_5.split(", "))
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

    if "gcatgc" in str(component_definition.sequence.elements):
        ecoflex_check_list.append("SphI restriction site" + " detected in " + str(component_definition.displayId)
                                  + " in transcription unit " + str(unit_number))
    if "cgtacg" in str(component_definition.sequence.elements):
        ecoflex_check_list.append("SphI restriction site" + " detected in " + str(component_definition.displayId)
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
    if "ctctgg" in str(component_definition.sequence.elements):
        ecoflex_check_list.append("BsaI restriction site" + " detected in " + str(component_definition.displayId)
                                  + " in transcription unit " + str(unit_number))
    if "gagacc" in str(component_definition.sequence.elements):
        ecoflex_check_list.append("BsaI restriction site" + " detected in " + str(component_definition.displayId)
                                  + " in transcription unit " + str(unit_number))

    if "cgtctc" in str(component_definition.sequence.elements):
        ecoflex_check_list.append("BsmBI restriction site" + " detected in " + str(component_definition.displayId)
                                  + " in transcription unit " + str(unit_number))
    if "gcagag" in str(component_definition.sequence.elements):
        ecoflex_check_list.append("BsmBI restriction site" + " detected in " + str(component_definition.displayId)
                                  + " in transcription unit " + str(unit_number))
    if "ctctgc" in str(component_definition.sequence.elements):
        ecoflex_check_list.append("BsmBI restriction site" + " detected in " + str(component_definition.displayId)
                                  + " in transcription unit " + str(unit_number))
    if "gagacg" in str(component_definition.sequence.elements):
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
    if sequence == "ctctgg":
        return "BsaI"
    if sequence == "gagacc":
        return "BsaI"
    if sequence == "cgtctc":
        return "BsmBI"
    if sequence == "gcagag":
        return "BsmBI"
    if sequence == "ctctgc":
        return "BsmBI"
    if sequence == "gagacg":
        return "BsmBI"
    if sequence == "gcatgc":
        return "SphI"
    if sequence == "cgtacg":
        return "SphI"


# Create codon-swapped variants of CDS parts that contain excluded restriction sites - For EcoFlex
def swap_codons_ecoflex():
    if int(GUI.transcription_unit_quantity_combo.get()) > 1:
        # Transcription unit 1
        cds_number = 0
        for cds in transcription_unit_1_cds:
            print(transcription_unit_1_cds)
            cds_number = cds_number + 1
            part_key = "unit1_c" + str(cds_number)
            global modification_dictionary
            modification_dictionary[part_key] = []
            modification_dictionary[part_key].append(cds)
            sequence = cds.sequence.elements
            if GUI.include_codon_swap_combo.get() == "No":
                for forbidden_site in forbidden_sites_ecoflex:
                    for location in re.finditer(forbidden_site, sequence):
                        site_name = restriction_site_name_library(forbidden_site)
                        modification_dictionary[part_key].append("Restriction site " + forbidden_site + " (" +
                                                                 site_name + ")" + " detected")
            if GUI.include_codon_swap_combo.get() == "Yes":
                detected_sites = True
                while detected_sites:
                    for forbidden_site in forbidden_sites_ecoflex:
                        count = (sequence.count(forbidden_site))
                        if count == 0:
                            if forbidden_site == forbidden_sites_ecoflex[-1]:
                                no_sites_detected = 0
                                for forbidden_site in forbidden_sites_ecoflex:
                                    count_2 = (sequence.count(forbidden_site))
                                    if count_2 == 0:
                                        no_sites_detected = no_sites_detected + 1
                                        if no_sites_detected == int(len(forbidden_sites_ecoflex)):
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
                                    codon_list[int((location / 3) + 1)] = "XXX"
                                    codon_string = (", ".join(codon_list))
                                    sequence = codon_string.replace(", ", "")
                                    modification_dictionary[part_key].append("Restriction site " + forbidden_site +
                                                                             " (" + site_name + ")" + " detected, "
                                                                             " but was unable to be changed due " +
                                                                             "to unavailable codon alternative " +
                                                                             "for " +
                                                                             str(codon) + "." +
                                                                             " This codon has been " +
                                                                             "substituted in the designed sequence "
                                                                             "for 'XXX' ")
                                    count = count - 1
                                    if count == 0:
                                        if forbidden_site == forbidden_sites_ecoflex[-1]:
                                            no_sites_detected = 0
                                            for forbidden_site in forbidden_sites_ecoflex:
                                                count_4 = (sequence.count(forbidden_site))
                                                if count_4 == 0:
                                                    no_sites_detected = no_sites_detected + 1
                                                    if no_sites_detected == len(forbidden_sites_ecoflex):
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
                                                                             str(new_codon)
                                                                             + " to remove " +
                                                                             forbidden_site + " (" + site_name + ")" +
                                                                             " restriction site")
                                    count = count - 1
                                    if count == 0:
                                        if forbidden_site == forbidden_sites_ecoflex[-1]:
                                            no_sites_detected = 0
                                            for forbidden_site in forbidden_sites_ecoflex:
                                                count_3 = (sequence.count(forbidden_site))
                                                if count_3 == 0:
                                                    no_sites_detected = no_sites_detected + 1
                                                    if no_sites_detected == len(forbidden_sites_ecoflex):
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
            if GUI.include_codon_swap_combo.get() == "No":
                for forbidden_site in forbidden_sites_ecoflex:
                    for location in re.finditer(forbidden_site, sequence):
                        site_name = restriction_site_name_library(forbidden_site)
                        modification_dictionary[part_key].append("Restriction site " + forbidden_site + " (" +
                                                                 site_name + ")" + " detected")
            if GUI.include_codon_swap_combo.get() == "Yes":
                detected_sites = True
                while detected_sites:
                    for forbidden_site in forbidden_sites_ecoflex:
                        count = (sequence.count(forbidden_site))
                        if count == 0:
                            if forbidden_site == forbidden_sites_ecoflex[-1]:
                                no_sites_detected = 0
                                for forbidden_site in forbidden_sites_ecoflex:
                                    count_2 = (sequence.count(forbidden_site))
                                    if count_2 == 0:
                                        no_sites_detected = no_sites_detected + 1
                                        if no_sites_detected == len(forbidden_sites_ecoflex):
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
                                    codon_list[int((location / 3) + 1)] = "XXX"
                                    codon_string = (", ".join(codon_list))
                                    sequence = codon_string.replace(", ", "")
                                    modification_dictionary[part_key].append("Restriction site " + forbidden_site +
                                                                             " (" + site_name + ")" + " detected"
                                                                             " but was unable to be changed due " +
                                                                             "to unavailable codon alternative " +
                                                                             "for " +
                                                                             str(codon) + "." +
                                                                             " This codon has been " +
                                                                             "substituted in the designed sequence "
                                                                             "for 'XXX' ")
                                    count = count - 1
                                    if count == 0:
                                        if forbidden_site == forbidden_sites_ecoflex[-1]:
                                            no_sites_detected = 0
                                            for forbidden_site in forbidden_sites_ecoflex:
                                                count_4 = (sequence.count(forbidden_site))
                                                if count_4 == 0:
                                                    no_sites_detected = no_sites_detected + 1
                                                    if no_sites_detected == len(forbidden_sites_ecoflex):
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
                                                                             str(new_codon)
                                                                             + " to remove " +
                                                                             forbidden_site + " (" + site_name + ")" +
                                                                             " restriction site")
                                    count = count - 1
                                    if count == 0:
                                        if forbidden_site == forbidden_sites_ecoflex[-1]:
                                            no_sites_detected = 0
                                            for forbidden_site in forbidden_sites_ecoflex:
                                                count_3 = (sequence.count(forbidden_site))
                                                if count_3 == 0:
                                                    no_sites_detected = no_sites_detected + 1
                                                    if no_sites_detected == len(forbidden_sites_ecoflex):
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
            if GUI.include_codon_swap_combo.get() == "No":
                for forbidden_site in forbidden_sites_ecoflex:
                    for location in re.finditer(forbidden_site, sequence):
                        site_name = restriction_site_name_library(forbidden_site)
                        modification_dictionary[part_key].append("Restriction site " + forbidden_site + " (" +
                                                                 site_name + ")" + " detected")
            if GUI.include_codon_swap_combo.get() == "Yes":
                detected_sites = True
                while detected_sites:
                    for forbidden_site in forbidden_sites_ecoflex:
                        count = (sequence.count(forbidden_site))
                        if count == 0:
                            if forbidden_site == forbidden_sites_ecoflex[-1]:
                                no_sites_detected = 0
                                for forbidden_site in forbidden_sites_ecoflex:
                                    count_2 = (sequence.count(forbidden_site))
                                    if count_2 == 0:
                                        no_sites_detected = no_sites_detected + 1
                                        if no_sites_detected == len(forbidden_sites_ecoflex):
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
                                    codon_list[int((location / 3) + 1)] = "XXX"
                                    codon_string = (", ".join(codon_list))
                                    sequence = codon_string.replace(", ", "")
                                    modification_dictionary[part_key].append("Restriction site " + forbidden_site +
                                                                             " (" + site_name + ")" + " detected,"
                                                                             " but was unable to be changed due " +
                                                                             "to unavailable codon alternative " +
                                                                             "for " +
                                                                             str(codon) + "." +
                                                                             " This codon has been " +
                                                                             "substituted in the designed sequence "
                                                                             "for 'XXX' ")
                                    count = count - 1
                                    if count == 0:
                                        if forbidden_site == forbidden_sites_ecoflex[-1]:
                                            no_sites_detected = 0
                                            for forbidden_site in forbidden_sites_ecoflex:
                                                count_4 = (sequence.count(forbidden_site))
                                                if count_4 == 0:
                                                    no_sites_detected = no_sites_detected + 1
                                                    if no_sites_detected == len(forbidden_sites_ecoflex):
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
                                                                             str(new_codon)
                                                                             + " to remove " +
                                                                             forbidden_site + " (" + site_name + ")" +
                                                                             " restriction site")
                                    count = count - 1
                                    if count == 0:
                                        if forbidden_site == forbidden_sites_ecoflex[-1]:
                                            no_sites_detected = 0
                                            for forbidden_site in forbidden_sites_ecoflex:
                                                count_3 = (sequence.count(forbidden_site))
                                                if count_3 == 0:
                                                    no_sites_detected = no_sites_detected + 1
                                                    if no_sites_detected == len(forbidden_sites_ecoflex):
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
            if GUI.include_codon_swap_combo.get() == "No":
                for forbidden_site in forbidden_sites_ecoflex:
                    for location in re.finditer(forbidden_site, sequence):
                        site_name = restriction_site_name_library(forbidden_site)
                        modification_dictionary[part_key].append("Restriction site " + forbidden_site + " (" +
                                                                 site_name + ")" + " detected")
            if GUI.include_codon_swap_combo.get() == "Yes":
                detected_sites = True
                while detected_sites:
                    for forbidden_site in forbidden_sites_ecoflex:
                        count = (sequence.count(forbidden_site))
                        if count == 0:
                            if forbidden_site == forbidden_sites_ecoflex[-1]:
                                no_sites_detected = 0
                                for forbidden_site in forbidden_sites_ecoflex:
                                    count_2 = (sequence.count(forbidden_site))
                                    if count_2 == 0:
                                        no_sites_detected = no_sites_detected + 1
                                        if no_sites_detected == len(forbidden_sites_ecoflex):
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
                                    codon_list[int((location / 3) + 1)] = "XXX"
                                    codon_string = (", ".join(codon_list))
                                    sequence = codon_string.replace(", ", "")
                                    modification_dictionary[part_key].append("Restriction site " + forbidden_site +
                                                                             " (" + site_name + ")" + " detected,"
                                                                             " but was unable to be changed due " +
                                                                             "to unavailable codon alternative " +
                                                                             "for " +
                                                                             str(codon) + "." +
                                                                             " This codon has been " +
                                                                             "substituted in the designed sequence "
                                                                             "for 'XXX' ")
                                    count = count - 1
                                    if count == 0:
                                        if forbidden_site == forbidden_sites_ecoflex[-1]:
                                            no_sites_detected = 0
                                            for forbidden_site in forbidden_sites_ecoflex:
                                                count_4 = (sequence.count(forbidden_site))
                                                if count_4 == 0:
                                                    no_sites_detected = no_sites_detected + 1
                                                    if no_sites_detected == len(forbidden_sites_ecoflex):
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
                                                                             str(new_codon)
                                                                             + " to remove " +
                                                                             forbidden_site + " (" + site_name + ")" +
                                                                             " restriction site")
                                    count = count - 1
                                    if count == 0:
                                        if forbidden_site == forbidden_sites_ecoflex[-1]:
                                            no_sites_detected = 0
                                            for forbidden_site in forbidden_sites_ecoflex:
                                                count_3 = (sequence.count(forbidden_site))
                                                if count_3 == 0:
                                                    no_sites_detected = no_sites_detected + 1
                                                    if no_sites_detected == len(forbidden_sites_ecoflex):
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
            if GUI.include_codon_swap_combo.get() == "No":
                for forbidden_site in forbidden_sites_ecoflex:
                    for location in re.finditer(forbidden_site, sequence):
                        site_name = restriction_site_name_library(forbidden_site)
                        modification_dictionary[part_key].append("Restriction site " + forbidden_site + " (" +
                                                                 site_name + ")" + " detected")
            if GUI.include_codon_swap_combo.get() == "Yes":
                detected_sites = True
                while detected_sites:
                    for forbidden_site in forbidden_sites_ecoflex:
                        count = (sequence.count(forbidden_site))
                        if count == 0:
                            if forbidden_site == forbidden_sites_ecoflex[-1]:
                                no_sites_detected = 0
                                for forbidden_site in forbidden_sites_ecoflex:
                                    count_2 = (sequence.count(forbidden_site))
                                    if count_2 == 0:
                                        no_sites_detected = no_sites_detected + 1
                                        if no_sites_detected == len(forbidden_sites_ecoflex):
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
                                    codon_list[int((location / 3) + 1)] = "XXX"
                                    codon_string = (", ".join(codon_list))
                                    sequence = codon_string.replace(", ", "")
                                    modification_dictionary[part_key].append("Restriction site " + forbidden_site +
                                                                             " (" + site_name + ")" + " detected,"
                                                                             " but was unable to be changed due " +
                                                                             "to unavailable codon alternative " +
                                                                             "for " +
                                                                             str(codon) + "." +
                                                                             " This codon has been " +
                                                                             "substituted in the designed sequence "
                                                                             "for 'XXX' ")
                                    count = count - 1
                                    if count == 0:
                                        if forbidden_site == forbidden_sites_ecoflex[-1]:
                                            no_sites_detected = 0
                                            for forbidden_site in forbidden_sites_ecoflex:
                                                count_4 = (sequence.count(forbidden_site))
                                                if count_4 == 0:
                                                    no_sites_detected = no_sites_detected + 1
                                                    if no_sites_detected == len(forbidden_sites_ecoflex):
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
                                                                             str(new_codon)
                                                                             + " to remove " +
                                                                             forbidden_site + " (" + site_name + ")" +
                                                                             " restriction site")
                                    count = count - 1
                                    if count == 0:
                                        if forbidden_site == forbidden_sites_ecoflex[-1]:
                                            no_sites_detected = 0
                                            for forbidden_site in forbidden_sites_ecoflex:
                                                count_3 = (sequence.count(forbidden_site))
                                                if count_3 == 0:
                                                    no_sites_detected = no_sites_detected + 1
                                                    if no_sites_detected == len(forbidden_sites_ecoflex):
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
            sequence = promoter.sequence.elements
            for forbidden_site in forbidden_sites_ecoflex:
                site_name = restriction_site_name_library(forbidden_site)
                count = (sequence.count(forbidden_site))
                if ("ctat" + promoter.sequence.elements[:5]).find(forbidden_site) >= 0:
                    modification_dictionary[part_key].append("Restriction site " + forbidden_site + " (" +
                                                             site_name + ")" + "has been created at the 5' end of "
                                                                               "this part as a result of the addition "
                                                                               "of the "
                                                                               "promoter prefix fusion "
                                                                               "site 'ctat'")
                if (promoter.sequence.elements[-5:] + "gtac").find(forbidden_site) >= 0:
                    modification_dictionary[part_key].append("Restriction site " + forbidden_site + " (" +
                                                             site_name + ")" + "has been created at the 3' end of "
                                                                               "this part as a result of the addition "
                                                                               "of the "
                                                                               "promoter suffix fusion "
                                                                               "site 'gtac'")
                if count > 0:
                    for location in re.finditer(forbidden_site, sequence):
                        modification_dictionary[part_key].append("Restriction site " + forbidden_site + " (" +
                                                                 site_name + ")" + " detected")

        rbs_number = 0
        for rbs in transcription_unit_1_rbs:
            rbs_number = rbs_number + 1
            part_key = "unit1_r" + str(rbs_number)
            modification_dictionary[part_key] = []
            modification_dictionary[part_key].append(rbs)
            sequence = rbs.sequence.elements
            for forbidden_site in forbidden_sites_ecoflex:
                count = (sequence.count(forbidden_site))
                site_name = restriction_site_name_library(forbidden_site)
                if ("gtac" + rbs.sequence.elements[:5]).find(forbidden_site) >= 0:
                    modification_dictionary[part_key].append("Restriction site " + forbidden_site + " (" +
                                                             site_name + ")" + "has been created at the 5' end of "
                                                                               "this part as a result of the addition "
                                                                               "of the "
                                                                               "rbs prefix fusion "
                                                                               "site 'gtac'")

                if GUI.include_signal_combo.get() == "Yes":
                    if (rbs.sequence.elements[-5:] + "taaa").find(forbidden_site) >= 0:
                        modification_dictionary[part_key].append("Restriction site " + forbidden_site + " (" +
                                                                 site_name + ")" + "has been created at the 3' end of "
                                                                                   "this part as a result of the "
                                                                                   "addition "
                                                                                   "of the "
                                                                                   "rbs suffix fusion "
                                                                                   "site 'taaa'")
                if GUI.include_signal_combo.get() == "No":
                    if (rbs.sequence.elements[-5:] + "cata").find(forbidden_site) >= 0:
                        modification_dictionary[part_key].append("Restriction site " + forbidden_site + " (" +
                                                                 site_name + ")" + "has been created at the 3' end of "
                                                                                   "this part as a result of the "
                                                                                   "addition "
                                                                                   "of the "
                                                                                   "rbs suffix fusion "
                                                                                   "site 'cata'")
                if count > 0:
                    for location in re.finditer(forbidden_site, sequence):
                        modification_dictionary[part_key].append("Restriction site " + forbidden_site + " (" +
                                                                 site_name + ")" + " detected")

        if GUI.include_signal_combo.get() == "Yes":
            signal_number = 0
            for signal in transcription_unit_1_signal:
                signal_number = signal_number + 1
                part_key = "unit1_s" + str(signal_number)
                modification_dictionary[part_key] = []
                modification_dictionary[part_key].append(signal)
                sequence = signal.sequence.elements
                for forbidden_site in forbidden_sites_ecoflex:
                    site_name = restriction_site_name_library(forbidden_site)
                    count = (sequence.count(forbidden_site))
                    if ("taaa" + signal.sequence.elements[:5]).find(forbidden_site) >= 0:
                        modification_dictionary[part_key].append("Restriction site " + forbidden_site + " (" +
                                                                 site_name + ")" + "has been created at the 5' end of "
                                                                                   "this part as a result of the "
                                                                                   "addition "
                                                                                   "of the "
                                                                                   "signal peptide prefix fusion "
                                                                                   "site 'taaa'")

                    if (signal.sequence.elements[-5:] + "cata").find(forbidden_site) >= 0:
                        modification_dictionary[part_key].append("Restriction site " + forbidden_site + " (" +
                                                                 site_name + ")" + "has been created at the 3' end of "
                                                                                   "this part as a result of the "
                                                                                   "addition "
                                                                                   "of the "
                                                                                   "signal peptide suffix fusion "
                                                                                   "site 'cata'")
                    if count > 0:
                        for location in re.finditer(forbidden_site, sequence):
                            modification_dictionary[part_key].append("Restriction site " + forbidden_site + " (" +
                                                                     site_name + ")" + " detected")

        terminator_number = 0
        for terminator in transcription_unit_1_terminator:
            terminator_number = terminator_number + 1
            part_key = "unit1_t" + str(terminator_number)
            modification_dictionary[part_key] = []
            modification_dictionary[part_key].append(terminator)
            sequence = terminator.sequence.elements
            for forbidden_site in forbidden_sites_ecoflex:
                site_name = restriction_site_name_library(forbidden_site)
                count = (sequence.count(forbidden_site))
                if ("tcga" + terminator.sequence.elements[:5]).find(forbidden_site) >= 0:
                    modification_dictionary[part_key].append("Restriction site " + forbidden_site + " (" +
                                                             site_name + ")" + "has been created at the 5' end of "
                                                                               "this part as a result of the "
                                                                               "addition "
                                                                               "of the "
                                                                               "terminator prefix fusion "
                                                                               "site 'tcga'")

                if (terminator.sequence.elements[-5:] + "tgtt").find(forbidden_site) >= 0:
                    modification_dictionary[part_key].append("Restriction site " + forbidden_site + " (" +
                                                             site_name + ")" + "has been created at the 3' end of "
                                                                               "this part as a result of the "
                                                                               "addition "
                                                                               "of the "
                                                                               "terminator suffix fusion "
                                                                               "site 'tgtt'")
                if count > 0:
                    for location in re.finditer(forbidden_site, sequence):
                        modification_dictionary[part_key].append("Restriction site " + forbidden_site + " (" +
                                                                 site_name + ")" + " detected")

        # Transcription unit 2
        promoter_number = 0
        for promoter in transcription_unit_2_promoter:
            promoter_number = promoter_number + 1
            part_key = "unit2_p" + str(promoter_number)
            modification_dictionary[part_key] = []
            modification_dictionary[part_key].append(promoter)
            sequence = promoter.sequence.elements
            for forbidden_site in forbidden_sites_ecoflex:
                site_name = restriction_site_name_library(forbidden_site)
                count = (sequence.count(forbidden_site))
                if ("ctat" + promoter.sequence.elements[:5]).find(forbidden_site) >= 0:
                    modification_dictionary[part_key].append("Restriction site " + forbidden_site + " (" +
                                                             site_name + ")" + "has been created at the 5' end of "
                                                                               "this part as a result of the addition "
                                                                               "of the "
                                                                               "promoter prefix fusion "
                                                                               "site 'ctat'")
                if (promoter.sequence.elements[-5:] + "gtac").find(forbidden_site) >= 0:
                    modification_dictionary[part_key].append("Restriction site " + forbidden_site + " (" +
                                                             site_name + ")" + "has been created at the 3' end of "
                                                                               "this part as a result of the addition "
                                                                               "of the "
                                                                               "promoter suffix fusion "
                                                                               "site 'gtac'")
                if count > 0:
                    for location in re.finditer(forbidden_site, sequence):
                        modification_dictionary[part_key].append("Restriction site " + forbidden_site + " (" +
                                                                 site_name + ")" + " detected")

        rbs_number = 0
        for rbs in transcription_unit_2_rbs:
            rbs_number = rbs_number + 1
            part_key = "unit2_r" + str(rbs_number)
            modification_dictionary[part_key] = []
            modification_dictionary[part_key].append(rbs)
            sequence = rbs.sequence.elements
            for forbidden_site in forbidden_sites_ecoflex:
                site_name = restriction_site_name_library(forbidden_site)
                count = (sequence.count(forbidden_site))
                if ("gtac" + rbs.sequence.elements[:5]).find(forbidden_site) >= 0:
                    modification_dictionary[part_key].append("Restriction site " + forbidden_site + " (" +
                                                             site_name + ")" + "has been created at the 5' end of "
                                                                               "this part as a result of the addition "
                                                                               "of the "
                                                                               "rbs prefix fusion "
                                                                               "site 'gtac'")

                if GUI.include_signal_combo.get() == "Yes":
                    if (rbs.sequence.elements[-5:] + "taaa").find(forbidden_site) >= 0:
                        modification_dictionary[part_key].append("Restriction site " + forbidden_site + " (" +
                                                                 site_name + ")" + "has been created at the 3' end of "
                                                                                   "this part as a result of the "
                                                                                   "addition "
                                                                                   "of the "
                                                                                   "rbs suffix fusion "
                                                                                   "site 'taaa'")
                if GUI.include_signal_combo.get() == "No":
                    if (rbs.sequence.elements[-5:] + "cata").find(forbidden_site) >= 0:
                        modification_dictionary[part_key].append("Restriction site " + forbidden_site + " (" +
                                                                 site_name + ")" + "has been created at the 3' end of "
                                                                                   "this part as a result of the "
                                                                                   "addition "
                                                                                   "of the "
                                                                                   "rbs suffix fusion "
                                                                                   "site 'cata'")
                if count > 0:
                    for location in re.finditer(forbidden_site, sequence):
                        modification_dictionary[part_key].append("Restriction site " + forbidden_site + " (" +
                                                                 site_name + ")" + " detected")

        if GUI.include_signal_combo.get() == "Yes":
            signal_number = 0
            for signal in transcription_unit_2_signal:
                signal_number = signal_number + 1
                part_key = "unit2_s" + str(signal_number)
                modification_dictionary[part_key] = []
                modification_dictionary[part_key].append(signal)
                sequence = signal.sequence.elements
                for forbidden_site in forbidden_sites_ecoflex:
                    site_name = restriction_site_name_library(forbidden_site)
                    count = (sequence.count(forbidden_site))
                    if ("taaa" + signal.sequence.elements[:5]).find(forbidden_site) >= 0:
                        modification_dictionary[part_key].append("Restriction site " + forbidden_site + " (" +
                                                                 site_name + ")" + "has been created at the 5' end of "
                                                                                   "this part as a result of the "
                                                                                   "addition "
                                                                                   "of the "
                                                                                   "signal peptide prefix fusion "
                                                                                   "site 'taaa'")

                    if (signal.sequence.elements[-5:] + "cata").find(forbidden_site) >= 0:
                        modification_dictionary[part_key].append("Restriction site " + forbidden_site + " (" +
                                                                 site_name + ")" + "has been created at the 3' end of "
                                                                                   "this part as a result of the "
                                                                                   "addition "
                                                                                   "of the "
                                                                                   "signal peptide suffix fusion "
                                                                                   "site 'cata'")
                    if count > 0:
                        for location in re.finditer(forbidden_site, sequence):
                            modification_dictionary[part_key].append("Restriction site " + forbidden_site + " (" +
                                                                     site_name + ")" + " detected")

        terminator_number = 0
        for terminator in transcription_unit_2_terminator:
            terminator_number = terminator_number + 1
            part_key = "unit2_t" + str(terminator_number)
            modification_dictionary[part_key] = []
            modification_dictionary[part_key].append(terminator)
            sequence = terminator.sequence.elements
            for forbidden_site in forbidden_sites_ecoflex:
                site_name = restriction_site_name_library(forbidden_site)
                count = (sequence.count(forbidden_site))
                if ("tcga" + terminator.sequence.elements[:5]).find(forbidden_site) >= 0:
                    modification_dictionary[part_key].append("Restriction site " + forbidden_site + " (" +
                                                             site_name + ")" + "has been created at the 5' end of "
                                                                               "this part as a result of the "
                                                                               "addition "
                                                                               "of the "
                                                                               "terminator prefix fusion "
                                                                               "site 'tcga'")

                if (terminator.sequence.elements[-5:] + "tgtt").find(forbidden_site) >= 0:
                    modification_dictionary[part_key].append("Restriction site " + forbidden_site + " (" +
                                                             site_name + ")" + "has been created at the 3' end of "
                                                                               "this part as a result of the "
                                                                               "addition "
                                                                               "of the "
                                                                               "terminator suffix fusion "
                                                                               "site 'tgtt'")
                if count > 0:
                    for location in re.finditer(forbidden_site, sequence):
                        modification_dictionary[part_key].append("Restriction site " + forbidden_site + " (" +
                                                                 site_name + ")" + " detected")

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
                site_name = restriction_site_name_library(forbidden_site)
                count = (sequence.count(forbidden_site))
                if ("ctat" + promoter.sequence.elements[:5]).find(forbidden_site) >= 0:
                    modification_dictionary[part_key].append("Restriction site " + forbidden_site + " (" +
                                                             site_name + ")" + "has been created at the 5' end of "
                                                                               "this part as a result of the addition "
                                                                               "of the "
                                                                               "promoter prefix fusion "
                                                                               "site 'ctat'")
                if (promoter.sequence.elements[-5:] + "gtac").find(forbidden_site) >= 0:
                    modification_dictionary[part_key].append("Restriction site " + forbidden_site + " (" +
                                                             site_name + ")" + "has been created at the 3' end of "
                                                                               "this part as a result of the addition "
                                                                               "of the "
                                                                               "promoter suffix fusion "
                                                                               "site 'gtac'")
                if count > 0:
                    for location in re.finditer(forbidden_site, sequence):
                        modification_dictionary[part_key].append("Restriction site " + forbidden_site + " (" +
                                                                 site_name + ")" + " detected")

        rbs_number = 0
        for rbs in transcription_unit_3_rbs:
            rbs_number = rbs_number + 1
            part_key = "unit3_r" + str(rbs_number)
            modification_dictionary[part_key] = []
            modification_dictionary[part_key].append(rbs)
            sequence = rbs.sequence.elements
            for forbidden_site in forbidden_sites_ecoflex:
                site_name = restriction_site_name_library(forbidden_site)
                count = (sequence.count(forbidden_site))
                if ("gtac" + rbs.sequence.elements[:5]).find(forbidden_site) >= 0:
                    modification_dictionary[part_key].append("Restriction site " + forbidden_site + " (" +
                                                             site_name + ")" + "has been created at the 5' end of "
                                                                               "this part as a result of the addition "
                                                                               "of the "
                                                                               "rbs prefix fusion "
                                                                               "site 'gtac'")

                if GUI.include_signal_combo.get() == "Yes":
                    if (rbs.sequence.elements[-5:] + "taaa").find(forbidden_site) >= 0:
                        modification_dictionary[part_key].append("Restriction site " + forbidden_site + " (" +
                                                                 site_name + ")" + "has been created at the 3' end of "
                                                                                   "this part as a result of the "
                                                                                   "addition "
                                                                                   "of the "
                                                                                   "rbs suffix fusion "
                                                                                   "site 'taaa'")
                if GUI.include_signal_combo.get() == "No":
                    if (rbs.sequence.elements[-5:] + "cata").find(forbidden_site) >= 0:
                        modification_dictionary[part_key].append("Restriction site " + forbidden_site + " (" +
                                                                 site_name + ")" + "has been created at the 3' end of "
                                                                                   "this part as a result of the "
                                                                                   "addition "
                                                                                   "of the "
                                                                                   "rbs suffix fusion "
                                                                                   "site 'cata'")
                if count > 0:
                    for location in re.finditer(forbidden_site, sequence):
                        modification_dictionary[part_key].append("Restriction site " + forbidden_site + " (" +
                                                                 site_name + ")" + " detected")
        if GUI.include_signal_combo.get() == "Yes":
            signal_number = 0
            for signal in transcription_unit_3_signal:
                signal_number = signal_number + 1
                part_key = "unit3_s" + str(signal_number)
                modification_dictionary[part_key] = []
                modification_dictionary[part_key].append(signal)
                sequence = signal.sequence.elements
                for forbidden_site in forbidden_sites_ecoflex:
                    site_name = restriction_site_name_library(forbidden_site)
                    count = (sequence.count(forbidden_site))
                    if ("taaa" + signal.sequence.elements[:5]).find(forbidden_site) >= 0:
                        modification_dictionary[part_key].append("Restriction site " + forbidden_site + " (" +
                                                                 site_name + ")" + "has been created at the 5' end of "
                                                                                   "this part as a result of the "
                                                                                   "addition "
                                                                                   "of the "
                                                                                   "signal peptide prefix fusion "
                                                                                   "site 'taaa'")

                    if (signal.sequence.elements[-5:] + "cata").find(forbidden_site) >= 0:
                        modification_dictionary[part_key].append("Restriction site " + forbidden_site + " (" +
                                                                 site_name + ")" + "has been created at the 3' end of "
                                                                                   "this part as a result of the "
                                                                                   "addition "
                                                                                   "of the "
                                                                                   "signal peptide suffix fusion "
                                                                                   "site 'cata'")
                    if count > 0:
                        for location in re.finditer(forbidden_site, sequence):
                            modification_dictionary[part_key].append("Restriction site " + forbidden_site + " (" +
                                                                     site_name + ")" + " detected")
        terminator_number = 0
        for terminator in transcription_unit_3_terminator:
            terminator_number = terminator_number + 1
            part_key = "unit3_t" + str(terminator_number)
            modification_dictionary[part_key] = []
            modification_dictionary[part_key].append(terminator)
            sequence = terminator.sequence.elements
            for forbidden_site in forbidden_sites_ecoflex:
                site_name = restriction_site_name_library(forbidden_site)
                count = (sequence.count(forbidden_site))
                if ("tcga" + terminator.sequence.elements[:5]).find(forbidden_site) >= 0:
                    modification_dictionary[part_key].append("Restriction site " + forbidden_site + " (" +
                                                             site_name + ")" + "has been created at the 5' end of "
                                                                               "this part as a result of the "
                                                                               "addition "
                                                                               "of the "
                                                                               "terminator prefix fusion "
                                                                               "site 'tcga'")

                if (terminator.sequence.elements[-5:] + "tgtt").find(forbidden_site) >= 0:
                    modification_dictionary[part_key].append("Restriction site " + forbidden_site + " (" +
                                                             site_name + ")" + "has been created at the 3' end of "
                                                                               "this part as a result of the "
                                                                               "addition "
                                                                               "of the "
                                                                               "terminator suffix fusion "
                                                                               "site 'tgtt'")
                if count > 0:
                    for location in re.finditer(forbidden_site, sequence):
                        modification_dictionary[part_key].append("Restriction site " + forbidden_site + " (" +
                                                                 site_name + ")" + " detected")

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
                site_name = restriction_site_name_library(forbidden_site)
                count = (sequence.count(forbidden_site))
                if ("ctat" + promoter.sequence.elements[:5]).find(forbidden_site) >= 0:
                    modification_dictionary[part_key].append("Restriction site " + forbidden_site + " (" +
                                                             site_name + ")" + "has been created at the 5' end of "
                                                                               "this part as a result of the addition "
                                                                               "of the "
                                                                               "promoter prefix fusion "
                                                                               "site 'ctat'")
                if (promoter.sequence.elements[-5:] + "gtac").find(forbidden_site) >= 0:
                    modification_dictionary[part_key].append("Restriction site " + forbidden_site + " (" +
                                                             site_name + ")" + "has been created at the 3' end of "
                                                                               "this part as a result of the addition "
                                                                               "of the "
                                                                               "promoter suffix fusion "
                                                                               "site 'gtac'")
                if count > 0:
                    for location in re.finditer(forbidden_site, sequence):
                        modification_dictionary[part_key].append("Restriction site " + forbidden_site + " (" +
                                                                 site_name + ")" + " detected")

        rbs_number = 0
        for rbs in transcription_unit_4_rbs:
            rbs_number = rbs_number + 1
            part_key = "unit4_r" + str(rbs_number)
            modification_dictionary[part_key] = []
            modification_dictionary[part_key].append(rbs)
            sequence = rbs.sequence.elements
            for forbidden_site in forbidden_sites_ecoflex:
                site_name = restriction_site_name_library(forbidden_site)
                count = (sequence.count(forbidden_site))
                if ("gtac" + rbs.sequence.elements[:5]).find(forbidden_site) >= 0:
                    modification_dictionary[part_key].append("Restriction site " + forbidden_site + " (" +
                                                             site_name + ")" + "has been created at the 5' end of "
                                                                               "this part as a result of the addition "
                                                                               "of the "
                                                                               "rbs prefix fusion "
                                                                               "site 'gtac'")

                if GUI.include_signal_combo.get() == "Yes":
                    if (rbs.sequence.elements[-5:] + "taaa").find(forbidden_site) >= 0:
                        modification_dictionary[part_key].append("Restriction site " + forbidden_site + " (" +
                                                                 site_name + ")" + "has been created at the 3' end of "
                                                                                   "this part as a result of the "
                                                                                   "addition "
                                                                                   "of the "
                                                                                   "rbs suffix fusion "
                                                                                   "site 'taaa'")
                if GUI.include_signal_combo.get() == "No":
                    if (rbs.sequence.elements[-5:] + "cata").find(forbidden_site) >= 0:
                        modification_dictionary[part_key].append("Restriction site " + forbidden_site + " (" +
                                                                 site_name + ")" + "has been created at the 3' end of "
                                                                                   "this part as a result of the "
                                                                                   "addition "
                                                                                   "of the "
                                                                                   "rbs suffix fusion "
                                                                                   "site 'cata'")
                if count > 0:
                    for location in re.finditer(forbidden_site, sequence):
                        modification_dictionary[part_key].append("Restriction site " + forbidden_site + " (" +
                                                                 site_name + ")" + " detected")

        if GUI.include_signal_combo.get() == "Yes":
            signal_number = 0
            for signal in transcription_unit_4_signal:
                signal_number = signal_number + 1
                part_key = "unit4_s" + str(signal_number)
                modification_dictionary[part_key] = []
                modification_dictionary[part_key].append(signal)
                sequence = signal.sequence.elements
                for forbidden_site in forbidden_sites_ecoflex:
                    site_name = restriction_site_name_library(forbidden_site)
                    count = (sequence.count(forbidden_site))
                    if ("taaa" + signal.sequence.elements[:5]).find(forbidden_site) >= 0:
                        modification_dictionary[part_key].append("Restriction site " + forbidden_site + " (" +
                                                                 site_name + ")" + "has been created at the 5' end of "
                                                                                   "this part as a result of the "
                                                                                   "addition "
                                                                                   "of the "
                                                                                   "signal peptide prefix fusion "
                                                                                   "site 'taaa'")

                    if (signal.sequence.elements[-5:] + "cata").find(forbidden_site) >= 0:
                        modification_dictionary[part_key].append("Restriction site " + forbidden_site + " (" +
                                                                 site_name + ")" + "has been created at the 3' end of "
                                                                                   "this part as a result of the "
                                                                                   "addition "
                                                                                   "of the "
                                                                                   "signal peptide suffix fusion "
                                                                                   "site 'cata'")
                    if count > 0:
                        for location in re.finditer(forbidden_site, sequence):
                            modification_dictionary[part_key].append("Restriction site " + forbidden_site + " (" +
                                                                     site_name + ")" + " detected")

        terminator_number = 0
        for terminator in transcription_unit_4_terminator:
            terminator_number = terminator_number + 1
            part_key = "unit4_t" + str(terminator_number)
            modification_dictionary[part_key] = []
            modification_dictionary[part_key].append(terminator)
            sequence = terminator.sequence.elements
            for forbidden_site in forbidden_sites_ecoflex:
                site_name = restriction_site_name_library(forbidden_site)
                count = (sequence.count(forbidden_site))
                if ("tcga" + terminator.sequence.elements[:5]).find(forbidden_site) >= 0:
                    modification_dictionary[part_key].append("Restriction site " + forbidden_site + " (" +
                                                             site_name + ")" + "has been created at the 5' end of "
                                                                               "this part as a result of the "
                                                                               "addition "
                                                                               "of the "
                                                                               "terminator prefix fusion "
                                                                               "site 'tcga'")

                if (terminator.sequence.elements[-5:] + "tgtt").find(forbidden_site) >= 0:
                    modification_dictionary[part_key].append("Restriction site " + forbidden_site + " (" +
                                                             site_name + ")" + "has been created at the 3' end of "
                                                                               "this part as a result of the "
                                                                               "addition "
                                                                               "of the "
                                                                               "terminator suffix fusion "
                                                                               "site 'tgtt'")
                if count > 0:
                    for location in re.finditer(forbidden_site, sequence):
                        modification_dictionary[part_key].append("Restriction site " + forbidden_site + " (" +
                                                                 site_name + ")" + " detected")

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
                site_name = restriction_site_name_library(forbidden_site)
                count = (sequence.count(forbidden_site))
                if ("ctat" + promoter.sequence.elements[:5]).find(forbidden_site) >= 0:
                    modification_dictionary[part_key].append("Restriction site " + forbidden_site + " (" +
                                                             site_name + ")" + "has been created at the 5' end of "
                                                                               "this part as a result of the addition "
                                                                               "of the "
                                                                               "promoter prefix fusion "
                                                                               "site 'ctat'")
                if (promoter.sequence.elements[-5:] + "gtac").find(forbidden_site) >= 0:
                    modification_dictionary[part_key].append("Restriction site " + forbidden_site + " (" +
                                                             site_name + ")" + "has been created at the 3' end of "
                                                                               "this part as a result of the addition "
                                                                               "of the "
                                                                               "promoter suffix fusion "
                                                                               "site 'gtac'")
                if count > 0:
                    for location in re.finditer(forbidden_site, sequence):
                        modification_dictionary[part_key].append("Restriction site " + forbidden_site + " (" +
                                                                 site_name + ")" + " detected")

        rbs_number = 0
        for rbs in transcription_unit_5_rbs:
            rbs_number = rbs_number + 1
            part_key = "unit5_r" + str(rbs_number)
            modification_dictionary[part_key] = []
            modification_dictionary[part_key].append(rbs)
            sequence = rbs.sequence.elements
            for forbidden_site in forbidden_sites_ecoflex:
                site_name = restriction_site_name_library(forbidden_site)
                count = (sequence.count(forbidden_site))
                if ("gtac" + rbs.sequence.elements[:5]).find(forbidden_site) >= 0:
                    modification_dictionary[part_key].append("Restriction site " + forbidden_site + " (" +
                                                             site_name + ")" + "has been created at the 5' end of "
                                                                               "this part as a result of the addition "
                                                                               "of the "
                                                                               "rbs prefix fusion "
                                                                               "site 'gtac'")

                if GUI.include_signal_combo.get() == "Yes":
                    if (rbs.sequence.elements[-5:] + "taaa").find(forbidden_site) >= 0:
                        modification_dictionary[part_key].append("Restriction site " + forbidden_site + " (" +
                                                                 site_name + ")" + "has been created at the 3' end of "
                                                                                   "this part as a result of the "
                                                                                   "addition "
                                                                                   "of the "
                                                                                   "rbs suffix fusion "
                                                                                   "site 'taaa'")
                if GUI.include_signal_combo.get() == "No":
                    if (rbs.sequence.elements[-5:] + "cata").find(forbidden_site) >= 0:
                        modification_dictionary[part_key].append("Restriction site " + forbidden_site + " (" +
                                                                 site_name + ")" + "has been created at the 3' end of "
                                                                                   "this part as a result of the "
                                                                                   "addition "
                                                                                   "of the "
                                                                                   "rbs suffix fusion "
                                                                                   "site 'cata'")
                if count > 0:
                    for location in re.finditer(forbidden_site, sequence):
                        modification_dictionary[part_key].append("Restriction site " + forbidden_site + " (" +
                                                                 site_name + ")" + " detected")

        if GUI.include_signal_combo.get() == "Yes":
            signal_number = 0
            for signal in transcription_unit_5_signal:
                signal_number = signal_number + 1
                part_key = "unit5_s" + str(signal_number)
                modification_dictionary[part_key] = []
                modification_dictionary[part_key].append(signal)
                sequence = signal.sequence.elements
                for forbidden_site in forbidden_sites_ecoflex:
                    site_name = restriction_site_name_library(forbidden_site)
                    count = (sequence.count(forbidden_site))
                    if ("taaa" + signal.sequence.elements[:5]).find(forbidden_site) >= 0:
                        modification_dictionary[part_key].append("Restriction site " + forbidden_site + " (" +
                                                                 site_name + ")" + "has been created at the 5' end of "
                                                                                   "this part as a result of the "
                                                                                   "addition "
                                                                                   "of the "
                                                                                   "signal peptide prefix fusion "
                                                                                   "site 'taaa'")

                    if (signal.sequence.elements[-5:] + "cata").find(forbidden_site) >= 0:
                        modification_dictionary[part_key].append("Restriction site " + forbidden_site + " (" +
                                                                 site_name + ")" + "has been created at the 3' end of "
                                                                                   "this part as a result of the "
                                                                                   "addition "
                                                                                   "of the "
                                                                                   "signal peptide suffix fusion "
                                                                                   "site 'cata'")
                    if count > 0:
                        for location in re.finditer(forbidden_site, sequence):
                            modification_dictionary[part_key].append("Restriction site " + forbidden_site + " (" +
                                                                     site_name + ")" + " detected")

        terminator_number = 0
        for terminator in transcription_unit_5_terminator:
            terminator_number = terminator_number + 1
            part_key = "unit5_t" + str(terminator_number)
            modification_dictionary[part_key] = []
            modification_dictionary[part_key].append(terminator)
            sequence = terminator.sequence.elements
            for forbidden_site in forbidden_sites_ecoflex:
                site_name = restriction_site_name_library(forbidden_site)
                count = (sequence.count(forbidden_site))
                if ("tcga" + terminator.sequence.elements[:5]).find(forbidden_site) >= 0:
                    modification_dictionary[part_key].append("Restriction site " + forbidden_site + " (" +
                                                             site_name + ")" + "has been created at the 5' end of "
                                                                               "this part as a result of the "
                                                                               "addition "
                                                                               "of the "
                                                                               "terminator prefix fusion "
                                                                               "site 'tcga'")

                if (terminator.sequence.elements[-5:] + "tgtt").find(forbidden_site) >= 0:
                    modification_dictionary[part_key].append("Restriction site " + forbidden_site + " (" +
                                                             site_name + ")" + "has been created at the 3' end of "
                                                                               "this part as a result of the "
                                                                               "addition "
                                                                               "of the "
                                                                               "terminator suffix fusion "
                                                                               "site 'tgtt'")
                if count > 0:
                    for location in re.finditer(forbidden_site, sequence):
                        modification_dictionary[part_key].append("Restriction site " + forbidden_site + " (" +
                                                                 site_name + ")" + " detected")


# Adding EcoFlex prefix and suffix to parts
def ecoflex_fusion_sites():
    # Transcription unit 1
    if GUI.include_fusion_site_combo.get() == "Yes":
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
                                                                             "fusion site (gtac), BsaI restriction "
                                                                             "site" +
                                                                             " (agagacc), and SphI overhang (catg)")

            if GUI.include_signal_combo.get() == "No":
                counter = 0
                for rbs in transcription_unit_1_rbs:
                    counter = counter + 1
                    if rbs.sequence.elements.startswith("taggtctcagtac"):
                        pass
                    else:
                        rbs.sequence.elements = "taggtctcagtac" + rbs.sequence.elements
                        modification_dictionary["unit1_r" + str(counter)].append(
                            "Prefix added for NdeI overhang (ta)," +
                            " BsaI restriction site (ggtctca)" +
                            " and golden gate RBS fusion site" +
                            " (gtac)")
                    if rbs.sequence.elements.endswith("cataagagacccatg"):
                        pass
                    else:
                        rbs.sequence.elements = rbs.sequence.elements + "cataagagacccatg"
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
                        modification_dictionary["unit1_r" + str(counter)].append(
                            "Prefix added for NdeI overhang (ta)," +
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
                        modification_dictionary["unit1_s" + str(counter)].append(
                            "Prefix added for NdeI overhang (ta)," +
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
                if cds.sequence.elements.startswith("tatg"):
                    pass
                elif cds.sequence.elements.startswith("atg"):
                    cds.sequence.elements = "t" + cds.sequence.elements
                    modification_dictionary["unit1_c" + str(counter)].append("Prefix added for NdeI overhang (t)")
                else:
                    cds.sequence.elements = "tatg" + cds.sequence.elements
                    modification_dictionary["unit1_c" + str(counter)].append("Start codon (atg) could not be found at" +
                                                                             " start of CDS region, please ensure that" +
                                                                             " this SBOL part contains only the CDS. " +
                                                                             "The atg start codon has been added to "
                                                                             "this" +
                                                                             " part, in addition to the prefix for the" +
                                                                             " NdeI overhang (t)")
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
                                                                             "fusion site (tgtt), BsaI restriction "
                                                                             "site" +
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
                                                                             "fusion site (gtac), BsaI restriction "
                                                                             "site" +
                                                                             " (agagacc), and SphI overhang (catg)")

            if GUI.include_signal_combo.get() == "No":
                counter = 0
                for rbs in transcription_unit_2_rbs:
                    counter = counter + 1
                    if rbs.sequence.elements.startswith("taggtctcagtac"):
                        pass
                    else:
                        rbs.sequence.elements = "taggtctcagtac" + rbs.sequence.elements
                        modification_dictionary["unit2_r" + str(counter)].append(
                            "Prefix added for NdeI overhang (ta)," +
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
                        modification_dictionary["unit2_r" + str(counter)].append(
                            "Prefix added for NdeI overhang (ta)," +
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
                        modification_dictionary["unit2_s" + str(counter)].append(
                            "Prefix added for NdeI overhang (ta)," +
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
                if cds.sequence.elements.startswith("tatg"):
                    pass
                elif cds.sequence.elements.startswith("atg"):
                    cds.sequence.elements = "t" + cds.sequence.elements
                    modification_dictionary["unit2_c" + str(counter)].append("Prefix added for NdeI overhang (t)")
                else:
                    cds.sequence.elements = "tatg" + cds.sequence.elements
                    modification_dictionary["unit2_c" + str(counter)].append("Start codon (atg) could not be found at" +
                                                                             " start of CDS region, please ensure that" +
                                                                             " this SBOL part contains only the CDS. " +
                                                                             "The atg start codon has been added to "
                                                                             "this" +
                                                                             " part, in addition to the prefix for the" +
                                                                             " NdeI overhang (t)")
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
                                                                             "fusion site (tgtt), BsaI restriction "
                                                                             "site" +
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
                                                                             "fusion site (gtac), BsaI restriction "
                                                                             "site" +
                                                                             " (agagacc), and SphI overhang (catg)")

            if GUI.include_signal_combo.get() == "No":
                counter = 0
                for rbs in transcription_unit_3_rbs:
                    counter = counter + 1
                    if rbs.sequence.elements.startswith("taggtctcagtac"):
                        pass
                    else:
                        rbs.sequence.elements = "taggtctcagtac" + rbs.sequence.elements
                        modification_dictionary["unit3_r" + str(counter)].append(
                            "Prefix added for NdeI overhang (ta)," +
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
                        modification_dictionary["unit3_r" + str(counter)].append(
                            "Prefix added for NdeI overhang (ta)," +
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
                        modification_dictionary["unit3_s" + str(counter)].append(
                            "Prefix added for NdeI overhang (ta)," +
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
                if cds.sequence.elements.startswith("tatg"):
                    pass
                elif cds.sequence.elements.startswith("atg"):
                    cds.sequence.elements = "t" + cds.sequence.elements
                    modification_dictionary["unit3_c" + str(counter)].append("Prefix added for NdeI overhang (t)")
                else:
                    cds.sequence.elements = "tatg" + cds.sequence.elements
                    modification_dictionary["unit3_c" + str(counter)].append("Start codon (atg) could not be found at" +
                                                                             " start of CDS region, please ensure that" 
                                                                             " this SBOL part contains only the CDS. " +
                                                                             "The atg start codon has been added to "
                                                                             "this" +
                                                                             " part, in addition to the prefix for the" 
                                                                             " NdeI overhang (t)")
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
                                                                             "fusion site (tgtt), BsaI restriction "
                                                                             "site" +
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
                                                                             "fusion site (gtac), BsaI restriction "
                                                                             "site" +
                                                                             " (agagacc), and SphI overhang (catg)")

            if GUI.include_signal_combo.get() == "No":
                counter = 0
                for rbs in transcription_unit_4_rbs:
                    counter = counter + 1
                    if rbs.sequence.elements.startswith("taggtctcagtac"):
                        pass
                    else:
                        rbs.sequence.elements = "taggtctcagtac" + rbs.sequence.elements
                        modification_dictionary["unit4_r" + str(counter)].append(
                            "Prefix added for NdeI overhang (ta)," +
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
                        modification_dictionary["unit4_r" + str(counter)].append(
                            "Prefix added for NdeI overhang (ta)," +
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
                        modification_dictionary["unit4_s" + str(counter)].append(
                            "Prefix added for NdeI overhang (ta)," +
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
                if cds.sequence.elements.startswith("tatg"):
                    pass
                elif cds.sequence.elements.startswith("atg"):
                    cds.sequence.elements = "t" + cds.sequence.elements
                    modification_dictionary["unit4_c" + str(counter)].append("Prefix added for NdeI overhang (t)")
                else:
                    cds.sequence.elements = "tatg" + cds.sequence.elements
                    modification_dictionary["unit4_c" + str(counter)].append("Start codon (atg) could not be found at" +
                                                                             " start of CDS region, please ensure that" 
                                                                             " this SBOL part contains only the CDS. " +
                                                                             "The atg start codon has been added to "
                                                                             "this" +
                                                                             " part, in addition to the prefix for the" 
                                                                             " NdeI overhang (t)")
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
                                                                             "fusion site (tgtt), BsaI restriction "
                                                                             "site" +
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
                                                                             "fusion site (gtac), BsaI restriction "
                                                                             "site" +
                                                                             " (agagacc), and SphI overhang (catg)")

            if GUI.include_signal_combo.get() == "No":
                counter = 0
                for rbs in transcription_unit_5_rbs:
                    counter = counter + 1
                    if rbs.sequence.elements.startswith("taggtctcagtac"):
                        pass
                    else:
                        rbs.sequence.elements = "taggtctcagtac" + rbs.sequence.elements
                        modification_dictionary["unit5_r" + str(counter)].append(
                            "Prefix added for NdeI overhang (ta)," +
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
                        modification_dictionary["unit5_r" + str(counter)].append(
                            "Prefix added for NdeI overhang (ta)," +
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
                        modification_dictionary["unit5_s" + str(counter)].append(
                            "Prefix added for NdeI overhang (ta)," +
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
                if cds.sequence.elements.startswith("tatg"):
                    pass
                elif cds.sequence.elements.startswith("atg"):
                    cds.sequence.elements = "t" + cds.sequence.elements
                    modification_dictionary["unit5_c" + str(counter)].append("Prefix added for NdeI overhang (t)")
                else:
                    cds.sequence.elements = "tatg" + cds.sequence.elements
                    modification_dictionary["unit5_c" + str(counter)].append("Start codon (atg) could not be found at" +
                                                                             " start of CDS region, please ensure that" 
                                                                             " this SBOL part contains only the CDS. " +
                                                                             "The atg start codon has been added to "
                                                                             "this" +
                                                                             " part, in addition to the prefix for the" 
                                                                             " NdeI overhang (t)")
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
                                                                             "fusion site (tgtt), BsaI restriction "
                                                                             "site" +
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


# List of final 5' to 3' oligonucleotides for selected parts. Duplicates removed.
def final_oligonucleotides_1():
    all_promoters_1 = []
    for promoter in transcription_unit_1_promoter:
        all_promoters_1.append(promoter)
    for promoter in transcription_unit_2_promoter:
        all_promoters_1.append(promoter)
    if int(GUI.transcription_unit_quantity_combo.get()) > 2:
        for promoter in transcription_unit_3_promoter:
            all_promoters_1.append(promoter)
    if int(GUI.transcription_unit_quantity_combo.get()) > 3:
        for promoter in transcription_unit_4_promoter:
            all_promoters_1.append(promoter)
    if int(GUI.transcription_unit_quantity_combo.get()) > 4:
        for promoter in transcription_unit_5_promoter:
            all_promoters_1.append(promoter)
    all_promoters_1 = list(dict.fromkeys(all_promoters_1))

    all_rbs_1 = []
    for rbs in transcription_unit_1_rbs:
        all_rbs_1.append(rbs)
    for rbs in transcription_unit_2_rbs:
        all_rbs_1.append(rbs)
    if int(GUI.transcription_unit_quantity_combo.get()) > 2:
        for rbs in transcription_unit_3_rbs:
            all_rbs_1.append(rbs)
    if int(GUI.transcription_unit_quantity_combo.get()) > 3:
        for rbs in transcription_unit_4_rbs:
            all_rbs_1.append(rbs)
    if int(GUI.transcription_unit_quantity_combo.get()) > 4:
        for rbs in transcription_unit_5_rbs:
            all_rbs_1.append(rbs)
    all_rbs_1 = list(dict.fromkeys(all_rbs_1))

    if GUI.include_signal_combo.get() == "Yes":
        all_signal_1 = []
        for signal in transcription_unit_1_signal:
            all_signal_1.append(signal)
        for signal in transcription_unit_2_signal:
            all_signal_1.append(signal)
        if int(GUI.transcription_unit_quantity_combo.get()) > 2:
            for signal in transcription_unit_3_signal:
                all_signal_1.append(signal)
        if int(GUI.transcription_unit_quantity_combo.get()) > 3:
            for signal in transcription_unit_4_signal:
                all_signal_1.append(signal)
        if int(GUI.transcription_unit_quantity_combo.get()) > 4:
            for signal in transcription_unit_5_signal:
                all_signal_1.append(signal)
        all_signal_1 = list(dict.fromkeys(all_signal_1))

    all_cds_1 = []
    for cds in transcription_unit_1_cds:
        all_cds_1.append(cds)
    for cds in transcription_unit_2_cds:
        all_cds_1.append(cds)
    if int(GUI.transcription_unit_quantity_combo.get()) > 2:
        for cds in transcription_unit_3_cds:
            all_cds_1.append(cds)
    if int(GUI.transcription_unit_quantity_combo.get()) > 3:
        for cds in transcription_unit_4_cds:
            all_cds_1.append(cds)
    if int(GUI.transcription_unit_quantity_combo.get()) > 4:
        for cds in transcription_unit_5_cds:
            all_cds_1.append(cds)
    all_cds_1 = list(dict.fromkeys(all_cds_1))

    all_terminator_1 = []
    for terminator in transcription_unit_1_terminator:
        all_terminator_1.append(terminator)
    for terminator in transcription_unit_2_terminator:
        all_terminator_1.append(terminator)
    if int(GUI.transcription_unit_quantity_combo.get()) > 2:
        for terminator in transcription_unit_3_terminator:
            all_terminator_1.append(terminator)
    if int(GUI.transcription_unit_quantity_combo.get()) > 3:
        for terminator in transcription_unit_4_terminator:
            all_terminator_1.append(terminator)
    if int(GUI.transcription_unit_quantity_combo.get()) > 4:
        for terminator in transcription_unit_5_terminator:
            all_terminator_1.append(terminator)
    all_terminator_1 = list(dict.fromkeys(all_terminator_1))

    if GUI.include_signal_combo.get() == "Yes":
        return [all_promoters_1, all_rbs_1, all_signal_1, all_cds_1, all_terminator_1]
    if GUI.include_signal_combo.get() == "No":
        return [all_promoters_1, all_rbs_1, all_cds_1, all_terminator_1]


# Create complement sequence, will also remove DNA regions corresponding to overhangs in 5' to 3' sequence
def create_complement(sequence):
    sequence_complement = ""
    for base in sequence:
        if base == "a":
            sequence_complement = sequence_complement + "t"
        if base == "t":
            sequence_complement = sequence_complement + "a"
        if base == "g":
            sequence_complement = sequence_complement + "c"
        if base == "c":
            sequence_complement = sequence_complement + "g"

    if GUI.include_fusion_site_combo.get() == "Yes":
        sequence_complement = sequence_complement[:-4]
        sequence_complement = sequence_complement[2:]
    return sequence_complement


# Creating 3' to 5' strands, getting part sequences, getting modifications, preparing lists for protocol generation
def final_oligonucleotides_2():
    global promoter_identities
    promoter_identities = []
    global promoter_descriptions
    promoter_descriptions = []
    global promoter_sequences_1
    promoter_sequences_1 = []
    global promoter_sequences_2
    promoter_sequences_2 = []
    global promoter_modifications
    promoter_modifications = []
    global rbs_identities
    rbs_identities = []
    global rbs_descriptions
    rbs_descriptions = []
    global rbs_sequences_1
    rbs_sequences_1 = []
    global rbs_sequences_2
    rbs_sequences_2 = []
    global rbs_modifications
    rbs_modifications = []
    global cds_identities
    cds_identities = []
    global cds_descriptions
    cds_descriptions = []
    global cds_sequences_1
    cds_sequences_1 = []
    global cds_sequences_2
    cds_sequences_2 = []
    global cds_modifications
    cds_modifications = []
    global terminator_identities
    terminator_identities = []
    global terminator_descriptions
    terminator_descriptions = []
    global terminator_sequences_1
    terminator_sequences_1 = []
    global terminator_sequences_2
    terminator_sequences_2 = []
    global terminator_modifications
    terminator_modifications = []

    strand_1 = final_oligonucleotides_1()
    if GUI.include_signal_combo.get() == "No":
        for promoter in strand_1[0]:
            promoter_identities.append(promoter.displayId)
            promoter_descriptions.append(promoter.description)
            promoter_sequences_1.append(promoter.sequence.elements)
            promoter_sequences_2.append(create_complement(promoter.sequence.elements))

        for rbs in strand_1[1]:
            rbs_identities.append(rbs.displayId)
            rbs_descriptions.append(rbs.description)
            rbs_sequences_1.append(rbs.sequence.elements)
            rbs_sequences_2.append(create_complement(rbs.sequence.elements))

        for cds in strand_1[2]:
            cds_identities.append(cds.displayId)
            cds_descriptions.append(cds.description)
            cds_sequences_1.append(cds.sequence.elements)
            cds_sequences_2.append(create_complement(cds.sequence.elements))

        for terminator in strand_1[3]:
            terminator_identities.append(terminator.displayId)
            terminator_descriptions.append(terminator.description)
            terminator_sequences_1.append(terminator.sequence.elements)
            terminator_sequences_2.append(create_complement(terminator.sequence.elements))

        for key in modification_dictionary:
            for promoter in strand_1[0]:
                if promoter == modification_dictionary[key][0]:
                    if not modification_dictionary[key][1:]:
                        promoter_modifications.append(" ")
                    else:
                        promoter_modifications.append(modification_dictionary[key][1:])

        for key in modification_dictionary:
            for rbs in strand_1[1]:
                if rbs == modification_dictionary[key][0]:
                    if not modification_dictionary[key][1:]:
                        rbs_modifications.append(" ")
                    else:
                        rbs_modifications.append(modification_dictionary[key][1:])

        for key in modification_dictionary:
            for cds in strand_1[2]:
                if cds == modification_dictionary[key][0]:
                    if not modification_dictionary[key][1:]:
                        cds_modifications.append(" ")
                    else:
                        cds_modifications.append(modification_dictionary[key][1:])

        for key in modification_dictionary:
            for terminator in strand_1[3]:
                if terminator == modification_dictionary[key][0]:
                    if not modification_dictionary[key][1:]:
                        terminator_modifications.append(" ")
                    else:
                        terminator_modifications.append(modification_dictionary[key][1:])

    if GUI.include_signal_combo.get() == "Yes":
        global signal_identities
        signal_identities = []
        global signal_descriptions
        signal_descriptions = []
        global signal_sequences_1
        signal_sequences_1 = []
        global signal_sequences_2
        signal_sequences_2 = []
        global signal_modifications
        signal_modifications = []

        for promoter in strand_1[0]:
            promoter_identities.append(promoter.displayId)
            promoter_descriptions.append(promoter.description)
            promoter_sequences_1.append(promoter.sequence.elements)
            promoter_sequences_2.append(create_complement(promoter.sequence.elements))

        for rbs in strand_1[1]:
            rbs_identities.append(rbs.displayId)
            rbs_descriptions.append(rbs.description)
            rbs_sequences_1.append(rbs.sequence.elements)
            rbs_sequences_2.append(create_complement(rbs.sequence.elements))

        for signal in strand_1[2]:
            signal_identities.append(signal.displayId)
            signal_descriptions.append(signal.description)
            signal_sequences_1.append(signal.sequence.elements)
            signal_sequences_2.append(create_complement(signal.sequence.elements))

        for cds in strand_1[3]:
            cds_identities.append(cds.displayId)
            cds_descriptions.append(cds.description)
            cds_sequences_1.append(cds.sequence.elements)
            cds_sequences_2.append(create_complement(cds.sequence.elements))

        for terminator in strand_1[4]:
            terminator_identities.append(terminator.displayId)
            terminator_descriptions.append(terminator.description)
            terminator_sequences_1.append(terminator.sequence.elements)
            terminator_sequences_2.append(create_complement(terminator.sequence.elements))

        for key in modification_dictionary:
            for promoter in strand_1[0]:
                if promoter == modification_dictionary[key][0]:
                    if not modification_dictionary[key][1:]:
                        promoter_modifications.append(" ")
                    else:
                        promoter_modifications.append(modification_dictionary[key][1:])

        for key in modification_dictionary:
            for rbs in strand_1[1]:
                if rbs == modification_dictionary[key][0]:
                    if not modification_dictionary[key][1:]:
                        rbs_modifications.append(" ")
                    else:
                        rbs_modifications.append(modification_dictionary[key][1:])

        for key in modification_dictionary:
            for signal in strand_1[2]:
                if signal == modification_dictionary[key][0]:
                    if not modification_dictionary[key][1:]:
                        signal_modifications.append(" ")
                    else:
                        signal_modifications.append(modification_dictionary[key][1:])

        for key in modification_dictionary:
            for cds in strand_1[3]:
                if cds == modification_dictionary[key][0]:
                    if not modification_dictionary[key][1:]:
                        cds_modifications.append(" ")
                    else:
                        cds_modifications.append(modification_dictionary[key][1:])

        for key in modification_dictionary:
            for terminator in strand_1[4]:
                if terminator == modification_dictionary[key][0]:
                    if not modification_dictionary[key][1:]:
                        terminator_modifications.append(" ")
                    else:
                        terminator_modifications.append(modification_dictionary[key][1:])


# Creating transcription unit sequences, formatting for display in generated protocol
def transcription_unit_format():
    global transcription_unit_1_sequences
    transcription_unit_1_sequences = []
    global transcription_unit_1_names
    transcription_unit_1_names = []
    global transcription_unit_1_part_id
    transcription_unit_1_part_id = []
    global transcription_unit_1_notes
    transcription_unit_1_notes = []
    global transcription_unit_2_sequences
    transcription_unit_2_sequences = []
    global transcription_unit_2_names
    transcription_unit_2_names = []
    global transcription_unit_2_part_id
    transcription_unit_2_part_id = []
    global transcription_unit_2_notes
    transcription_unit_2_notes = []
    global transcription_unit_3_sequences
    transcription_unit_3_sequences = []
    global transcription_unit_3_names
    transcription_unit_3_names = []
    global transcription_unit_3_part_id
    transcription_unit_3_part_id = []
    global transcription_unit_3_notes
    transcription_unit_3_notes = []
    global transcription_unit_4_sequences
    transcription_unit_4_sequences = []
    global transcription_unit_4_names
    transcription_unit_4_names = []
    global transcription_unit_4_part_id
    transcription_unit_4_part_id = []
    global transcription_unit_4_notes
    transcription_unit_4_notes = []
    global transcription_unit_5_sequences
    transcription_unit_5_sequences = []
    global transcription_unit_5_names
    transcription_unit_5_names = []
    global transcription_unit_5_part_id
    transcription_unit_5_part_id = []
    global transcription_unit_5_notes
    transcription_unit_5_notes = []
    global level_1_transcription_unit_dictionary
    level_1_transcription_unit_dictionary = {}

    if int(GUI.transcription_unit_quantity_combo.get()) > 1:
        # Transcription unit 1
        if GUI.include_signal_combo.get() == "No":
            counter = 0
            for key in transcription_unit_1_variants:
                promoter = transcription_unit_1_variants[key][0].sequence.elements
                rbs = transcription_unit_1_variants[key][1].sequence.elements
                cds = transcription_unit_1_variants[key][2].sequence.elements
                terminator = transcription_unit_1_variants[key][3].sequence.elements
                promoter_sequence = promoter[9:-15]
                rbs_sequence = rbs[9:-15]
                cds_sequence = "ca" + cds[:-4]
                terminator_sequence = terminator[9:-11]
                counter = counter + 1
                transcription_unit_1_notes.append("Prefix atct and suffix tgcc fusion sites conferred to sequence by "
                                                  "level 1 plasmid backbone pTU1-A-RFP")
                transcription_unit_1_sequences.append(
                    ["atct" + promoter_sequence + rbs_sequence + cds_sequence + terminator_sequence + "tgcc"])
                transcription_unit_1_names.append("Transcription unit 1 variant " + str(counter))
                transcription_unit_1_part_id.append([transcription_unit_1_variants[key][0].displayId,
                                                     transcription_unit_1_variants[key][1].displayId,
                                                     transcription_unit_1_variants[key][2].displayId,
                                                     transcription_unit_1_variants[key][3].displayId])
                level_1_transcription_unit_dictionary["Transcription unit 1 variant " + str(counter)] = (
                    transcription_unit_1_part_id[counter - 1])

        if GUI.include_signal_combo.get() == "Yes":
            counter = 0
            for key in transcription_unit_1_variants:
                promoter = transcription_unit_1_variants[key][0].sequence.elements
                rbs = transcription_unit_1_variants[key][1].sequence.elements
                signal = transcription_unit_1_variants[key][2].sequence.elements
                cds = transcription_unit_1_variants[key][3].sequence.elements
                terminator = transcription_unit_1_variants[key][4].sequence.elements
                promoter_sequence = promoter[9:-15]
                rbs_sequence = rbs[9:-15]
                signal_sequence = signal[9:-15]
                cds_sequence = "ca" + cds[:-4]
                terminator_sequence = terminator[9:-11]
                counter = counter + 1
                transcription_unit_1_notes.append("Prefix atct and suffix tgcc fusion sites conferred to sequence by "
                                                  "level 1 plasmid backbone pTU1-A-RFP")
                transcription_unit_1_sequences.append(
                    ["atct" + promoter_sequence + rbs_sequence + signal_sequence + cds_sequence + terminator_sequence +
                     "tgcc"])

                transcription_unit_1_names.append("Transcription unit 1 variant " + str(counter))
                transcription_unit_1_part_id.append([transcription_unit_1_variants[key][0].displayId,
                                                     transcription_unit_1_variants[key][1].displayId,
                                                     transcription_unit_1_variants[key][2].displayId,
                                                     transcription_unit_1_variants[key][3].displayId,
                                                     transcription_unit_1_variants[key][4].displayId])
                level_1_transcription_unit_dictionary["Transcription unit 1 variant " + str(counter)] = (
                    transcription_unit_1_part_id[counter - 1])

        # Transcription unit 2
        if GUI.include_signal_combo.get() == "No":
            counter = 0
            for key in transcription_unit_2_variants:
                promoter = transcription_unit_2_variants[key][0].sequence.elements
                rbs = transcription_unit_2_variants[key][1].sequence.elements
                cds = transcription_unit_2_variants[key][2].sequence.elements
                terminator = transcription_unit_2_variants[key][3].sequence.elements
                promoter_sequence = promoter[9:-15]
                rbs_sequence = rbs[9:-15]
                cds_sequence = "ca" + cds[:-4]
                terminator_sequence = terminator[9:-11]
                counter = counter + 1
                transcription_unit_2_notes.append("Prefix tgcc and suffix ccgg fusion sites conferred to sequence by "
                                                  "level 1 plasmid backbone pTU1-B-RFP")
                transcription_unit_2_sequences.append(
                    ["tgcc" + promoter_sequence + rbs_sequence + cds_sequence + terminator_sequence +
                     "ccgg"])
                transcription_unit_2_names.append("Transcription unit 2 variant " + str(counter))
                transcription_unit_2_part_id.append([transcription_unit_2_variants[key][0].displayId,
                                                     transcription_unit_2_variants[key][1].displayId,
                                                     transcription_unit_2_variants[key][2].displayId,
                                                     transcription_unit_2_variants[key][3].displayId])
                level_1_transcription_unit_dictionary["Transcription unit 2 variant " + str(counter)] = (
                    transcription_unit_2_part_id[counter - 1])

        if GUI.include_signal_combo.get() == "Yes":
            counter = 0
            for key in transcription_unit_2_variants:
                promoter = transcription_unit_2_variants[key][0].sequence.elements
                rbs = transcription_unit_2_variants[key][1].sequence.elements
                signal = transcription_unit_2_variants[key][2].sequence.elements
                cds = transcription_unit_2_variants[key][3].sequence.elements
                terminator = transcription_unit_2_variants[key][4].sequence.elements
                promoter_sequence = promoter[9:-15]
                rbs_sequence = rbs[9:-15]
                signal_sequence = signal[9:-15]
                cds_sequence = "ca" + cds[:-4]
                terminator_sequence = terminator[9:-11]
                counter = counter + 1
                transcription_unit_2_notes.append("Prefix tgcc and suffix ccgg fusion sites conferred to sequence by "
                                                  "level 1 plasmid backbone pTU1-B-RFP")
                transcription_unit_2_sequences.append(
                    ["tgcc" + promoter_sequence + rbs_sequence + signal_sequence + cds_sequence + terminator_sequence +
                     "ccgg"])
                transcription_unit_2_names.append("Transcription unit 2 variant " + str(counter))
                transcription_unit_2_part_id.append([transcription_unit_2_variants[key][0].displayId,
                                                     transcription_unit_2_variants[key][1].displayId,
                                                     transcription_unit_2_variants[key][2].displayId,
                                                     transcription_unit_2_variants[key][3].displayId,
                                                     transcription_unit_2_variants[key][4].displayId])
                level_1_transcription_unit_dictionary["Transcription unit 2 variant " + str(counter)] = (
                    transcription_unit_2_part_id[counter - 1])

    if int(GUI.transcription_unit_quantity_combo.get()) > 2:
        # Transcription unit 3
        if GUI.include_signal_combo.get() == "No":
            counter = 0
            for key in transcription_unit_3_variants:
                promoter = transcription_unit_3_variants[key][0].sequence.elements
                rbs = transcription_unit_3_variants[key][1].sequence.elements
                cds = transcription_unit_3_variants[key][2].sequence.elements
                terminator = transcription_unit_3_variants[key][3].sequence.elements
                promoter_sequence = promoter[9:-15]
                rbs_sequence = rbs[9:-15]
                cds_sequence = "ca" + cds[:-4]
                terminator_sequence = terminator[9:-11]
                counter = counter + 1
                transcription_unit_3_notes.append("Prefix ccgg and suffix gaag fusion sites conferred to sequence by "
                                                  "level 1 plasmid backbone pTU1-C-RFP")
                transcription_unit_3_sequences.append(
                    ["ccgg" + promoter_sequence + rbs_sequence + cds_sequence + terminator_sequence +
                     "gaag"])
                transcription_unit_3_names.append("Transcription unit 3 variant " + str(counter))
                transcription_unit_3_part_id.append([transcription_unit_3_variants[key][0].displayId,
                                                     transcription_unit_3_variants[key][1].displayId,
                                                     transcription_unit_3_variants[key][2].displayId,
                                                     transcription_unit_3_variants[key][3].displayId])
                level_1_transcription_unit_dictionary["Transcription unit 3 variant " + str(counter)] = (
                    transcription_unit_3_part_id[counter - 1])

        if GUI.include_signal_combo.get() == "Yes":
            counter = 0
            for key in transcription_unit_3_variants:
                promoter = transcription_unit_3_variants[key][0].sequence.elements
                rbs = transcription_unit_3_variants[key][1].sequence.elements
                signal = transcription_unit_3_variants[key][2].sequence.elements
                cds = transcription_unit_3_variants[key][3].sequence.elements
                terminator = transcription_unit_3_variants[key][4].sequence.elements
                promoter_sequence = promoter[9:-15]
                rbs_sequence = rbs[9:-15]
                signal_sequence = signal[9:-15]
                cds_sequence = "ca" + cds[:-4]
                terminator_sequence = terminator[9:-11]
                counter = counter + 1
                transcription_unit_3_notes.append("Prefix ccgg and suffix gaag fusion sites conferred to sequence by "
                                                  "level 1 plasmid backbone pTU1-C-RFP")
                transcription_unit_3_sequences.append(
                    ["ccgg" + promoter_sequence + rbs_sequence + signal_sequence + cds_sequence + terminator_sequence +
                     "gaag"])
                transcription_unit_3_names.append("Transcription unit 3 variant " + str(counter))
                transcription_unit_3_part_id.append([transcription_unit_3_variants[key][0].displayId,
                                                     transcription_unit_3_variants[key][1].displayId,
                                                     transcription_unit_3_variants[key][2].displayId,
                                                     transcription_unit_3_variants[key][3].displayId,
                                                     transcription_unit_3_variants[key][4].displayId])
                level_1_transcription_unit_dictionary["Transcription unit 3 variant " + str(counter)] = (
                    transcription_unit_3_part_id[counter - 1])

    if int(GUI.transcription_unit_quantity_combo.get()) > 3:
        # Transcription unit 4
        if GUI.include_signal_combo.get() == "No":
            counter = 0
            for key in transcription_unit_4_variants:
                promoter = transcription_unit_4_variants[key][0].sequence.elements
                rbs = transcription_unit_4_variants[key][1].sequence.elements
                cds = transcription_unit_4_variants[key][2].sequence.elements
                terminator = transcription_unit_4_variants[key][3].sequence.elements
                promoter_sequence = promoter[9:-15]
                rbs_sequence = rbs[9:-15]
                cds_sequence = "ca" + cds[:-4]
                terminator_sequence = terminator[9:-11]
                counter = counter + 1
                if int(GUI.transcription_unit_quantity_combo.get()) == 4:
                    transcription_unit_4_notes.append(
                        "Prefix gaag and suffix ttag fusion sites conferred to sequence by "
                        "level 1 plasmid backbone pTU1-D-RFP")
                    transcription_unit_4_sequences.append(
                        ["gaag" + promoter_sequence + rbs_sequence + cds_sequence + terminator_sequence + "ttag"])
                if int(GUI.transcription_unit_quantity_combo.get()) == 5:
                    transcription_unit_4_notes.append(
                        "Prefix gaag and suffix cttc fusion sites conferred to sequence by "
                        "level 1 plasmid backbone pTU1-D1-RFP")
                    transcription_unit_4_sequences.append(
                        ["gaag" + promoter_sequence + rbs_sequence + cds_sequence + terminator_sequence + "cttc"])
                transcription_unit_4_names.append("Transcription unit 4 variant " + str(counter))
                transcription_unit_4_part_id.append([transcription_unit_4_variants[key][0].displayId,
                                                     transcription_unit_4_variants[key][1].displayId,
                                                     transcription_unit_4_variants[key][2].displayId,
                                                     transcription_unit_4_variants[key][3].displayId])
                level_1_transcription_unit_dictionary["Transcription unit 4 variant " + str(counter)] = (
                    transcription_unit_4_part_id[counter - 1])

        if GUI.include_signal_combo.get() == "Yes":
            counter = 0
            for key in transcription_unit_4_variants:
                promoter = transcription_unit_4_variants[key][0].sequence.elements
                rbs = transcription_unit_4_variants[key][1].sequence.elements
                signal = transcription_unit_4_variants[key][2].sequence.elements
                cds = transcription_unit_4_variants[key][3].sequence.elements
                terminator = transcription_unit_4_variants[key][4].sequence.elements
                promoter_sequence = promoter[9:-15]
                rbs_sequence = rbs[9:-15]
                signal_sequence = signal[9:-15]
                cds_sequence = "ca" + cds[:-4]
                terminator_sequence = terminator[9:-11]
                counter = counter + 1
                if int(GUI.transcription_unit_quantity_combo.get()) == 4:
                    transcription_unit_4_notes.append(
                        "Prefix gaag and suffix ttag fusion sites conferred to sequence by "
                        "level 1 plasmid backbone pTU1-D-RFP")
                    transcription_unit_4_sequences.append(
                        ["gaag" + promoter_sequence + rbs_sequence + signal_sequence + cds_sequence
                         + terminator_sequence + "ttag"])

                if int(GUI.transcription_unit_quantity_combo.get()) == 5:
                    transcription_unit_4_notes.append(
                        "Prefix gaag and suffix cttc fusion sites conferred to sequence by "
                        "level 1 plasmid backbone pTU1-D1-RFP")
                    transcription_unit_4_sequences.append(
                        ["gaag" + promoter_sequence + rbs_sequence + signal_sequence + cds_sequence
                         + terminator_sequence + "cttc"])

                transcription_unit_4_names.append("Transcription unit 4 variant " + str(counter))
                transcription_unit_4_part_id.append([transcription_unit_4_variants[key][0].displayId,
                                                     transcription_unit_4_variants[key][1].displayId,
                                                     transcription_unit_4_variants[key][2].displayId,
                                                     transcription_unit_4_variants[key][3].displayId,
                                                     transcription_unit_4_variants[key][4].displayId])
                level_1_transcription_unit_dictionary["Transcription unit 4 variant " + str(counter)] = (
                    transcription_unit_4_part_id[counter - 1])

    if int(GUI.transcription_unit_quantity_combo.get()) > 4:
        # Transcription unit 5
        if GUI.include_signal_combo.get() == "No":
            counter = 0
            for key in transcription_unit_5_variants:
                promoter = transcription_unit_5_variants[key][0].sequence.elements
                rbs = transcription_unit_5_variants[key][1].sequence.elements
                cds = transcription_unit_5_variants[key][2].sequence.elements
                terminator = transcription_unit_5_variants[key][3].sequence.elements
                promoter_sequence = promoter[9:-15]
                rbs_sequence = rbs[9:-15]
                cds_sequence = "ca" + cds[:-4]
                terminator_sequence = terminator[9:-11]
                counter = counter + 1
                transcription_unit_5_notes.append("Prefix cttc and suffix ttag fusion sites conferred to sequence by "
                                                  "level 1 plasmid backbone pTU1-E-RFP")
                transcription_unit_5_sequences.append(
                    ["cttc" + promoter_sequence + rbs_sequence + cds_sequence + terminator_sequence + "ttag"])
                transcription_unit_5_names.append("Transcription unit 5 variant " + str(counter))
                transcription_unit_5_part_id.append([transcription_unit_5_variants[key][0].displayId,
                                                     transcription_unit_5_variants[key][1].displayId,
                                                     transcription_unit_5_variants[key][2].displayId,
                                                     transcription_unit_5_variants[key][3].displayId])
                level_1_transcription_unit_dictionary["Transcription unit 5 variant " + str(counter)] = (
                    transcription_unit_5_part_id[counter - 1])

        if GUI.include_signal_combo.get() == "Yes":
            counter = 0
            for key in transcription_unit_5_variants:
                promoter = transcription_unit_5_variants[key][0].sequence.elements
                rbs = transcription_unit_5_variants[key][1].sequence.elements
                signal = transcription_unit_5_variants[key][2].sequence.elements
                cds = transcription_unit_5_variants[key][3].sequence.elements
                terminator = transcription_unit_5_variants[key][4].sequence.elements
                promoter_sequence = promoter[9:-15]
                rbs_sequence = rbs[9:-15]
                signal_sequence = signal[9:-15]
                cds_sequence = "ca" + cds[:-4]
                terminator_sequence = terminator[9:-11]
                counter = counter + 1
                transcription_unit_5_notes.append("Prefix cttc and suffix ttag fusion sites conferred to sequence by "
                                                  "level 1 plasmid backbone pTU1-E-RFP")
                transcription_unit_5_sequences.append(
                    ["cttc" + promoter_sequence + rbs_sequence + signal_sequence + cds_sequence + terminator_sequence
                     + "ttag"])
                transcription_unit_5_names.append("Transcription unit 5 variant " + str(counter))
                transcription_unit_5_part_id.append([transcription_unit_5_variants[key][0].displayId,
                                                     transcription_unit_5_variants[key][1].displayId,
                                                     transcription_unit_5_variants[key][2].displayId,
                                                     transcription_unit_5_variants[key][3].displayId,
                                                     transcription_unit_5_variants[key][4].displayId])
                level_1_transcription_unit_dictionary["Transcription unit 5 variant " + str(counter)] = (
                    transcription_unit_5_part_id[counter - 1])


# Creating sequences for level 2 constructs, formatting for display in generated protocol
def level_2_format():
    global level_2_names
    level_2_names = []
    global level_2_sub_units
    level_2_sub_units = []
    global level_2_sequences
    level_2_sequences = []
    global level_2_vector_name
    level_2_vector_name = ""
    global level_2_transcription_unit_dictionary
    level_2_transcription_unit_dictionary = {}

    counter = 0
    if int(GUI.transcription_unit_quantity_combo.get()) == 2:
        level_2_vector_name = "pTU2-a-RFP, available from 'http://www.addgene.org/72958/'"

        for variant in transcription_unit_1_names:
            for variant2 in transcription_unit_2_names:
                counter = counter + 1
                level_2_names.append("Level 2 construct variant " + str(counter))
                level_2_sub_units.append([variant, variant2])
                level_2_transcription_unit_dictionary["Level 2 construct variant " + str(counter)] = (
                    level_2_sub_units[counter - 1])

        for sequence1 in transcription_unit_1_sequences:
            for sequence2 in transcription_unit_2_sequences:
                unit_1_sequence = str(sequence1[0])
                unit_2_sequence = str(sequence2[0])
                level_2_sequences.append([unit_1_sequence + unit_2_sequence])

    if int(GUI.transcription_unit_quantity_combo.get()) == 3:
        level_2_vector_name = "pTU2-b-RFP, available from 'http://www.addgene.org/72959/'"
        counter = counter + 1
        level_2_names.append("Level 2 construct variant " + str(counter))

        for variant in transcription_unit_1_names:
            for variant2 in transcription_unit_2_names:
                for variant3 in transcription_unit_3_names:
                    level_2_sub_units.append([variant, variant2, variant3])
                    level_2_transcription_unit_dictionary["Level 2 construct variant " + str(counter)] = (
                        level_2_sub_units[counter - 1])

        for sequence1 in transcription_unit_1_sequences:
            for sequence2 in transcription_unit_2_sequences:
                for sequence3 in transcription_unit_3_sequences:
                    unit_1_sequence = str(sequence1[0])
                    unit_2_sequence = str(sequence2[0])
                    unit_3_sequence = str(sequence3[0])
                    level_2_sequences.append([unit_1_sequence + unit_2_sequence + unit_3_sequence])

    if int(GUI.transcription_unit_quantity_combo.get()) == 4:
        level_2_vector_name = "pTU2-A-RFP, available from 'http://www.addgene.org/72954/'"

        for variant in transcription_unit_1_names:
            for variant2 in transcription_unit_2_names:
                for variant3 in transcription_unit_3_names:
                    for variant4 in transcription_unit_4_names:
                        counter = counter + 1
                        level_2_names.append("Level 2 construct variant " + str(counter))
                        level_2_sub_units.append([variant, variant2, variant3, variant4])
                        level_2_transcription_unit_dictionary["Level 2 construct variant " + str(counter)] = (
                            level_2_sub_units[counter - 1])

        for sequence1 in transcription_unit_1_sequences:
            for sequence2 in transcription_unit_2_sequences:
                for sequence3 in transcription_unit_3_sequences:
                    for sequence4 in transcription_unit_4_sequences:
                        unit_1_sequence = str(sequence1[0])
                        unit_2_sequence = str(sequence2[0])
                        unit_3_sequence = str(sequence3[0])
                        unit_4_sequence = str(sequence4[0])
                        level_2_sequences.append([unit_1_sequence + unit_2_sequence + unit_3_sequence +
                                                  unit_4_sequence])

    if int(GUI.transcription_unit_quantity_combo.get()) == 5:
        level_2_vector_name = "pTU2-A-RFP, available from 'http://www.addgene.org/72954/"

        for variant in transcription_unit_1_names:
            for variant2 in transcription_unit_2_names:
                for variant3 in transcription_unit_3_names:
                    for variant4 in transcription_unit_4_names:
                        for variant5 in transcription_unit_5_names:
                            counter = counter + 1
                            level_2_names.append("Level 2 construct variant " + str(counter))
                            level_2_sub_units.append([variant, variant2, variant3, variant4, variant5])
                            level_2_transcription_unit_dictionary["Level 2 construct variant " + str(counter)] = (
                                level_2_sub_units[counter - 1])

        for sequence1 in transcription_unit_1_sequences:
            for sequence2 in transcription_unit_2_sequences:
                for sequence3 in transcription_unit_3_sequences:
                    for sequence4 in transcription_unit_4_sequences:
                        for sequence5 in transcription_unit_5_sequences:
                            unit_1_sequence = str(sequence1[0])
                            unit_2_sequence = str(sequence2[0])
                            unit_3_sequence = str(sequence3[0])
                            unit_4_sequence = str(sequence4[0])
                            unit_5_sequence = str(sequence5[0])
                            level_2_sequences.append([unit_1_sequence + unit_2_sequence + unit_3_sequence +
                                                      unit_4_sequence + unit_5_sequence])


# Calculate the amount of times that each part occurs across produced level 1 TU variants
def part_use_quantity():
    global part_quantities
    part_quantities = {}
    for list in transcription_unit_1_part_id:
        for part in list:
            keys = part_quantities.keys()
            if str(part) in keys:
                part_quantities[str(part)] += 1
            else:
                part_quantities[str(part)] = 1

    for list in transcription_unit_2_part_id:
        for part in list:
            keys = part_quantities.keys()
            if str(part) in keys:
                part_quantities[str(part)] += 1
            else:
                part_quantities[str(part)] = 1

    if int(GUI.transcription_unit_quantity_combo.get()) > 2:
        for list in transcription_unit_3_part_id:
            for part in list:
                keys = part_quantities.keys()
                if str(part) in keys:
                    part_quantities[str(part)] += 1
                else:
                    part_quantities[str(part)] = 1

    if int(GUI.transcription_unit_quantity_combo.get()) > 3:
        for list in transcription_unit_4_part_id:
            for part in list:
                keys = part_quantities.keys()
                if str(part) in keys:
                    part_quantities[str(part)] += 1
                else:
                    part_quantities[str(part)] = 1

    if int(GUI.transcription_unit_quantity_combo.get()) > 4:
        for list in transcription_unit_5_part_id:
            for part in list:
                keys = part_quantities.keys()
                if str(part) in keys:
                    part_quantities[str(part)] += 1
                else:
                    part_quantities[str(part)] = 1


# Calculate the amount of times that a level 1 TU variant occurs across produced level 2 TU variants
def transcription_unit_use_quantity():
    global tu1_quantities
    tu1_quantities = {}
    for list in level_2_sub_units:
        for variant in list:
            keys = tu1_quantities.keys()
            if str(variant) in keys:
                tu1_quantities[str(variant)] += 1
            else:
                tu1_quantities[str(variant)] = 1


# Directory for protocol creation
def create_protocol_directory(event):
    chassis_choice = GUI.chassis_selection_combo.get()
    if chassis_choice == "EcoFlex":
        final_ecoflex_check()
        if not ecoflex_check_list:
            from EcoFlex_protocol import create_protocol
            create_protocol("<Button-1>")
        else:
            GUI.restriction_site_warning_ecoflex()
    if chassis_choice == "B. subtilis":
        print("PLACEHOLDER B. SUBTILIS PROTOCOL DIRECTORY")