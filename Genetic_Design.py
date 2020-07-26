# Import libraries
from sbol import *

# Import scripts
import Main
import GUI

# Specifying SynBioHub part repository for query
igem = PartShop('https://synbiohub.org/public/igem')

# Global variables (Not all)
component_definition_list = []
design_roles = []
design_identities = []
design_descriptions = []
doc = Document()

# Add part to design from file
def add_file_part():
    try:
        GUI.incompatible_part_label.pack_forget()
    except AttributeError:
        pass
    temp_list = []
    temp_list_2 = []
    doc2 = Document()
    doc2.read(str(GUI.imported_part))
    for components in doc2.componentDefinitions:
        temp_list.append(components)
    if str(temp_list[0]) == "https://synbiohub.org/public/igem/BBa_B0015/1":
        try:
            part1_uri = (temp_list[2])
            part2_uri = (temp_list[1])
            BBa_B0015 = ComponentDefinition("BBa_B0015")
            BBa_B0010 = ComponentDefinition("BBa_B0010")
            BBa_B0012 = ComponentDefinition("BBa_B0012")
            BBa_B0015.roles = SO_TERMINATOR
            BBa_B0010.roles = SO_TERMINATOR
            BBa_B0012.roles = SO_TERMINATOR
            doc.addComponentDefinition([BBa_B0015, BBa_B0010, BBa_B0012])
            BBa_B0015.description = "Double terminator BBa_B0010 + BBa_B0012"
            BBa_B0015.assemblePrimaryStructure([BBa_B0010, BBa_B0012])
            BBa_B0010.sequence = Sequence("BBa_B0010", str(part1_uri.sequence.elements))
            BBa_B0012.sequence = Sequence("BBa_B0012", str(part2_uri.sequence.elements))
            BBa_B0015_fixed = BBa_B0015.compile()
            for obj in doc:
                temp_list_2.append(obj)
            component_definition_list.append("https://synbiohub.org/public/igem//ComponentDefinition/BBa_B0015/1")
            design_roles.append("http://identifiers.org/so/SO:0000141")
            design_identities.append("BBa_B0015")
            design_descriptions.append("Double terminator BBa_B0010 + BBa_B0012")
            GUI.display_assembled_design(design_roles)
            GUI.create_description_button_design()
        except RuntimeError:
            for obj in doc:
                temp_list_2.append(obj)
            component_definition_list.append("https://synbiohub.org/public/igem//ComponentDefinition/BBa_B0015/1")
            design_roles.append("http://identifiers.org/so/SO:0000141")
            design_identities.append("BBa_B0015")
            design_descriptions.append("Double terminator BBa_B0010 + BBa_B0012")
            GUI.display_assembled_design(design_roles)
            GUI.create_description_button_design()
    else:
        for component in doc2.componentDefinitions:
            if len(component.components) > 0:
                GUI.incompatible_part()
                return

        for components in doc2.componentDefinitions:
            component_definition_list.append(str(components))
            doc.append(str(GUI.imported_part))
            design_display_lists(components)
            GUI.display_assembled_design(design_roles)




# SynBioHub part query
def part_search(query):
    query2 = query.replace(" ", "_")
    global records
    records = igem.search(query2, SBOL_COMPONENT_DEFINITION, 0, 10)
    print(records)
    button_display()


# Contents of button display for queried parts
def button_display():
    global button_1_display
    global button_2_display
    global button_3_display
    global button_4_display
    global button_5_display
    global button_6_display
    global button_7_display
    global button_8_display
    global button_9_display
    global button_10_display
    print(len(records))
    try:
        button_1_display = ("Part identity: " + str(records[0].displayId) + "\n" + "Part description: " +
                            str(records[0].description))
    except ValueError:
        return
    try:
        button_2_display = ("Part identity: " + str(records[1].displayId) + "\n" + "Part description: " +
                            str(records[1].description))
    except ValueError:
        return
    try:
        button_3_display = ("Part identity: " + str(records[2].displayId) + "\n" + "Part description: " +
                            str(records[2].description))
    except ValueError:
        return
    try:
        button_4_display = ("Part identity: " + str(records[3].displayId) + "\n" + "Part description: " +
                            str(records[3].description))
    except ValueError:
        return
    try:
        button_5_display = ("Part identity: " + str(records[4].displayId) + "\n" + "Part description: " +
                            str(records[4].description))
    except ValueError:
        return
    try:
        button_6_display = ("Part identity: " + str(records[5].displayId) + "\n" + "Part description: " +
                            str(records[5].description))
    except ValueError:
        return
    try:
        button_7_display = ("Part identity: " + str(records[6].displayId) + "\n" + "Part description: " +
                            str(records[6].description))
    except ValueError:
        return
    try:
        button_8_display = ("Part identity: " + str(records[7].displayId) + "\n" + "Part description: " +
                            str(records[7].description))
    except ValueError:
        return
    try:
        button_9_display = ("Part identity: " + str(records[8].displayId) + "\n" + "Part description: " +
                            str(records[8].description))
    except ValueError:
        return
    try:
        button_10_display = ("Part identity: " + str(records[9].displayId) + "\n" + "Part description: " +
                             str(records[9].description))
    except ValueError:
        return


