# Import libraries
import sys
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from sbol import *
import os

# Import scripts
import Genetic_Design
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
tab4 = ttk.Frame(tab_parent)
tab_parent.add(tab1, text="Create Part")
tab_parent.add(tab2, text="Create Design")
tab_parent.add(tab4, text="MoClo Assembly")
tab_parent.pack(expand=1, fill='both')

# Assigning SBOL GIF glyphs to variables
promoter_glyph = tk.PhotoImage(file="SBOL_Glyphs/promoter-specification.gif")
rbs_glyph = tk.PhotoImage(file="SBOL_Glyphs/ribosome-entry-site-specification.gif")
cds_glyph = tk.PhotoImage(file="SBOL_Glyphs/cds-specification.gif")
terminator_glyph = tk.PhotoImage(file="SBOL_Glyphs/terminator-specification.gif")
other_glyph = tk.PhotoImage(file="SBOL_Glyphs/no-glyph-assigned-specification.gif")


# toolbar (top of GUI)
class MenuBar(ttk.Frame):

    def __init__(self):
        super().__init__()

        self.init_gui()

    def init_gui(self):
        self.master.title("Main menu")

        menu_bar = tk.Menu(self.master)
        self.master.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar)
        file_menu.add_command(label="Upload to SynbioHub", command=self.upload_window)
        file_menu.add_command(label="About", command=self.about_popup)
        file_menu.add_command(label="Exit", command=self.exit_software)
        menu_bar.add_cascade(label="File", menu=file_menu)

    def exit_software(self):
        self.quit()

    def upload_window(self):
        synbiohub_upload("<Button-1>")

    def about_popup(self):
        print("PLACEHOLDER")


# Initialising toolbar
MenuBar()


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
    password_entry = tk.Entry(upload_window, show="*")
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
create_part_title.grid(column=1, row=0)

# Create from GenBank file button
import_file_creation = tk.Button(tab1, text="Create from GenBank file")
import_file_creation.bind("<Button-1>", Part_Creation.part_creation_genbank)
import_file_creation.grid(column=1, row=15)

# DNA sequence entry
dna_entry_label = tk.Label(tab1, text="Enter part DNA sequence")
dna_entry_label.grid(column=0, row=3)

sequence_entry = tk.Entry(tab1)
sequence_entry.grid(column=1, row=3)

# Part name entry
part_name_entry_label = tk.Label(tab1, text="Enter part name")
part_name_entry_label.grid(column=0, row=5)

part_name_entry = tk.Entry(tab1)
part_name_entry.grid(column=1, row=5)

# Part identifier entry
part_identifier_label = tk.Label(tab1, text="Enter part identifier (e.g BBa_B0...)")
part_identifier_label.grid(column=0, row=7)

part_identifier_entry = tk.Entry(tab1)
part_identifier_entry.grid(column=1, row=7)

# Role selection dropdown
part_role_label = tk.Label(tab1, text="Select the part role")
part_role_label.grid(column=0, row=9)

part_role_combo = ttk.Combobox(tab1, values=["Promoter",
                                             "RBS",
                                             "CDS",
                                             "Terminator",
                                             "Signal peptide",
                                             "Other", ])
part_role_combo.grid(column=1, row=9)

# Part description entry
part_description_label = tk.Label(tab1, text="Enter a part description")
part_description_label.grid(column=0, row=11)

part_description_entry = tk.Entry(tab1)
part_description_entry.grid(column=1, row=11)


# Select GenBank file for conversion
def select_genbank_file():
    window.filename = filedialog.askopenfilename(initialdir=str(sys.argv[0]), title="select file",
                                                 filetypes=(("GenBank Files (gb)", "*.gb"), ("all files", "*.*")))
    global genbank_file
    genbank_file = window.filename


# Successful conversion label
def successful_conversion():
    global successful_conversion_label
    successful_conversion_label = tk.Label(tab1, font=(None, 10), fg="green", text="Genbank file converted successfully"
                                           )
    successful_conversion_label.grid(column=1, row=16)


# Part creation failed error message
def part_creation_success():
    global creation_success_label
    creation_success_label = tk.Label(tab1, font=(None, 10), fg="green", text="Part created and saved successfully")
    creation_success_label.grid(column=1, row=16)


