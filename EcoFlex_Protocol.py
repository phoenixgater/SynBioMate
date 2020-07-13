# Import libraries
from docx import Document

# Import scripts
import GUI
import MoClo

# Global variables
# Document for writing protocol with docx (This is NOT a pySBOL document)
document = Document()
parts_level_1 = []
level_1_wells = {}

# Imported user input parameters
transcription_unit_quantity = GUI.transcription_unit_quantity_combo.get()
signal_peptide_choice = GUI.include_signal_combo.get()


# Calculate part quantity
def calculate_part_quantity():
    global part_quantity
    if GUI.include_signal_combo.get() == "Yes":
        part_quantity = (len(MoClo.promoter_identities) + len(MoClo.rbs_identities) + len(MoClo.signal_identities)
                         + len(MoClo.cds_identities) + len(MoClo.terminator_identities))
    elif GUI.include_signal_combo.get() == "No":
        part_quantity = (len(MoClo.promoter_identities) + len(MoClo.rbs_identities)
                         + len(MoClo.cds_identities) + len(MoClo.terminator_identities))


# Title and introduction of document
def title_introduction():
    if GUI.assembly_method_combo.get() == "Automatic":
        document.add_heading("Automated MoClo assembly protocol", 0)
        document.add_paragraph("Hello! This document contains a protocol for the assembly of genetic parts using" +
                               " MoClo assembly with an automated liquid handler. This document was produced by the" +
                               " software 'SynBioMate' (https://github.com/phoenixgater/SynBioMate)")
    elif GUI.assembly_method_combo.get() == "Manual":
        document.add_heading("Manual MoClo assembly protocol", 0)
        document.add_paragraph("Hello! This document contains a protocol for the manual assembly of genetic parts" +
                               " using MoClo assembly. This document was produced by the" +
                               " software 'SynBioMate' (https://github.com/phoenixgater/SynBioMate)")
    document.add_paragraph("The protocols and fusion sites in this protocol are designed to be compatible with" +
                           " the EcoFlex MoClo kit, available from: http://www.addgene.org/kits/freemont-ecoflex-moclo/")
    part_notes = document.add_paragraph("")
    part_notes.add_run("Notes on this document and its contents:").bold = True
    part_notes.add_run("\n" + "-For restriction sites detected in open reading frames (coding regions, CDSs, ORFs)," +
                       " a codon in this region has been swapped to ensure that the part is MoClo compatible." +
                       " This codon swap is specified in this documents appendix.")
    part_notes.add_run("\n" + "\n" + "-If an ATG start codon could not" +
                       " be found at the start of an ORF/CDS part, this has been added, and noted in the appendix as" +
                       " well.")
    part_notes.add_run(" It is, however, highly advised that the use of these parts be reconsidered").bold = True
    part_notes.add_run("\n" + "\n" + "-This software is unable to suggest base substitutions for excluded restriction "
                                     "sites" +
                       " detected in non-coding genetic parts (e.g Promoters, RBSs, etc), but the presence" +
                       " of these restriction sites will be noted in this documents appendix.")
    part_notes.add_run(" It is highly advised that the use of these parts be reconsidered").bold = True

    input_notes = document.add_paragraph("Please note that the contents of this document will only be valid for " +
                                         "the user-input parameters that were given at the time of this documents " +
                                         "creation. These were:")
    input_notes.add_run("\n" + "Signal peptide included:").bold = True
    input_notes.add_run(" " + GUI.include_signal_combo.get())
    input_notes.add_run("\n" + "Chassis system:").bold = True
    input_notes.add_run(" " + GUI.chassis_selection_combo.get())
    input_notes.add_run("\n" + "Transcription unit quantity:").bold = True
    input_notes.add_run(" " + GUI.transcription_unit_quantity_combo.get())
    input_notes.add_run("\n" + "Assembly method:").bold = True
    input_notes.add_run(" " + GUI.assembly_method_combo.get())
    document.add_page_break()