# Addition of queried parts to the lists used to create the GUI display of the design
def design_display_lists(part_uri):
    for roles in part_uri.roles:
        if "SO" in roles:
            design_roles.append(roles)
    design_identities.append(part_uri.displayId)
    design_descriptions.append(part_uri.description)
    GUI.create_description_button_design()


# Query submission
def query_submit(event):
    query_request = GUI.query_request_entry.get()
    part_search(query_request)
    try:
        GUI.part_choice_button_1()
    except AttributeError:
        return
    try:
        GUI.part_choice_button_2()
    except AttributeError:
        return
    try:
        GUI.part_choice_button_3()
    except AttributeError:
        return
    try:
        GUI.part_choice_button_4()
    except AttributeError:
        return
    try:
        GUI.part_choice_button_5()
    except AttributeError:
        return
    try:
        GUI.part_choice_button_6()
    except AttributeError:
        return
    try:
        GUI.part_choice_button_7()
    except AttributeError:
        return
    try:
        GUI.part_choice_button_8()
    except AttributeError:
        return
    try:
        GUI.part_choice_button_9()
    except AttributeError:
        return
    try:
        GUI.part_choice_button_10()
    except AttributeError:
        return



# Add query result 1 to doc
def query_to_doc_1(event):
    try:
        GUI.incompatible_part_label.pack_forget()
    except AttributeError:
        pass
    doc2 = Document()
    igem.pull(str(records[0]), doc2)
    GUI.clear_all_query()
    sub_components = 0
    part_cd = doc2.getComponentDefinition(str(records[0]))
    for component in part_cd.components:
        sub_components = sub_components + 1
    if str(records[0]) == "https://synbiohub.org/public/igem/BBa_B0015/1":
        terminator_cd = doc2.getComponentDefinition(str(records[0]))
        try:
            sub_components = []
            for component in terminator_cd.components:
                sub_components.append(component.definition)
            BBa_B0012_sequence = (doc2.getComponentDefinition(sub_components[0])).sequence.elements
            BBa_B0010_sequence = (doc2.getComponentDefinition(sub_components[1])).sequence.elements
            BBa_B0015 = ComponentDefinition("BBa_B0015")
            BBa_B0010 = ComponentDefinition("BBa_B0010")
            BBa_B0012 = ComponentDefinition("BBa_B0012")
            BBa_B0015.roles = SO_TERMINATOR
            BBa_B0010.roles = SO_TERMINATOR
            BBa_B0012.roles = SO_TERMINATOR
            doc.addComponentDefinition([BBa_B0015, BBa_B0010, BBa_B0012])
            BBa_B0015.description = "Double terminator BBa_B0010 + BBa_B0012"
            BBa_B0015.assemblePrimaryStructure([BBa_B0010, BBa_B0012])
            BBa_B0010.sequence = Sequence("BBa_B0010", str(BBa_B0010_sequence))
            BBa_B0012.sequence = Sequence("BBa_B0012", str(BBa_B0012_sequence))
            BBa_B0015_fixed = BBa_B0015.compile()
            component_definition_list.append("https://synbiohub.org/public/igem//ComponentDefinition/BBa_B0015/1")
            design_roles.append("http://identifiers.org/so/SO:0000141")
            design_identities.append("BBa_B0015")
            design_descriptions.append("Double terminator BBa_B0010 + BBa_B0012")
            GUI.display_assembled_design(design_roles)
            GUI.create_description_button_design()

        except RuntimeError:
            component_definition_list.append("https://synbiohub.org/public/igem//ComponentDefinition/BBa_B0015/1")
            design_roles.append("http://identifiers.org/so/SO:0000141")
            design_identities.append("BBa_B0015")
            design_descriptions.append("Double terminator BBa_B0010 + BBa_B0012")
            GUI.display_assembled_design(design_roles)
            GUI.create_description_button_design()

    else:
        global part_repeats
        part_repeats = 0
        if sub_components > 0:
            GUI.incompatible_part()
        else:
            for uri in component_definition_list:
                if str(records[0]) == str(uri):
                    part_repeats = part_repeats + 1
            if part_repeats == 0:
                igem.pull(str(records[0]), doc)
                component_definition_list.append(records[0])
                part_uri = doc2.getComponentDefinition(str(records[0]))
                design_display_lists(part_uri)
                GUI.display_assembled_design(design_roles)
                print("test1")
            else:
                component_definition_list.append(records[0])
                part_uri = doc2.getComponentDefinition(str(records[0]))
                design_display_lists(part_uri)
                GUI.display_assembled_design(design_roles)


