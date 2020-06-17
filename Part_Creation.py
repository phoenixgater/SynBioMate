# Import libraries
from sbol import *

# Import scripts
import Main
import GUI
import converter


#Get user input for part creation
def create_part():
    global identifier
    identifier = GUI.part_identifier_entry.get().replace(" ", "_")
    global part_name
    part_name = GUI.part_name_entry.get().replace(" ", "_")
    global dna_sequence
    dna_sequence = GUI.sequence_entry.get()
    global part_role
    part_role = GUI.part_role_combo.get()
    global description
    part_description = GUI.part_description_entry.get()
    part = ComponentDefinition(str(identifier))
    if part_role == "Promoter":
        part.roles = SO_PROMOTER
    elif part_role == "RBS":
        part.roles = SO_RBS
    elif part_role == "CDS":
        part.roles = SO_CDS
    elif part_role == "Terminator":
        part.roles = SO_TERMINATOR
    elif part_role == "Backbone":
        part.roles = SO_PLASMID
    part.sequence = Sequence(str(identifier), str(dna_sequence))
    part.description = str(part_description)
    Main.doc.addComponentDefinition(part)


#Part creation genbank
def part_creation_genbank(event):
    GUI.select_genbank_file()
    converter.convert(GUI.genbank_file)


#Save part
def save_created_part(event):
    create_part()
    result = Main.doc.write(str(part_name) + ".xml")
    print(result)


#Part creation genbank
def part_creation_genbank(event):
    GUI.select_genbank_file()
    converter.convert(GUI.genbank_file)

