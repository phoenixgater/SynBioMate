# Import libraries
from sbol import *

# Import scripts
import Main
import GUI

# Specifying SynBioHub part repository for query
igem = PartShop('https://synbiohub.org/public/igem')

# Global variables (Not all)
component_definition_list = []


# Assemble from file
def add_file_part():
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
            Main.doc.addComponentDefinition([BBa_B0015, BBa_B0010, BBa_B0012])
            BBa_B0015.assemblePrimaryStructure([BBa_B0010, BBa_B0012])
            BBa_B0010.sequence = Sequence("BBa_B0010", str(part1_uri.sequence.elements))
            BBa_B0012.sequence = Sequence("BBa_B0012", str(part2_uri.sequence.elements))
            BBa_B0015_fixed = BBa_B0015.compile()
            for obj in Main.doc:
                temp_list_2.append(obj)
            component_definition_list.append(temp_list_2[0])
        except RuntimeError:
            for obj in Main.doc:
                temp_list_2.append(obj)
            component_definition_list.append(temp_list_2[0])
    else:
        for components in doc2.componentDefinitions:
            component_definition_list.append(str(components))
            Main.doc.append(str(GUI.imported_part))



# SynBioHub part query
def part_search(query):
    query2 = query.replace(" ", "_")
    global records
    records = igem.search(query2, SBOL_COMPONENT_DEFINITION, 0, 10)
    print(records)


# Query submission
def query_submit(event):
    query_request = GUI.query_request_entry.get()
    part_search(query_request)
    GUI.part_choice_button_1()
    GUI.part_choice_button_2()
    GUI.part_choice_button_3()
    GUI.part_choice_button_4()
    GUI.part_choice_button_5()
    GUI.part_choice_button_6()
    GUI.part_choice_button_7()
    GUI.part_choice_button_8()
    GUI.part_choice_button_9()
    GUI.part_choice_button_10()


# query to doc, display of items in doc in GUI, clearing of part list in GUI, raise part counter, Store URI in variable
def query_to_doc_1(event):
    doc2 = Document()
    igem.pull(str(records[0]), doc2)
    GUI.clear_all_query()
    if str(records[0]) == "https://synbiohub.org/public/igem/BBa_B0015/1":
        terminator_cd = doc2.getComponentDefinition(str(records[0]))
        try:
            sub_components = []
            for component in terminator_cd.components:
                sub_components.append(component.definition)
            BBa_B0012_sequence = (doc2.getComponentDefinition(sub_components[0])).sequence.elements
            BBa_B0010_sequence = (doc2.getComponentDefinition(sub_components[1])).sequence.elements
            print(str(BBa_B0012_sequence))
            BBa_B0015 = ComponentDefinition("BBa_B0015")
            BBa_B0010 = ComponentDefinition("BBa_B0010")
            BBa_B0012 = ComponentDefinition("BBa_B0012")
            BBa_B0015.roles = SO_TERMINATOR
            BBa_B0010.roles = SO_TERMINATOR
            BBa_B0012.roles = SO_TERMINATOR
            Main.doc.addComponentDefinition([BBa_B0015, BBa_B0010, BBa_B0012])
            BBa_B0015.assemblePrimaryStructure([BBa_B0010, BBa_B0012])
            BBa_B0010.sequence = Sequence("BBa_B0010", str(BBa_B0010_sequence))
            BBa_B0012.sequence = Sequence("BBa_B0012", str(BBa_B0012_sequence))
            BBa_B0015_fixed = BBa_B0015.compile()
            component_definition_list.append("https://synbiohub.org/public/igem//ComponentDefinition/BBa_B0015/1")

        except RuntimeError:
            component_definition_list.append("https://synbiohub.org/public/igem//ComponentDefinition/BBa_B0015/1")

    else:
        igem.pull(str(records[0]), Main.doc)
        component_definition_list.append(records[0])

