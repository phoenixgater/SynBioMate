# Import libraries
from sbol import *
import xlsxwriter

# import scripts
import GUI
import MoClo
import EcoFlex_protocol

# Global variables
part_quantity = EcoFlex_protocol.part_quantity
level_1_tu_quantity = EcoFlex_protocol.level_1_tu_quantity
level_1_384PP = EcoFlex_protocol.level_1_384PP
level_1_LDV = EcoFlex_protocol.level_1_LDV
level_1_6RES = EcoFlex_protocol.level_1_6RES
level_1_output = EcoFlex_protocol.level_1_output


def create_scripts():
    level_1_transcription_units()


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


# level 1 assembly scripts
def level_1_transcription_units():
    # 6RES reagents (deionised water)
    workbook = xlsxwriter.Workbook("6res.xlsx")
    worksheet = workbook.add_worksheet()
    script_headers(worksheet)
    row = 0
    uid = 0
    for destination_well in level_1_output.keys():
        row += 1
        uid += 1
        worksheet.write(row, 0, uid)
        worksheet.write(row, 1, "level 1 6RES source plate")
        worksheet.write(row, 2, "6RES_AQ_BP")
        worksheet.write(row, 6, destination_well)
        worksheet.write(row, 5, "Echo® Qualified 384-Well Polypropylene Source Microplate (384PP)")
        worksheet.write(row, 4, "384-Well Level 1 MoClo output plate")
        worksheet.write(row, 8, "Deionised water")
        worksheet.write(row, 7, 1875)
        dead_volume_6res = 250000
        transfer_volume = 1875
        for key in level_1_6RES:
            if level_1_6RES[key][0] == "deionised water":
                if level_1_6RES[key][1] >= dead_volume_6res + transfer_volume:
                    level_1_6RES[key][1] -= transfer_volume
                    worksheet.write(row, 3, key)
                    break
                else:
                    pass
            else:
                pass
    workbook.close()

    # LDV reagents (enzymes and buffers)
    workbook = xlsxwriter.Workbook("ldv.xlsx")
    worksheet = workbook.add_worksheet()
    script_headers(worksheet)
    row = 0
    uid = 0
    # Transfers for DNA ligase buffer
    for destination_well in level_1_output.keys():
        row += 1
        uid += 1
        worksheet.write(row, 0, uid)
        worksheet.write(row, 1, "level 1 LDV source plate")
        worksheet.write(row, 2, "384LDV_AQ_B")
        worksheet.write(row, 6, destination_well)
        worksheet.write(row, 5, "Echo® Qualified 384-Well Polypropylene Source Microplate (384PP)")
        worksheet.write(row, 4, "384-Well Level 1 MoClo output plate")
        worksheet.write(row, 8, "DNA ligase buffer")
        dead_volume_ldv_buffer = 3000
        transfer_volume = 500
        worksheet.write(row, 7, transfer_volume)
        for key in level_1_LDV:
            if level_1_LDV[key][0] == "10x DNA ligase buffer (Promega)":
                if level_1_LDV[key][1] >= dead_volume_ldv_buffer + transfer_volume:
                    level_1_LDV[key][1] -= transfer_volume
                    worksheet.write(row, 3, key)
                    break
                else:
                    pass
            else:
                pass

    # Transfers for DNA ligase
    for destination_well in level_1_output.keys():
        row += 1
        uid += 1
        worksheet.write(row, 0, uid)
        worksheet.write(row, 1, "level 1 LDV source plate")
        worksheet.write(row, 2, "384LDV_AQ_B")
        worksheet.write(row, 6, destination_well)
        worksheet.write(row, 5, "Echo® Qualified 384-Well Polypropylene Source Microplate (384PP)")
        worksheet.write(row, 4, "384-Well Level 1 MoClo output plate")
        worksheet.write(row, 8, "DNA ligase")
        dead_volume_ldv_enzyme = 6000
        transfer_volume = 125
        worksheet.write(row, 7, transfer_volume)
        for key in level_1_LDV:
            if level_1_LDV[key][0] == "1-3 units T4 DNA ligase (Promega)":
                if level_1_LDV[key][1] >= dead_volume_ldv_enzyme + transfer_volume:
                    level_1_LDV[key][1] -= transfer_volume
                    worksheet.write(row, 3, key)
                    break
                else:
                    pass
            else:
                pass

    # Transfer for BsaI-HF (restriction enzyme)
    for destination_well in level_1_output.keys():
        row += 1
        uid += 1
        worksheet.write(row, 0, uid)
        worksheet.write(row, 1, "level 1 LDV source plate")
        worksheet.write(row, 2, "384LDV_AQ_B")
        worksheet.write(row, 6, destination_well)
        worksheet.write(row, 5, "Echo® Qualified 384-Well Polypropylene Source Microplate (384PP)")
        worksheet.write(row, 4, "384-Well Level 1 MoClo output plate")
        worksheet.write(row, 8, "BsaI-HF")
        dead_volume_ldv_enzyme = 6000
        transfer_volume = 250
        worksheet.write(row, 7, transfer_volume)
        for key in level_1_LDV:
            if level_1_LDV[key][0] == "BsaI-HF (NEB)":
                if level_1_LDV[key][1] >= dead_volume_ldv_enzyme + transfer_volume:
                    level_1_LDV[key][1] -= transfer_volume
                    worksheet.write(row, 3, key)
                    break
                else:
                    pass
            else:
                pass

    workbook.close()

    # Parts and plasmid backbones
    workbook = xlsxwriter.Workbook("dna.xlsx")
    worksheet = workbook.add_worksheet()
    script_headers(worksheet)
    row = 0
    uid = 0
    for destination_well in level_1_output.keys():
        row += 1
        uid += 1





    level_1_variant_dictionary_1 = MoClo.transcription_unit_1_variants
    for variant in level_1_variant_dictionary_1:
        for part in level_1_variant_dictionary_1[variant]:
            print(part.displayId)



    print(level_1_output)