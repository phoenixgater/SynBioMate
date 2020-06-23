# Import libraries
import sys
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from sbol import *

# Import scripts
import Genetic_Design
import Protocol_Generation
import Part_Creation
import Main
import MoClo

# Global variables
design_display_list = []
igem = PartShop('https://synbiohub.org/public/igem')

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


# Upload to synbiohub window
def synbiohub_upload(event):
    global upload_window
    upload_window = tk.Toplevel(window)
    upload_window.title("Upload to SynBioHub")
    upload_window.geometry("400x300")

    synbiohub_title = tk.Label(upload_window, text="Upload to SynBioHub", font=(None, 15))
    synbiohub_title.pack()

    global username_entry_label
    username_entry_label = tk.Label(upload_window, text="SynBioHub Username")
    username_entry_label.pack()

    global username_entry
    username_entry = tk.Entry(upload_window)
    username_entry.pack()

    global password_entry_label
    password_entry_label = tk.Label(upload_window, text="SynBioHub Password")
    password_entry_label.pack()

    global password_entry
    password_entry = tk.Entry(upload_window)
    password_entry.pack()

    global login_button
    login_button = tk.Button(upload_window, text="login")
    login_button.bind("<Button-1>", synbiohub_login)
    login_button.pack()


# SynBioHub Login
def synbiohub_login(event):
    global login_failed_label
    try:
        username = username_entry.get()
        password = password_entry.get()
        igem.login(str(username), str(password))
        successful_login()

    except RuntimeError:
        try:
            login_failed_label.pack_forget
        except NameError:
            login_failed_label = tk.Label(upload_window, text="Login failed")
            login_failed_label.pack()


def successful_login():
    username_entry_label.pack_forget()
    username_entry.pack_forget()
    password_entry_label.pack_forget()
    password_entry.pack_forget()
    login_button.pack_forget()

    upload_label = tk.Label(upload_window, text=("Please select the file you wish to upload"))
    upload_label.pack()

    select_upload_button = tk.Button(upload_window, text="Select file")
    select_upload_button.bind("<Button-1>", select_upload)
    select_upload_button.pack()


def select_upload(event):
    upload_window.filename = filedialog.askopenfilename(initialdir=str(sys.argv[0]), title="select file",
                                                        filetypes=(("SBOL files .xml", "*.xml"), ("all files", "*.*")))
    global selected_file
    selected_file = upload_window.filename
    selected_file_label = tk.Label(upload_window, text=str(selected_file))
    selected_file_label.pack()

    global collection_id
    collection_id_label = tk.Label(upload_window, text="Enter collection ID")
    collection_id_label.pack()
    collection_id = tk.Entry(upload_window)
    collection_id.pack()

    global collection_name
    collection_name_label = tk.Label(upload_window, text="Enter collection name")
    collection_name_label.pack()
    collection_name = tk.Entry(upload_window)
    collection_name.pack()

    global collection_description
    collection_description_label = tk.Label(upload_window, text="Enter collection description")
    collection_description_label.pack()
    collection_description = tk.Entry(upload_window)
    collection_description.pack()

    upload_file_button = tk.Button(upload_window, text="Upload")
    upload_file_button.bind("<Button-1>", upload_file)
    upload_file_button.pack()


def upload_file(event):
    Main.doc.read(str(selected_file))
    Main.doc.displayId = collection_id.get()
    Main.doc.name = collection_name.get()
    Main.doc.description = collection_description.get()
    igem.submit(Main.doc)
    successful_upload_label = tk.Label(upload_window, text="File uploaded")
    successful_upload_label.pack()


################### Create part GUI ################
create_part_title = tk.Label(tab1, text="Create Part", font=(None, 15))
create_part_title.pack()

# Upload part to Synbiohub button
upload_part_synbiohub = tk.Button(tab1, text="Upload part to SynbioHub")
upload_part_synbiohub.bind("<Button-1>", synbiohub_upload)
upload_part_synbiohub.pack()

# Create from GenBank file button
import_file_creation = tk.Button(tab1, text="Create from GenBank file")
import_file_creation.bind("<Button-1>", Part_Creation.part_creation_genbank)
import_file_creation.pack()

# Manual DNA entry
or_label = tk.Label(tab1, text="or")
or_label.pack()

