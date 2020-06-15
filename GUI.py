# Import libraries
import sys
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

# Import scripts
import Genetic_Design
import Protocol_Generation
import Part_Creation

# Global variables
design_display_list = []

################### General_GUI ########################
# Creating GUI window
window = tk.Tk()
window.title("SynBioMate")
window.geometry("1000x700")

# Adding tabs to GUI
tab_parent = ttk.Notebook(window)
tab1 = ttk.Frame(tab_parent)
tab2 = ttk.Frame(tab_parent)
tab3 = ttk.Frame(tab_parent)
tab4 = ttk.Frame(tab_parent)
tab_parent.add(tab1, text="Create Part")
tab_parent.add(tab2, text="Create Design")
tab_parent.add(tab3, text="Protocol Generation")
tab_parent.add(tab4, text="MoClo Assembly")
tab_parent.pack(expand=1, fill='both')

# Assigning SBOL GIF glyphs to variables
promoter_glyph = tk.PhotoImage(file="SBOL_Glyphs/promoter-specification.gif")
rbs_glyph = tk.PhotoImage(file="SBOL_Glyphs/ribosome-entry-site-specification.gif")
cds_glyph = tk.PhotoImage(file="SBOL_Glyphs/cds-specification.gif")
terminator_glyph = tk.PhotoImage(file="SBOL_Glyphs/terminator-specification.gif")
other_glyph = tk.PhotoImage(file="SBOL_Glyphs/no-glyph-assigned-specification.gif")

################### Create part GUI ################
create_part_title = tk.Label(tab1, text="Create Part", font=(None, 20))
create_part_title.pack()

#Create from GenBank file button
import_file_creation = tk.Button(tab1, text="Convert GenBank file")
import_file_creation.bind("<Button-1>", Part_Creation.part_creation_genbank)
import_file_creation.pack()


#Manual DNA entry
or_label = tk.Label(tab1, text= "or")
or_label.pack()

dna_entry_label = tk.Label(tab1, text="Enter part DNA sequence")
dna_entry_label.pack()
sequence_entry = tk.Entry(tab1)
sequence_entry.pack()

#Part name entry
part_name_entry_label = tk.Label(tab1, text="Enter part name")
part_name_entry_label.pack()

part_name_entry = tk.Entry(tab1)
part_name_entry.pack()

#Part identifier entry
part_identifier_label = tk.Label(tab1, text = "Enter part identifier (e.g BBa_B0...)")
part_identifier_label.pack()

part_identifier_entry = tk.Entry(tab1)
part_identifier_entry.pack()

#Role selection dropdown
part_role_label = tk.Label(tab1, text = "Select the part role")
part_role_label.pack()

part_role_combo = ttk.Combobox(tab1, values = ["Promoter",
                                                 "RBS",
                                                 "CDS",
                                                 "Terminator",
                                                 "Backbone",])
part_role_combo.pack()

#Part description entry
part_description_label = tk.Label(tab1, text = "Enter a part description")
part_description_label.pack()

part_description_entry = tk.Entry(tab1)
part_description_entry.pack()

#Save part button
save_part_button = tk.Button(tab1, text = "Save part")
save_part_button.bind("<Button-1>", Part_Creation.save_created_part)
save_part_button.pack()

#Upload part to Synbiohub button
upload_part_synbiohub = tk.Button(tab1, text= "Upload part to SynbioHub")
#Placeholder for button bind
upload_part_synbiohub.pack()

#Select GenBank file for conversion
def select_genbank_file():
    window.filename = filedialog.askopenfilename(initialdir=str(sys.argv[0]), title="select file",
                                                 filetypes=(("GenBank Files (gb)", "*.gb"), ("all files", "*.*")))
    global genbank_file
    genbank_file = window.filename

#Successful conversion label
def successful_conversion():
    successful_conversion_label = tk.Label(tab1, text="Genbank file converted successfully")
    successful_conversion_label.pack()


###################### Genetic_Design GUI #####################