# Write manual protocol to word document
def create_manual_protocol():
    document.add_heading("Protocol", 1)
    document.add_heading("Creating level 0 library and cloning into level 0 plasmid backbones", 2)
    biopart_prep = document.add_paragraph("")
    biopart_prep.add_run("a) For each of the BioParts in this documents appendix (all parts EXCLUDING CDS/ORF): ")
    biopart_prep.add_run("\n" + "1. Design and create/purchase forward and reverse primers for the BioPart")
    biopart_prep.add_run("\n" + "2. Anneal forward and reverse primers (20 uM of each) in 1 x T4 DNA ligase buffer " +
                         "at 90°C for 1 min, followed by cooling on ice")
    biopart_prep.add_run("\n" + "3. Phosphorylate with T4 PNK for 1 hour at 37°C")
    biopart_prep.add_run("\n" + "4. Digest 40 ng/uL-1 (24nM) of pBP-lacZa with 1 unit of NdeI and SphI " +
                         "in CutSmart buffer for 1 hour at 37°C, heat inactivate at 80°C for 10 min")
    biopart_prep.add_run("\n" + "5. Add 2 uL (80 ng) of NdeI-SphI digested pBP-lacZa plasmid with 2 uL of 200 nM "
                         + "annealed primers in 2 x Rapid ligation buffer (Promega) and 1-3 units of T4 ligase " +
                         "(Promega)")
    biopart_prep.add_run("\n" + "6. Incubate at room-temperature (19-21 °C) for 30-60 min")
    biopart_prep.add_run("\n" + "7. Transform 5 uL into 50 uL of DH10a competent cells")
    biopart_prep.add_run("\n" + "8. Grow on 35 ug mL-1 chloramphenicol LB plates with 0.1 mM IPTG and 40 ug " +
                         "mL-1 X-Gal (Sigma) for 24 hrs")
    biopart_prep.add_run("\n" + "9. Place in cold room overnight for clear visualisation of negative blue colonies")
    biopart_prep.add_run("\n" + "10. Pick 1-2 white colonies for plasmid preparation and sequencing")

    biopart_prep.add_run("\n" + "\n" + "b) For each of the CDS/ORF parts in this documents appendix: ")
    biopart_prep.add_run("\n" + "1. Design and create/purchase forward and reverse primers for the CDS part")
    biopart_prep.add_run("\n" + "Anneal forward and reverse primers (20 uM of each) in 1 x T4 DNA ligase buffer at " +
                         "90°C for 1 min, followed by cooling on ice")
    biopart_prep.add_run("\n" + "3. Phosphorylate with T4 PNK for 1 hour at 37°C")
    biopart_prep.add_run("\n" + "4. Digest 40 ng/uL-1 (24nM) of pBP-ORF with 1 unit of NdeI and BamHI " +
                         "in CutSmart buffer for 1 hour at 37°C, heat inactivate at 80°C for 10 min")
    biopart_prep.add_run("\n" + "5. Add 2 uL (80 ng) of NdeI-BamHI digested pBP-ORF plasmid with 2 uL of 200 nM " +
                         "annealed primers in 2 x Rapid ligation buffer (Promega) and 1-3 units of T4 ligase (Promega)")
    biopart_prep.add_run("\n" + "6. Incubate at room-temperature (19-21 °C) for 30-60 min")
    biopart_prep.add_run("\n" + "7. Transform 5 uL into 50 uL of DH10a competent cells")
    biopart_prep.add_run("\n" + "8. Grow on 35 ug mL-1 chloramphenicol LB plates with 0.1 mM IPTG and 40 ug" +
                         " mL-1 X-Gal (Sigma) for 24 hrs")
    biopart_prep.add_run("\n" + "9. Place in cold room overnight for clear visualisation of negative blue colonies")
    biopart_prep.add_run("\n" + "10. Pick 1-2 white colonies for plasmid preparation and sequencing")

    document.add_heading("Creating level 1 transcription units (TUs)", 2)
    tu_prep = document.add_paragraph("")
    tu_prep.add_run("For each level 1 transcription unit variant in this documents appendix:")
    tu_prep.add_run("\n" + "Create a mixture consisting of:" + "\n" + "-100ng of each included part" +
                    "\n" + "-50ng of the level 1 destination plasmid backbone (Backbones will differ for each TU," +
                    " the backbone to be used for each respective TU is specified in the appendix)" + "\n" +
                    "-20 units BsaI-HF (NEB)" + "\n" + "-1-3 units T4 DNA ligase (Promega)")
    tu_prep.add_run("\n" + "\n" + "b) Run a PCR protocol for this mixture, consisting of:" + "\n" + "15-30 cycles of:" +
                    "\n" + "-5 minutes at 37°C" + "\n" + "-10 minutes at 16°C" + "\n" + "Followed by:" + "\n" +
                    "-5 minutes at 50°C" + "\n" + "-5 minutes at 80°C")
    tu_prep.add_run("\n" + "c) Transform 5 uL of the mixture into 50uL of chemically competent" +
                    "Escherichia coli (E. coli) dH10a by heat shock transformation")

    document.add_heading("Creating level 2 transcription units (TUs)", 2)
    tu2_prep = document.add_paragraph("")
    tu2_prep.add_run("For each level 2 transcription unit variant in this document:")
    tu2_prep.add_run("\n" + "a) Create a mixture consisting of:")
    tu2_prep.add_run("\n" + "-100ng of each included level 1 transcription unit" + "\n" +
                     "-50ng of level 2 destination vector" + "\n" + "-10 units BsmBI (NEB)" + "\n" +
                     "-1-3 units T4 DNA ligase (Promega)")
    tu2_prep.add_run("\n" + "\n" + "b) Incubate mixture at 37°C for 16 hours")
    tu2_prep.add_run("\n" + "c) Incubate at 80°C for 5 minutes")
    tu2_prep.add_run("\n" + "d) Transform 5 uL of the mixture into 50uL of chemically competent E. coli dH10a " +
                     "by heat shock transformation")