# Add query result 2 to doc
def query_to_doc_2(event):
    try:
        GUI.incompatible_part_label.pack_forget()
    except AttributeError:
        pass
    doc2 = Document()
    igem.pull(str(records[1]), doc2)
    GUI.clear_all_query()
    sub_components = 0
    part_cd = doc2.getComponentDefinition(str(records[1]))
    for component in part_cd.components:
        sub_components = sub_components + 1
    if str(records[1]) == "https://synbiohub.org/public/igem/BBa_B0015/1":
        terminator_cd = doc2.getComponentDefinition(str(records[1]))
        try:
            sub_components = []
            for component in terminator_cd.components:
                sub_components.append(component.definition)
            BBa_B0012_sequence = (doc2.getComponentDefinition(sub_components[0])).sequence.elements
            BBa_B0010_sequence = (doc2.getComponentDefinition(sub_components[1])).sequence.elements
            BBa_B0015 = ComponentDefinition("BBa_B0015")
            BBa_B0010 = ComponentDefinition("BBa_B0010")
            BBa_B0012 = ComponentDefinition("BBa_B0012")
            BBa_B0015.roles = SO_TERMINATOR
            BBa_B0010.roles = SO_TERMINATOR
            BBa_B0012.roles = SO_TERMINATOR
            doc.addComponentDefinition([BBa_B0015, BBa_B0010, BBa_B0012])
            BBa_B0015.description = "Double terminator BBa_B0010 + BBa_B0012"
            BBa_B0015.assemblePrimaryStructure([BBa_B0010, BBa_B0012])
            BBa_B0010.sequence = Sequence("BBa_B0010", str(BBa_B0010_sequence))
            BBa_B0012.sequence = Sequence("BBa_B0012", str(BBa_B0012_sequence))
            BBa_B0015_fixed = BBa_B0015.compile()
            design_descriptions.append("Double terminator BBa_B0010 + BBa_B0012")
            component_definition_list.append("https://synbiohub.org/public/igem//ComponentDefinition/BBa_B0015/1")
            design_roles.append("http://identifiers.org/so/SO:0000141")
            design_identities.append("BBa_B0015")
            GUI.display_assembled_design(design_roles)
            GUI.create_description_button_design()

        except RuntimeError:
            component_definition_list.append("https://synbiohub.org/public/igem//ComponentDefinition/BBa_B0015/1")
            design_roles.append("http://identifiers.org/so/SO:0000141")
            design_identities.append("BBa_B0015")
            design_descriptions.append("Double terminator BBa_B0010 + BBa_B0012")
            GUI.display_assembled_design(design_roles)
            GUI.create_description_button_design()

    else:
        global part_repeats
        part_repeats = 0
        if sub_components > 0:
            GUI.incompatible_part()
        else:
            for uri in component_definition_list:
                if str(records[1]) == str(uri):
                    part_repeats = part_repeats + 1
            if part_repeats == 0:
                igem.pull(str(records[1]), doc)
                component_definition_list.append(records[1])
                part_uri = doc2.getComponentDefinition(str(records[1]))
                design_display_lists(part_uri)
                GUI.display_assembled_design(design_roles)
            else:
                component_definition_list.append(records[1])
                part_uri = doc2.getComponentDefinition(str(records[1]))
                design_display_lists(part_uri)
                GUI.display_assembled_design(design_roles)


# Add query result 3 to doc
def query_to_doc_3(event):
    try:
        GUI.incompatible_part_label.pack_forget()
    except AttributeError:
        pass
    doc2 = Document()
    igem.pull(str(records[2]), doc2)
    GUI.clear_all_query()
    sub_components = 0
    part_cd = doc2.getComponentDefinition(str(records[2]))
    for component in part_cd.components:
        sub_components = sub_components + 1
    if str(records[2]) == "https://synbiohub.org/public/igem/BBa_B0015/1":
        terminator_cd = doc2.getComponentDefinition(str(records[2]))
        try:
            sub_components = []
            for component in terminator_cd.components:
                sub_components.append(component.definition)
            BBa_B0012_sequence = (doc2.getComponentDefinition(sub_components[0])).sequence.elements
            BBa_B0010_sequence = (doc2.getComponentDefinition(sub_components[1])).sequence.elements
            BBa_B0015 = ComponentDefinition("BBa_B0015")
            BBa_B0010 = ComponentDefinition("BBa_B0010")
            BBa_B0012 = ComponentDefinition("BBa_B0012")
            BBa_B0015.roles = SO_TERMINATOR
            BBa_B0010.roles = SO_TERMINATOR
            BBa_B0012.roles = SO_TERMINATOR
            doc.addComponentDefinition([BBa_B0015, BBa_B0010, BBa_B0012])
            BBa_B0015.description = "Double terminator BBa_B0010 + BBa_B0012"
            BBa_B0015.assemblePrimaryStructure([BBa_B0010, BBa_B0012])
            BBa_B0010.sequence = Sequence("BBa_B0010", str(BBa_B0010_sequence))
            BBa_B0012.sequence = Sequence("BBa_B0012", str(BBa_B0012_sequence))
            BBa_B0015_fixed = BBa_B0015.compile()
            design_descriptions.append("Double terminator BBa_B0010 + BBa_B0012")
            component_definition_list.append("https://synbiohub.org/public/igem//ComponentDefinition/BBa_B0015/1")
            design_roles.append("http://identifiers.org/so/SO:0000141")
            design_identities.append("BBa_B0015")
            GUI.display_assembled_design(design_roles)
            GUI.create_description_button_design()

        except RuntimeError:
            component_definition_list.append("https://synbiohub.org/public/igem//ComponentDefinition/BBa_B0015/1")
            design_roles.append("http://identifiers.org/so/SO:0000141")
            design_identities.append("BBa_B0015")
            design_descriptions.append("Double terminator BBa_B0010 + BBa_B0012")
            GUI.display_assembled_design(design_roles)
            GUI.create_description_button_design()

    else:
        global part_repeats
        part_repeats = 0
        if sub_components > 0:
            GUI.incompatible_part()
        else:
            for uri in component_definition_list:
                if str(records[2]) == str(uri):
                    part_repeats = part_repeats + 1
            if part_repeats == 0:
                igem.pull(str(records[2]), doc)
                component_definition_list.append(records[2])
                part_uri = doc2.getComponentDefinition(str(records[2]))
                design_display_lists(part_uri)
                GUI.display_assembled_design(design_roles)
            else:
                component_definition_list.append(records[2])
                part_uri = doc2.getComponentDefinition(str(records[2]))
                design_display_lists(part_uri)
                GUI.display_assembled_design(design_roles)