def part_creation_failure():
    global creation_failure_label
    creation_failure_label = tk.Label(tab1, font=(None, 10), fg="red", text="Part creation failed, part not saved")
    creation_failure_label.grid(column=1, row=16)


# Error message for no identifier input
def identifier_error():
    global identifier_error_label
    identifier_error_label = tk.Label(tab1, font=(None, 8), fg="red", text="Please enter a valid identifier")
    identifier_error_label.grid(column=1, row=6)


# Error message for no part name input
def part_name_error():
    global part_name_error_label
    part_name_error_label = tk.Label(tab1, font=(None, 8), fg="red", text="Please enter a valid part name")
    part_name_error_label.grid(column=1, row=4)


# Error message for no dna input
def dna_error():
    global dna_error_label
    dna_error_label = tk.Label(tab1, font=(None, 8), fg="red", text="Please enter a valid DNA sequence")
    dna_error_label.grid(column=1, row=2)


# Error message for no role input
def part_role_error():
    global role_error_label
    role_error_label = tk.Label(tab1, font=(None, 8), fg="red", text="Please select a valid part role")
    role_error_label.grid(column=1, row=8)


# Error message for no description input
def part_description_error():
    global description_error_label
    description_error_label = tk.Label(tab1, font=(None, 8), fg="red", text="Please enter a valid part description")
    description_error_label.grid(column=1, row=10)


# Wipes current error and success labels (if present) from GUI
def refresh_gui_part_creation(event):
    try:
        successful_conversion_label.grid_forget()
    except NameError:
        pass
    try:
        identifier_error_label.grid_forget()
    except NameError:
        pass
    try:
        part_name_error_label.grid_forget()
    except NameError:
        pass
    try:
        dna_error_label.grid_forget()
    except NameError:
        pass
    try:
        role_error_label.grid_forget()
    except NameError:
        pass
    try:
        description_error_label.grid_forget()
    except NameError:
        pass
    try:
        creation_success_label.grid_forget()
    except NameError:
        pass
    try:
        creation_failure_label.grid_forget()
    except NameError:
        pass
    Part_Creation.save_created_part("<Button-1>")


# Create part button
create_part_button = tk.Button(tab1, text="Create part")
create_part_button.bind("<Button-1>", refresh_gui_part_creation)
create_part_button.grid(column=1, row=13)


# Popup dialog box for saving of created part
def save_part_popup():
    window.filename = filedialog.asksaveasfilename(initialdir=str(os.getcwd()) + "\genetic_parts",
                                                   initialfile=Part_Creation.part_name, title="select file",
                                                   filetypes=(("SBOL files (xml)", "*.xml"), ("all files", "*.*")))
    if not window.filename:
        return False
    else:
        return window.filename


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


############################# MoClo GUI ##############################################

# Selection of design to import
def select_design_import():
    window.filename = filedialog.askopenfilename(initialdir=str(sys.argv[0]), title="select file",
                                                 filetypes=(("xml files", "*.xml"), ("all files", "*.*")))
    global single_imported_design
    single_imported_design = window.filename


# tab title
moclo_title = tk.Label(tab4, text="MoClo assembly", font=(None, 15))
moclo_title.grid(column=0, row=0, columnspan=4, sticky="e")

# Import design button for MoClo tab
import_design_button_moclo = tk.Button(tab4, text="Import Design")
import_design_button_moclo.bind("<Button-1>", MoClo.import_design)
import_design_button_moclo.grid(column=0, row=1, sticky="e")


# Refresh display canvas in MoClo tab
def refresh_canvas_moclo():
    try:
        design_canvas_display_moclo.grid_forget()
    except NameError:
        pass
    display_canvas_moclo()


# Function to create design display canvas in MoClo tab
def display_canvas_moclo():
    global design_canvas_display_moclo
    design_canvas_display_moclo = tk.Canvas(tab4, width=1000, height=150)
    design_canvas_display_moclo.grid(column=0, row=2, columnspan=1000)


