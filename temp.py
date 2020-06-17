# Import libraries
from sbol import *

# Import scripts
import Main
import GUI


# Specifying SynBioHub part repository for query
igem = PartShop('https://synbiohub.org/public/igem')

# Global variables (Not all)
part_count = 0
sub_component = []


# Counter function
def part_counter():
    global part_count
    part_count = part_count + 1
    return part_count


# SynBioHub part query
def part_search(query):
    query2 = query.replace(" ", "_")
    global records
    records = igem.search(query2, SBOL_COMPONENT_DEFINITION, 0, 10)
    print(records)


# Show objects in doc
def objects_in_doc():
    dictionary_doc = [obj for obj in Main.doc]
    return dictionary_doc



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
    igem.pull(str(records[0]), Main.doc)
    part = records[0]
    GUI.clear_all_query()
    part_counter()
    sub_component_detection(part)


def query_to_doc_2(event):
    igem.pull(str(records[1]), Main.doc)
    part = records[1]
    GUI.clear_all_query()
    part_counter()
    sub_component_detection(part)


def query_to_doc_3(event):
    igem.pull(str(records[2]), Main.doc)
    part = records[2]
    GUI.clear_all_query()
    part_counter()
    sub_component_detection(part)


def query_to_doc_4(event):
    igem.pull(str(records[3]), Main.doc)
    part = records[3]
    GUI.clear_all_query()
    part_counter()
    sub_component_detection(part)


def query_to_doc_5(event):
    igem.pull(str(records[4]), Main.doc)
    part = records[4]
    GUI.clear_all_query()
    part_counter()
    sub_component_detection(part)


def query_to_doc_6(event):
    igem.pull(str(records[5]), Main.doc)
    part = records[5]
    GUI.clear_all_query()
    part_counter()
    sub_component_detection(part)


def query_to_doc_7(event):
    igem.pull(str(records[6]), Main.doc)
    part = records[6]
    GUI.clear_all_query()
    part_counter()
    sub_component_detection(part)


def query_to_doc_8(event):
    igem.pull(str(records[7]), Main.doc)
    part = records[7]
    GUI.clear_all_query()
    part_counter()
    sub_component_detection(part)


def query_to_doc_9(event):
    igem.pull(str(records[8]), Main.doc)
    part = records[8]
    GUI.clear_all_query()
    part_counter()
    sub_component_detection(part)


def query_to_doc_10(event):
    igem.pull(str(records[9]), Main.doc)
    part = records[9]
    GUI.clear_all_query()
    part_counter()
    sub_component_detection(part)


# Detect multiple URI parts
def sub_component_detection(part):
    partcd = Main.doc.getComponentDefinition(str(part))
    for component in partcd.components:
        sub_component.append(component.definition)
    if len(sub_component) == 0:
        part_uri_isolation(part)
    elif len(sub_component) > 0:
        multiple_uri_isolation()


# Isolating URI's of components with multiple parts
def multiple_uri_isolation():
    if part_count == 1:
        global part_1_components
        if len(sub_component) == 2:
            global part1a
            global part1b
            part1a = (sub_component[0])
            part1b = (sub_component[1])
            part_1_components = 2
    elif part_count == 2:
        global part_2_components
        if len(sub_component) == 2:
            global part2a
            global part2b
            part2a = (sub_component[0])
            part2b = (sub_component[1])
            part_2_components = 2
    elif part_count == 3:
        global part_3_components
        if len(sub_component) == 2:
            global part3a
            global part3b
            part3a = (sub_component[0])
            part3b = (sub_component[1])
            part_3_components = 2
    elif part_count == 4:
        global part_4_components
        if len(sub_component) == 2:
            global part4a
            global part4b
            part4a = (sub_component[0])
            part4b = (sub_component[1])
            part_4_components = 2
    elif part_count == 5:
        global part_5_components
        if len(sub_component) == 2:
            global part5a
            global part5b
            part5a = (sub_component[0])
            part5b = (sub_component[1])
            part_5_components = 2
    elif part_count == 6:
        global part_6_components
        if len(sub_component) == 2:
            global part6a
            global part6b
            part6a = (sub_component[0])
            part6b = (sub_component[1])
            part_6_components = 2
    elif part_count == 7:
        global part_7_components
        if len(sub_component) == 2:
            global part7a
            global part7b
            part7a = (sub_component[0])
            part7b = (sub_component[1])
            part_7_components = 2
    elif part_count == 8:
        global part_8_components
        if len(sub_component) == 2:
            global part8a
            global part8b
            part8a = (sub_component[0])
            part8b = (sub_component[1])
            part_8_components = 2
    elif part_count == 9:
        global part_9_components
        if len(sub_component) == 2:
            global part9a
            global part9b
            part9a = (sub_component[0])
            part9b = (sub_component[1])
            part_9_components = 2
    elif part_count == 10:
        global part_10_components
        if len(sub_component) == 2:
            global part10a
            global part10b
            part10a = (sub_component[0])
            part10b = (sub_component[1])
            part_10_components = 2