# Write automatic protocol to word document
def create_automatic_protocol():
    document.add_heading("Protocol", 1)
    document.add_heading("Creating level 0 library and cloning into level 0 plasmid backbones", 2)
    biopart_prep = document.add_paragraph("")
    biopart_prep.add_run("a) For each of the BioParts in this documents appendix (all parts EXCLUDING CDS/ORF): ")
    biopart_prep.add_run("\n" + "1. Design and create/purchase forward and reverse primers for the BioPart")
    biopart_prep.add_run(
        "\n" + "2. Anneal forward and reverse primers (20 uM of each) in 1 x T4 DNA ligase buffer " +
        "at 90°C for 1 min, followed by cooling on ice")
    biopart_prep.add_run("\n" + "3. Phosphorylate with T4 PNK for 1 hour at 37°C")
    biopart_prep.add_run("\n" + "4. Digest 40 ng/uL-1 (24nM) of pBP-lacZa with 1 unit of NdeI and SphI " +
                         "in CutSmart buffer for 1 hour at 37°C, heat inactivate at 80°C for 10 min")
    biopart_prep.add_run("\n" + "5. Add 2 uL (80 ng) of NdeI-SphI digested pBP-lacZa plasmid with 2 uL of 200 nM "
                         + "annealed primers in 2 x Rapid ligation buffer (Promega) and 1-3 units of T4 ligase " +
                         "(Promega)")
    biopart_prep.add_run("\n" + "6. Incubate at room-temperature (19-21 °C) for 30-60 min")
    biopart_prep.add_run("\n" + "7. Transform 5 uL into 50 uL of DH10a competent cells")
    biopart_prep.add_run("\n" + "8. Grow on 35 ug mL-1 chloramphenicol LB plates with 0.1 mM IPTG and 40 ug " +
                         "mL-1 X-Gal (Sigma) for 24 hrs")
    biopart_prep.add_run("\n" + "9. Place in cold room overnight for clear visualisation of negative blue colonies")
    biopart_prep.add_run("\n" + "10. Pick 1-2 white colonies for plasmid preparation and sequencing")

    biopart_prep.add_run("\n" + "\n" + "b) For each of the CDS/ORF parts in this documents appendix: ")
    biopart_prep.add_run("\n" + "1. Design and create/purchase forward and reverse primers for the CDS part")
    biopart_prep.add_run(
        "\n" + "Anneal forward and reverse primers (20 uM of each) in 1 x T4 DNA ligase buffer at " +
        "90°C for 1 min, followed by cooling on ice")
    biopart_prep.add_run("\n" + "3. Phosphorylate with T4 PNK for 1 hour at 37°C")
    biopart_prep.add_run("\n" + "4. Digest 40 ng/uL-1 (24nM) of pBP-ORF with 1 unit of NdeI and BamHI " +
                         "in CutSmart buffer for 1 hour at 37°C, heat inactivate at 80°C for 10 min")
    biopart_prep.add_run("\n" + "5. Add 2 uL (80 ng) of NdeI-BamHI digested pBP-ORF plasmid with 2 uL of 200 nM " +
                         "annealed primers in 2 x Rapid ligation buffer (Promega) and 1-3 units of T4 ligase (Promega)")
    biopart_prep.add_run("\n" + "6. Incubate at room-temperature (19-21 °C) for 30-60 min")
    biopart_prep.add_run("\n" + "7. Transform 5 uL into 50 uL of DH10a competent cells")
    biopart_prep.add_run("\n" + "8. Grow on 35 ug mL-1 chloramphenicol LB plates with 0.1 mM IPTG and 40 ug" +
                         " mL-1 X-Gal (Sigma) for 24 hrs")
    biopart_prep.add_run("\n" + "9. Place in cold room overnight for clear visualisation of negative blue colonies")
    biopart_prep.add_run("\n" + "10. Pick 1-2 white colonies for plasmid preparation and sequencing")

    document.add_page_break()

    document.add_heading("Creating level 1 transcription units (TUs)", 2)
    tu_1_prep_1 = document.add_paragraph("")
    tu_1_prep_1.add_run("a) Add genetic parts and level 1 transcription unit backbones "
                        "into their corresponding wells in" +
                        " the Echo® Qualified 384-Well Polypropylene Source Microplate (384PP) as" +
                        " outlined below")
    if GUI.include_signal_combo.get() == "No":
        part_lists = [MoClo.promoter_identities, MoClo.rbs_identities, MoClo.cds_identities,
                      MoClo.terminator_identities]
    if GUI.include_signal_combo.get() == "Yes":
        part_lists = [MoClo.promoter_identities, MoClo.rbs_identities, MoClo.signal_identities,
                      MoClo.cds_identities, MoClo.terminator_identities]

    level_1_protocol_table = document.add_table(rows=1, cols=3)
    row_1_cells = level_1_protocol_table.rows[0].cells
    row_1_cells[0].text = "Well"
    row_1_cells[1].text = "Genetic part"
    row_1_cells[2].text = "Quantity (ul)"
    counter = 0
    for list in part_lists:
        for part in list:
            counter = counter + 1
            row_cells = level_1_protocol_table.add_row().cells
            row_cells[0].text = "A" + str(counter)
            row_cells[1].text = part
            row_cells[2].text = "PLACEHOLDER"
            level_1_wells["A" + str(counter)] = part
            parts_level_1.append(part)

    counter_col_f = 0
    if int(GUI.transcription_unit_quantity_combo.get()) > 1:
        counter_col_f = counter_col_f + 1
        row_cells = level_1_protocol_table.add_row().cells
        row_cells[0].text = "F" + str(counter_col_f)
        level_1_wells["F" + str(counter_col_f)] = "pTU1-A-lacZ"
        row_cells[1].text = "pTU1-A-lacZ"
        row_cells[2].text = "PLACEHOLDER"
        counter_col_f = counter_col_f + 1
        row_cells = level_1_protocol_table.add_row().cells
        row_cells[0].text = "F" + str(counter_col_f)
        level_1_wells["F" + str(counter_col_f)] = "pTU1-B-lacZ"
        row_cells[1].text = "pTU1-B-lacZ"
        row_cells[2].text = "PLACEHOLDER"

    if int(GUI.transcription_unit_quantity_combo.get()) > 2:
        counter_col_f = counter_col_f + 1
        row_cells = level_1_protocol_table.add_row().cells
        row_cells[0].text = "F" + str(counter_col_f)
        level_1_wells["F" + str(counter_col_f)] = "pTU1-C-lacZ"
        row_cells[1].text = "pTU1-C-lacZ"
        row_cells[2].text = "PLACEHOLDER"

    if int(GUI.transcription_unit_quantity_combo.get()) > 3:
        counter_col_f = counter_col_f + 1
        row_cells = level_1_protocol_table.add_row().cells
        row_cells[0].text = "F" + str(counter_col_f)
        if int(GUI.transcription_unit_quantity_combo.get()) == 4:
            level_1_wells["F" + str(counter_col_f)] = "pTU1-D-lacZ"
            row_cells[1].text = "pTU1-D-lacZ"
        elif int(GUI.transcription_unit_quantity_combo.get()) == 5:
            level_1_wells["F" + str(counter_col_f)] = "pTU1-D1-lacZ"
            row_cells[1].text = "pTU1-D1-lacZ"
        row_cells[2].text = "PLACEHOLDER"

    if int(GUI.transcription_unit_quantity_combo.get()) > 4:
        counter_col_f = counter_col_f + 1
        row_cells = level_1_protocol_table.add_row().cells
        row_cells[0].text = "F" + str(counter_col_f)
        level_1_wells["F" + str(counter_col_f)] = "PTU1-E-lacZ"
        row_cells[1].text = "pTU1-E-lacZ"
        row_cells[2].text = "PLACEHOLDER"

    # 6 RES reagents
    level_1_prep_6res = document.add_paragraph("")
    level_1_prep_6res.add_run("\n" + "b) Add reagents to their corresponding wells in the Echo® Qualified Reservoir "
                                     "as outlined below")

    level_1_6res_table = document.add_table(rows=1, cols=3)
    row_1_cells = level_1_6res_table.rows[0].cells
    row_1_cells[0].text = "Well"
    row_1_cells[1].text = "Genetic part"
    row_1_cells[2].text = "Quantity (ul)"
    row_cells = level_1_6res_table.add_row().cells
    row_cells[0].text = "A1"
    row_cells[1].text = "Deionised water"
    row_cells[2].text = "PLACEHOLDER"
    row_cells = level_1_6res_table.add_row().cells
    row_cells[0].text = "A2"
    row_cells[1].text = "10x T4 DNA ligase buffer (Promega)"
    row_cells[2].text = "PLACEHOLDER"
    row_cells = level_1_6res_table.add_row().cells
    row_cells[0].text = "A3"
    row_cells[1].text = "1-3 units T4 DNA ligase (Promega)"
    row_cells[2].text = "PLACEHOLDER"
    row_cells = level_1_6res_table.add_row().cells
    row_cells[0].text = "B1"
    row_cells[1].text = "BsaI-HF (NEB)"
    row_cells[2].text = "PLACEHOLDER"









# Appendix of document, containing all parts, transcription units, and final designs
def create_appendix():
    # Parts
    document.add_page_break()
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

    # Level 0 plasmid backbones

    # Level 1 plasmid backbones

    # Level 2 plasmid backbone


# Create EcoFlex protocol
def create_protocol(event):
    MoClo.swap_codons_ecoflex()
    MoClo.check_biopart_sites_ecoflex()
    MoClo.ecoflex_fusion_sites()
    MoClo.create_transcription_unit_variants()
    MoClo.final_oligonucleotides_2()
    MoClo.transcription_unit_format()
    MoClo.level_2_format()
    calculate_part_quantity()
    title_introduction()
    if GUI.assembly_method_combo.get() == "Manual":
        create_manual_protocol()
    else:
        create_automatic_protocol()
        from EcoFlex_scripts import create_scripts
        create_scripts()

    create_appendix()

    document.save("test.docx")