# Create design display in MoClo tab
def display_assembled_design_moclo(SO_list):
    counter = 0
    design_canvas_display_moclo.create_text(100, 60, font=("Arial", "11", "bold"), text="Design structure:")
    for x in SO_list:
        counter = counter + 1
        if "0000167" in x:
            design_canvas_display_moclo.create_image(counter * 70, 100, image=promoter_glyph)
            design_canvas_display_moclo.create_text(counter * 70, 140, font=("arial", "8"),
                                                    text=MoClo.primary_structure_identities[counter - 1])
        elif "0000139" in x:
            design_canvas_display_moclo.create_image(counter * 70, 100, image=rbs_glyph)
            design_canvas_display_moclo.create_text(counter * 70, 140, font=("arial", "8"),
                                                    text=MoClo.primary_structure_identities[counter - 1])
        elif "0000316" in x:
            design_canvas_display_moclo.create_image(counter * 70, 100, image=cds_glyph)
            design_canvas_display_moclo.create_text(counter * 70, 140, font=("arial", "8"),
                                                    text=MoClo.primary_structure_identities[counter - 1])
        elif "0000141" in x:
            design_canvas_display_moclo.create_image(counter * 70, 100, image=terminator_glyph)
            design_canvas_display_moclo.create_text(counter * 70, 140, font=("arial", "8"),
                                                    text=MoClo.primary_structure_identities[counter - 1])
        else:
            design_canvas_display_moclo.create_image(counter * 70, 100, image=other_glyph)
            design_canvas_display_moclo.create_text(counter * 70, 140, font=("arial", "8"),
                                                    text=MoClo.primary_structure_identities[counter - 1])


# Create part description button in moclo tab
def create_description_button_moclo():
    global part_description_button_moclo
    try:
        part_description_button_moclo.grid_forget()
        hide_part_description_button_moclo.grid_forget()
        part_description_button_moclo = tk.Button(tab4, text="Show part descriptions")
        part_description_button_moclo.bind("<Button-1>", part_description_moclo)
        part_description_button_moclo.grid(column=1, row=3)
        counter = 0
        for description in MoClo.primary_structure_descriptions:
            counter = counter + 1
            part_description_button_name = "part_key_description" + "_" + str(counter) + "button"
            globals()[part_description_button_name].grid_forget()
    except KeyError:
        part_description_button_moclo.grid_forget()
        hide_part_description_button_moclo.grid_forget()
        part_description_button_moclo = tk.Button(tab4, text="Show part descriptions")
        part_description_button_moclo.bind("<Button-1>", part_description_moclo)
        part_description_button_moclo.grid(column=1, row=3)
    except NameError:
        part_description_button_moclo = tk.Button(tab4, text="Show part descriptions")
        part_description_button_moclo.bind("<Button-1>", part_description_moclo)
        part_description_button_moclo.grid(column=1, row=3)


# Show part description in moclo tab
def part_description_moclo(event):
    counter = 0
    for description in MoClo.primary_structure_descriptions:
        counter = counter + 1
        part_description_button_name = "part_key_description" + "_" + str(counter) + "button"
        globals()[part_description_button_name] = tk.Label(tab4, text=str(
            MoClo.primary_structure_identities[counter - 1]) + " - " + description)
        globals()[part_description_button_name].grid(column=1, row=3 + counter)
    hide_description_button_moclo()


# Button for hiding part descriptions in moclo tab
def hide_description_button_moclo():
    part_description_button_moclo.grid_forget()
    global hide_part_description_button_moclo
    hide_part_description_button_moclo = tk.Button(tab4, text="Hide part descriptions")
    hide_part_description_button_moclo.bind("<Button-1>", hide_description_moclo)
    hide_part_description_button_moclo.grid(column=1, row=3)


# Hiding part descriptions in moclo tab
def hide_description_moclo(event):
    counter = 0
    for description in MoClo.primary_structure_descriptions:
        counter = counter + 1
        part_description_button_name = "part_key_description" + "_" + str(counter) + "button"
        globals()[part_description_button_name].grid_forget()
    hide_part_description_button_moclo.grid_forget()
    part_description_button_moclo.grid(column=1, row=3)


