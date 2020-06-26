# Import libraries
from docx import Document

# Import scripts
import Main
import GUI
import MoClo


#Global variables
document = Document()



# Imported user input parameters
transcription_unit_quantity = GUI.transcription_unit_quantity_combo.get()
signal_peptide_choice = GUI.include_signal_combo.get()
primer_selection = GUI.primer_selection_combo.get()
liquid_handler_choice = GUI.liquid_handler_combo.get()

# Import selected parts






def create_protocol():
    document.save("protocols_and_scripts/test.docx")