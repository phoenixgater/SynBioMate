# Import libraries
from docx import Document

# Import scripts
import Main
import GUI
import MoClo

# Global variables
# Document for writing protocol with docx (This is NOT a pySBOL document)
document = Document()

# Imported user input parameters
transcription_unit_quantity = GUI.transcription_unit_quantity_combo.get()
signal_peptide_choice = GUI.include_signal_combo.get()
liquid_handler_choice = GUI.liquid_handler_combo.get()


# Title and introduction of document
def title_introduction():
    document.add_heading("Automated MoClo assembly protocol", 0)
    document.add_paragraph("Hello! This document contains a protocol for the assembly of genetic parts using" +
                           " MoClo assembly with an automated liquid handler. This document was produced by the" +
                           " software 'SynBioMate' (https://github.com/phoenixgater/SynBioMate)")
    document.add_paragraph("Notes on this document and its contents:")
    document.add_paragraph("-For restriction sites detected in open reading frames (coding regions, CDSs, ORFs)," +
                           " a codon in this region has been swapped to ensure that the part is MoClo compatible." +
                           " This codon swap is specified in this documents appendix.")
    document.add_paragraph("-This software is unable to suggest base substitutions for excluded restriction sites" +
                           " detected in non-coding genetic parts (e.g Promoters, RBSs, etc), but the presence" +
                           " of these restriction sites will be noted in this documents appendix as well.")


# Get original parts and their sequences
def get_parts():
    print("placeholder")


# Get original designs and their sequences
def get_designs():
    print("placeholder")


# Appendix of document, containing all parts, transcription units, and final designs
def create_appendix():
    document.add_heading("Appendix", 1)
    document.add_heading("Promoters", 2)
    for promoter in MoClo.promoter_identities:
        document.add_heading(promoter, 3)
        document.add_paragraph(MoClo.promoter_descriptions)
        document.add_paragraph(MoClo.promoter_sequences_1)
        document.add_paragraph(MoClo.promoter_sequences_2)





# Create EcoFlex protocol
def create_protocol(event):
    MoClo.swap_codons_ecoflex()
    MoClo.check_biopart_sites_ecoflex()
    MoClo.ecoflex_fusion_sites()
    MoClo.create_transcription_unit_variants()
    MoClo.create_level_2_variants()
    MoClo.final_oligonucleotides_2()
    title_introduction()
    create_appendix()
    document.save("test.docx")