def query_to_doc_2(event):
    doc2 = Document()
    igem.pull(str(records[1]), doc2)
    GUI.clear_all_query()
    if str(records[1]) == "https://synbiohub.org/public/igem/BBa_B0015/1":
        terminator_cd = doc2.getComponentDefinition(str(records[1]))
        try:
            sub_components = []
            for component in terminator_cd.components:
                sub_components.append(component.definition)
            BBa_B0012_sequence = (doc2.getComponentDefinition(sub_components[0])).sequence.elements
            BBa_B0010_sequence = (doc2.getComponentDefinition(sub_components[1])).sequence.elements
            print(str(BBa_B0012_sequence))
            BBa_B0015 = ComponentDefinition("BBa_B0015")
            BBa_B0010 = ComponentDefinition("BBa_B0010")
            BBa_B0012 = ComponentDefinition("BBa_B0012")
            BBa_B0015.roles = SO_TERMINATOR
            BBa_B0010.roles = SO_TERMINATOR
            BBa_B0012.roles = SO_TERMINATOR
            Main.doc.addComponentDefinition([BBa_B0015, BBa_B0010, BBa_B0012])
            BBa_B0015.assemblePrimaryStructure([BBa_B0010, BBa_B0012])
            BBa_B0010.sequence = Sequence("BBa_B0010", str(BBa_B0010_sequence))
            BBa_B0012.sequence = Sequence("BBa_B0012", str(BBa_B0012_sequence))
            BBa_B0015_fixed = BBa_B0015.compile()
            component_definition_list.append("https://synbiohub.org/public/igem//ComponentDefinition/BBa_B0015/1")

        except RuntimeError:
            component_definition_list.append("https://synbiohub.org/public/igem//ComponentDefinition/BBa_B0015/1")

    else:
        igem.pull(str(records[1]), Main.doc)
        component_definition_list.append(records[1])


def query_to_doc_3(event):
    doc2 = Document()
    igem.pull(str(records[2]), doc2)
    GUI.clear_all_query()
    if str(records[2]) == "https://synbiohub.org/public/igem/BBa_B0015/1":
        terminator_cd = doc2.getComponentDefinition(str(records[2]))
        try:
            sub_components = []
            for component in terminator_cd.components:
                sub_components.append(component.definition)
            BBa_B0012_sequence = (doc2.getComponentDefinition(sub_components[0])).sequence.elements
            BBa_B0010_sequence = (doc2.getComponentDefinition(sub_components[1])).sequence.elements
            print(str(BBa_B0012_sequence))
            BBa_B0015 = ComponentDefinition("BBa_B0015")
            BBa_B0010 = ComponentDefinition("BBa_B0010")
            BBa_B0012 = ComponentDefinition("BBa_B0012")
            BBa_B0015.roles = SO_TERMINATOR
            BBa_B0010.roles = SO_TERMINATOR
            BBa_B0012.roles = SO_TERMINATOR
            Main.doc.addComponentDefinition([BBa_B0015, BBa_B0010, BBa_B0012])
            BBa_B0015.assemblePrimaryStructure([BBa_B0010, BBa_B0012])
            BBa_B0010.sequence = Sequence("BBa_B0010", str(BBa_B0010_sequence))
            BBa_B0012.sequence = Sequence("BBa_B0012", str(BBa_B0012_sequence))
            BBa_B0015_fixed = BBa_B0015.compile()
            component_definition_list.append("https://synbiohub.org/public/igem//ComponentDefinition/BBa_B0015/1")

        except RuntimeError:
            component_definition_list.append("https://synbiohub.org/public/igem//ComponentDefinition/BBa_B0015/1")

    else:
        igem.pull(str(records[2]), Main.doc)
        component_definition_list.append(records[2])