# Add query result 4 to doc
def query_to_doc_4(event):
    try:
        GUI.incompatible_part_label.pack_forget()
    except AttributeError:
        pass
    doc2 = Document()
    igem.pull(str(records[3]), doc2)
    GUI.clear_all_query()
    sub_components = 0
    part_cd = doc2.getComponentDefinition(str(records[3]))
    for component in part_cd.components:
        sub_components = sub_components + 1
    if str(records[3]) == "https://synbiohub.org/public/igem/BBa_B0015/1":
        terminator_cd = doc2.getComponentDefinition(str(records[3]))
        try:
            sub_components = []
            for component in terminator_cd.components:
                sub_components.append(component.definition)
            BBa_B0012_sequence = (doc2.getComponentDefinition(sub_components[0])).sequence.elements
            BBa_B0010_sequence = (doc2.getComponentDefinition(sub_components[1])).sequence.elements
            BBa_B0015 = ComponentDefinition("BBa_B0015")
            BBa_B0010 = ComponentDefinition("BBa_B0010")
            BBa_B0012 = ComponentDefinition("BBa_B0012")
            BBa_B0015.roles = SO_TERMINATOR
            BBa_B0010.roles = SO_TERMINATOR
            BBa_B0012.roles = SO_TERMINATOR
            doc.addComponentDefinition([BBa_B0015, BBa_B0010, BBa_B0012])
            BBa_B0015.description = "Double terminator BBa_B0010 + BBa_B0012"
            BBa_B0015.assemblePrimaryStructure([BBa_B0010, BBa_B0012])
            BBa_B0010.sequence = Sequence("BBa_B0010", str(BBa_B0010_sequence))
            BBa_B0012.sequence = Sequence("BBa_B0012", str(BBa_B0012_sequence))
            BBa_B0015_fixed = BBa_B0015.compile()
            design_descriptions.append("Double terminator BBa_B0010 + BBa_B0012")
            component_definition_list.append("https://synbiohub.org/public/igem//ComponentDefinition/BBa_B0015/1")
            design_roles.append("http://identifiers.org/so/SO:0000141")
            design_identities.append("BBa_B0015")
            GUI.display_assembled_design(design_roles)
            GUI.create_description_button_design()

        except RuntimeError:
            component_definition_list.append("https://synbiohub.org/public/igem//ComponentDefinition/BBa_B0015/1")
            design_roles.append("http://identifiers.org/so/SO:0000141")
            design_identities.append("BBa_B0015")
            design_descriptions.append("Double terminator BBa_B0010 + BBa_B0012")
            GUI.display_assembled_design(design_roles)
            GUI.create_description_button_design()

    else:
        global part_repeats
        part_repeats = 0
        if sub_components > 0:
            GUI.incompatible_part()
        else:
            for uri in component_definition_list:
                if str(records[3]) == str(uri):
                    part_repeats = part_repeats + 1
            if part_repeats == 0:
                igem.pull(str(records[3]), doc)
                component_definition_list.append(records[3])
                part_uri = doc2.getComponentDefinition(str(records[3]))
                design_display_lists(part_uri)
                GUI.display_assembled_design(design_roles)
            else:
                component_definition_list.append(records[3])
                part_uri = doc2.getComponentDefinition(str(records[3]))
                design_display_lists(part_uri)
                GUI.display_assembled_design(design_roles)


