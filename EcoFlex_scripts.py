# Import libraries
from sbol import *
import xlsxwriter

# import scripts
import GUI
import MoClo
import EcoFlex_protocol

# Global variables
global part_quantity
if GUI.include_signal_combo.get() == "Yes":
    part_quantity = (len(MoClo.promoter_identities) + len(MoClo.rbs_identities) + len(MoClo.signal_identities)
                     + len(MoClo.cds_identities) + len(MoClo.terminator_identities))
elif GUI.include_signal_combo.get() == "No":
    part_quantity = (len(MoClo.promoter_identities) + len(MoClo.rbs_identities)
                     + len(MoClo.cds_identities) + len(MoClo.terminator_identities))

uid_counter = 0


def create_scripts():
    level_1_transcription_units()



def add_uid():
    global uid_counter
    uid_counter = uid_counter + 1
    return uid_counter

def script_headers(worksheet):
    worksheet.write(0, 0, "UID")
    worksheet.write(0, 1, "Source Plate Name")
    worksheet.write(0, 2, "Source plate Type")
    worksheet.write(0, 3, "Source Well")
    worksheet.write(0, 4, "Destination Plate Name")
    worksheet.write(0, 5, "Destination Plate Type")
    worksheet.write(0, 6, "Destination Well")
    worksheet.write(0, 7, "Transfer Volume")
    worksheet.write(0, 8, "Reagent")



