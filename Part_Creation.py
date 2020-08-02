# Import libraries
from sbol import *

# Import scripts
import GUI
import converter


# Get user input for part creation
def create_part():
    global doc
    doc = Document()
    global part_compliance
    global identifier
    identifier = GUI.part_identifier_entry.get().replace(" ", "_")
    if len(identifier) == 0:
        GUI.identifier_error()
        part_compliance = False

    global part_name
    part_name = GUI.part_name_entry.get().replace(" ", "_")
    if len(part_name) == 0:
        GUI.part_name_error()
        part_compliance = False

    global dna_sequence
    dna_sequence = GUI.sequence_entry.get()
    if len(dna_sequence) == 0:
        GUI.dna_error()
        part_compliance = False

    global part_role
    part_role = GUI.part_role_combo.get()
    if len(part_role) == 0:
        GUI.part_role_error()
        part_compliance = False

    global part_description
    part_description = GUI.part_description_entry.get()
    if len(part_description) == 0:
        GUI.part_description_error()
        part_compliance = False

    if part_compliance is True:
        part = ComponentDefinition(str(identifier))
        if part_role == "Promoter":
            part.roles = SO_PROMOTER
        elif part_role == "RBS":
            part.roles = SO_RBS
        elif part_role == "CDS":
            part.roles = SO_CDS
        elif part_role == "Terminator":
            part.roles = SO_TERMINATOR
        elif part_role == "Signal peptide":
            part.roles = ["http://identifiers.org/so/SO:0000324",
                          "http://wiki.synbiohub.org/wiki/Terms/igem#partType/Tag"]
        elif part_role == "Other":
            part.roles = SO_MISC

        part.sequence = Sequence(str(identifier), (str(dna_sequence)).lower())
        part.description = str(part_description)
        doc.addComponentDefinition(part)


# Save part
def save_created_part(event):
    global doc
    global part_compliance
    part_compliance = True
    create_part()
    if part_compliance is True:
        directory = GUI.save_part_popup()
        if directory is False:
            GUI.part_creation_failure()
        else:
            GUI.part_creation_success()
            result = doc.write(directory + ".xml")
            print(result)
    else:
        GUI.part_creation_failure()


# Part creation genbank
def part_creation_genbank(event):
    GUI.refresh_gui_part_creation()
    GUI.select_genbank_file()
    if not GUI.genbank_file:
        GUI.conversion_failure()
    else:
        converter.convert(GUI.genbank_file)