# Storing URI's as variables
def part_uri_isolation(uri):
    if part_count == 1:
        global part1
        global part_1_components
        part1 = uri
        part_1_components = 0
        print(part1)
    elif part_count == 2:
        global part_2_components
        global part2
        part2 = uri
        part_2_components = 0
    elif part_count == 3:
        global part_3_components
        global part3
        part3 = uri
        part_3_components = 0
    elif part_count == 4:
        global part_4_components
        global part4
        part4 = uri
        part_4_components = 0
    elif part_count == 5:
        global part_5_components
        global part5
        part5 = uri
        part_5_components = 0
    elif part_count == 6:
        global part_6_components
        global part6
        part6 = uri
        part_6_components = 0
    elif part_count == 7:
        global part_7_components
        global part7
        part7 = uri
        part_7_components = 0
    elif part_count == 8:
        global part_8_components
        global part8
        part8 = uri
        part_8_components = 0
    elif part_count == 9:
        global part_9_components
        global part9
        part9 = uri
        part_9_components = 0
    elif part_count == 10:
        global part_10_components
        global part10
        part10 = uri
        part_10_components = 0


# Design assembly directory 1
def design_assembly_directory(event):
    if part_count == 0:
        print("Please add more parts before trying to assemble")
    elif part_count == 1:
        print("Please Add more parts before trying to assemble")
    elif part_count == 2:
        design_assembly_2()
    elif part_count == 3:
        design_assembly_3()
    elif part_count == 4:
        design_assembly_4()
    elif part_count == 5:
        design_assembly_5()
    elif part_count == 6:
        design_assembly_6()
    elif part_count == 7:
        design_assembly_7()
    elif part_count == 8:
        design_assembly_8()
    elif part_count == 9:
        design_assembly_9()
    elif part_count == 10:
        design_assembly_10()

# Design assembly directory 2
def design_assembly_2():
    design_name = GUI.design_name_entry.get()
    assembled_design = ComponentDefinition(str(design_name))
    Main.doc.addComponentDefinition(assembled_design)
    part1_cd = Main.doc.getComponentDefinition(str(part1))
    if part_2_components == 0:
        part2_cd = Main.doc.getComponentDefinition(str(part2))
        assembled_design.assemblePrimaryStructure([part1_cd, part2_cd])
        assembled_design.compile()
        result = Main.doc.write((str(design_name)) + ".xml")
        print(result)
    elif part_2_components == 2:
        part2a_cd = Main.doc.getComponentDefinition(str(part2a))
        part2b_cd = Main.doc.getComponentDefinition(str(part2b))
        assembled_design.assemblePrimaryStructure([part1_cd, part2b_cd, part2a_cd])
        result = Main.doc.write((str(design_name)) + ".xml")
        print(result)


def design_assembly_3():
    design_name = GUI.design_name_entry.get()
    assembled_design = ComponentDefinition(str(designt_name))
    Main.doc.addComponentDefinition(assembled_design)
    part1_cd = Main.doc.getComponentDefinition(str(part1))
    part2_cd = Main.doc.getComponentDefinition(str(part2))
    if part_3_components == 0:
        part3_cd = Main.doc.getComponentDefinition(str(part3))
        assembled_design.assemblePrimaryStructure([part1_cd, part2_cd, part3_cd])
        assembled.design.compile()
        result = Main.doc.write((str(design_name)) + ".xml")
        print(result)
    elif part_3_components == 2:
        part3a_cd = Main.doc.getComponentDefinition(str(part3a))
        part3b_cd = Main.doc.getComponentDefinition(str(part3b))
        assembled_design.assemblePrimaryStructure([part1_cd, part2_cd, part3b_cd, part3a_cd])
        result = Main.doc.write((str(design_name)) + ".xml")
        print(result)


def design_assembly_4():
    design_name = GUI.design_name_entry.get()
    assembled_design = ComponentDefinition(str(design_name))
    Main.doc.addComponentDefinition(assembled_design)
    part1_cd = Main.doc.getComponentDefinition(str(part1))
    part2_cd = Main.doc.getComponentDefinition(str(part2))
    part3_cd = Main.doc.getComponentDefinition(str(part3))
    if part_4_components == 0:
        part4_cd = Main.doc.getComponentDefinition(str(part4))
        assembled_design.assemblePrimaryStructure([part1_cd, part2_cd, part3_cd, part4_cd])
        assembled_design.compile()
        result = Main.doc.write((str(design_name)) + ".xml")
        print(result)
    elif part_4_components == 2:
        part4a_cd = Main.doc.getComponentDefinition(str(part4a))
        part4b_cd = Main.doc.getComponentDefinition(str(part4b))
        assembled_design.assemblePrimaryStructure([part1_cd, part2_cd, part3_cd, part4b_cd, part4a_cd])
        result = Main.doc.write((str(design_name)) + ".xml")
        print(result)