# Create analysis button moclo tab
def create_analysis_button_moclo():
    global design_analysis_button_moclo
    try:
        design_analysis_button_moclo.grid_forget()
        hide_design_analysis_button_moclo.grid_forget()
        design_analysis_button_moclo = tk.Button(tab4, text="Show design analysis")
        design_analysis_button_moclo.bind("<Button-1>", design_analysis_moclo)
        design_analysis_button_moclo.grid(column=2, row=3)
        counter = 0
        for site_detection in MoClo.detected_restriction_sites:
            counter = counter + 1
            design_analysis_label_name = "design_analysis" + "_" + str(counter) + "label"
            globals()[design_analysis_label_name].grid_forget()
        base_composition_moclo.grid_forget()
    except KeyError:
        design_analysis_button_moclo.grid_forget()
        hide_design_analysis_button_moclo.grid_forget()
        design_analysis_button_moclo = tk.Button(tab4, text="Show design analysis")
        design_analysis_button_moclo.bind("<Button-1>", design_analysis_moclo)
        design_analysis_button_moclo.grid(column=2, row=3)
    except NameError:
        design_analysis_button_moclo = tk.Button(tab4, text="Show design analysis")
        design_analysis_button_moclo.bind("<Button-1>", design_analysis_moclo)
        design_analysis_button_moclo.grid(column=2, row=3)


# Show analysis in moclo tab
def design_analysis_moclo(event):
    counter = 0
    for site_detection in MoClo.detected_restriction_sites:
        counter = counter + 1
        design_analysis_label_name = "design_analysis" + "_" + str(counter) + "label"
        globals()[design_analysis_label_name] = tk.Label(tab4, text=str(site_detection))
        globals()[design_analysis_label_name].grid()
        global base_composition_moclo
    base_composition_moclo = tk.Label(tab4, text=MoClo.base_composition)
    base_composition_moclo.grid()
    create_hide_design_analysis_button_moclo()


# Button for hiding analysis in moclo tab
def create_hide_design_analysis_button_moclo():
    design_analysis_button_moclo.grid_forget()
    global hide_design_analysis_button_moclo
    hide_design_analysis_button_moclo = tk.Button(tab4, text="Hide design analysis")
    hide_design_analysis_button_moclo.bind("<Button-1>", hide_analysis_moclo)
    hide_design_analysis_button_moclo.grid(column=2, row=3)


# Hiding analysis in moclo tab
def hide_analysis_moclo(event):
    counter = 0
    for rfc10_detection in MoClo.detected_restriction_sites:
        counter = counter + 1
        design_analysis_label_name = "design_analysis" + "_" + str(counter) + "label"
        globals()[design_analysis_label_name].grid_forget()
    design_analysis_button_moclo.grid()
    base_composition_moclo.grid_forget()
    hide_design_analysis_button_moclo.grid_forget()


# Refresh design parts to level 0 library button
def refresh_design_parts_to_library():
    try:
        design_to_library_button.grid_forget()
    except NameError:
        pass
    design_parts_to_library()


# import design parts to level 0 library button
def design_parts_to_library():
    global design_to_library_button
    design_to_library_button = tk.Button(tab4, text="Import design parts to level 0 library")
    design_to_library_button.bind("<Button-1>", MoClo.import_design_parts_to_library)
    design_to_library_button.grid(column=0, row=3)


# clear level 0 library from GUI
def refresh_level_0_library():
    try:
        promoters_moclo.grid_forget()
    except NameError:
        pass
    try:
        rbs_moclo.grid_forget()
    except NameError:
        pass
    try:
        cds_moclo.grid_forget()
    except NameError:
        pass
    try:
        terminator_moclo.grid_forget()
    except NameError:
        pass
    try:
        other_moclo.grid_forget()
    except NameError:
        pass
    try:
        signal_moclo.grid_forget()
    except NameError:
        pass
    display_level_0_library()


# Display level 0 library
def display_level_0_library():
    global promoters_moclo
    global rbs_moclo
    global cds_moclo
    global terminator_moclo
    global signal_moclo
    global other_moclo
    promoters_moclo = tk.Label(tab4, text=MoClo.level_0_promoter_display)
    rbs_moclo = tk.Label(tab4, text=MoClo.level_0_rbs_display)
    cds_moclo = tk.Label(tab4, text=MoClo.level_0_cds_display)
    terminator_moclo = tk.Label(tab4, text=MoClo.level_0_terminator_display)
    signal_moclo = tk.Label(tab4, text=MoClo.level_0_signal_display)
    other_moclo = tk.Label(tab4, text=MoClo.level_0_other_display)
    promoters_moclo.grid(column=0, row=4)
    rbs_moclo.grid(column=0, row=5)
    cds_moclo.grid(column=0, row=6)
    terminator_moclo.grid(column=0, row=7)
    signal_moclo.grid(column=0, row=8)
    other_moclo.grid(column=0, row=9)