# Scripts for reagents in 6RES plate level 1 assembly
def level_1_transcription_units():
    workbook = xlsxwriter.Workbook("script1.xlsx")
    worksheet = workbook.add_worksheet()
    script_headers(worksheet)

    # Transcription unit 1 variations

    # Transcription unit 2 variations

    # Transcription unit 3 variations

    # Transcription unit 4 variations






    '''if int(GUI.transcription_unit_quantity_combo.get()) > 1:
        row = 1
        col = 4
        for variant in MoClo.transcription_unit_1_names:
            all_variants.append(variant)
            worksheet.write(row, col, variant)
            worksheet.write(row, 0, add_uid())
            worksheet.write(row, 2, "6RES_AQ_BP")
            worksheet.write(row, 1, "Reagents")
            worksheet.write(row, 5, "384-Well Polypropylene Source Microplate")
            worksheet.write(row, 8, "Deionised water")
            worksheet.write(row, 7, "VOLUME PLACEHOLDER")
            worksheet.write(row, 3, "A1")
            if len(all_variants) < 17:
                counter_col_j = counter_col_j + 1
                worksheet.write(row, 6, "J" + str(counter_col_j))
            if 16 < len(all_variants) < 33:
                counter_col_k = counter_col_k + 1
                worksheet.write(row, 6, "K" + str(counter_col_k))
            if 32 < len(all_variants) < 49:
                counter_col_l = counter_col_l + 1
                worksheet.write(row, 6, "L" + str(counter_col_l))
            if 48 < len(all_variants) < 65:
                counter_col_m = counter_col_m + 1
                worksheet.write(row, 6, "M" + str(counter_col_m))
            if 64 < len(all_variants) < 81:
                counter_col_n = counter_col_n + 1
                worksheet.write(row, 6, "N" + str(counter_col_n))
            if 80 < len(all_variants) < 97:
                counter_col_o = counter_col_o + 1
                worksheet.write(row, 6, "O" + str(counter_col_o))
            if 96 < len(all_variants) < 113:
                counter_col_p = counter_col_p + 1
                worksheet.write(row, 6, "P" + str(counter_col_p))
            if len(all_variants) > 113:
                worksheet.write(row, 6, "ERROR: WELL CAPACITY REACHED")
            row = row + 1

        for variant in MoClo.transcription_unit_2_names:
            all_variants.append(variant)
            worksheet.write(row, col, variant)
            worksheet.write(row, 0, add_uid())
            worksheet.write(row, 2, "6RES_AQ_BP")
            worksheet.write(row, 1, "Reagents")
            worksheet.write(row, 5, "384-Well Polypropylene Source Microplate")
            worksheet.write(row, 8, "Deionised water")
            worksheet.write(row, 7, "VOLUME PLACEHOLDER")
            worksheet.write(row, 3, "A1")
            if len(all_variants) < 17:
                counter_col_j = counter_col_j + 1
                worksheet.write(row, 6, "J" + str(counter_col_j))
            if 16 < len(all_variants) < 33:
                counter_col_k = counter_col_k + 1
                worksheet.write(row, 6, "K" + str(counter_col_k))
            if 32 < len(all_variants) < 49:
                counter_col_l = counter_col_l + 1
                worksheet.write(row, 6, "L" + str(counter_col_l))
            if 48 < len(all_variants) < 65:
                counter_col_m = counter_col_m + 1
                worksheet.write(row, 6, "M" + str(counter_col_m))
            if 64 < len(all_variants) < 81:
                counter_col_n = counter_col_n + 1
                worksheet.write(row, 6, "N" + str(counter_col_n))
            if 80 < len(all_variants) < 97:
                counter_col_o = counter_col_o + 1
                worksheet.write(row, 6, "O" + str(counter_col_o))
            if 96 < len(all_variants) < 113:
                counter_col_p = counter_col_p + 1
                worksheet.write(row, 6, "P" + str(counter_col_p))
            if len(all_variants) > 113:
                worksheet.write(row, 6, "ERROR: WELL CAPACITY REACHED")
            row = row + 1


############### DNA ligase buffer ###################
    all_variants = []
    counter_col_j = 0
    counter_col_k = 0
    counter_col_l = 0
    counter_col_m = 0
    counter_col_n = 0
    counter_col_o = 0
    counter_col_p = 0


    if int(GUI.transcription_unit_quantity_combo.get()) > 1:
        for variant in MoClo.transcription_unit_1_names:
            all_variants.append(variant)
            worksheet.write(row, col, variant)
            worksheet.write(row, 0, add_uid())
            worksheet.write(row, 2, "6RES_AQ_BP")
            worksheet.write(row, 1, "Reagents")
            worksheet.write(row, 5, "384-Well Polypropylene Source Microplate")
            worksheet.write(row, 8, "10x T4 DNA ligase buffer")
            worksheet.write(row, 7, "VOLUME PLACEHOLDER")
            worksheet.write(row, 3, "A2")
            if len(all_variants) < 17:
                counter_col_j = counter_col_j + 1
                worksheet.write(row, 6, "J" + str(counter_col_j))
            if 16 < len(all_variants) < 33:
                counter_col_k = counter_col_k + 1
                worksheet.write(row, 6, "K" + str(counter_col_k))
            if 32 < len(all_variants) < 49:
                counter_col_l = counter_col_l + 1
                worksheet.write(row, 6, "L" + str(counter_col_l))
            if 48 < len(all_variants) < 65:
                counter_col_m = counter_col_m + 1
                worksheet.write(row, 6, "M" + str(counter_col_m))
            if 64 < len(all_variants) < 81:
                counter_col_n = counter_col_n + 1
                worksheet.write(row, 6, "N" + str(counter_col_n))
            if 80 < len(all_variants) < 97:
                counter_col_o = counter_col_o + 1
                worksheet.write(row, 6, "O" + str(counter_col_o))
            if 96 < len(all_variants) < 113:
                counter_col_p = counter_col_p + 1
                worksheet.write(row, 6, "P" + str(counter_col_p))
            if len(all_variants) > 113:
                worksheet.write(row, 6, "ERROR: WELL CAPACITY REACHED")
            row = row + 1

        for variant in MoClo.transcription_unit_2_names:
            all_variants.append(variant)
            worksheet.write(row, col, variant)
            worksheet.write(row, 0, add_uid())
            worksheet.write(row, 2, "6RES_AQ_BP")
            worksheet.write(row, 1, "Reagents")
            worksheet.write(row, 5, "384-Well Polypropylene Source Microplate")
            worksheet.write(row, 8, "10x T4 DNA ligase buffer")
            worksheet.write(row, 7, "VOLUME PLACEHOLDER")
            worksheet.write(row, 3, "A2")
            if len(all_variants) < 17:
                counter_col_j = counter_col_j + 1
                worksheet.write(row, 6, "J" + str(counter_col_j))
            if 16 < len(all_variants) < 33:
                counter_col_k = counter_col_k + 1
                worksheet.write(row, 6, "K" + str(counter_col_k))
            if 32 < len(all_variants) < 49:
                counter_col_l = counter_col_l + 1
                worksheet.write(row, 6, "L" + str(counter_col_l))
            if 48 < len(all_variants) < 65:
                counter_col_m = counter_col_m + 1
                worksheet.write(row, 6, "M" + str(counter_col_m))
            if 64 < len(all_variants) < 81:
                counter_col_n = counter_col_n + 1
                worksheet.write(row, 6, "N" + str(counter_col_n))
            if 80 < len(all_variants) < 97:
                counter_col_o = counter_col_o + 1
                worksheet.write(row, 6, "O" + str(counter_col_o))
            if 96 < len(all_variants) < 113:
                counter_col_p = counter_col_p + 1
                worksheet.write(row, 6, "P" + str(counter_col_p))
            if len(all_variants) > 113:
                worksheet.write(row, 6, "ERROR: WELL CAPACITY REACHED")
            row = row + 1

        ############### DNA ligase buffer ###################
        all_variants = []
        counter_col_j = 0
        counter_col_k = 0
        counter_col_l = 0
        counter_col_m = 0
        counter_col_n = 0
        counter_col_o = 0
        counter_col_p = 0

        if int(GUI.transcription_unit_quantity_combo.get()) > 1:
            for variant in MoClo.transcription_unit_1_names:
                all_variants.append(variant)
                worksheet.write(row, col, variant)
                worksheet.write(row, 0, add_uid())
                worksheet.write(row, 2, "6RES_AQ_BP")
                worksheet.write(row, 1, "Reagents")
                worksheet.write(row, 5, "384-Well Polypropylene Source Microplate")
                worksheet.write(row, 8, "10x T4 DNA ligase")
                worksheet.write(row, 7, "VOLUME PLACEHOLDER")
                worksheet.write(row, 3, "A3")
                if len(all_variants) < 17:
                    counter_col_j = counter_col_j + 1
                    worksheet.write(row, 6, "J" + str(counter_col_j))
                if 16 < len(all_variants) < 33:
                    counter_col_k = counter_col_k + 1
                    worksheet.write(row, 6, "K" + str(counter_col_k))
                if 32 < len(all_variants) < 49:
                    counter_col_l = counter_col_l + 1
                    worksheet.write(row, 6, "L" + str(counter_col_l))
                if 48 < len(all_variants) < 65:
                    counter_col_m = counter_col_m + 1
                    worksheet.write(row, 6, "M" + str(counter_col_m))
                if 64 < len(all_variants) < 81:
                    counter_col_n = counter_col_n + 1
                    worksheet.write(row, 6, "N" + str(counter_col_n))
                if 80 < len(all_variants) < 97:
                    counter_col_o = counter_col_o + 1
                    worksheet.write(row, 6, "O" + str(counter_col_o))
                if 96 < len(all_variants) < 113:
                    counter_col_p = counter_col_p + 1
                    worksheet.write(row, 6, "P" + str(counter_col_p))
                if len(all_variants) > 113:
                    worksheet.write(row, 6, "ERROR: WELL CAPACITY REACHED")
                row = row + 1

            for variant in MoClo.transcription_unit_2_names:
                all_variants.append(variant)
                worksheet.write(row, col, variant)
                worksheet.write(row, 0, add_uid())
                worksheet.write(row, 2, "6RES_AQ_BP")
                worksheet.write(row, 1, "Reagents")
                worksheet.write(row, 5, "384-Well Polypropylene Source Microplate")
                worksheet.write(row, 8, "10x T4 DNA ligase")
                worksheet.write(row, 7, "VOLUME PLACEHOLDER")
                worksheet.write(row, 3, "A3")
                if len(all_variants) < 17:
                    counter_col_j = counter_col_j + 1
                    worksheet.write(row, 6, "J" + str(counter_col_j))
                if 16 < len(all_variants) < 33:
                    counter_col_k = counter_col_k + 1
                    worksheet.write(row, 6, "K" + str(counter_col_k))
                if 32 < len(all_variants) < 49:
                    counter_col_l = counter_col_l + 1
                    worksheet.write(row, 6, "L" + str(counter_col_l))
                if 48 < len(all_variants) < 65:
                    counter_col_m = counter_col_m + 1
                    worksheet.write(row, 6, "M" + str(counter_col_m))
                if 64 < len(all_variants) < 81:
                    counter_col_n = counter_col_n + 1
                    worksheet.write(row, 6, "N" + str(counter_col_n))
                if 80 < len(all_variants) < 97:
                    counter_col_o = counter_col_o + 1
                    worksheet.write(row, 6, "O" + str(counter_col_o))
                if 96 < len(all_variants) < 113:
                    counter_col_p = counter_col_p + 1
                    worksheet.write(row, 6, "P" + str(counter_col_p))
                if len(all_variants) > 113:
                    worksheet.write(row, 6, "ERROR: WELL CAPACITY REACHED")
                row = row + 1

        ############### BsaI-HF restriction enzyme ###################
        all_variants = []
        counter_col_j = 0
        counter_col_k = 0
        counter_col_l = 0
        counter_col_m = 0
        counter_col_n = 0
        counter_col_o = 0
        counter_col_p = 0

        if int(GUI.transcription_unit_quantity_combo.get()) > 1:
            for variant in MoClo.transcription_unit_1_names:
                all_variants.append(variant)
                worksheet.write(row, col, variant)
                worksheet.write(row, 0, add_uid())
                worksheet.write(row, 2, "6RES_AQ_BP")
                worksheet.write(row, 1, "Reagents")
                worksheet.write(row, 5, "384-Well Polypropylene Source Microplate")
                worksheet.write(row, 8, "BsaI-HF (NEB)")
                worksheet.write(row, 7, "VOLUME PLACEHOLDER")
                worksheet.write(row, 3, "B1")
                if len(all_variants) < 17:
                    counter_col_j = counter_col_j + 1
                    worksheet.write(row, 6, "J" + str(counter_col_j))
                if 16 < len(all_variants) < 33:
                    counter_col_k = counter_col_k + 1
                    worksheet.write(row, 6, "K" + str(counter_col_k))
                if 32 < len(all_variants) < 49:
                    counter_col_l = counter_col_l + 1
                    worksheet.write(row, 6, "L" + str(counter_col_l))
                if 48 < len(all_variants) < 65:
                    counter_col_m = counter_col_m + 1
                    worksheet.write(row, 6, "M" + str(counter_col_m))
                if 64 < len(all_variants) < 81:
                    counter_col_n = counter_col_n + 1
                    worksheet.write(row, 6, "N" + str(counter_col_n))
                if 80 < len(all_variants) < 97:
                    counter_col_o = counter_col_o + 1
                    worksheet.write(row, 6, "O" + str(counter_col_o))
                if 96 < len(all_variants) < 113:
                    counter_col_p = counter_col_p + 1
                    worksheet.write(row, 6, "P" + str(counter_col_p))
                if len(all_variants) > 113:
                    worksheet.write(row, 6, "ERROR: WELL CAPACITY REACHED")
                row = row + 1

            for variant in MoClo.transcription_unit_2_names:
                all_variants.append(variant)
                worksheet.write(row, col, variant)
                worksheet.write(row, 0, add_uid())
                worksheet.write(row, 2, "6RES_AQ_BP")
                worksheet.write(row, 1, "Reagents")
                worksheet.write(row, 5, "384-Well Polypropylene Source Microplate")
                worksheet.write(row, 8, "BsaI-HF (NEB)")
                worksheet.write(row, 7, "VOLUME PLACEHOLDER")
                worksheet.write(row, 3, "B1")
                if len(all_variants) < 17:
                    counter_col_j = counter_col_j + 1
                    worksheet.write(row, 6, "J" + str(counter_col_j))
                if 16 < len(all_variants) < 33:
                    counter_col_k = counter_col_k + 1
                    worksheet.write(row, 6, "K" + str(counter_col_k))
                if 32 < len(all_variants) < 49:
                    counter_col_l = counter_col_l + 1
                    worksheet.write(row, 6, "L" + str(counter_col_l))
                if 48 < len(all_variants) < 65:
                    counter_col_m = counter_col_m + 1
                    worksheet.write(row, 6, "M" + str(counter_col_m))
                if 64 < len(all_variants) < 81:
                    counter_col_n = counter_col_n + 1
                    worksheet.write(row, 6, "N" + str(counter_col_n))
                if 80 < len(all_variants) < 97:
                    counter_col_o = counter_col_o + 1
                    worksheet.write(row, 6, "O" + str(counter_col_o))
                if 96 < len(all_variants) < 113:
                    counter_col_p = counter_col_p + 1
                    worksheet.write(row, 6, "P" + str(counter_col_p))
                if len(all_variants) > 113:
                    worksheet.write(row, 6, "ERROR: WELL CAPACITY REACHED")
                row = row + 1'''








    workbook.close()





'''
    # Promoters
    row = 0
    col = 0
    for promoter in MoClo.promoter_identities:
        worksheet.write(row, col, promoter)
        row += 1
    workbook.close()
'''