def design_assembly_5():
    design_name = GUI.design_name_entry.get()
    assembled_design = ComponentDefinition(str(design_name))
    Main.doc.addComponentDefinition(assembled_design)
    part1_cd = Main.doc.getComponentDefinition(str(part1))
    part2_cd = Main.doc.getComponentDefinition(str(part2))
    part3_cd = Main.doc.getComponentDefinition(str(part3))
    part4_cd = Main.doc.getComponentDefinition(str(part4))
    if part_5_components == 0:
        part5_cd = Main.doc.getComponentDefinition(str(part5))
        assembled_design.assemblePrimaryStructure([part1_cd, part2_cd, part3_cd, part4_cd, part5_cd])
        assembled.design.compile()
        result = Main.doc.write((str(design_name)) + ".xml")
        print(result)
    elif part_5_components == 2:
        part5a_cd = Main.doc.getComponentDefinition(str(part5a))
        part5b_cd = Main.doc.getComponentDefinition(str(part5b))
        assembled_design.assemblePrimaryStructure([part1_cd, part2_cd, part3_cd, part4_cd, part5b_cd, part5a_cd])
        assembled.design.compile()
        result = Main.doc.write((str(design_name)) + ".xml")



def design_assembly_6():
    design_name = GUI.design_name_entry.get()
    assembled_design = ComponentDefinition(str(design_name))
    Main.doc.addComponentDefinition(assembled_design)
    part1_cd = Main.doc.getComponentDefinition(str(part1))
    part2_cd = Main.doc.getComponentDefinition(str(part2))
    part3_cd = Main.doc.getComponentDefinition(str(part3))
    part4_cd = Main.doc.getComponentDefinition(str(part4))
    part5_cd = Main.doc.getComponentDefinition(str(part5))
    if part_6_components == 0:
        part6_cd = Main.doc.getComponentDefinition(str(part6))
        assembled_design.assemblePrimaryStructure([part1_cd, part2_cd, part3_cd, part4_cd, part5_cd, part6_cd])
        assembled.design.compile()
        result = Main.doc.write((str(design_name)) + ".xml")
        print(result)
    elif part_6_components == 2:
        part6a_cd = Main.doc.getComponentDefinition(str(part6a))
        part6b_dc = Main.doc.getComponentDefinition(str(part6b))
        assembled_design.assemblePrimaryStructure([part1_cd, part2_cd, part3_cd, part4_cd, part5_cd, part6b_cd,
                                                      part6a_cd])
        assembled.design.compile()
        result = Main.doc.write((str(design_name)) + ".xml")
        print(result)


def design_assembly_7():
    design_name = GUI.design_name_entry.get()
    assembled_design = ComponentDefinition(str(design_name))
    Main.doc.addComponentDefinition(assembled_design)
    part1_cd = Main.doc.getComponentDefinition(str(part1))
    part2_cd = Main.doc.getComponentDefinition(str(part2))
    part3_cd = Main.doc.getComponentDefinition(str(part3))
    part4_cd = Main.doc.getComponentDefinition(str(part4))
    part5_cd = Main.doc.getComponentDefinition(str(part5))
    part6_cd = Main.doc.getComponentDefinition(str(part6))
    if part_7_components == 0:
        part7_cd = Main.doc.getComponentDefinition(str(part7))
        assembled_design.assemblePrimaryStructure([part1_cd, part2_cd, part3_cd, part4_cd, part5_cd, part6_cd,
                                                      part7_cd])
        assembled.design.compile()
        result = Main.doc.write((str(design_name)) + ".xml")
        print(result)
    if part_7_components == 2:
        part7a_cd = Main.doc.getComponentDefinition(str(part7a))
        part7b_cd = Main.doc.getComponentDefinition(str(part7b))
        assembled_design.assemblePrimaryStructure([part1_cd, part2_cd, part3_cd, part4_cd, part5_cd, part6b_cd,
                                                      part6a_cd, part7b_cd, part7a_cd])
        assembled.design.compile()
        result = Main.doc.write((str(design_name)) + ".xml")
        print(result)


