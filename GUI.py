# Import libraries
import sys
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from sbol import *
import os
import tkinter.scrolledtext as st

# Import scripts
import Genetic_Design
import Part_Creation
import Main
import MoClo

# Global variables
design_display_list = []
doc = Document()

################### General_GUI ########################
# Creating GUI window
window = tk.Tk()
window.title("SynBioMate")
window.geometry("1200x950")

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
        self.master.title("SynBioMate")

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
        print("placeholder")


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
        igem = PartShop('https://synbiohub.org')
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
    doc.read(str(selected_file))
    doc.displayId = collection_id.get()
    doc.name = collection_name.get()
    doc.description = collection_description.get()
    doc.submit(doc)
    successful_upload_label = tk.Label(upload_window, text="File uploaded")
    successful_upload_label.pack()


################### Create part GUI ###################################################################################
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

part_role_combo = ttk.Combobox(tab1, state="readonly", values=["Promoter",
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

# Failed conversion label
def conversion_failure():
    global failed_conversion_label
    failed_conversion_label = tk.Label(tab1, font=(None, 10), fg="red", text="Genbank file conversion failed")
    failed_conversion_label.grid(column=1, row=16)


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
def refresh_gui_part_creation():
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
    try:
        failed_conversion_label.grid_forget()
    except NameError:
        pass



# Create part
def create_part(event):
    refresh_gui_part_creation()
    Part_Creation.save_created_part("<Button-1>")


# Create part button
create_part_button = tk.Button(tab1, text="Create part")
create_part_button.bind("<Button-1>", create_part)
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


###################### Genetic_Design GUI #############################################################################

# Title of Genetic Design assembly tab
designassemblytitle = tk.Label(tab2, text="Create Genetic Design", font=(None, 15))
designassemblytitle.grid(row=0, column=0)

# Clear all button
clear_all_design = tk.Button(tab2, fg="red", text="Clear all")
clear_all_design.bind("<Button-1>", Genetic_Design.clear_all_genetic_design)
clear_all_design.grid(row=1, column=0)


# Canvas for design display in Genetic Design tab
def genetic_design_display_canvas():
    global design_canvas_display
    design_canvas_display = tk.Canvas(tab2, width=1000, height=150)
    design_canvas_display.grid(columnspan=5000, row=15)


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


# import parts and designs title
import_parts_and_designs_label = tk.Label(tab2, font=("Arial", "12", "bold"), text="Import parts and designs")
import_parts_and_designs_label.grid(row=2, column=1)

# Import from file title
import_from_file_label = tk.Label(tab2, font=("Arial", "10", "bold"), text="Import from file")
import_from_file_label.grid(row=4, column=0)

# Import SBOL file button
import_part_from_file = tk.Button(tab2, text="Import SBOL file")
import_part_from_file.bind("<Button-1>", Genetic_Design.add_file_part)
import_part_from_file.grid(row=6, column=0)

# Import from synbiohub title
import_from_database_label = tk.Label(tab2, font=("Arial", "10", "bold"), text="Import from SynBioHub")
import_from_database_label.grid(row=4, column=2)

# Query submission label and entry widget
query_request_label = tk.Label(tab2, text="Please enter a search term")
query_request_label.grid(row=6, column=2)
query_request_entry = tk.Entry(tab2)
query_request_entry.grid(row=8, column=2)

# Query submit button
query_submit_button = tk.Button(tab2, text="Submit")
query_submit_button.bind("<Button-1>", Genetic_Design.query_submit)
query_submit_button.grid(row=9, column=2)


# Clear query button
def create_clear_query_button():
    global clear_query_button
    clear_query_button = tk.Button(tab2, fg="red", text="Clear query")
    clear_query_button.bind("<Button-1>", clear_all_query)
    clear_query_button.grid(row=9, column=1)


# Button to show part descriptions in genetic design tab
def create_description_button_design():
    global part_description_button_design
    try:
        part_description_button_design.grid_forget()
        hide_part_description_button_design.grid_forget()
        hide_description_design("<Button-1>")
        part_description_button_design = tk.Button(tab2, text="Show part descriptions")
        part_description_button_design.bind("<Button-1>", part_description_design)
        part_description_button_design.grid(row=16, column=0)
    except KeyError:
        part_description_button_design.grid_forget()
        hide_part_description_button_design.grid_forget()
        part_description_button_design = tk.Button(tab2, text="Show part descriptions")
        part_description_button_design.bind("<Button-1>", part_description_design)
        part_description_button_design.grid(row=16, column=0)
    except NameError:
        part_description_button_design = tk.Button(tab2, text="Show part descriptions")
        part_description_button_design.bind("<Button-1>", part_description_design)
        part_description_button_design.grid(row=16, column=0)


# Show part description in genetic design tab
def part_description_design(event):
    global description_frame
    counter = 0
    try:
        description_frame.grid_forget()
    except NameError:
        pass
    description_frame = tk.Frame(tab2)
    for description in Genetic_Design.design_descriptions:
        counter = counter + 1
        part_description_button_name = "part_key_description" + "_" + str(counter) + "button"
        globals()[part_description_button_name] = tk.Label(description_frame, text=str(
            Genetic_Design.design_identities[counter - 1]) + " - " + description)
        globals()[part_description_button_name].grid()
    description_frame.grid(row=17, column=0)
    hide_description_button_design()


# Button for hiding part descriptions in genetic design tab
def hide_description_button_design():
    part_description_button_design.grid_forget()
    global hide_part_description_button_design
    hide_part_description_button_design = tk.Button(tab2, text="Hide part descriptions")
    hide_part_description_button_design.bind("<Button-1>", hide_description_design)
    hide_part_description_button_design.grid(row=16, column=0)


# Hiding part descriptions in genetic design tab
def hide_description_design(event):
    description_frame.grid_forget()
    counter = 0
    for description in Genetic_Design.design_descriptions:
        counter = counter + 1
        part_description_button_name = "part_key_description" + "_" + str(counter) + "button"
        globals()[part_description_button_name].grid_forget()
    part_description_button_design.grid(row=16, column=0)
    hide_part_description_button_design.grid_forget()


# Part from file selection
def part_file_selection(event):
    window.filename = filedialog.askopenfilename(initialdir=str(sys.argv[0]), title="select file",
                                                 filetypes=(("SBOL files (.xml)", "*.xml"), ("all files", "*.*")))
    global imported_part
    imported_part = window.filename


# GUI binding of writing queried part to doc
def part_choice_button_1():
    global query_result_button_1
    query_result_button_1 = tk.Button(tab2, text=Genetic_Design.button_1_display)
    query_result_button_1.bind("<Button-1>", Genetic_Design.query_to_doc_1)
    query_result_button_1.grid(column=1, row=10, )


def part_choice_button_2():
    global query_result_button_2
    query_result_button_2 = tk.Button(tab2, text=Genetic_Design.button_2_display)
    query_result_button_2.bind("<Button-1>", Genetic_Design.query_to_doc_2)
    query_result_button_2.grid(column=1, row=11)


def part_choice_button_3():
    global query_result_button_3
    query_result_button_3 = tk.Button(tab2, text=Genetic_Design.button_3_display)
    query_result_button_3.bind("<Button-1>", Genetic_Design.query_to_doc_3)
    query_result_button_3.grid(column=1, row=12)


def part_choice_button_4():
    global query_result_button_4
    query_result_button_4 = tk.Button(tab2, text=Genetic_Design.button_4_display)
    query_result_button_4.bind("<Button-1>", Genetic_Design.query_to_doc_4)
    query_result_button_4.grid(column=1, row=13)


def part_choice_button_5():
    global query_result_button_5
    query_result_button_5 = tk.Button(tab2, text=Genetic_Design.button_5_display)
    query_result_button_5.bind("<Button-1>", Genetic_Design.query_to_doc_5)
    query_result_button_5.grid(column=1, row=14)


def part_choice_button_6():
    global query_result_button_6
    query_result_button_6 = tk.Button(tab2, text=Genetic_Design.button_6_display)
    query_result_button_6.bind("<Button-1>", Genetic_Design.query_to_doc_6)
    query_result_button_6.grid(column=2, row=10)


def part_choice_button_7():
    global query_result_button_7
    query_result_button_7 = tk.Button(tab2, text=Genetic_Design.button_7_display)
    query_result_button_7.bind("<Button-1>", Genetic_Design.query_to_doc_7)
    query_result_button_7.grid(column=2, row=11)


def part_choice_button_8():
    global query_result_button_8
    query_result_button_8 = tk.Button(tab2, text=Genetic_Design.button_8_display)
    query_result_button_8.bind("<Button-1>", Genetic_Design.query_to_doc_8)
    query_result_button_8.grid(column=2, row=12)


def part_choice_button_9():
    global query_result_button_9
    query_result_button_9 = tk.Button(tab2, text=Genetic_Design.button_9_display)
    query_result_button_9.bind("<Button-1>", Genetic_Design.query_to_doc_9)
    query_result_button_9.grid(column=2, row=13)


def part_choice_button_10():
    global query_result_button_10
    query_result_button_10 = tk.Button(tab2, text=Genetic_Design.button_10_display)
    query_result_button_10.bind("<Button-1>", Genetic_Design.query_to_doc_10)
    query_result_button_10.grid(column=2, row=14)


def clear_all_query(event):
    try:
        clear_query_button.grid_forget()
    except NameError:
        pass
    try:
        query_result_button_1.grid_forget()
    except NameError:
        return
    try:
        query_result_button_2.grid_forget()
    except NameError:
        return
    try:
        query_result_button_3.grid_forget()
    except NameError:
        return
    try:
        query_result_button_4.grid_forget()
    except NameError:
        return
    try:
        query_result_button_5.grid_forget()
    except NameError:
        return
    try:
        query_result_button_6.grid_forget()
    except NameError:
        return
    try:
        query_result_button_7.grid_forget()
    except NameError:
        return
    try:
        query_result_button_8.grid_forget()
    except NameError:
        return
    try:
        query_result_button_9.grid_forget()
    except NameError:
        return
    try:
        query_result_button_10.grid_forget()
    except NameError:
        return


# Assembly title
assembly_title = tk.Label(tab2, font=("Arial", "11", "bold"), text="Assemble Design")
assembly_title.grid(column=1, row=18, pady=(80, 0))

# Genetic Design assembly entry label
name_design_label = tk.Label(tab2, text="Please enter the name of your genetic design")
name_design_label.grid(column=1, row=19)

# Design assembly name entry
design_name_entry = tk.Entry(tab2)
design_name_entry.grid(column=1, row=21)

# Genetic Design assembly button
design_assembly_button = tk.Button(tab2, text="Assemble Design")
design_assembly_button.bind("<Button-1>", Genetic_Design.design_assembly)
design_assembly_button.grid(column=1, row=22)


# Select save destination for assembled design
def select_save_destination_assembly():
    window.filename = filedialog.asksaveasfilename(initialdir=str(os.getcwd()) + "\genetic_designs",
                                                   initialfile=design_name_entry.get(), title="select file",
                                                   filetypes=(("SBOL files (xml)", "*.xml"), ("all files", "*.*")))
    if not window.filename:
        return False
    else:
        return window.filename


# Failed assembly error
def failed_assembly():
    global failed_assembly_label
    failed_assembly_label = tk.Label(tab2, font=(None, 10), fg="red", text="Assembly failed")
    failed_assembly_label.grid(column=1, row=20)


# Successful assembly error
def successful_assembly():
    global successful_assembly_label
    successful_assembly_label = tk.Label(tab2, font=(None, 10), fg="green", text="Assembly Successful")
    successful_assembly_label.grid(column=1, row=20)


# Enter a design name error
def design_name_error():
    global design_name_error_label
    design_name_error_label = tk.Label(tab2, font=(None, 10), fg="red", text="Please enter a design name")
    design_name_error_label.grid(column=1, row=20)


# Only a single import error
def assembly_import_error():
    global assembly_import_error_label
    assembly_import_error_label = tk.Label(tab2, font=(None, 10), fg="red",
                                           text="Assembly requires a minimum of two previously unassembled "
                                                "parts/designs")
    assembly_import_error_label.grid(column=1, row=20)


# No sequence constraints error
def no_sequence_constraints():
    global no_sequence_constraints_label
    no_sequence_constraints_label = tk.Label(tab2, font=(None, 10), fg="red",
                                             text="SBOL import failed, the specified SBOL file contains parts with no "
                                                  "sequence "
                                                  "constraints")
    no_sequence_constraints_label.grid(row=3, column=0, columnspan=10)


# Multiple primary structures error
def multiple_primary_structures():
    global multiple_primary_structures_label
    multiple_primary_structures_label = tk.Label(tab2, font=(None, 10), fg="red",
                                                 text="SBOL import failed, this softwares assembly tool does not "
                                                      "currently support "
                                                      "designs with multiple primary structures")
    multiple_primary_structures_label.grid(row=3, column=0, columnspan=10)


# No search term error
def query_search_error():
    global query_search_error_label
    query_search_error_label = tk.Label(tab2, font=(None, 10), fg="red", text="Please enter a valid search term")
    query_search_error_label.grid(row=7, column=2)


# Import failed
def import_failed_error():
    global import_failed_error_label
    import_failed_error_label = tk.Label(tab2, font=(None, 10), fg="red", text="Import failed")
    import_failed_error_label.grid(row=5, column=0)


# Unused components error
def unused_components_error():
    global unused_components_error_label
    unused_components_error_label = tk.Label(tab2, font=(None, 10), fg="red",
                                             text="SBOL import failed, the specified SBOL file contains multiple "
                                                  "parts but has no design structure")
    unused_components_error_label.grid(row=3, column=0, columnspan=10)


# Error for importing a design
def design_import_error():
    global design_import_error_label
    design_import_error_label = tk.Label(tab2, font=(None, 10), fg="red", text="This software does not currently "
                                                                               "support assembly with existing designs")
    design_import_error_label.grid(row=3, column=0, columnspan=10)


# Clear all error and success labels in design tab
def clear_all_notes_design():
    try:
        design_import_error_label.grid_forget()
    except NameError:
        pass
    try:
        failed_assembly_label.grid_forget()
    except NameError:
        pass
    try:
        successful_assembly_label.grid_forget()
    except NameError:
        pass
    try:
        design_name_error_label.grid_forget()
    except NameError:
        pass
    try:
        assembly_import_error_label.grid_forget()
    except NameError:
        pass
    try:
        no_sequence_constraints_label.grid_forget()
    except NameError:
        pass
    try:
        multiple_primary_structures_label.grid_forget()
    except NameError:
        pass
    try:
        query_search_error_label.grid_forget()
    except NameError:
        pass
    try:
        import_failed_error_label.grid_forget()
    except NameError:
        pass
    try:
        unused_components_error_label.grid_forget()
    except NameError:
        pass


# Clear descriptions and description button from GUI
def clear_descriptions_design():
    global design_canvas_display
    global hide_part_description_button_design
    global part_description_button_design
    try:
        design_canvas_display.delete("all")
    except NameError:
        pass
    try:
        hide_part_description_button_design.grid_forget()
    except NameError:
        pass
    try:
        hide_description_design("<Button-1>")
    except NameError:
        pass
    except KeyError:
        pass
    try:
        part_description_button_design.grid_forget()
    except NameError:
        pass
    try:
        del part_description_button_design
    except NameError:
        pass
    try:
        del hide_part_description_button_design
    except NameError:
        pass


############################# MoClo GUI ###############################################################################

# Selection of design to import
def select_design_import():
    window.filename = filedialog.askopenfilename(initialdir=str(sys.argv[0]), title="select file",
                                                 filetypes=(("xml files", "*.xml"), ("all files", "*.*")))
    global single_imported_design
    single_imported_design = window.filename


# tab title
moclo_title = tk.Label(tab4, text="MoClo assembly", font=(None, 15))
moclo_title.grid(column=0, row=0, columnspan=4)

# Import design button for MoClo tab
import_design_button_moclo = tk.Button(tab4, text="Import SBOL file")
import_design_button_moclo.bind("<Button-1>", MoClo.import_design)
import_design_button_moclo.grid(column=0, row=2)


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
    design_canvas_display_moclo.grid(column=0, row=3, columnspan=1000)


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
        part_description_button_moclo.grid(column=1, row=4)
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
        part_description_button_moclo.grid(column=1, row=4)
    except NameError:
        part_description_button_moclo = tk.Button(tab4, text="Show part descriptions")
        part_description_button_moclo.bind("<Button-1>", part_description_moclo)
        part_description_button_moclo.grid(column=1, row=4)


# Show part description in moclo tab
def part_description_moclo(event):
    global description_frame_moclo
    counter = 0
    try:
        description_frame_moclo.grid_forget()
    except NameError:
        pass
    description_frame_moclo = tk.Frame(tab4)
    for description in MoClo.primary_structure_descriptions:
        counter = counter + 1
        part_description_button_name = "part_key_description" + "_" + str(counter) + "button"
        globals()[part_description_button_name] = tk.Label(description_frame_moclo, text=str(
            MoClo.primary_structure_identities[counter - 1]) + " - " + description)
        globals()[part_description_button_name].grid(column=1, row=3 + counter)
    description_frame_moclo.grid(column=1, row=5, sticky="w")
    hide_description_button_moclo()


# Button for hiding part descriptions in moclo tab
def hide_description_button_moclo():
    part_description_button_moclo.grid_forget()
    global hide_part_description_button_moclo
    hide_part_description_button_moclo = tk.Button(tab4, text="Hide part descriptions")
    hide_part_description_button_moclo.bind("<Button-1>", hide_description_moclo)
    hide_part_description_button_moclo.grid(column=1, row=4)


# Hiding part descriptions in moclo tab
def hide_description_moclo(event):
    global description_frame_moclo
    description_frame_moclo.grid_forget()
    counter = 0
    for description in MoClo.primary_structure_descriptions:
        counter = counter + 1
        part_description_button_name = "part_key_description" + "_" + str(counter) + "button"
        globals()[part_description_button_name].grid_forget()
    hide_part_description_button_moclo.grid_forget()
    part_description_button_moclo.grid(column=1, row=4)


# Create analysis button moclo tab
def create_analysis_button_moclo():
    global design_analysis_button_moclo
    try:
        design_analysis_button_moclo.grid_forget()
        hide_design_analysis_button_moclo.grid_forget()
        design_analysis_button_moclo = tk.Button(tab4, text="Show design analysis")
        design_analysis_button_moclo.bind("<Button-1>", design_analysis_moclo)
        design_analysis_button_moclo.grid(column=2, row=4)
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
        design_analysis_button_moclo.grid(column=2, row=4)
    except NameError:
        design_analysis_button_moclo = tk.Button(tab4, text="Show design analysis")
        design_analysis_button_moclo.bind("<Button-1>", design_analysis_moclo)
        design_analysis_button_moclo.grid(column=2, row=4)


# Show analysis in moclo tab
def design_analysis_moclo(event):
    global design_analysis_frame
    counter = 0
    try:
        design_analysis_frame.grid_forget()
    except NameError:
        pass
    design_analysis_frame = tk.Frame(tab4)

    for site_detection in MoClo.detected_restriction_sites:
        counter = counter + 1
        design_analysis_label_name = "design_analysis" + "_" + str(counter) + "label"
        globals()[design_analysis_label_name] = tk.Label(design_analysis_frame, text=str(site_detection))
        globals()[design_analysis_label_name].grid()
        global base_composition_moclo
    base_composition_moclo = tk.Label(design_analysis_frame, text=MoClo.base_composition)
    base_composition_moclo.grid()
    design_analysis_frame.grid(column=2, row=5)
    create_hide_design_analysis_button_moclo()


# Button for hiding analysis in moclo tab
def create_hide_design_analysis_button_moclo():
    design_analysis_button_moclo.grid_forget()
    global hide_design_analysis_button_moclo
    hide_design_analysis_button_moclo = tk.Button(tab4, text="Hide design analysis")
    hide_design_analysis_button_moclo.bind("<Button-1>", hide_analysis_moclo)
    hide_design_analysis_button_moclo.grid(column=2, row=4)


# Hiding analysis in moclo tab
def hide_analysis_moclo(event):
    global design_analysis_frame
    design_analysis_frame.grid_forget()
    counter = 0
    for rfc10_detection in MoClo.detected_restriction_sites:
        counter = counter + 1
        design_analysis_label_name = "design_analysis" + "_" + str(counter) + "label"
        globals()[design_analysis_label_name].grid_forget()
    design_analysis_button_moclo.grid(column=2, row=4)
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
    design_to_library_button.grid(column=0, row=4)


# clear level 0 library from GUI
def refresh_level_0_library():
    try:
        level_0_library_frame.grid_forget()
    except NameError:
        pass
    display_level_0_library()


# Display level 0 library
def display_level_0_library():
    global level_0_library_frame
    global promoters_moclo
    global rbs_moclo
    global cds_moclo
    global terminator_moclo
    global signal_moclo
    global other_moclo

    try:
        level_0_library_frame.grid_forget()
    except NameError:
        pass

    level_0_library_frame = tk.Frame(tab4)

    level_0_library_title = tk.Label(level_0_library_frame, font=("Arial", "10", "bold"), text="level 0 library:")
    level_0_library_title.grid(column=0, row=1)

    promoter_display = []
    for component in MoClo.level_0_promoter:
        promoter_display.append(component + ". " + MoClo.level_0_promoter[component].displayId)
    promoters_moclo = tk.Label(level_0_library_frame, text=promoter_display)

    rbs_display = []
    for component in MoClo.level_0_rbs:
        rbs_display.append(component + ". " + MoClo.level_0_rbs[component].displayId)
    rbs_moclo = tk.Label(level_0_library_frame, text=rbs_display)

    cds_display = []
    for component in MoClo.level_0_cds:
        cds_display.append(component + ". " + MoClo.level_0_cds[component].displayId)
    cds_moclo = tk.Label(level_0_library_frame, text=cds_display)

    terminator_display = []
    for component in MoClo.level_0_terminator:
        terminator_display.append(component + ". " + MoClo.level_0_terminator[component].displayId)
    terminator_moclo = tk.Label(level_0_library_frame, text=terminator_display)

    signal_display = []
    for component in MoClo.level_0_signal:
        signal_display.append(component + ". " + MoClo.level_0_signal[component].displayId)
    signal_moclo = tk.Label(level_0_library_frame, text=signal_display)

    other_display = []
    for component in MoClo.level_0_other:
        other_display.append(component + ". " + MoClo.level_0_other[component].displayId)
    other_moclo = tk.Label(level_0_library_frame, text=other_display)

    promoters_moclo.grid(column=0, row=4)
    rbs_moclo.grid(column=0, row=5)
    cds_moclo.grid(column=0, row=6)
    terminator_moclo.grid(column=0, row=7)
    signal_moclo.grid(column=0, row=8)
    other_moclo.grid(column=0, row=9)
    level_0_library_frame.grid(column=0, row=5)


# Move level 0 library parts to different part types
def move_parts_library():
    global part_to_move_entry
    global destination_library_select
    global part_to_move_label
    global destination_library_label
    global part_move_button
    part_to_move_label = tk.Label(tab4, text="Key of part to move (e.g p1 or r3)")
    part_to_move_label.grid(column=0, row=6)
    part_to_move_entry = tk.Entry(tab4)
    part_to_move_entry.grid(column=0, row=8)
    destination_library_label = tk.Label(tab4, text="Destination group")
    destination_library_label.grid(column=1, row=6)
    destination_library_select = ttk.Combobox(tab4, state="readonly",
                                              values=["Promoter (p)", "RBS (r)", "Signal peptide "
                                                                                 "(s)", "Coding "
                                                                                        "region ("
                                                                                        "c)",
                                                      "Terminator (t)", "Other (o)"])
    destination_library_select.grid(column=1, row=8)
    part_move_button = tk.Button(tab4, text="Move")
    part_move_button.bind("<Button-1>", MoClo.move_parts_in_library)
    part_move_button.grid(column=2, row=8, sticky="w")


# Remove stage 1 GUI
def remove_stage_1_GUI():
    include_signal_label.grid_forget()
    include_signal_combo.grid_forget()
    chassis_selection_combo.grid_forget()
    chassis_selection_label.grid_forget()
    transcription_unit_quantity_combo.grid_forget()
    transcription_unit_quantity_label.grid_forget()
    assembly_method_combo.grid_forget()
    assembly_method_label.grid_forget()
    transcription_unit_create.grid_forget()
    level_1_volume_ratio_label.grid_forget()
    level_1_volume_ratio_checkbox_1_1.grid_forget()
    level_1_volume_ratio_checkbox_1_2.grid_forget()
    level_1_volume_ratio_checkbox_2_1.grid_forget()
    level_2_volume_ratio_label.grid_forget()
    level_2_volume_ratio_checkbox_1_1.grid_forget()
    level_2_volume_ratio_checkbox_1_2.grid_forget()
    level_2_volume_ratio_checkbox_2_1.grid_forget()
    include_codon_swap_label.grid_forget()
    include_codon_swap_combo.grid_forget()
    include_fusion_site_label.grid_forget()
    include_fusion_site_combo.grid_forget()
    transcription_unit_create.grid_forget()


# Create transcription unit entries and labels
def stage_2_GUI(event):
    clear_all_errors_moclo()
    parameters_fulfilled = True
    if not include_signal_combo.get():
        combo_error_signal()
        parameters_fulfilled = False
    if not chassis_selection_combo.get():
        combo_error_toolkit()
        parameters_fulfilled = False
    if not transcription_unit_quantity_combo.get():
        combo_error_tu()
        parameters_fulfilled = False
    if not assembly_method_combo.get():
        combo_error_assembly()
        parameters_fulfilled = False
    if not include_codon_swap_combo.get():
        combo_error_cds()
        parameters_fulfilled = False
    if not include_fusion_site_combo.get():
        combo_error_fusion()
        parameters_fulfilled = False

    if parameters_fulfilled:
        remove_stage_1_GUI()
        transcription_unit_quantity = transcription_unit_quantity_combo.get()
        global stage_2_label
        stage_2_label = tk.Label(tab4, font=(None, 12, 'bold'),
                                 text="Please enter keys of desired parts (e.g p1, p2, p3, "
                                      "for promoters)")
        stage_2_label.grid(column=1, row=10, columnspan=5)
        if int(transcription_unit_quantity) > 0:
            global transcription_unit_1_label
            transcription_unit_1_label = tk.Label(tab4, text="Transcription unit 1")
            transcription_unit_1_label.grid(column=0, row=13)

            global transcription_unit_1_promoter_label
            transcription_unit_1_promoter_label = tk.Label(tab4, text="Promoters (p)")
            transcription_unit_1_promoter_label.grid(column=1, row=11)
            global transcription_unit_1_promoter_entry
            transcription_unit_1_promoter_entry = tk.Entry(tab4)
            transcription_unit_1_promoter_entry.grid(column=1, row=13)

            global transcription_unit_1_rbs_label
            transcription_unit_1_rbs_label = tk.Label(tab4, text="RBSs (r)")
            transcription_unit_1_rbs_label.grid(column=2, row=11)
            global transcription_unit_1_rbs_entry
            transcription_unit_1_rbs_entry = tk.Entry(tab4)
            transcription_unit_1_rbs_entry.grid(column=2, row=13)

            if include_signal_combo.get() == "Yes":
                global transcription_unit_1_signal_label
                transcription_unit_1_signal_label = tk.Label(tab4, text="Signal peptides (s)")
                transcription_unit_1_signal_label.grid(column=3, row=11)
                global transcription_unit_1_signal_entry
                transcription_unit_1_signal_entry = tk.Entry(tab4)
                transcription_unit_1_signal_entry.grid(column=3, row=13)

            global transcription_unit_1_cds_label
            transcription_unit_1_cds_label = tk.Label(tab4, text="CDSs (c)")
            transcription_unit_1_cds_label.grid(column=4, row=11)
            global transcription_unit_1_cds_entry
            transcription_unit_1_cds_entry = tk.Entry(tab4)
            transcription_unit_1_cds_entry.grid(column=4, row=13)

            global transcription_unit_1_terminator_label
            transcription_unit_1_terminator_label = tk.Label(tab4, text="Terminators (t)")
            transcription_unit_1_terminator_label.grid(column=5, row=11)
            global transcription_unit_1_terminator_entry
            transcription_unit_1_terminator_entry = tk.Entry(tab4)
            transcription_unit_1_terminator_entry.grid(column=5, row=13)

        if int(transcription_unit_quantity) > 1:
            global transcription_unit_2_label
            transcription_unit_2_label = tk.Label(tab4, text="Transcription unit 2")
            transcription_unit_2_label.grid(column=0, row=15)

            global transcription_unit_2_promoter_entry
            transcription_unit_2_promoter_entry = tk.Entry(tab4)
            transcription_unit_2_promoter_entry.grid(column=1, row=15)

            global transcription_unit_2_rbs_entry
            transcription_unit_2_rbs_entry = tk.Entry(tab4)
            transcription_unit_2_rbs_entry.grid(column=2, row=15)

            if include_signal_combo.get() == "Yes":
                global transcription_unit_2_signal_entry
                transcription_unit_2_signal_entry = tk.Entry(tab4)
                transcription_unit_2_signal_entry.grid(column=3, row=15)

            global transcription_unit_2_cds_entry
            transcription_unit_2_cds_entry = tk.Entry(tab4)
            transcription_unit_2_cds_entry.grid(column=4, row=15)

            global transcription_unit_2_terminator_entry
            transcription_unit_2_terminator_entry = tk.Entry(tab4)
            transcription_unit_2_terminator_entry.grid(column=5, row=15)

        if int(transcription_unit_quantity) > 2:
            global transcription_unit_3_label
            transcription_unit_3_label = tk.Label(tab4, text="Transcription unit 3")
            transcription_unit_3_label.grid(column=0, row=17)

            global transcription_unit_3_promoter_entry
            transcription_unit_3_promoter_entry = tk.Entry(tab4)
            transcription_unit_3_promoter_entry.grid(column=1, row=17)

            global transcription_unit_3_rbs_entry
            transcription_unit_3_rbs_entry = tk.Entry(tab4)
            transcription_unit_3_rbs_entry.grid(column=2, row=17)

            if include_signal_combo.get() == "Yes":
                global transcription_unit_3_signal_entry
                transcription_unit_3_signal_entry = tk.Entry(tab4)
                transcription_unit_3_signal_entry.grid(column=3, row=17)

            global transcription_unit_3_cds_entry
            transcription_unit_3_cds_entry = tk.Entry(tab4)
            transcription_unit_3_cds_entry.grid(column=4, row=17)

            global transcription_unit_3_terminator_entry
            transcription_unit_3_terminator_entry = tk.Entry(tab4)
            transcription_unit_3_terminator_entry.grid(column=5, row=17)

        if int(transcription_unit_quantity) > 3:
            global transcription_unit_4_label
            transcription_unit_4_label = tk.Label(tab4, text="Transcription unit 4")
            transcription_unit_4_label.grid(column=0, row=19)

            global transcription_unit_4_promoter_entry
            transcription_unit_4_promoter_entry = tk.Entry(tab4)
            transcription_unit_4_promoter_entry.grid(column=1, row=19)

            global transcription_unit_4_rbs_entry
            transcription_unit_4_rbs_entry = tk.Entry(tab4)
            transcription_unit_4_rbs_entry.grid(column=2, row=19)

            if include_signal_combo.get() == "Yes":
                global transcription_unit_4_signal_entry
                transcription_unit_4_signal_entry = tk.Entry(tab4)
                transcription_unit_4_signal_entry.grid(column=3, row=19)

            global transcription_unit_4_cds_entry
            transcription_unit_4_cds_entry = tk.Entry(tab4)
            transcription_unit_4_cds_entry.grid(column=4, row=19)

            global transcription_unit_4_terminator_entry
            transcription_unit_4_terminator_entry = tk.Entry(tab4)
            transcription_unit_4_terminator_entry.grid(column=5, row=19)

        if int(transcription_unit_quantity) > 4:
            global transcription_unit_5_label
            transcription_unit_5_label = tk.Label(tab4, text="Transcription unit 5")
            transcription_unit_5_label.grid(column=0, row=21)

            global transcription_unit_5_promoter_entry
            transcription_unit_5_promoter_entry = tk.Entry(tab4)
            transcription_unit_5_promoter_entry.grid(column=1, row=21)

            global transcription_unit_5_rbs_entry
            transcription_unit_5_rbs_entry = tk.Entry(tab4)
            transcription_unit_5_rbs_entry.grid(column=2, row=21)

            if include_signal_combo.get() == "Yes":
                global transcription_unit_5_signal_entry
                transcription_unit_5_signal_entry = tk.Entry(tab4)
                transcription_unit_5_signal_entry.grid(column=3, row=21)

            global transcription_unit_5_cds_entry
            transcription_unit_5_cds_entry = tk.Entry(tab4)
            transcription_unit_5_cds_entry.grid(column=4, row=21)

            global transcription_unit_5_terminator_entry
            transcription_unit_5_terminator_entry = tk.Entry(tab4)
            transcription_unit_5_terminator_entry.grid(column=5, row=21)

        if assembly_method_combo.get() == "Automatic":
            liquid_handler_selection()
        create_create_protocol_button()
        protocol_name_entry_gui()


# Stage 1 GUI
def stage_1_GUI():
    # Option to include signal peptide label
    global include_signal_label
    include_signal_label = tk.Label(tab4, text="Include signal peptide?")
    include_signal_label.grid(column=0, row=10)

    # Option to include signal peptide combo selection
    global include_signal_combo
    include_signal_combo = ttk.Combobox(tab4, state="readonly", values=["Yes", "No"])
    include_signal_combo.grid(column=0, row=12)

    # Select toolkit label
    global chassis_selection_label
    chassis_selection_label = tk.Label(tab4, text="Toolkit")
    chassis_selection_label.grid(column=1, row=10)

    # Select chassis system combo box
    global chassis_selection_combo
    chassis_selection_combo = ttk.Combobox(tab4, state="readonly", values=["EcoFlex"])
    chassis_selection_combo.grid(column=1, row=12)

    # Label for transcription unit quantity entry
    global transcription_unit_quantity_label
    transcription_unit_quantity_label = tk.Label(tab4, text="transcription unit (TU) quantity")
    transcription_unit_quantity_label.grid(column=2, row=10)

    # Entry for transcription unit quantity
    global transcription_unit_quantity_combo
    transcription_unit_quantity_combo = ttk.Combobox(tab4, state="readonly", values=["2", "3", "4", "5"])
    transcription_unit_quantity_combo.grid(column=2, row=12)

    # Protocol design title
    global protocol_design_title
    protocol_design_title = tk.Label(tab4, font=("Arial", "11", "bold"), text="Protocol design")
    protocol_design_title.grid(column=0, row=9, pady=(20, 0))

    # Create stage 2 GUI button
    global transcription_unit_create
    transcription_unit_create = tk.Button(tab4, text="Create")
    transcription_unit_create.bind("<Button-1>", stage_2_GUI)
    transcription_unit_create.grid(column=1, row=21)

    # Automatic/Manual selection
    global assembly_method_label
    assembly_method_label = tk.Label(tab4, text="Assembly method")
    assembly_method_label.grid(column=3, row=10)
    global assembly_method_combo
    assembly_method_combo = ttk.Combobox(tab4, state="readonly", values=["Automatic", "Manual"])
    assembly_method_combo.grid(column=3, row=12)

    # User selection for part:level 1 backbone volume ratio
    global level_1_ratio_1_1
    global level_1_ratio_1_2
    global level_1_ratio_2_1
    level_1_ratio_1_1 = tk.IntVar()
    level_1_ratio_1_2 = tk.IntVar()
    level_1_ratio_2_1 = tk.IntVar()

    global level_1_volume_ratio_label
    level_1_volume_ratio_label = tk.Label(tab4,
                                          text="Part : level 1 backbone reaction volumetric ratios (2:1 is default "
                                               "if none selected, "
                                               "multiple selection is allowed):")
    level_1_volume_ratio_label.grid(column=0, row=16, columnspan=6, sticky="w")
    global level_1_volume_ratio_checkbox_1_1
    global level_1_volume_ratio_checkbox_1_2
    global level_1_volume_ratio_checkbox_2_1
    level_1_volume_ratio_checkbox_1_1 = ttk.Checkbutton(tab4, text="1:1", variable=level_1_ratio_1_1)
    level_1_volume_ratio_checkbox_1_1.grid(column=0, row=17)
    level_1_volume_ratio_checkbox_1_2 = ttk.Checkbutton(tab4, text="1:2", variable=level_1_ratio_1_2)
    level_1_volume_ratio_checkbox_1_2.grid(column=1, row=17)
    level_1_volume_ratio_checkbox_2_1 = ttk.Checkbutton(tab4, text="2:1", variable=level_1_ratio_2_1)
    level_1_volume_ratio_checkbox_2_1.grid(column=2, row=17)

    # User selection for TU: level 2 backbone ratio
    global level_2_ratio_1_1
    global level_2_ratio_1_2
    global level_2_ratio_2_1
    level_2_ratio_1_1 = tk.IntVar()
    level_2_ratio_1_2 = tk.IntVar()
    level_2_ratio_2_1 = tk.IntVar()

    global level_2_volume_ratio_label
    level_2_volume_ratio_label = tk.Label(tab4,
                                          text="TU : level 2 backbone reaction volumetric ratios (2:1 is default if "
                                               "none selected, "
                                               "multiple selection is allowed):")
    level_2_volume_ratio_label.grid(column=0, row=18, columnspan=6, sticky="w")

    global level_2_volume_ratio_checkbox_1_1
    global level_2_volume_ratio_checkbox_1_2
    global level_2_volume_ratio_checkbox_2_1
    level_2_volume_ratio_checkbox_1_1 = ttk.Checkbutton(tab4, text="1:1", variable=level_2_ratio_1_1)
    level_2_volume_ratio_checkbox_1_1.grid(column=0, row=19)
    level_2_volume_ratio_checkbox_1_2 = ttk.Checkbutton(tab4, text="1:2", variable=level_2_ratio_1_2)
    level_2_volume_ratio_checkbox_1_2.grid(column=1, row=19)
    level_2_volume_ratio_checkbox_2_1 = ttk.Checkbutton(tab4, text="2:1", variable=level_2_ratio_2_1)
    level_2_volume_ratio_checkbox_2_1.grid(column=2, row=19)

    # User selection to include codon swap
    global include_codon_swap_label
    global include_codon_swap_combo
    include_codon_swap_label = tk.Label(tab4, text="Substitute CDS restriction sites?")
    include_codon_swap_label.grid(column=0, row=13)
    include_codon_swap_combo = ttk.Combobox(tab4, state="readonly", values=["Yes", "No"])
    include_codon_swap_combo.grid(column=0, row=15)

    # User selection to turn fusion site addition off
    global include_fusion_site_label
    global include_fusion_site_combo
    include_fusion_site_label = tk.Label(tab4, text="Add fusion sites to parts?")
    include_fusion_site_label.grid(column=1, row=13)
    include_fusion_site_combo = ttk.Combobox(tab4, state="readonly", values=["Yes", "No"])
    include_fusion_site_combo.grid(column=1, row=15)


# Initialise stage 1 GUI on startup
stage_1_GUI()


# Clear stage 2 GUI
def clear_stage_2_GUI():
    try:
        part_move_button.grid_forget()
        part_to_move_label.grid_forget()
        destination_library_label.grid_forget()
        part_to_move_entry.grid_forget()
        destination_library_select.grid_forget()
    except NameError:
        pass

    protocol_design_title.grid_forget()
    clear_all_errors_moclo()
    stage_2_label.grid_forget()

    transcription_unit_1_label.grid_forget()
    transcription_unit_1_promoter_label.grid_forget()
    transcription_unit_1_rbs_label.grid_forget()
    if include_signal_combo.get() == "Yes":
        transcription_unit_1_signal_label.grid_forget()
    transcription_unit_1_cds_label.grid_forget()
    transcription_unit_1_terminator_label.grid_forget()
    transcription_unit_1_promoter_entry.grid_forget()
    transcription_unit_1_rbs_entry.grid_forget()
    if include_signal_combo.get() == "Yes":
        transcription_unit_1_signal_entry.grid_forget()
    transcription_unit_1_cds_entry.grid_forget()
    transcription_unit_1_terminator_entry.grid_forget()

    transcription_unit_2_label.grid_forget()
    transcription_unit_2_promoter_entry.grid_forget()
    transcription_unit_2_rbs_entry.grid_forget()
    if include_signal_combo.get() == "Yes":
        transcription_unit_2_signal_entry.grid_forget()
    transcription_unit_2_cds_entry.grid_forget()
    transcription_unit_2_terminator_entry.grid_forget()

    try:
        if int(transcription_unit_quantity_combo.get()) > 2:
            transcription_unit_3_label.grid_forget()
            transcription_unit_3_promoter_entry.grid_forget()
            transcription_unit_3_rbs_entry.grid_forget()
            if include_signal_combo.get() == "Yes":
                transcription_unit_3_signal_entry.grid_forget()
            transcription_unit_3_cds_entry.grid_forget()
            transcription_unit_3_terminator_entry.grid_forget()

        if int(transcription_unit_quantity_combo.get()) > 3:
            transcription_unit_4_label.grid_forget()
            transcription_unit_4_promoter_entry.grid_forget()
            transcription_unit_4_rbs_entry.grid_forget()
            if include_signal_combo.get() == "Yes":
                transcription_unit_4_signal_entry.grid_forget()
            transcription_unit_4_cds_entry.grid_forget()
            transcription_unit_4_terminator_entry.grid_forget()

        if int(transcription_unit_quantity_combo.get()) > 4:
            transcription_unit_5_label.grid_forget()
            transcription_unit_5_promoter_entry.grid_forget()
            transcription_unit_5_rbs_entry.grid_forget()
            if include_signal_combo.get() == "Yes":
                transcription_unit_5_signal_entry.grid_forget()
            transcription_unit_5_cds_entry.grid_forget()
            transcription_unit_5_terminator_entry.grid_forget()
    except ValueError:
        pass

    if assembly_method_combo.get() == "Automatic":
        liquid_handler_selection_label.grid_forget()
        liquid_handler_selection_combo.grid_forget()
    create_protocol_button.grid_forget()
    protocol_name_label.grid_forget()
    protocol_name_entry.grid_forget()


# Create protocol button
def create_create_protocol_button():
    global create_protocol_button
    create_protocol_button = tk.Button(tab4, text="Create protocol")
    create_protocol_button.bind("<Button-1>", MoClo.create_protocol_directory)
    create_protocol_button.grid(column=2, row=28)


# Final prompt before protocol generation
def final_prompt():
    clear_stage_2_GUI()
    formatted_list = []
    global final_check_title
    final_check_title = tk.Label(tab4, font=("Arial", "11", "bold"), text="Final check")
    final_check_title.grid(column=2, row=10, pady=(20, 0))
    if assembly_method_combo.get() == "Automatic":
        level_1_output_requirement = MoClo.calculate_well_requirements()[0]
        level_2_output_requirement = MoClo.calculate_well_requirements()[1]
        global level_1_output_requirement_label
        global level_2_output_requirement_label
        if level_1_output_requirement > 384:
            level_1_output_requirement_label = tk.Label(tab4, fg="red", text="-Output capacity reached for level 1 "
                                                                             "transcription unit assembly " + "(" +
                                                                             str(level_1_output_requirement) + "/" +
                                                                             "384" + ")" +
                                                                             ". CSV scripts will not be valid")
        else:
            level_1_output_requirement_label = tk.Label(tab4, fg="green", text="Level 1 assembly output " +
                                                                               str(level_1_output_requirement) +
                                                                               "/" + "384")

        if level_2_output_requirement > 384:
            level_2_output_requirement_label = tk.Label(tab4, fg="red", text="-Output capacity reached for level 2 "
                                                                             "transcription unit assembly " + "(" +
                                                                             str(level_2_output_requirement) + "/" +
                                                                             "384" + ")" +
                                                                             ". CSV scripts will not be valid")
        else:
            level_2_output_requirement_label = tk.Label(tab4, fg="green", text="Level 2 assembly output " +
                                                                               str(level_2_output_requirement) +
                                                                               "/" + "384")
        level_1_output_requirement_label.grid(column=2, row=11)
        level_2_output_requirement_label.grid(column=2, row=12)

    if not MoClo.ecoflex_check_list:
        global no_sites_detected_label
        no_sites_detected_label = tk.Label(tab4, fg="green", text="No restriction sites detected")
        no_sites_detected_label.grid(column=2, row=13)
    else:
        global restriction_site_title
        global pre_creation_check
        restriction_site_title = tk.Label(tab4, fg="red", text="Restriction sites detected:")
        restriction_site_title.grid(column=2, row=14)
        for warning in MoClo.ecoflex_check_list:
            formatted_list.append("\n" + warning)
        pre_creation_check = st.ScrolledText(tab4, font=(None, 8), fg="red", bg="SystemButtonFace", height=6, width=60)
        pre_creation_check.grid(column=2, row=15)
        pre_creation_check.insert(tk.INSERT, formatted_list)
        pre_creation_check.configure(state="disabled")
    from EcoFlex_protocol import create_protocol

    global continue_button
    continue_button = tk.Button(tab4, text="Continue with creation")
    continue_button.bind("<Button-1>", create_protocol)
    continue_button.grid(column=2, row=17)
    global stop_button
    stop_button = tk.Button(tab4, text="Stop")
    stop_button.bind("<Button-1>", revert_stage_2_GUI)
    stop_button.grid(column=2, row=16)


# Reinstating stage 2 GUI from final check
def revert_stage_2_GUI(event):
    final_check_title.grid_forget()
    if assembly_method_combo.get() == "Automatic":
        level_1_output_requirement_label.grid_forget()
        level_2_output_requirement_label.grid_forget()
    if not MoClo.ecoflex_check_list:
        no_sites_detected_label.grid_forget()
    else:
        restriction_site_title.grid_forget()
        pre_creation_check.grid_forget()
    continue_button.grid_forget()
    stop_button.grid_forget()
    stage_2_GUI("<Button-1>")
    move_parts_library()



# Liquid handler selection
def liquid_handler_selection():
    global liquid_handler_selection_combo
    global liquid_handler_selection_label
    liquid_handler_selection_label = tk.Label(tab4, text="Select liquid handler")
    liquid_handler_selection_label.grid(column=2, row=22)
    liquid_handler_selection_combo = ttk.Combobox(tab4, state="readonly", values=["Echo 525"])
    liquid_handler_selection_combo.grid(column=2, row=24)


# Protocol name
def protocol_name_entry_gui():
    global protocol_name_entry
    global protocol_name_label
    protocol_name_label = tk.Label(tab4, text="Enter protocol name")
    protocol_name_label.grid(column=2, row=25)
    protocol_name_entry = tk.Entry(tab4)
    protocol_name_entry.grid(column=2, row=27)


# SBOL import failed error
def import_failed_moclo():
    global import_failed_label
    import_failed_label = tk.Label(tab4, fg="red", text="Import failed")
    import_failed_label.grid(row=1, column=0)


# Error message for invalid part key for level 0 library move
def part_move_error():
    global part_move_error_label
    part_move_error_label = tk.Label(tab4, fg="red", text="Part key invalid")
    part_move_error_label.grid(column=0, row=7)


# Error message for invalid destination group for level 0 library move
def destination_group_error():
    global destination_group_error_label
    destination_group_error_label = tk.Label(tab4, fg="red", text="Invalid destination group")
    destination_group_error_label.grid(column=1, row=7)


# Error message for no selection signal
def combo_error_signal():
    global combo_error_signal_label
    combo_error_signal_label = tk.Label(tab4, fg="red", text="Please select an option")
    combo_error_signal_label.grid(column=0, row=11)


# Error message for no selection toolkit
def combo_error_toolkit():
    global combo_error_toolkit_label
    combo_error_toolkit_label = tk.Label(tab4, fg="red", text="Please select an option")
    combo_error_toolkit_label.grid(column=1, row=11)


# Error message for no selection TU quantity
def combo_error_tu():
    global combo_error_tu_label
    combo_error_tu_label = tk.Label(tab4, fg="red", text="Please select an option")
    combo_error_tu_label.grid(column=2, row=11)


# Error message for no selection assembly method
def combo_error_assembly():
    global combo_error_assembly_label
    combo_error_assembly_label = tk.Label(tab4, fg="red", text="Please select an option")
    combo_error_assembly_label.grid(column=3, row=11)


# Error message for no selection CDS substitution
def combo_error_cds():
    global combo_error_cds_label
    combo_error_cds_label = tk.Label(tab4, fg="red", text="Please select an option")
    combo_error_cds_label.grid(column=0, row=14)


# Error message for no selection fusion sites
def combo_error_fusion():
    global combo_error_fusion_label
    combo_error_fusion_label = tk.Label(tab4, fg="red", text="Please select an option")
    combo_error_fusion_label.grid(column=1, row=14)


# Error message for no selection of liquid handler
def combo_error_handler():
    global combo_error_handler_label
    combo_error_handler_label = tk.Label(tab4, fg="red", text="Please select an option")
    combo_error_handler_label.grid(column=2, row=23)


# Invalid part key error transcription unit 1
def invalid_part_key_error_tu1():
    global invalid_part_key_tu1_label
    invalid_part_key_tu1_label = tk.Label(tab4, fg="red", text="One or more parts keys are invalid in transcription "
                                                               "unit 1")
    invalid_part_key_tu1_label.grid(column=1, row=12, columnspan=5)


# Invalid part key error transcription unit 2
def invalid_part_key_error_tu2():
    global invalid_part_key_tu2_label
    invalid_part_key_tu2_label = tk.Label(tab4, fg="red", text="One or more parts keys are invalid in transcription "
                                                               "unit 2")
    invalid_part_key_tu2_label.grid(column=1, row=14, columnspan=5)


# Invalid part key error transcription unit 3
def invalid_part_key_error_tu3():
    global invalid_part_key_tu3_label
    invalid_part_key_tu3_label = tk.Label(tab4, fg="red", text="One or more parts keys are invalid in transcription "
                                                               "unit 3")
    invalid_part_key_tu3_label.grid(column=1, row=16, columnspan=5)


# Invalid part key error transcription unit 4
def invalid_part_key_error_tu4():
    global invalid_part_key_tu4_label
    invalid_part_key_tu4_label = tk.Label(tab4, fg="red", text="One or more parts keys are invalid in transcription "
                                                               "unit 4")
    invalid_part_key_tu4_label.grid(column=1, row=18, columnspan=5)


# Invalid part key error transcription unit 5
def invalid_part_key_error_tu5():
    global invalid_part_key_tu5_label
    invalid_part_key_tu5_label = tk.Label(tab4, fg="red", text="One or more parts keys are invalid in transcription "
                                                               "unit 5")
    invalid_part_key_tu5_label.grid(column=1, row=20, columnspan=5)


# Protocol name error
def protocol_name_error():
    global protocol_name_error_label
    protocol_name_error_label = tk.Label(tab4, fg="red", text="Protocol name invalid")
    protocol_name_error_label.grid(column=2, row=26)


# Creation successful label
def successful_creation():
    global successful_creation_label
    successful_creation_label = tk.Label(tab4, font=("Arial", "10", "bold"), fg="green",
                                         text="Protocol generation successful, contents saved to "
                                              "SynBioMate/protocols_and_scripts")
    successful_creation_label.grid(column=0, columnspan=5000)


# Clear all error labels in MoClo GUI
def clear_all_errors_moclo():
    try:
        import_failed_label.grid_forget()
    except NameError:
        pass
    try:
        part_move_error_label.grid_forget()
    except NameError:
        pass
    try:
        destination_group_error_label.grid_forget()
    except NameError:
        pass
    try:
        protocol_name_error_label.grid_forget()
    except NameError:
        pass
    try:
        combo_error_fusion_label.grid_forget()
    except NameError:
        pass
    try:
        combo_error_cds_label.grid_forget()
    except NameError:
        pass
    try:
        combo_error_assembly_label.grid_forget()
    except NameError:
        pass
    try:
        combo_error_tu_label.grid_forget()
    except NameError:
        pass
    try:
        combo_error_toolkit_label.grid_forget()
    except NameError:
        pass
    try:
        combo_error_signal_label.grid_forget()
    except NameError:
        pass
    try:
        combo_error_handler_label.grid_forget()
    except NameError:
        pass
    try:
        invalid_part_key_tu1_label.grid_forget()
    except NameError:
        pass
    try:
        invalid_part_key_tu2_label.grid_forget()
    except NameError:
        pass
    try:
        invalid_part_key_tu3_label.grid_forget()
    except NameError:
        pass
    try:
        invalid_part_key_tu4_label.grid_forget()
    except NameError:
        pass
    try:
        invalid_part_key_tu5_label.grid_forget()
    except NameError:
        pass
    try:
        successful_creation_label.grid_forget()
    except NameError:
        pass


# Reset GUI and global variables
def moclo_reset(event):
    # Clear existing GUI
    clear_all_errors_moclo()
    try:
        design_canvas_display_moclo.grid_forget()
    except NameError:
        pass
    try:
        design_to_library_button.grid_forget()
    except NameError:
        pass
    try:
        design_analysis_button_moclo.grid_forget()
    except NameError:
        pass
    try:
        hide_design_analysis_button_moclo.grid_forget()
    except NameError:
        pass
    try:
        design_analysis_frame.grid_forget()
    except NameError:
        pass
    try:
        part_description_button_moclo.grid_forget()
    except NameError:
        pass
    try:
        hide_part_description_button_moclo.grid_forget()
    except NameError:
        pass
    try:
        description_frame_moclo.grid_forget()
    except NameError:
        pass
    try:
        level_0_library_frame.grid_forget()
    except NameError:
        pass
    try:
        part_to_move_entry.grid_forget()
    except NameError:
        pass
    try:
        destination_library_select.grid_forget()
    except NameError:
        pass
    try:
        part_to_move_label.grid_forget()
    except NameError:
        pass
    try:
        destination_library_label.grid_forget()
    except NameError:
        pass
    try:
        part_move_button.grid_forget()
    except NameError:
        pass
    try:
        final_check_title.grid_forget()
    except NameError:
        pass
    try:
        level_1_output_requirement_label.grid_forget()
    except NameError:
        pass
    try:
        level_2_output_requirement_label.grid_forget()
    except NameError:
        pass
    try:
        no_sites_detected_label.grid_forget()
    except NameError:
        pass
    try:
        restriction_site_title.grid_forget()
    except NameError:
        pass
    try:
        pre_creation_check.grid_forget()
    except NameError:
        pass
    try:
        continue_button.grid_forget()
    except NameError:
        pass
    try:
        stop_button.grid_forget()
    except NameError:
        pass
    try:
        remove_stage_1_GUI()
    except NameError:
        pass
    try:
        protocol_design_title.grid_forget()
    except NameError:
        pass
    try:
        clear_stage_2_GUI()
    except NameError:
        pass
    # Reinstate stage 1 GUI
    stage_1_GUI()

    # Clear global variables
    MoClo.clear_moclo_globals()

clear_all_button = tk.Button(tab4, fg="red", text="Clear all")
clear_all_button.bind("<Button-1>", moclo_reset)
clear_all_button.grid(column=5, row=0)

################ Main_loop #################
window.mainloop()
