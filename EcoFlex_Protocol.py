# Import libraries
from docx import Document

# Import scripts
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


# Write protocol to word document
def create_protocol():
    print("test")


# Appendix of document, containing all parts, transcription units, and final designs
def create_appendix():
    # Parts
    document.add_heading("Appendix", 1)
    document.add_heading("Promoters", 2)
    counter = 0
    for promoter in MoClo.promoter_identities:
        document.add_heading(promoter, 3)
        description = document.add_paragraph("")
        description.add_run("Description: ").bold = True
        description.add_run(MoClo.promoter_descriptions[counter])
        modifications = document.add_paragraph("")
        modifications.add_run("Modifications:").bold = True
        for modification in MoClo.promoter_modifications[counter]:
            modifications.add_run("\n" + "-" + modification)
        design = document.add_paragraph("")
        design.add_run("Part design: ").bold = True
        design.add_run("\n" + "5' " + MoClo.promoter_sequences_1[counter] + " 3'" + "\n" +
                       "3'     " + MoClo.promoter_sequences_2[counter] + "         5'")
        counter = counter + 1

    document.add_heading("Ribosome binding sites (RBSs)", 2)
    counter = 0
    for rbs in MoClo.rbs_identities:
        document.add_heading(rbs, 3)
        description = document.add_paragraph("")
        description.add_run("Description: ").bold = True
        description.add_run(MoClo.rbs_descriptions[counter])
        modifications = document.add_paragraph("")
        modifications.add_run("Modifications:").bold = True
        for modification in MoClo.rbs_modifications[counter]:
            modifications.add_run("\n" + "-" + modification)
        design = document.add_paragraph("")
        design.add_run("Part design: ").bold = True
        design.add_run("\n" + "5' " + MoClo.rbs_sequences_1[counter] + " 3'" + "\n" +
                       "3'     " + MoClo.rbs_sequences_2[counter] + "         5'")
        counter = counter + 1

    if GUI.include_signal_combo.get() == "Yes":
        document.add_heading("Signal peptides", 2)
        counter = 0
        for signal in MoClo.signal_identities:
            document.add_heading(signal, 3)
            description = document.add_paragraph("")
            description.add_run("Description: ").bold = True
            description.add_run(MoClo.signal_descriptions[counter])
            modifications = document.add_paragraph("")
            modifications.add_run("Modifications:").bold = True
            for modification in MoClo.signal_modifications[counter]:
                modifications.add_run("\n" + "-" + modification)
            design = document.add_paragraph("")
            design.add_run("Part design: ").bold = True
            design.add_run("\n" + "5' " + MoClo.signal_sequences_1[counter] + " 3'" + "\n" +
                           "3'     " + MoClo.signal_sequences_2[counter] + "         5'")
            counter = counter + 1

    document.add_heading("Coding regions (CDSs)", 2)
    counter = 0
    for cds in MoClo.cds_identities:
        document.add_heading(cds, 3)
        description = document.add_paragraph("")
        description.add_run("Description: ").bold = True
        description.add_run(MoClo.cds_descriptions[counter])
        modifications = document.add_paragraph("")
        modifications.add_run("Modifications:").bold = True
        for modification in MoClo.cds_modifications[counter]:
            modifications.add_run("\n" + "-" + modification)
        design = document.add_paragraph("")
        design.add_run("Part design: ").bold = True
        design.add_run("\n" + "5' " + MoClo.cds_sequences_1[counter] + " 3'" + "\n" +
                       "3'     " + MoClo.cds_sequences_2[counter] + "         5'")
        counter = counter + 1

    document.add_heading("Terminators", 2)
    counter = 0
    for terminator in MoClo.terminator_identities:
        document.add_heading(terminator, 3)
        description = document.add_paragraph("")
        description.add_run("Description: ").bold = True
        description.add_run(MoClo.terminator_descriptions[counter])
        modifications = document.add_paragraph("")
        modifications.add_run("Modifications:").bold = True
        for modification in MoClo.terminator_modifications[counter]:
            modifications.add_run("\n" + "-" + modification)
        design = document.add_paragraph("")
        design.add_run("Part design: ").bold = True
        design.add_run("\n" + "5' " + MoClo.terminator_sequences_1[counter] + " 3'" + "\n" +
                       "3'     " + MoClo.terminator_sequences_2[counter] + "         5'")
        counter = counter + 1

    # Level 1 transcription units
    document.add_heading("Level 1 transcription units", 2)
    if int(GUI.transcription_unit_quantity_combo.get()) > 1:
        counter = 0
        for variant in MoClo.transcription_unit_1_names:
            document.add_heading(variant, 3)
            part_list = document.add_paragraph("")
            part_list.add_run("Parts: ").bold = True
            for part in MoClo.transcription_unit_1_part_id[counter]:
                part_list.add_run("Modified " + part)
                part_list.add_run(", ")
            notes = document.add_paragraph("")
            notes.add_run("Notes: ").bold = True
            notes.add_run(MoClo.transcription_unit_1_notes[counter])
            sequences = document.add_paragraph("")
            sequences.add_run("Sequence (Excluding plasmid backbone): ").bold = True
            sequences.add_run("5' ")
            sequences.add_run(MoClo.transcription_unit_1_sequences[counter])
            sequences.add_run(" 3'")
            counter = counter + 1

        counter = 0
        for variant in MoClo.transcription_unit_2_names:
            document.add_heading(variant, 3)
            part_list = document.add_paragraph("")
            part_list.add_run("Parts: ").bold = True
            for part in MoClo.transcription_unit_2_part_id[counter]:
                part_list.add_run("Modified " + part)
                part_list.add_run(", ")
            notes = document.add_paragraph("")
            notes.add_run("Notes: ").bold = True
            notes.add_run(MoClo.transcription_unit_2_notes[counter])
            sequences = document.add_paragraph("")
            sequences.add_run("Sequence (Excluding plasmid backbone): ").bold = True
            sequences.add_run("5' ")
            sequences.add_run(MoClo.transcription_unit_2_sequences[counter])
            sequences.add_run(" 3'")
            counter = counter + 1

    if int(GUI.transcription_unit_quantity_combo.get()) > 2:
        counter = 0
        for variant in MoClo.transcription_unit_3_names:
            document.add_heading(variant, 3)
            part_list = document.add_paragraph("")
            part_list.add_run("Parts: ").bold = True
            for part in MoClo.transcription_unit_3_part_id[counter]:
                part_list.add_run("Modified " + part)
                part_list.add_run(", ")
            notes = document.add_paragraph("")
            notes.add_run("Notes: ").bold = True
            notes.add_run(MoClo.transcription_unit_3_notes[counter])
            sequences = document.add_paragraph("")
            sequences.add_run("Sequence (Excluding plasmid backbone): ").bold = True
            sequences.add_run("5' ")
            sequences.add_run(MoClo.transcription_unit_3_sequences[counter])
            sequences.add_run(" 3'")
            counter = counter + 1

    if int(GUI.transcription_unit_quantity_combo.get()) > 3:
        counter = 0
        for variant in MoClo.transcription_unit_4_names:
            document.add_heading(variant, 3)
            part_list = document.add_paragraph("")
            part_list.add_run("Parts: ").bold = True
            for part in MoClo.transcription_unit_4_part_id[counter]:
                part_list.add_run("Modified " + part)
                part_list.add_run(", ")
            notes = document.add_paragraph("")
            notes.add_run("Notes: ").bold = True
            notes.add_run(MoClo.transcription_unit_4_notes[counter])
            sequences = document.add_paragraph("")
            sequences.add_run("Sequence (Excluding plasmid backbone): ").bold = True
            sequences.add_run("5' ")
            sequences.add_run(MoClo.transcription_unit_4_sequences[counter])
            sequences.add_run(" 3'")
            counter = counter + 1

    if int(GUI.transcription_unit_quantity_combo.get()) > 4:
        counter = 0
        for variant in MoClo.transcription_unit_5_names:
            document.add_heading(variant, 3)
            part_list = document.add_paragraph("")
            part_list.add_run("Parts: ").bold = True
            for part in MoClo.transcription_unit_5_part_id[counter]:
                part_list.add_run("Modified " + part)
                part_list.add_run(", ")
            notes = document.add_paragraph("")
            notes.add_run("Notes: ").bold = True
            notes.add_run(MoClo.transcription_unit_5_notes[counter])
            sequences = document.add_paragraph("")
            sequences.add_run("Sequence (Excluding plasmid backbone): ").bold = True
            sequences.add_run("5' ")
            sequences.add_run(MoClo.transcription_unit_5_sequences[counter])
            sequences.add_run(" 3'")
            counter = counter + 1

    # Level 2 transcription units
    counter = 0
    document.add_heading("Level 2 multi-TU constructs", 2)
    selected_vector = document.add_paragraph("")
    selected_vector.add_run("Level 2 plasmid backbone: ").bold = True
    selected_vector.add_run(MoClo.level_2_vector_name)
    for variant in MoClo.level_2_names:
        document.add_heading(variant, 3)
        sub_units = document.add_paragraph("")
        sub_units.add_run("Sub-units: ").bold = True
        for unit in MoClo.level_2_sub_units[counter]:
            sub_units.add_run(unit)
            sub_units.add_run(", ")
        sequences = document.add_paragraph("")
        sequences.add_run("Sequence (Excluding plasmid backbone): ").bold = True
        sequences.add_run("5' ")
        sequences.add_run(MoClo.level_2_sequences[counter])
        sequences.add_run(" 3'")
        counter = counter + 1















# Create EcoFlex protocol
def create_protocol(event):
    MoClo.swap_codons_ecoflex()
    MoClo.check_biopart_sites_ecoflex()
    MoClo.ecoflex_fusion_sites()
    MoClo.create_transcription_unit_variants()
    MoClo.final_oligonucleotides_2()
    MoClo.transcription_unit_format()
    MoClo.level_2_format()
    title_introduction()
    create_protocol()
    create_appendix()

    document.save("test.docx")