dna_entry_label = tk.Label(tab1, text="Enter part DNA sequence")
dna_entry_label.pack()
sequence_entry = tk.Entry(tab1)
sequence_entry.pack()

# Part name entry
part_name_entry_label = tk.Label(tab1, text="Enter part name")
part_name_entry_label.pack()

part_name_entry = tk.Entry(tab1)
part_name_entry.pack()

# Part identifier entry
part_identifier_label = tk.Label(tab1, text="Enter part identifier (e.g BBa_B0...)")
part_identifier_label.pack()

part_identifier_entry = tk.Entry(tab1)
part_identifier_entry.pack()

# Role selection dropdown
part_role_label = tk.Label(tab1, text="Select the part role")
part_role_label.pack()

part_role_combo = ttk.Combobox(tab1, values=["Promoter",
                                             "RBS",
                                             "CDS",
                                             "Terminator",
                                             "Backbone", ])
part_role_combo.pack()

# Part description entry
part_description_label = tk.Label(tab1, text="Enter a part description")
part_description_label.pack()

part_description_entry = tk.Entry(tab1)
part_description_entry.pack()

# Save part button
save_part_button = tk.Button(tab1, text="Save part")
save_part_button.bind("<Button-1>", Part_Creation.save_created_part)
save_part_button.pack()


# Select GenBank file for conversion
def select_genbank_file():
    window.filename = filedialog.askopenfilename(initialdir=str(sys.argv[0]), title="select file",
                                                 filetypes=(("GenBank Files (gb)", "*.gb"), ("all files", "*.*")))
    global genbank_file
    genbank_file = window.filename


# Successful conversion label
def successful_conversion():
    successful_conversion_label = tk.Label(tab1, text="Genbank file converted successfully")
    successful_conversion_label.pack()


###################### Genetic_Design GUI #####################

# Title of Genetic Design assembly tab
designassemblytitle = tk.Label(tab2, text="Create Genetic Design", font=(None, 15))
designassemblytitle.pack()


# Canvas for design display in Genetic Design tab
def genetic_design_display_canvas():
    global design_canvas_display
    design_canvas_display = tk.Canvas(tab2, width=1000, height=200)
    design_canvas_display.pack()


# Initialise genetic design display for Genetic_Design tab
genetic_design_display_canvas()


# Display design glyphs in genetic design tab
def display_assembled_design(SO_list):
    counter = 0
    design_canvas_display.create_text(100, 60, font=("Arial", "11", "bold"), text="Design structure:")
    for x in SO_list:
        counter = counter + 1
        if "0000167" in x:
            design_canvas_display.create_image(counter * 70, 100, image=promoter_glyph)
            design_canvas_display.create_text(counter * 70, 140, font=("arial", "8"),
                                              text=Genetic_Design.design_identities[counter - 1])
        elif "0000139" in x:
            design_canvas_display.create_image(counter * 70, 100, image=rbs_glyph)
            design_canvas_display.create_text(counter * 70, 140, font=("arial", "8"),
                                              text=Genetic_Design.design_identities[counter - 1])
        elif "0000316" in x:
            design_canvas_display.create_image(counter * 70, 100, image=cds_glyph)
            design_canvas_display.create_text(counter * 70, 140, font=("arial", "8"),
                                              text=Genetic_Design.design_identities[counter - 1])
        elif "0000141" in x:
            design_canvas_display.create_image(counter * 70, 100, image=terminator_glyph)
            design_canvas_display.create_text(counter * 70, 140, font=("arial", "8"),
                                              text=Genetic_Design.design_identities[counter - 1])
        else:
            design_canvas_display.create_image(counter * 70, 100, image=other_glyph)
            design_canvas_display.create_text(counter * 70, 140, font=("arial", "8"),
                                              text=Genetic_Design.design_identities[counter - 1])


# Button to show part descriptions in genetic design tab
def create_description_button_design():
    global part_description_button_design
    try:
        part_description_button_design.pack_forget()
        hide_part_description_button_design.pack_forget()
        hide_description_design("<Button-1>")
        part_description_button_design = tk.Button(tab2, text="Show part descriptions")
        part_description_button_design.bind("<Button-1>", part_description_design)
        part_description_button_design.pack()
    except KeyError:
        part_description_button_design.pack_forget()
        hide_part_description_button_design.pack_forget()
        part_description_button_design = tk.Button(tab2, text="Show part descriptions")
        part_description_button_design.bind("<Button-1>", part_description_design)
        part_description_button_design.pack()
    except NameError:
        part_description_button_design = tk.Button(tab2, text="Show part descriptions")
        part_description_button_design.bind("<Button-1>", part_description_design)
        part_description_button_design.pack()