def query_to_doc_4(event):
    doc2 = Document()
    igem.pull(str(records[3]), doc2)
    GUI.clear_all_query()
    if str(records[3]) == "https://synbiohub.org/public/igem/BBa_B0015/1":
        terminator_cd = doc2.getComponentDefinition(str(records[3]))
        try:
            sub_components = []
            for component in terminator_cd.components:
                sub_components.append(component.definition)
            BBa_B0012_sequence = (doc2.getComponentDefinition(sub_components[0])).sequence.elements
            BBa_B0010_sequence = (doc2.getComponentDefinition(sub_components[1])).sequence.elements
            print(str(BBa_B0012_sequence))
            BBa_B0015 = ComponentDefinition("BBa_B0015")
            BBa_B0010 = ComponentDefinition("BBa_B0010")
            BBa_B0012 = ComponentDefinition("BBa_B0012")
            BBa_B0015.roles = SO_TERMINATOR
            BBa_B0010.roles = SO_TERMINATOR
            BBa_B0012.roles = SO_TERMINATOR
            Main.doc.addComponentDefinition([BBa_B0015, BBa_B0010, BBa_B0012])
            BBa_B0015.assemblePrimaryStructure([BBa_B0010, BBa_B0012])
            BBa_B0010.sequence = Sequence("BBa_B0010", str(BBa_B0010_sequence))
            BBa_B0012.sequence = Sequence("BBa_B0012", str(BBa_B0012_sequence))
            BBa_B0015_fixed = BBa_B0015.compile()
            component_definition_list.append("https://synbiohub.org/public/igem//ComponentDefinition/BBa_B0015/1")

        except RuntimeError:
            component_definition_list.append("https://synbiohub.org/public/igem//ComponentDefinition/BBa_B0015/1")

    else:
        igem.pull(str(records[3]), Main.doc)
        component_definition_list.append(records[3])

    '''for components in doc2.componentDefinitions:
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
                Main.doc.addComponentDefinition([BBa_B0015, BBa_B0010, BBa_B0012])
                BBa_B0015.assemblePrimaryStructure([BBa_B0010, BBa_B0012])
                BBa_B0010.sequence = Sequence("BBa_B0010", str(part1_uri.sequence.elements))
                BBa_B0012.sequence = Sequence("BBa_B0012", str(part2_uri.sequence.elements))
                BBa_B0015_fixed = BBa_B0015.compile()
                for obj in Main.doc:
                    temp_list_2.append(obj)
                component_definition_list.append(temp_list_2[0])
            except RuntimeError:
                for obj in Main.doc:
                    temp_list_2.append(obj)
                component_definition_list.append(temp_list_2[0])
        else:
            for components in doc2.componentDefinitions:
                component_definition_list.append(str(components))
                igem.pull(str(records[3]), Main.doc)'''


def query_to_doc_5(event):
    doc2 = Document()
    igem.pull(str(records[4]), doc2)
    GUI.clear_all_query()
    if str(records[4]) == "https://synbiohub.org/public/igem/BBa_B0015/1":
        terminator_cd = doc2.getComponentDefinition(str(records[4]))
        try:
            sub_components = []
            for component in terminator_cd.components:
                sub_components.append(component.definition)
            BBa_B0012_sequence = (doc2.getComponentDefinition(sub_components[0])).sequence.elements
            BBa_B0010_sequence = (doc2.getComponentDefinition(sub_components[1])).sequence.elements
            print(str(BBa_B0012_sequence))
            BBa_B0015 = ComponentDefinition("BBa_B0015")
            BBa_B0010 = ComponentDefinition("BBa_B0010")
            BBa_B0012 = ComponentDefinition("BBa_B0012")
            BBa_B0015.roles = SO_TERMINATOR
            BBa_B0010.roles = SO_TERMINATOR
            BBa_B0012.roles = SO_TERMINATOR
            Main.doc.addComponentDefinition([BBa_B0015, BBa_B0010, BBa_B0012])
            BBa_B0015.assemblePrimaryStructure([BBa_B0010, BBa_B0012])
            BBa_B0010.sequence = Sequence("BBa_B0010", str(BBa_B0010_sequence))
            BBa_B0012.sequence = Sequence("BBa_B0012", str(BBa_B0012_sequence))
            BBa_B0015_fixed = BBa_B0015.compile()
            component_definition_list.append("https://synbiohub.org/public/igem//ComponentDefinition/BBa_B0015/1")

        except RuntimeError:
            component_definition_list.append("https://synbiohub.org/public/igem//ComponentDefinition/BBa_B0015/1")

    else:
        igem.pull(str(records[4]), Main.doc)
        component_definition_list.append(records[4])

def query_to_doc_6(event):
    doc2 = Document()
    igem.pull(str(records[5]), doc2)
    GUI.clear_all_query()
    if str(records[5]) == "https://synbiohub.org/public/igem/BBa_B0015/1":
        terminator_cd = doc2.getComponentDefinition(str(records[5]))
        try:
            sub_components = []
            for component in terminator_cd.components:
                sub_components.append(component.definition)
            BBa_B0012_sequence = (doc2.getComponentDefinition(sub_components[0])).sequence.elements
            BBa_B0010_sequence = (doc2.getComponentDefinition(sub_components[1])).sequence.elements
            print(str(BBa_B0012_sequence))
            BBa_B0015 = ComponentDefinition("BBa_B0015")
            BBa_B0010 = ComponentDefinition("BBa_B0010")
            BBa_B0012 = ComponentDefinition("BBa_B0012")
            BBa_B0015.roles = SO_TERMINATOR
            BBa_B0010.roles = SO_TERMINATOR
            BBa_B0012.roles = SO_TERMINATOR
            Main.doc.addComponentDefinition([BBa_B0015, BBa_B0010, BBa_B0012])
            BBa_B0015.assemblePrimaryStructure([BBa_B0010, BBa_B0012])
            BBa_B0010.sequence = Sequence("BBa_B0010", str(BBa_B0010_sequence))
            BBa_B0012.sequence = Sequence("BBa_B0012", str(BBa_B0012_sequence))
            BBa_B0015_fixed = BBa_B0015.compile()
            component_definition_list.append("https://synbiohub.org/public/igem//ComponentDefinition/BBa_B0015/1")

        except RuntimeError:
            component_definition_list.append("https://synbiohub.org/public/igem//ComponentDefinition/BBa_B0015/1")

    else:
        igem.pull(str(records[5]), Main.doc)
        component_definition_list.append(records[5])