# Add query result 5 to doc
def query_to_doc_5(event):
    try:
        GUI.incompatible_part_label.pack_forget()
    except AttributeError:
        pass
    doc2 = Document()
    igem.pull(str(records[4]), doc2)
    GUI.clear_all_query()
    sub_components = 0
    part_cd = doc2.getComponentDefinition(str(records[4]))
    for component in part_cd.components:
        sub_components = sub_components + 1
    if str(records[4]) == "https://synbiohub.org/public/igem/BBa_B0015/1":
        terminator_cd = doc2.getComponentDefinition(str(records[4]))
        try:
            sub_components = []
            for component in terminator_cd.components:
                sub_components.append(component.definition)
            BBa_B0012_sequence = (doc2.getComponentDefinition(sub_components[0])).sequence.elements
            BBa_B0010_sequence = (doc2.getComponentDefinition(sub_components[1])).sequence.elements
            BBa_B0015 = ComponentDefinition("BBa_B0015")
            BBa_B0010 = ComponentDefinition("BBa_B0010")
            BBa_B0012 = ComponentDefinition("BBa_B0012")
            BBa_B0015.roles = SO_TERMINATOR
            BBa_B0010.roles = SO_TERMINATOR
            BBa_B0012.roles = SO_TERMINATOR
            doc.addComponentDefinition([BBa_B0015, BBa_B0010, BBa_B0012])
            BBa_B0015.description = "Double terminator BBa_B0010 + BBa_B0012"
            BBa_B0015.assemblePrimaryStructure([BBa_B0010, BBa_B0012])
            BBa_B0010.sequence = Sequence("BBa_B0010", str(BBa_B0010_sequence))
            BBa_B0012.sequence = Sequence("BBa_B0012", str(BBa_B0012_sequence))
            BBa_B0015_fixed = BBa_B0015.compile()
            design_descriptions.append("Double terminator BBa_B0010 + BBa_B0012")
            component_definition_list.append("https://synbiohub.org/public/igem//ComponentDefinition/BBa_B0015/1")
            design_roles.append("http://identifiers.org/so/SO:0000141")
            design_identities.append("BBa_B0015")
            GUI.display_assembled_design(design_roles)
            GUI.create_description_button_design()

        except RuntimeError:
            component_definition_list.append("https://synbiohub.org/public/igem//ComponentDefinition/BBa_B0015/1")
            design_roles.append("http://identifiers.org/so/SO:0000141")
            design_identities.append("BBa_B0015")
            design_descriptions.append("Double terminator BBa_B0010 + BBa_B0012")
            GUI.display_assembled_design(design_roles)
            GUI.create_description_button_design()

    else:
        global part_repeats
        part_repeats = 0
        if sub_components > 0:
            GUI.incompatible_part()
        else:
            for uri in component_definition_list:
                if str(records[4]) == str(uri):
                    part_repeats = part_repeats + 1
            if part_repeats == 0:
                igem.pull(str(records[4]), doc)
                component_definition_list.append(records[4])
                part_uri = doc2.getComponentDefinition(str(records[4]))
                design_display_lists(part_uri)
                GUI.display_assembled_design(design_roles)
            else:
                component_definition_list.append(records[4])
                part_uri = doc2.getComponentDefinition(str(records[4]))
                design_display_lists(part_uri)
                GUI.display_assembled_design(design_roles)


# Add query result 6 to doc
def query_to_doc_6(event):
    try:
        GUI.incompatible_part_label.pack_forget()
    except AttributeError:
        pass
    doc2 = Document()
    igem.pull(str(records[5]), doc2)
    GUI.clear_all_query()
    sub_components = 0
    part_cd = doc2.getComponentDefinition(str(records[5]))
    for component in part_cd.components:
        sub_components = sub_components + 1
    if str(records[5]) == "https://synbiohub.org/public/igem/BBa_B0015/1":
        terminator_cd = doc2.getComponentDefinition(str(records[5]))
        try:
            sub_components = []
            for component in terminator_cd.components:
                sub_components.append(component.definition)
            BBa_B0012_sequence = (doc2.getComponentDefinition(sub_components[0])).sequence.elements
            BBa_B0010_sequence = (doc2.getComponentDefinition(sub_components[1])).sequence.elements
            BBa_B0015 = ComponentDefinition("BBa_B0015")
            BBa_B0010 = ComponentDefinition("BBa_B0010")
            BBa_B0012 = ComponentDefinition("BBa_B0012")
            BBa_B0015.roles = SO_TERMINATOR
            BBa_B0010.roles = SO_TERMINATOR
            BBa_B0012.roles = SO_TERMINATOR
            doc.addComponentDefinition([BBa_B0015, BBa_B0010, BBa_B0012])
            BBa_B0015.description = "Double terminator BBa_B0010 + BBa_B0012"
            BBa_B0015.assemblePrimaryStructure([BBa_B0010, BBa_B0012])
            BBa_B0010.sequence = Sequence("BBa_B0010", str(BBa_B0010_sequence))
            BBa_B0012.sequence = Sequence("BBa_B0012", str(BBa_B0012_sequence))
            BBa_B0015_fixed = BBa_B0015.compile()
            design_descriptions.append("Double terminator BBa_B0010 + BBa_B0012")
            component_definition_list.append("https://synbiohub.org/public/igem//ComponentDefinition/BBa_B0015/1")
            design_roles.append("http://identifiers.org/so/SO:0000141")
            design_identities.append("BBa_B0015")
            GUI.display_assembled_design(design_roles)
            GUI.create_description_button_design()

        except RuntimeError:
            component_definition_list.append("https://synbiohub.org/public/igem//ComponentDefinition/BBa_B0015/1")
            design_roles.append("http://identifiers.org/so/SO:0000141")
            design_identities.append("BBa_B0015")
            design_descriptions.append("Double terminator BBa_B0010 + BBa_B0012")
            GUI.display_assembled_design(design_roles)
            GUI.create_description_button_design()

    else:
        global part_repeats
        part_repeats = 0
        if sub_components > 0:
            GUI.incompatible_part()
        else:
            for uri in component_definition_list:
                if str(records[5]) == str(uri):
                    part_repeats = part_repeats + 1
            if part_repeats == 0:
                igem.pull(str(records[5]), doc)
                component_definition_list.append(records[5])
                part_uri = doc2.getComponentDefinition(str(records[5]))
                design_display_lists(part_uri)
                GUI.display_assembled_design(design_roles)
            else:
                component_definition_list.append(records[5])
                part_uri = doc2.getComponentDefinition(str(records[5]))
                design_display_lists(part_uri)
                GUI.display_assembled_design(design_roles)