# Title of Genetic Design assembly tab
designassemblytitle = tk.Label(tab2, text="Create Genetic Design", font=(None, 20))
designassemblytitle.pack()


# Query submission label and entry widget
query_request_label = tk.Label(tab2, text="Please enter a search term")
query_request_label.pack()
query_request_entry = tk.Entry(tab2)
query_request_entry.pack()

# Query submit button
query_submit_button = tk.Button(tab2, text="Submit")
query_submit_button.bind("<Button-1>", Genetic_Design.query_submit)
query_submit_button.pack()


# GUI binding of writing queried part to doc
def part_choice_button_1():
    global query_result_button_1
    query_result_button_1 = tk.Button(tab2, text=Genetic_Design.records[0])
    query_result_button_1.bind("<Button-1>", Genetic_Design.query_to_doc_1)
    query_result_button_1.pack()


def part_choice_button_2():
    global query_result_button_2
    query_result_button_2 = tk.Button(tab2, text=Genetic_Design.records[1])
    query_result_button_2.bind("<Button-1>", Genetic_Design.query_to_doc_2)
    query_result_button_2.pack()


def part_choice_button_3():
    global query_result_button_3
    query_result_button_3 = tk.Button(tab2, text=Genetic_Design.records[2])
    query_result_button_3.bind("<Button-1>", Genetic_Design.query_to_doc_3)
    query_result_button_3.pack()


def part_choice_button_4():
    global query_result_button_4
    query_result_button_4 = tk.Button(tab2, text=Genetic_Design.records[3])
    query_result_button_4.bind("<Button-1>", Genetic_Design.query_to_doc_4)
    query_result_button_4.pack()


def part_choice_button_5():
    global query_result_button_5
    query_result_button_5 = tk.Button(tab2, text=Genetic_Design.records[4])
    query_result_button_5.bind("<Button-1>", Genetic_Design.query_to_doc_5)
    query_result_button_5.pack()


def part_choice_button_6():
    global query_result_button_6
    query_result_button_6 = tk.Button(tab2, text=Genetic_Design.records[5])
    query_result_button_6.bind("<Button-1>", Genetic_Design.query_to_doc_6)
    query_result_button_6.pack()


def part_choice_button_7():
    global query_result_button_7
    query_result_button_7 = tk.Button(tab2, text=Genetic_Design.records[6])
    query_result_button_7.bind("<Button-1>", Genetic_Design.query_to_doc_7)
    query_result_button_7.pack()


def part_choice_button_8():
    global query_result_button_8
    query_result_button_8 = tk.Button(tab2, text=Genetic_Design.records[7])
    query_result_button_8.bind("<Button-1>", Genetic_Design.query_to_doc_8)
    query_result_button_8.pack()


def part_choice_button_9():
    global query_result_button_9
    query_result_button_9 = tk.Button(tab2, text=Genetic_Design.records[8])
    query_result_button_9.bind("<Button-1>", Genetic_Design.query_to_doc_9)
    query_result_button_9.pack()


def part_choice_button_10():
    global query_result_button_10
    (query_result_button_10) = tk.Button(tab2, text=Genetic_Design.records[9])
    query_result_button_10.bind("<Button-1>", Genetic_Design.query_to_doc_10)
    query_result_button_10.pack()


def clear_all_query():
    query_result_button_1.pack_forget()
    query_result_button_2.pack_forget()
    query_result_button_3.pack_forget()
    query_result_button_4.pack_forget()
    query_result_button_5.pack_forget()
    query_result_button_6.pack_forget()
    query_result_button_7.pack_forget()
    query_result_button_8.pack_forget()
    query_result_button_9.pack_forget()
    query_result_button_10.pack_forget()


# Genetic Design assembly entry label
name_design_label = tk.Label(tab2, text="Please enter the name of your genetic design")
name_design_label.pack()

# Design assembly name entry
design_name_entry = tk.Entry(tab2)
design_name_entry.pack()

