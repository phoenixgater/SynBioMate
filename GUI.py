# Import libraries
import sys
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

# Import scripts
import Construct_Design
import Protocol_Generation

################### General_GUI ########################
# Creating GUI window
window = tk.Tk()
window.title("SynBioMate")
window.geometry("700x500")

# Adding tabs to GUI
tab_parent = ttk.Notebook(window)
tab1 = ttk.Frame(tab_parent)
tab2 = ttk.Frame(tab_parent)
tab3 = ttk.Frame(tab_parent)
tab4 = ttk.Frame(tab_parent)
tab_parent.add(tab1, text="Construct Assembly")
tab_parent.add(tab2, text="Construct Modification")
tab_parent.add(tab3, text="Protocol Generation")
tab_parent.add(tab4, text="Liquid Handling Scripts")
tab_parent.pack(expand=1, fill='both')

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
construct_assembly_button = tk.Button(tab1, text="Assemble Construct")
construct_assembly_button.bind("<Button-1>", Construct_Design.construct_assembly_directory)
construct_assembly_button.pack()

####################### Protocol_Generation_Main GUI ###################################
# Protocol generation title label
protocol_generation_title = tk.Label(tab3, text="Protocol Generation", font=(None, 20))
protocol_generation_title.pack()


# Selection of construct to import
def select_construct_import():
    window.filename = filedialog.askopenfilename(initialdir=str(sys.argv[0]), title="select file",
                                                 filetypes=(("xml files", "*.xml"), ("all files", "*.*")))
    global single_imported_construct
    single_imported_construct = window.filename


# Import construct button
import_construct_button = tk.Button(tab3, text="Import Construct")
import_construct_button.bind("<Button-1>", Protocol_Generation.import_construct)
import_construct_button.pack()


# Display objects in doc GUI
def objects_in_doc_display_protocol():
    doc_contents_display_protocol = tk.Message(tab3, text=Protocol_Generation.objects_in_doc())
    doc_contents_display_protocol.pack()




################ Main_loop #################
window.mainloop()