# import part from file button
import_file_button_moclo = tk.Button(tab4, text="import part from file")
import_file_button_moclo.bind("<Button-1>", MoClo.import_part_from_file)
import_file_button_moclo.grid(row=1, column=1, sticky="w")

# Option to include signal peptide label
include_signal_label = tk.Label(tab4, text="Include signal peptide?")
include_signal_label.grid(column=0, row=10)

# Option to include signal peptide combo selection
include_signal_combo = ttk.Combobox(tab4, values=["Yes", "No"])
include_signal_combo.grid(column=0, row=11)

# Select chassis system label
chassis_selection_label = tk.Label(tab4, text="Chassis system")
chassis_selection_label.grid(column=1, row=10)

# Select chassis system combo box
chassis_selection_combo = ttk.Combobox(tab4, values=["E. coli", "B. subtilis"])
chassis_selection_combo.grid(column=1, row=11)

# Label for transcription unit quantity entry
transcription_unit_quantity_label = tk.Label(tab4, text="transcription unit (TU) quantity")
transcription_unit_quantity_label.grid(column=2, row=10)

# Entry for transcription unit quantity
transcription_unit_quantity_combo = ttk.Combobox(tab4, values=["2", "3", "4", "5"])
transcription_unit_quantity_combo.grid(column=2, row=11)