def design_assembly_8():
    design_name = GUI.design_name_entry.get()
    assembled_design = ComponentDefinition(str(design_name))
    Main.doc.addComponentDefinition(design_design)
    part1_cd = Main.doc.getComponentDefinition(str(part1))
    part2_cd = Main.doc.getComponentDefinition(str(part2))
    part3_cd = Main.doc.getComponentDefinition(str(part3))
    part4_cd = Main.doc.getComponentDefinition(str(part4))
    part5_cd = Main.doc.getComponentDefinition(str(part5))
    part6_cd = Main.doc.getComponentDefinition(str(part6))
    part7_cd = Main.doc.getComponentDefinition(str(part7))
    if part_8_components == 0:
        part8_cd = Main.doc.getComponentDefinition(str(part8))
        assembled_design.assemblePrimaryStructure([part1_cd, part2_cd, part3_cd, part4_cd, part5_cd, part6_cd,
                                                      part7_cd, part8_cd])
        assembled.design.compile()
        result = Main.doc.write((str(design_name)) + ".xml")
        print(result)
    elif part_8_components == 2:
        part8a_cd = Main.doc.getComponentDefinition(str(part8a))
        part8b_cd = Main.doc.getComponentDefinition(str(part8b))
        assembled_design.assemblePrimaryStructure([part1_cd, part2_cd, part3_cd, part4_cd, part5_cd, part6_cd,
                                                      part7_cd, part8b_cd, part8a_cd])
        assembled.design.compile()
        result = Main.doc.write((str(design_name)) + ".xml")
        print(result)


def design_assembly_9():
    design_name = GUI.design_name_entry.get()
    assembled_design = ComponentDefinition(str(design_name))
    Main.doc.addComponentDefinition(assembled_design)
    part1_cd = Main.doc.getComponentDefinition(str(part1))
    part2_cd = Main.doc.getComponentDefinition(str(part2))
    part3_cd = Main.doc.getComponentDefinition(str(part3))
    part4_cd = Main.doc.getComponentDefinition(str(part4))
    part5_cd = Main.doc.getComponentDefinition(str(part5))
    part6_cd = Main.doc.getComponentDefinition(str(part6))
    part7_cd = Main.doc.getComponentDefinition(str(part7))
    part8_cd = Main.doc.getComponentDefinition(str(part8))
    if part_9_components == 0:
        part9_cd = Main.doc.getComponentDefinition(str(part9))
        assembled_design.assemblePrimaryStructure([part1_cd, part2_cd, part3_cd, part4_cd, part5_cd, part6_cd,
                                                      part7_cd, part8_cd, part9_cd])
        assembled.design.compile()
        result = Main.doc.write((str(design_name)) + ".xml")
        print(result)
    if part_9_components == 2:
        part9a_cd = Main.doc.getComponentDefinition(str(part9a))
        part9b_cd = Main.doc.getComponentDefinition(str(part9b))
        assembled_design.assemblePrimaryStructure([part1_cd, part2_cd, part3_cd, part4_cd, part5_cd, part6_cd,
                                                      part7_cd, part8_cd, part9b_cd, part9a_cd])
        assembled.design.compile()
        result = Main.doc.write((str(design_name)) + ".xml")
        print(result)



def design_assembly_10():
    design_name = GUI.design_name_entry.get()
    assembled_design = ComponentDefinition(str(design_name))
    Main.doc.addComponentDefinition(assembled_design)
    part1_cd = Main.doc.getComponentDefinition(str(part1))
    part2_cd = Main.doc.getComponentDefinition(str(part2))
    part3_cd = Main.doc.getComponentDefinition(str(part3))
    part4_cd = Main.doc.getComponentDefinition(str(part4))
    part5_cd = Main.doc.getComponentDefinition(str(part5))
    part6_cd = Main.doc.getComponentDefinition(str(part6))
    part7_cd = Main.doc.getComponentDefinition(str(part7))
    part8_cd = Main.doc.getComponentDefinition(str(part8))
    part9_cd = Main.doc.getComponentDefinition(str(part9))
    if part_10_components == 0:
        part10_cd = Main.doc.getComponentDefinition(str(part10))
        assembled_design.assemblePrimaryStructure([part1_cd, part2_cd, part3_cd, part4_cd, part5_cd, part6_cd,
                                                      part7_cd, part8_cd, part9_cd, part10_cd])
        assembled.design.compile()
        result = Main.doc.write((str(design_name)) + ".xml")
        print(result)
    elif part_10_components == 2:
        part10a_cd = Main.doc.getComponentDefinition(str(part10a))
        part10b_cd = Main.doc.getComponentDefinition(str(part10b))
        assembled_design.assemblePrimaryStructure([part1_cd, part2_cd, part3_cd, part4_cd, part5_cd, part6_cd,
                                                      part7_cd, part8_cd, part9_cd, part10b_cd, part10a_cd])
        assembled.design.compile()
        result = Main.doc.write((str(design_name)) + ".xml")
        print(result)