# Add query result 7 to doc
def query_to_doc_7(event):
    try:
        GUI.incompatible_part_label.pack_forget()
    except AttributeError:
        pass
    doc2 = Document()
    igem.pull(str(records[6]), doc2)
    GUI.clear_all_query()
    sub_components = 0
    part_cd = doc2.getComponentDefinition(str(records[6]))
    for component in part_cd.components:
        sub_components = sub_components + 1
    if str(records[6]) == "https://synbiohub.org/public/igem/BBa_B0015/1":
        terminator_cd = doc2.getComponentDefinition(str(records[6]))
        try:
            sub_components = []
            for component in terminator_cd.components:
                sub_components.append(component.definition)
            BBa_B0012_sequence = (doc2.getComponentDefinition(sub_components[0])).sequence.elements
            BBa_B0010_sequence = (doc2.getComponentDefinition(sub_components[1])).sequence.elements
            BBa_B0015 = ComponentDefinition("BBa_B0015")
            BBa_B0010 = ComponentDefinition("BBa_B0010")
            BBa_B0012 = ComponentDefinition("BBa_B0012")
            BBa_B0015.roles = SO_TERMINATOR
            BBa_B0010.roles = SO_TERMINATOR
            BBa_B0012.roles = SO_TERMINATOR
            doc.addComponentDefinition([BBa_B0015, BBa_B0010, BBa_B0012])
            BBa_B0015.description = "Double terminator BBa_B0010 + BBa_B0012"
            BBa_B0015.assemblePrimaryStructure([BBa_B0010, BBa_B0012])
            BBa_B0010.sequence = Sequence("BBa_B0010", str(BBa_B0010_sequence))
            BBa_B0012.sequence = Sequence("BBa_B0012", str(BBa_B0012_sequence))
            BBa_B0015_fixed = BBa_B0015.compile()
            design_descriptions.append("Double terminator BBa_B0010 + BBa_B0012")
            component_definition_list.append("https://synbiohub.org/public/igem//ComponentDefinition/BBa_B0015/1")
            design_roles.append("http://identifiers.org/so/SO:0000141")
            design_identities.append("BBa_B0015")
            GUI.display_assembled_design(design_roles)
            GUI.create_description_button_design()

        except RuntimeError:
            component_definition_list.append("https://synbiohub.org/public/igem//ComponentDefinition/BBa_B0015/1")
            design_roles.append("http://identifiers.org/so/SO:0000141")
            design_identities.append("BBa_B0015")
            design_descriptions.append("Double terminator BBa_B0010 + BBa_B0012")
            GUI.display_assembled_design(design_roles)
            GUI.create_description_button_design()

    else:
        global part_repeats
        part_repeats = 0
        if sub_components > 0:
            GUI.incompatible_part()
        else:
            for uri in component_definition_list:
                if str(records[6]) == str(uri):
                    part_repeats = part_repeats + 1
            if part_repeats == 0:
                igem.pull(str(records[6]), doc)
                component_definition_list.append(records[6])
                part_uri = doc2.getComponentDefinition(str(records[6]))
                design_display_lists(part_uri)
                GUI.display_assembled_design(design_roles)
            else:
                component_definition_list.append(records[6])
                part_uri = doc2.getComponentDefinition(str(records[6]))
                design_display_lists(part_uri)
                GUI.display_assembled_design(design_roles)