# Create transcription unit entries and labels
def create_transcription_unit_entry(event):
    transcription_unit_quantity = transcription_unit_quantity_combo.get()
    if int(transcription_unit_quantity) > 0:
        transcription_unit_1_label = tk.Label(tab4, text="Transcription unit 1")
        transcription_unit_1_label.grid(column=0, row=13)

        transcription_unit_1_promoter_label = tk.Label(tab4, text="Promoters")
        transcription_unit_1_promoter_label.grid(column=1, row=12)
        global transcription_unit_1_promoter_entry
        transcription_unit_1_promoter_entry = tk.Entry(tab4)
        transcription_unit_1_promoter_entry.grid(column=1, row=13)

        transcription_unit_1_rbs_label = tk.Label(tab4, text="RBSs")
        transcription_unit_1_rbs_label.grid(column=2, row=12)
        global transcription_unit_1_rbs_entry
        transcription_unit_1_rbs_entry = tk.Entry(tab4)
        transcription_unit_1_rbs_entry.grid(column=2, row=13)

        if include_signal_combo.get() == "Yes":
            transcription_unit_1_signal_label = tk.Label(tab4, text="Signal peptides")
            transcription_unit_1_signal_label.grid(column=3, row=12)
            global transcription_unit_1_signal_entry
            transcription_unit_1_signal_entry = tk.Entry(tab4)
            transcription_unit_1_signal_entry.grid(column=3, row=13)

        transcription_unit_1_cds_label = tk.Label(tab4, text="CDSs")
        transcription_unit_1_cds_label.grid(column=4, row=12)
        global transcription_unit_1_cds_entry
        transcription_unit_1_cds_entry = tk.Entry(tab4)
        transcription_unit_1_cds_entry.grid(column=4, row=13)

        transcription_unit_1_terminator_label = tk.Label(tab4, text="Terminators")
        transcription_unit_1_terminator_label.grid(column=5, row=12)
        global transcription_unit_1_terminator_entry
        transcription_unit_1_terminator_entry = tk.Entry(tab4)
        transcription_unit_1_terminator_entry.grid(column=5, row=13)


    else:
        pass
    if int(transcription_unit_quantity) > 1:
        transcription_unit_2_label = tk.Label(tab4, text="Transcription unit 2")
        transcription_unit_2_label.grid(column=0, row=14)

        transcription_unit_2_promoter_label = tk.Label(tab4, text="Promoters")
        transcription_unit_2_promoter_label.grid()
        global transcription_unit_2_promoter_entry
        transcription_unit_2_promoter_entry = tk.Entry(tab4)
        transcription_unit_2_promoter_entry.grid(column=1, row=14)

        transcription_unit_2_rbs_label = tk.Label(tab4, text="RBSs")
        transcription_unit_2_rbs_label.grid()
        global transcription_unit_2_rbs_entry
        transcription_unit_2_rbs_entry = tk.Entry(tab4)
        transcription_unit_2_rbs_entry.grid(column=2, row=14)

        if include_signal_combo.get() == "Yes":
            transcription_unit_2_signal_label = tk.Label(tab4, text="Signal peptides")
            transcription_unit_2_signal_label.grid()
            global transcription_unit_2_signal_entry
            transcription_unit_2_signal_entry = tk.Entry(tab4)
            transcription_unit_2_signal_entry.grid(column=3, row=14)

        transcription_unit_2_cds_label = tk.Label(tab4, text="CDSs")
        transcription_unit_2_cds_label.grid()
        global transcription_unit_2_cds_entry
        transcription_unit_2_cds_entry = tk.Entry(tab4)
        transcription_unit_2_cds_entry.grid(column=4, row=14)

        transcription_unit_2_terminator_label = tk.Label(tab4, text="Terminators")
        transcription_unit_2_terminator_label.grid()
        global transcription_unit_2_terminator_entry
        transcription_unit_2_terminator_entry = tk.Entry(tab4)
        transcription_unit_2_terminator_entry.grid(column=5, row=14)

    else:
        pass
    if int(transcription_unit_quantity) > 2:
        transcription_unit_3_label = tk.Label(tab4, text="Transcription unit 3")
        transcription_unit_3_label.grid()

        transcription_unit_3_promoter_label = tk.Label(tab4, text="Promoters")
        transcription_unit_3_promoter_label.grid()
        global transcription_unit_3_promoter_entry
        transcription_unit_3_promoter_entry = tk.Entry(tab4)
        transcription_unit_3_promoter_entry.grid()

        transcription_unit_3_rbs_label = tk.Label(tab4, text="RBSs")
        transcription_unit_3_rbs_label.grid()
        global transcription_unit_3_rbs_entry
        transcription_unit_3_rbs_entry = tk.Entry(tab4)
        transcription_unit_3_rbs_entry.grid()

        if include_signal_combo.get() == "Yes":
            transcription_unit_3_signal_label = tk.Label(tab4, text="Signal peptides")
            transcription_unit_3_signal_label.grid()
            global transcription_unit_3_signal_entry
            transcription_unit_3_signal_entry = tk.Entry(tab4)
            transcription_unit_3_signal_entry.grid()

        transcription_unit_3_cds_label = tk.Label(tab4, text="CDSs")
        transcription_unit_3_cds_label.grid()
        global transcription_unit_3_cds_entry
        transcription_unit_3_cds_entry = tk.Entry(tab4)
        transcription_unit_3_cds_entry.grid()

        transcription_unit_3_terminator_label = tk.Label(tab4, text="Terminators")
        transcription_unit_3_terminator_label.grid()
        global transcription_unit_3_terminator_entry
        transcription_unit_3_terminator_entry = tk.Entry(tab4)
        transcription_unit_3_terminator_entry.grid()
    else:
        pass
    if int(transcription_unit_quantity) > 3:
        transcription_unit_4_label = tk.Label(tab4, text="Transcription unit 4")
        transcription_unit_4_label.grid()

        transcription_unit_4_promoter_label = tk.Label(tab4, text="Promoters")
        transcription_unit_4_promoter_label.grid()
        global transcription_unit_4_promoter_entry
        transcription_unit_4_promoter_entry = tk.Entry(tab4)
        transcription_unit_4_promoter_entry.grid()

        transcription_unit_4_rbs_label = tk.Label(tab4, text="RBSs")
        transcription_unit_4_rbs_label.grid()
        global transcription_unit_4_rbs_entry
        transcription_unit_4_rbs_entry = tk.Entry(tab4)
        transcription_unit_4_rbs_entry.grid()

        if include_signal_combo.get() == "Yes":
            transcription_unit_4_signal_label = tk.Label(tab4, text="Signal peptides")
            transcription_unit_4_signal_label.grid()
            global transcription_unit_4_signal_entry
            transcription_unit_4_signal_entry = tk.Entry(tab4)
            transcription_unit_4_signal_entry.grid()

        transcription_unit_4_cds_label = tk.Label(tab4, text="CDSs")
        transcription_unit_4_cds_label.grid()
        global transcription_unit_4_cds_entry
        transcription_unit_4_cds_entry = tk.Entry(tab4)
        transcription_unit_4_cds_entry.grid()

        transcription_unit_4_terminator_label = tk.Label(tab4, text="Terminators")
        transcription_unit_4_terminator_label.grid()
        global transcription_unit_4_terminator_entry
        transcription_unit_4_terminator_entry = tk.Entry(tab4)
        transcription_unit_4_terminator_entry.grid()

    else:
        pass
    if int(transcription_unit_quantity) > 4:
        transcription_unit_5_label = tk.Label(tab4, text="Transcription unit 5")
        transcription_unit_5_label.grid()

        transcription_unit_5_promoter_label = tk.Label(tab4, text="Promoters")
        transcription_unit_5_promoter_label.grid()
        global transcription_unit_5_promoter_entry
        transcription_unit_5_promoter_entry = tk.Entry(tab4)
        transcription_unit_5_promoter_entry.grid()

        transcription_unit_5_rbs_label = tk.Label(tab4, text="RBSs")
        transcription_unit_5_rbs_label.grid()
        global transcription_unit_5_rbs_entry
        transcription_unit_5_rbs_entry = tk.Entry(tab4)
        transcription_unit_5_rbs_entry.grid()

        if include_signal_combo.get() == "Yes":
            transcription_unit_5_signal_label = tk.Label(tab4, text="Signal peptides")
            transcription_unit_5_signal_label.grid()
            global transcription_unit_5_signal_entry
            transcription_unit_5_signal_entry = tk.Entry(tab4)
            transcription_unit_5_signal_entry.grid()

        transcription_unit_5_cds_label = tk.Label(tab4, text="CDSs")
        transcription_unit_5_cds_label.grid()
        global transcription_unit_5_cds_entry
        transcription_unit_5_cds_entry = tk.Entry(tab4)
        transcription_unit_5_cds_entry.grid()

        transcription_unit_5_terminator_label = tk.Label(tab4, text="Terminators")
        transcription_unit_5_terminator_label.grid()
        global transcription_unit_5_terminator_entry
        transcription_unit_5_terminator_entry = tk.Entry(tab4)
        transcription_unit_5_terminator_entry.grid()

    else:
        pass
    create_protocol_button()