# Show part description in genetic design tab
def part_description_design(event):
    counter = 0
    for description in Genetic_Design.design_descriptions:
        counter = counter + 1
        part_description_button_name = "part_key_description" + "_" + str(counter) + "button"
        globals()[part_description_button_name] = tk.Label(tab2, text=str(
            Genetic_Design.design_identities[counter - 1]) + " - " + description)
        globals()[part_description_button_name].pack()
    hide_description_button_design()


# Button for hiding part descriptions in genetic design tab
def hide_description_button_design():
    part_description_button_design.pack_forget()
    global hide_part_description_button_design
    hide_part_description_button_design = tk.Button(tab2, text="Hide part descriptions")
    hide_part_description_button_design.bind("<Button-1>", hide_description_design)
    hide_part_description_button_design.pack()


# Hiding part descriptions in genetic design tab
def hide_description_design(event):
    counter = 0
    for description in Genetic_Design.design_descriptions:
        counter = counter + 1
        part_description_button_name = "part_key_description" + "_" + str(counter) + "button"
        globals()[part_description_button_name].pack_forget()
    part_description_button_design.pack()
    hide_part_description_button_design.pack_forget()


# Part from file selection
def part_file_selection(event):
    window.filename = filedialog.askopenfilename(initialdir=str(sys.argv[0]), title="select file",
                                                 filetypes=(("SBOL files (.xml)", "*.xml"), ("all files", "*.*")))
    global imported_part
    imported_part = window.filename
    Genetic_Design.add_file_part()


# Import part from file button
import_file_button = tk.Button(tab2, text="Import part from file")
import_file_button.bind("<Button-1>", part_file_selection)
import_file_button.pack()

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
    query_result_button_1 = tk.Button(tab2, text=Genetic_Design.button_1_display)
    query_result_button_1.bind("<Button-1>", Genetic_Design.query_to_doc_1)
    query_result_button_1.pack()


def part_choice_button_2():
    global query_result_button_2
    query_result_button_2 = tk.Button(tab2, text=Genetic_Design.button_2_display)
    query_result_button_2.bind("<Button-1>", Genetic_Design.query_to_doc_2)
    query_result_button_2.pack()


def part_choice_button_3():
    global query_result_button_3
    query_result_button_3 = tk.Button(tab2, text=Genetic_Design.button_3_display)
    query_result_button_3.bind("<Button-1>", Genetic_Design.query_to_doc_3)
    query_result_button_3.pack()


def part_choice_button_4():
    global query_result_button_4
    query_result_button_4 = tk.Button(tab2, text=Genetic_Design.button_4_display)
    query_result_button_4.bind("<Button-1>", Genetic_Design.query_to_doc_4)
    query_result_button_4.pack()


def part_choice_button_5():
    global query_result_button_5
    query_result_button_5 = tk.Button(tab2, text=Genetic_Design.button_5_display)
    query_result_button_5.bind("<Button-1>", Genetic_Design.query_to_doc_5)
    query_result_button_5.pack()


def part_choice_button_6():
    global query_result_button_6
    query_result_button_6 = tk.Button(tab2, text=Genetic_Design.button_6_display)
    query_result_button_6.bind("<Button-1>", Genetic_Design.query_to_doc_6)
    query_result_button_6.pack()


def part_choice_button_7():
    global query_result_button_7
    query_result_button_7 = tk.Button(tab2, text=Genetic_Design.button_7_display)
    query_result_button_7.bind("<Button-1>", Genetic_Design.query_to_doc_7)
    query_result_button_7.pack()


def part_choice_button_8():
    global query_result_button_8
    query_result_button_8 = tk.Button(tab2, text=Genetic_Design.button_8_display)
    query_result_button_8.bind("<Button-1>", Genetic_Design.query_to_doc_8)
    query_result_button_8.pack()