# Genetic Design assembly button
design_assembly_button = tk.Button(tab2, text="Assemble Design")
design_assembly_button.bind("<Button-1>", Genetic_Design.design_assembly_directory)
design_assembly_button.pack()

####################### Protocol_Generation_Main GUI ###################################
# Protocol generation title label
protocol_generation_title = tk.Label(tab3, text="Protocol Generation", font=(None, 20))
protocol_generation_title.pack()


# Selection of design to import
def select_design_import():
    window.filename = filedialog.askopenfilename(initialdir=str(sys.argv[0]), title="select file",
                                                 filetypes=(("xml files", "*.xml"), ("all files", "*.*")))
    global single_imported_design
    single_imported_design = window.filename


# Import design button
import_design_button = tk.Button(tab3, text="Import Design")
import_design_button.bind("<Button-1>", Protocol_Generation.import_design)
import_design_button.pack()

# Canvas for design display in assembly tab
design_canvas_assembly = tk.Canvas(tab3, width=1000, height=200)
design_canvas_assembly.pack()


# Display SBOL glyphs in assembly tab
def display_design_GUI(SO_list):
    counter = 0
    design_canvas_assembly.create_text(100, 60, font=("Arial", "11", "bold"), text="Design structure:")
    for x in SO_list:
        counter = counter + 1
        if "0000167" in x:
            design_canvas_assembly.create_image(counter * 70, 100, image=promoter_glyph)
            design_canvas_assembly.create_text(counter * 70, 140, font=("arial", "8"),
                                                  text=Protocol_Generation.part_names[counter - 1])
        elif "0000139" in x:
            design_canvas_assembly.create_image(counter * 70, 100, image=rbs_glyph)
            design_canvas_assembly.create_text(counter * 70, 140, font=("arial", "8"),
                                                  text=Protocol_Generation.part_names[counter - 1])
        elif "0000316" in x:
            design_canvas_assembly.create_image(counter * 70, 100, image=cds_glyph)
            design_canvas_assembly.create_text(counter * 70, 140, font=("arial", "8"),
                                                  text=Protocol_Generation.part_names[counter - 1])
        elif "0000141" in x:
            design_canvas_assembly.create_image(counter * 70, 100, image=terminator_glyph)
            design_canvas_assembly.create_text(counter * 70, 140, font=("arial", "8"),
                                                  text=Protocol_Generation.part_names[counter - 1])
        else:
            design_canvas_assembly.create_image(counter * 70, 100, image=other_glyph)
            design_canvas_assembly.create_text(counter * 70, 140, font=("arial", "8"),
                                                  text=Protocol_Generation.part_names[counter - 1])


# Show part description in GUI button
def create_description_button():
    global part_description_button
    part_description_button = tk.Button(tab3, text="Show part descriptions")
    part_description_button.bind("<Button-1>", part_description)
    part_description_button.pack()

# Show part description in GUI
def part_description(event):
    counter = 0
    for description in Protocol_Generation.part_descriptions:
        counter = counter +1
        part_description_button_name = "part_key_description" + "_" + str(counter) + "button"
        globals()[part_description_button_name] = tk.Label(tab3, text =str(Protocol_Generation.part_names[counter-1]) + " - " + description)
        globals()[part_description_button_name].pack()
    hide_description_button()


# Hide part description in GUI button
def hide_description_button():
    part_description_button.pack_forget()
    global hide_part_description_button
    hide_part_description_button = tk.Button(tab3, text = "Hide part descriptions")
    hide_part_description_button.bind("<Button-1>", hide_description)
    hide_part_description_button.pack()

def hide_description(event):
    counter = 0
    for description in Protocol_Generation.part_descriptions:
        counter = counter +1
        part_description_button_name = "part_key_description" + "_" + str(counter) + "button"
        globals()[part_description_button_name].pack_forget()
    create_description_button()
    hide_part_description_button.pack_forget()



################ Main_loop #################
window.mainloop()