# Add query result 8 to doc
def query_to_doc_8(event):
    try:
        GUI.incompatible_part_label.pack_forget()
    except AttributeError:
        pass
    doc2 = Document()
    igem.pull(str(records[7]), doc2)
    GUI.clear_all_query()
    sub_components = 0
    part_cd = doc2.getComponentDefinition(str(records[7]))
    for component in part_cd.components:
        sub_components = sub_components + 1
    if str(records[7]) == "https://synbiohub.org/public/igem/BBa_B0015/1":
        terminator_cd = doc2.getComponentDefinition(str(records[7]))
        try:
            sub_components = []
            for component in terminator_cd.components:
                sub_components.append(component.definition)
            BBa_B0012_sequence = (doc2.getComponentDefinition(sub_components[0])).sequence.elements
            BBa_B0010_sequence = (doc2.getComponentDefinition(sub_components[1])).sequence.elements
            BBa_B0015 = ComponentDefinition("BBa_B0015")
            BBa_B0010 = ComponentDefinition("BBa_B0010")
            BBa_B0012 = ComponentDefinition("BBa_B0012")
            BBa_B0015.roles = SO_TERMINATOR
            BBa_B0010.roles = SO_TERMINATOR
            BBa_B0012.roles = SO_TERMINATOR
            doc.addComponentDefinition([BBa_B0015, BBa_B0010, BBa_B0012])
            BBa_B0015.description = "Double terminator BBa_B0010 + BBa_B0012"
            BBa_B0015.assemblePrimaryStructure([BBa_B0010, BBa_B0012])
            BBa_B0010.sequence = Sequence("BBa_B0010", str(BBa_B0010_sequence))
            BBa_B0012.sequence = Sequence("BBa_B0012", str(BBa_B0012_sequence))
            BBa_B0015_fixed = BBa_B0015.compile()
            design_descriptions.append("Double terminator BBa_B0010 + BBa_B0012")
            component_definition_list.append("https://synbiohub.org/public/igem//ComponentDefinition/BBa_B0015/1")
            design_roles.append("http://identifiers.org/so/SO:0000141")
            design_identities.append("BBa_B0015")
            GUI.display_assembled_design(design_roles)
            GUI.create_description_button_design()

        except RuntimeError:
            component_definition_list.append("https://synbiohub.org/public/igem//ComponentDefinition/BBa_B0015/1")
            design_roles.append("http://identifiers.org/so/SO:0000141")
            design_identities.append("BBa_B0015")
            design_descriptions.append("Double terminator BBa_B0010 + BBa_B0012")
            GUI.display_assembled_design(design_roles)
            GUI.create_description_button_design()

    else:
        global part_repeats
        part_repeats = 0
        if sub_components > 0:
            GUI.incompatible_part()
        else:
            for uri in component_definition_list:
                if str(records[7]) == str(uri):
                    part_repeats = part_repeats + 1
            if part_repeats == 0:
                igem.pull(str(records[7]), doc)
                component_definition_list.append(records[7])
                part_uri = doc2.getComponentDefinition(str(records[7]))
                design_display_lists(part_uri)
                GUI.display_assembled_design(design_roles)
            else:
                component_definition_list.append(records[7])
                part_uri = doc2.getComponentDefinition(str(records[7]))
                design_display_lists(part_uri)
                GUI.display_assembled_design(design_roles)


# Add query result 9 to doc
def query_to_doc_9(event):
    try:
        GUI.incompatible_part_label.pack_forget()
    except AttributeError:
        pass
    doc2 = Document()
    igem.pull(str(records[8]), doc2)
    GUI.clear_all_query()
    sub_components = 0
    part_cd = doc2.getComponentDefinition(str(records[8]))
    for component in part_cd.components:
        sub_components = sub_components + 1
    if str(records[8]) == "https://synbiohub.org/public/igem/BBa_B0015/1":
        terminator_cd = doc2.getComponentDefinition(str(records[8]))
        try:
            sub_components = []
            for component in terminator_cd.components:
                sub_components.append(component.definition)
            BBa_B0012_sequence = (doc2.getComponentDefinition(sub_components[0])).sequence.elements
            BBa_B0010_sequence = (doc2.getComponentDefinition(sub_components[1])).sequence.elements
            BBa_B0015 = ComponentDefinition("BBa_B0015")
            BBa_B0010 = ComponentDefinition("BBa_B0010")
            BBa_B0012 = ComponentDefinition("BBa_B0012")
            BBa_B0015.roles = SO_TERMINATOR
            BBa_B0010.roles = SO_TERMINATOR
            BBa_B0012.roles = SO_TERMINATOR
            doc.addComponentDefinition([BBa_B0015, BBa_B0010, BBa_B0012])
            BBa_B0015.description = "Double terminator BBa_B0010 + BBa_B0012"
            BBa_B0015.assemblePrimaryStructure([BBa_B0010, BBa_B0012])
            BBa_B0010.sequence = Sequence("BBa_B0010", str(BBa_B0010_sequence))
            BBa_B0012.sequence = Sequence("BBa_B0012", str(BBa_B0012_sequence))
            BBa_B0015_fixed = BBa_B0015.compile()
            design_descriptions.append("Double terminator BBa_B0010 + BBa_B0012")
            component_definition_list.append("https://synbiohub.org/public/igem//ComponentDefinition/BBa_B0015/1")
            design_roles.append("http://identifiers.org/so/SO:0000141")
            design_identities.append("BBa_B0015")
            GUI.display_assembled_design(design_roles)
            GUI.create_description_button_design()

        except RuntimeError:
            component_definition_list.append("https://synbiohub.org/public/igem//ComponentDefinition/BBa_B0015/1")
            design_roles.append("http://identifiers.org/so/SO:0000141")
            design_identities.append("BBa_B0015")
            design_descriptions.append("Double terminator BBa_B0010 + BBa_B0012")
            GUI.display_assembled_design(design_roles)
            GUI.create_description_button_design()

    else:
        global part_repeats
        part_repeats = 0
        if sub_components > 0:
            GUI.incompatible_part()
        else:
            for uri in component_definition_list:
                if str(records[8]) == str(uri):
                    part_repeats = part_repeats + 1
            if part_repeats == 0:
                igem.pull(str(records[8]), doc)
                component_definition_list.append(records[8])
                part_uri = doc2.getComponentDefinition(str(records[8]))
                design_display_lists(part_uri)
                GUI.display_assembled_design(design_roles)
            else:
                component_definition_list.append(records[8])
                part_uri = doc2.getComponentDefinition(str(records[8]))
                design_display_lists(part_uri)
                GUI.display_assembled_design(design_roles)