def part_choice_button_9():
    global query_result_button_9
    query_result_button_9 = tk.Button(tab2, text=Genetic_Design.button_9_display)
    query_result_button_9.bind("<Button-1>", Genetic_Design.query_to_doc_9)
    query_result_button_9.pack()


def part_choice_button_10():
    global query_result_button_10
    query_result_button_10 = tk.Button(tab2, text=Genetic_Design.button_10_display)
    query_result_button_10.bind("<Button-1>", Genetic_Design.query_to_doc_10)
    query_result_button_10.pack()


def clear_all_query():
    try:
        query_result_button_1.pack_forget()
    except NameError:
        return
    try:
        query_result_button_2.pack_forget()
    except NameError:
        return
    try:
        query_result_button_3.pack_forget()
    except NameError:
        return
    try:
        query_result_button_4.pack_forget()
    except NameError:
        return
    try:
        query_result_button_5.pack_forget()
    except NameError:
        return
    try:
        query_result_button_6.pack_forget()
    except NameError:
        return
    try:
        query_result_button_7.pack_forget()
    except NameError:
        return
    try:
        query_result_button_8.pack_forget()
    except NameError:
        return
    try:
        query_result_button_9.pack_forget()
    except NameError:
        return
    try:
        query_result_button_10.pack_forget()
    except NameError:
        return


# Genetic Design assembly entry label
name_design_label = tk.Label(tab2, text="Please enter the name of your genetic design")
name_design_label.pack()

# Design assembly name entry
design_name_entry = tk.Entry(tab2)
design_name_entry.pack()

# Genetic Design assembly button
design_assembly_button = tk.Button(tab2, text="Assemble Design")
design_assembly_button.bind("<Button-1>", Genetic_Design.design_assembly)
design_assembly_button.pack()


# Incompatible part error
def incompatible_part():
    global incompatible_part_label
    incompatible_part_label = tk.Label(tab2, font=(None, 12), fg="red", text="Error: Importing multiple parts is not "
                                                                             "supported")
    incompatible_part_label.pack()


# Failed assembly error
def failed_assembly():
    global failed_assembly_label
    failed_assembly_label = tk.Label(tab2, font=(None, 12), fg="red", text="Assembly failed")
    failed_assembly_label.pack()


# Successful assembly
def successful_assembly():
    global successful_assembly_label
    successful_assembly_label = tk.Label(tab2, font=(None, 12), fg="green", text="Assembly Successful")
    successful_assembly_label.pack()


####################### Protocol_Generation_Main GUI ###################################
# Protocol generation title label
protocol_generation_title = tk.Label(tab3, text="Protocol Generation", font=(None, 15))
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
        counter = counter + 1
        part_description_button_name = "part_key_description" + "_" + str(counter) + "button"
        globals()[part_description_button_name] = tk.Label(tab3, text=str(
            Protocol_Generation.part_names[counter - 1]) + " - " + description)
        globals()[part_description_button_name].pack()
    hide_description_button()


# Hide part description in GUI button
def hide_description_button():
    part_description_button.pack_forget()
    global hide_part_description_button
    hide_part_description_button = tk.Button(tab3, text="Hide part descriptions")
    hide_part_description_button.bind("<Button-1>", hide_description)
    hide_part_description_button.pack()


def hide_description(event):
    counter = 0
    for description in Protocol_Generation.part_descriptions:
        counter = counter + 1
        part_description_button_name = "part_key_description" + "_" + str(counter) + "button"
        globals()[part_description_button_name].pack_forget()
    create_description_button()
    hide_part_description_button.pack_forget()


##################### MoClo Assembly GUI #########################

# Tab title
moclo_title = tk.Label(tab4, font=(None, 15), text="MoClo Assembly")
moclo_title.grid(row=1, column=1)

# Import part button
import_part_button = tk.Button(tab4, text="Import part from file")
import_part_button.bind("<Button-1>", MoClo.part_from_file)
import_part_button.grid(row=2, column=2)


# Canvas for design display in Genetic Design tab
def moclo_display_canvas():
    global moclo_design_canvas_display
    moclo_design_canvas_display = tk.Canvas(tab4, width=1000, height=200)
    moclo_design_canvas_display.grid(row=3, column=3)

# Initialise MoClo display canvas
moclo_display_canvas()











################ Main_loop #################
window.mainloop()
