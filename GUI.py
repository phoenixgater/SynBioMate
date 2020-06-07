# Import libraries
import sys
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

# Import scripts
import Construct_Design
import Protocol_Generation

# Global variables
construct_display_list = []

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
tab_parent.add(tab1, text="Construct Assembly")
tab_parent.add(tab2, text="Construct Modification")
tab_parent.add(tab3, text="Protocol Generation")
tab_parent.add(tab4, text="MoClo Assembly")
tab_parent.pack(expand=1, fill='both')

# Assigning SBOL GIF glyphs to variables
promoter_glyph = tk.PhotoImage(file="SBOL_Glyphs/promoter-specification.gif")
rbs_glyph = tk.PhotoImage(file="SBOL_Glyphs/ribosome-entry-site-specification.gif")
cds_glyph = tk.PhotoImage(file="SBOL_Glyphs/cds-specification.gif")
terminator_glyph = tk.PhotoImage(file="SBOL_Glyphs/terminator-specification.gif")
other_glyph = tk.PhotoImage(file="SBOL_Glyphs/no-glyph-assigned-specification.gif")

###################### Construct_Design GUI #####################

# Title of construct assembly tab
constructassemblytitle = tk.Label(tab1, text="Construct Assembly", font=(None, 20))
constructassemblytitle.pack()


# Display objects in doc in GUI
def objects_in_doc_display():
    global doc_contents_display
    Construct_Design.clear_doc_display()
    doc_contents_display = tk.Message(tab1, text=Construct_Design.objects_in_doc())
    doc_contents_display.pack()


# Query submission label and entry widget
query_request_label = tk.Label(tab1, text="Please enter a search term")
query_request_label.pack()
query_request_entry = tk.Entry(tab1)
query_request_entry.pack()

# Query submit button
query_submit_button = tk.Button(tab1, text="Submit")
query_submit_button.bind("<Button-1>", Construct_Design.query_submit)
query_submit_button.pack()


# GUI binding of writing queried part to doc
def part_choice_button_1():
    global query_result_button_1
    query_result_button_1 = tk.Button(tab1, text=Construct_Design.records[0])
    query_result_button_1.bind("<Button-1>", Construct_Design.query_to_doc_1)
    query_result_button_1.pack()


def part_choice_button_2():
    global query_result_button_2
    query_result_button_2 = tk.Button(tab1, text=Construct_Design.records[1])
    query_result_button_2.bind("<Button-1>", Construct_Design.query_to_doc_2)
    query_result_button_2.pack()


def part_choice_button_3():
    global query_result_button_3
    query_result_button_3 = tk.Button(tab1, text=Construct_Design.records[2])
    query_result_button_3.bind("<Button-1>", Construct_Design.query_to_doc_3)
    query_result_button_3.pack()


def part_choice_button_4():
    global query_result_button_4
    query_result_button_4 = tk.Button(tab1, text=Construct_Design.records[3])
    query_result_button_4.bind("<Button-1>", Construct_Design.query_to_doc_4)
    query_result_button_4.pack()


def part_choice_button_5():
    global query_result_button_5
    query_result_button_5 = tk.Button(tab1, text=Construct_Design.records[4])
    query_result_button_5.bind("<Button-1>", Construct_Design.query_to_doc_5)
    query_result_button_5.pack()


def part_choice_button_6():
    global query_result_button_6
    query_result_button_6 = tk.Button(tab1, text=Construct_Design.records[5])
    query_result_button_6.bind("<Button-1>", Construct_Design.query_to_doc_6)
    query_result_button_6.pack()


def part_choice_button_7():
    global query_result_button_7
    query_result_button_7 = tk.Button(tab1, text=Construct_Design.records[6])
    query_result_button_7.bind("<Button-1>", Construct_Design.query_to_doc_7)
    query_result_button_7.pack()


def part_choice_button_8():
    global query_result_button_8
    query_result_button_8 = tk.Button(tab1, text=Construct_Design.records[7])
    query_result_button_8.bind("<Button-1>", Construct_Design.query_to_doc_8)
    query_result_button_8.pack()


def part_choice_button_9():
    global query_result_button_9
    query_result_button_9 = tk.Button(tab1, text=Construct_Design.records[8])
    query_result_button_9.bind("<Button-1>", Construct_Design.query_to_doc_9)
    query_result_button_9.pack()


def part_choice_button_10():
    global query_result_button_10
    (query_result_button_10) = tk.Button(tab1, text=Construct_Design.records[9])
    query_result_button_10.bind("<Button-1>", Construct_Design.query_to_doc_10)
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


# Construct assembly entry label
name_construct_label = tk.Label(tab1, text="Please enter the name of your genetic construct")
name_construct_label.pack()

# Construct assembly name entry
construct_name_entry = tk.Entry(tab1)
construct_name_entry.pack()

# Construct assembly button
construct_assembly_button = tk.Button(tab1, text="Assemble Design")
construct_assembly_button.bind("<Button-1>", Construct_Design.construct_assembly_directory)
construct_assembly_button.pack()

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