# Add query result 10 to doc
def query_to_doc_10(event):
    try:
        GUI.incompatible_part_label.pack_forget()
    except AttributeError:
        pass
    doc2 = Document()
    igem.pull(str(records[9]), doc2)
    GUI.clear_all_query()
    sub_components = 0
    part_cd = doc2.getComponentDefinition(str(records[9]))
    for component in part_cd.components:
        sub_components = sub_components + 1
    if str(records[9]) == "https://synbiohub.org/public/igem/BBa_B0015/1":
        terminator_cd = doc2.getComponentDefinition(str(records[9]))
        try:
            sub_components = []
            for component in terminator_cd.components:
                sub_components.append(component.definition)
            BBa_B0012_sequence = (doc2.getComponentDefinition(sub_components[0])).sequence.elements
            BBa_B0010_sequence = (doc2.getComponentDefinition(sub_components[1])).sequence.elements
            BBa_B0015 = ComponentDefinition("BBa_B0015")
            BBa_B0010 = ComponentDefinition("BBa_B0010")
            BBa_B0012 = ComponentDefinition("BBa_B0012")
            BBa_B0015.roles = SO_TERMINATOR
            BBa_B0010.roles = SO_TERMINATOR
            BBa_B0012.roles = SO_TERMINATOR
            doc.addComponentDefinition([BBa_B0015, BBa_B0010, BBa_B0012])
            BBa_B0015.description = "Double terminator BBa_B0010 + BBa_B0012"
            BBa_B0015.assemblePrimaryStructure([BBa_B0010, BBa_B0012])
            BBa_B0010.sequence = Sequence("BBa_B0010", str(BBa_B0010_sequence))
            BBa_B0012.sequence = Sequence("BBa_B0012", str(BBa_B0012_sequence))
            BBa_B0015_fixed = BBa_B0015.compile()
            design_descriptions.append("Double terminator BBa_B0010 + BBa_B0012")
            component_definition_list.append("https://synbiohub.org/public/igem//ComponentDefinition/BBa_B0015/1")
            design_roles.append("http://identifiers.org/so/SO:0000141")
            design_identities.append("BBa_B0015")
            GUI.display_assembled_design(design_roles)
            GUI.create_description_button_design()

        except RuntimeError:
            component_definition_list.append("https://synbiohub.org/public/igem//ComponentDefinition/BBa_B0015/1")
            design_roles.append("http://identifiers.org/so/SO:0000141")
            design_identities.append("BBa_B0015")
            design_descriptions.append("Double terminator BBa_B0010 + BBa_B0012")
            GUI.display_assembled_design(design_roles)
            GUI.create_description_button_design()

    else:
        global part_repeats
        part_repeats = 0
        if sub_components > 0:
            GUI.incompatible_part()
        else:
            for uri in component_definition_list:
                if str(records[9]) == str(uri):
                    part_repeats = part_repeats + 1
            if part_repeats == 0:
                igem.pull(str(records[9]), doc)
                component_definition_list.append(records[9])
                part_uri = doc2.getComponentDefinition(str(records[9]))
                design_display_lists(part_uri)
                GUI.display_assembled_design(design_roles)
            else:
                component_definition_list.append(records[9])
                part_uri = doc2.getComponentDefinition(str(records[9]))
                design_display_lists(part_uri)
                GUI.display_assembled_design(design_roles)

# Assembly of selected parts into a single genetic design
def design_assembly(event):
    try:
        GUI.successful_assembly_label.pack_forget()
    except AttributeError:
        pass
    try:
        GUI.failed_assembly_label.pack_forget()
    except AttributeError:
        pass
    try:
        design_name = (str(GUI.design_name_entry.get())).replace(" ", "_")
        assembled_design = ComponentDefinition(design_name)
        doc.addComponentDefinition(assembled_design)
        temp_list = []
        for component in component_definition_list:
            part_cd = doc.getComponentDefinition(str(component))
            temp_list.append(part_cd)

        assembled_design.assemblePrimaryStructure(temp_list)
        compile_design = assembled_design.compile()
        print(assembled_design.getPrimaryStructure())
        result = doc.write(design_name + ".xml")
        print(result)
        component_definition_list.clear()
        clear_all_genetic_design()
        GUI.successful_assembly()
    except LookupError:
        GUI.failed_assembly()


# Wipes the GUI, and empties all variables, lists, and documents
def clear_all_genetic_design():
    print("placeholder")