def query_to_doc_7(event):
    doc2 = Document()
    igem.pull(str(records[6]), doc2)
    GUI.clear_all_query()
    if str(records[6]) == "https://synbiohub.org/public/igem/BBa_B0015/1":
        terminator_cd = doc2.getComponentDefinition(str(records[6]))
        try:
            sub_components = []
            for component in terminator_cd.components:
                sub_components.append(component.definition)
            BBa_B0012_sequence = (doc2.getComponentDefinition(sub_components[0])).sequence.elements
            BBa_B0010_sequence = (doc2.getComponentDefinition(sub_components[1])).sequence.elements
            print(str(BBa_B0012_sequence))
            BBa_B0015 = ComponentDefinition("BBa_B0015")
            BBa_B0010 = ComponentDefinition("BBa_B0010")
            BBa_B0012 = ComponentDefinition("BBa_B0012")
            BBa_B0015.roles = SO_TERMINATOR
            BBa_B0010.roles = SO_TERMINATOR
            BBa_B0012.roles = SO_TERMINATOR
            Main.doc.addComponentDefinition([BBa_B0015, BBa_B0010, BBa_B0012])
            BBa_B0015.assemblePrimaryStructure([BBa_B0010, BBa_B0012])
            BBa_B0010.sequence = Sequence("BBa_B0010", str(BBa_B0010_sequence))
            BBa_B0012.sequence = Sequence("BBa_B0012", str(BBa_B0012_sequence))
            BBa_B0015_fixed = BBa_B0015.compile()
            component_definition_list.append("https://synbiohub.org/public/igem//ComponentDefinition/BBa_B0015/1")

        except RuntimeError:
            component_definition_list.append("https://synbiohub.org/public/igem//ComponentDefinition/BBa_B0015/1")

    else:
        igem.pull(str(records[6]), Main.doc)
        component_definition_list.append(records[6])


def query_to_doc_8(event):
    doc2 = Document()
    igem.pull(str(records[7]), doc2)
    GUI.clear_all_query()
    if str(records[7]) == "https://synbiohub.org/public/igem/BBa_B0015/1":
        terminator_cd = doc2.getComponentDefinition(str(records[7]))
        try:
            sub_components = []
            for component in terminator_cd.components:
                sub_components.append(component.definition)
            BBa_B0012_sequence = (doc2.getComponentDefinition(sub_components[0])).sequence.elements
            BBa_B0010_sequence = (doc2.getComponentDefinition(sub_components[1])).sequence.elements
            print(str(BBa_B0012_sequence))
            BBa_B0015 = ComponentDefinition("BBa_B0015")
            BBa_B0010 = ComponentDefinition("BBa_B0010")
            BBa_B0012 = ComponentDefinition("BBa_B0012")
            BBa_B0015.roles = SO_TERMINATOR
            BBa_B0010.roles = SO_TERMINATOR
            BBa_B0012.roles = SO_TERMINATOR
            Main.doc.addComponentDefinition([BBa_B0015, BBa_B0010, BBa_B0012])
            BBa_B0015.assemblePrimaryStructure([BBa_B0010, BBa_B0012])
            BBa_B0010.sequence = Sequence("BBa_B0010", str(BBa_B0010_sequence))
            BBa_B0012.sequence = Sequence("BBa_B0012", str(BBa_B0012_sequence))
            BBa_B0015_fixed = BBa_B0015.compile()
            component_definition_list.append("https://synbiohub.org/public/igem//ComponentDefinition/BBa_B0015/1")

        except RuntimeError:
            component_definition_list.append("https://synbiohub.org/public/igem//ComponentDefinition/BBa_B0015/1")

    else:
        igem.pull(str(records[7]), Main.doc)
        component_definition_list.append(records[7])