# Create transcription unit entries and labels button
transcription_unit_create = tk.Button(tab4, text="Create")
transcription_unit_create.bind("<Button-1>", create_transcription_unit_entry)
transcription_unit_create.grid(column=4, row=11)

# Automatic/Manual selection
assembly_method_label = tk.Label(tab4, text="Assembly method")
assembly_method_label.grid(column=3, row=10)
assembly_method_combo = ttk.Combobox(tab4, values=["Automatic", "Manual"])
assembly_method_combo.grid(column=3, row=11)


def create_protocol_button():
    create_protocol_button = tk.Button(tab4, text="Create protocol")
    create_protocol_button.bind("<Button-1>", MoClo.create_protocol_directory)
    create_protocol_button.grid()


def restriction_site_warning_ecoflex():
    counter = 0
    for warning in MoClo.ecoflex_check_list:
        counter = counter + 1
        warning_label_name = "warning" + "_" + str(counter)
        globals()[warning_label_name] = tk.Label(tab4, font=(None, 8), fg="red", text=warning)
        globals()[warning_label_name].grid()
    from EcoFlex_protocol import create_protocol
    global continue_button
    continue_button = tk.Button(tab4, text="Continue with creation")
    continue_button.bind("<Button-1>", create_protocol)
    continue_button.grid()
    global stop_button
    stop_button = tk.Button(tab4, text="Stop")
    stop_button.bind("<Button-1>", remove_warnings)
    stop_button.grid()


def remove_warnings(event):
    continue_button.grid_forget()
    stop_button.grid_forget()
    counter = 0
    for warning in MoClo.ecoflex_check_list:
        counter = counter + 1
        warning_label_name = "warning" + "_" + str(counter)
        globals()[warning_label_name].grid_forget()


################ Main_loop #################
window.mainloop()