def query_to_doc_9(event):
    doc2 = Document()
    igem.pull(str(records[8]), doc2)
    GUI.clear_all_query()
    if str(records[8]) == "https://synbiohub.org/public/igem/BBa_B0015/1":
        terminator_cd = doc2.getComponentDefinition(str(records[8]))
        try:
            sub_components = []
            for component in terminator_cd.components:
                sub_components.append(component.definition)
            BBa_B0012_sequence = (doc2.getComponentDefinition(sub_components[0])).sequence.elements
            BBa_B0010_sequence = (doc2.getComponentDefinition(sub_components[1])).sequence.elements
            print(str(BBa_B0012_sequence))
            BBa_B0015 = ComponentDefinition("BBa_B0015")
            BBa_B0010 = ComponentDefinition("BBa_B0010")
            BBa_B0012 = ComponentDefinition("BBa_B0012")
            BBa_B0015.roles = SO_TERMINATOR
            BBa_B0010.roles = SO_TERMINATOR
            BBa_B0012.roles = SO_TERMINATOR
            Main.doc.addComponentDefinition([BBa_B0015, BBa_B0010, BBa_B0012])
            BBa_B0015.assemblePrimaryStructure([BBa_B0010, BBa_B0012])
            BBa_B0010.sequence = Sequence("BBa_B0010", str(BBa_B0010_sequence))
            BBa_B0012.sequence = Sequence("BBa_B0012", str(BBa_B0012_sequence))
            BBa_B0015_fixed = BBa_B0015.compile()
            component_definition_list.append("https://synbiohub.org/public/igem//ComponentDefinition/BBa_B0015/1")

        except RuntimeError:
            component_definition_list.append("https://synbiohub.org/public/igem//ComponentDefinition/BBa_B0015/1")

    else:
        igem.pull(str(records[8]), Main.doc)
        component_definition_list.append(records[8])


def query_to_doc_10(event):
    doc2 = Document()
    igem.pull(str(records[9]), doc2)
    GUI.clear_all_query()
    if str(records[9]) == "https://synbiohub.org/public/igem/BBa_B0015/1":
        terminator_cd = doc2.getComponentDefinition(str(records[9]))
        try:
            sub_components = []
            for component in terminator_cd.components:
                sub_components.append(component.definition)
            BBa_B0012_sequence = (doc2.getComponentDefinition(sub_components[0])).sequence.elements
            BBa_B0010_sequence = (doc2.getComponentDefinition(sub_components[1])).sequence.elements
            print(str(BBa_B0012_sequence))
            BBa_B0015 = ComponentDefinition("BBa_B0015")
            BBa_B0010 = ComponentDefinition("BBa_B0010")
            BBa_B0012 = ComponentDefinition("BBa_B0012")
            BBa_B0015.roles = SO_TERMINATOR
            BBa_B0010.roles = SO_TERMINATOR
            BBa_B0012.roles = SO_TERMINATOR
            Main.doc.addComponentDefinition([BBa_B0015, BBa_B0010, BBa_B0012])
            BBa_B0015.assemblePrimaryStructure([BBa_B0010, BBa_B0012])
            BBa_B0010.sequence = Sequence("BBa_B0010", str(BBa_B0010_sequence))
            BBa_B0012.sequence = Sequence("BBa_B0012", str(BBa_B0012_sequence))
            BBa_B0015_fixed = BBa_B0015.compile()
            component_definition_list.append("https://synbiohub.org/public/igem//ComponentDefinition/BBa_B0015/1")

        except RuntimeError:
            component_definition_list.append("https://synbiohub.org/public/igem//ComponentDefinition/BBa_B0015/1")

    else:
        igem.pull(str(records[9]), Main.doc)
        component_definition_list.append(records[9])


def design_assembly(event):
    design_name = (str(GUI.design_name_entry.get())).replace(" ", "_")
    assembled_design = ComponentDefinition(design_name)
    Main.doc.addComponentDefinition(assembled_design)
    temp_list = []
    for component in component_definition_list:
        part_cd = Main.doc.getComponentDefinition(str(component))
        temp_list.append(part_cd)

    assembled_design.assemblePrimaryStructure(temp_list)
    compile_design = assembled_design.compile()
    print(assembled_design.getPrimaryStructure())
    result = Main.doc.write(design_name + ".xml")
    print(result)
    component_definition_list.clear()
    Main.doc = Document()




