# Import libraries
from sbol import *
import xlsxwriter

# import scripts
import GUI
import MoClo
import EcoFlex_protocol

# Global variables
# Level 1
part_quantity = EcoFlex_protocol.part_quantity
level_1_tu_quantity = EcoFlex_protocol.level_1_tu_quantity
level_1_dictionary = MoClo.level_1_transcription_unit_dictionary
level_1_384PP = EcoFlex_protocol.level_1_384PP
level_1_LDV = EcoFlex_protocol.level_1_LDV
level_1_6RES = EcoFlex_protocol.level_1_6RES
level_1_output = EcoFlex_protocol.level_1_output

# Level 2
level_2_dictionary = MoClo.level_2_transcription_unit_dictionary
level_2_384PP = EcoFlex_protocol.level_2_384PP
level_2_LDV = EcoFlex_protocol.level_2_LDV
level_2_6RES = EcoFlex_protocol.level_2_6RES
level_2_output = EcoFlex_protocol.level_2_output


def create_scripts():
    level_1_transcription_units()
    level_2_transcription_units()


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
        if level_1_output[destination_well][0].find("reaction 1:1") >= 0:
            transfer_volume = EcoFlex_protocol.transfer_volume("level_1_water_1_1")
        elif level_1_output[destination_well][0].find("reaction 1:2") >= 0:
            transfer_volume = EcoFlex_protocol.transfer_volume("level_1_water_1_2")
        elif level_1_output[destination_well][0].find("reaction 2:1") >= 0:
            transfer_volume = EcoFlex_protocol.transfer_volume("level_1_water_2_1")
        row += 1
        uid += 1
        worksheet.write(row, 0, uid)
        worksheet.write(row, 1, "level 1 6RES source plate")
        worksheet.write(row, 2, "6RES_AQ_BP")
        worksheet.write(row, 6, destination_well)
        worksheet.write(row, 5, "Echo® Qualified 384-Well Polypropylene Source Microplate (384PP)")
        worksheet.write(row, 4, "384-Well Level 1 MoClo output plate")
        worksheet.write(row, 8, "Deionised water")
        worksheet.write(row, 7, transfer_volume)
        dead_volume_6res = 250000
        for key in level_1_6RES:
            if level_1_6RES[key][0] == "deionised water":
                if level_1_6RES[key][1] >= dead_volume_6res + transfer_volume:
                    level_1_6RES[key][1] -= transfer_volume
                    worksheet.write(row, 3, key)
                    break
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
    workbook.close()

    # Parts and plasmid backbones
    workbook = xlsxwriter.Workbook("dna.xlsx")
    worksheet = workbook.add_worksheet()
    script_headers(worksheet)

    # Parts
    dead_volume_dna = 15000
    row = 0
    uid = 0

    for destination_well in level_1_output.keys():
        for tu_name in level_1_dictionary.keys():
            if level_1_output[destination_well][0].find(tu_name) >= 0:
                part_list = level_1_dictionary[tu_name]
                for part in part_list:
                    for source_well in level_1_384PP.keys():
                        if part == level_1_384PP[source_well][0]:
                                if level_1_output[destination_well][0].find("reaction 1:1") >= 0:
                                    transfer_volume = EcoFlex_protocol.transfer_volume("level_1_part_1_1")
                                elif level_1_output[destination_well][0].find("reaction 1:2") >= 0:
                                    transfer_volume = EcoFlex_protocol.transfer_volume("level_1_part_1_2")
                                elif level_1_output[destination_well][0].find("reaction 2:1") >= 0:
                                    transfer_volume = EcoFlex_protocol.transfer_volume("level_1_part_2_1")
                                if level_1_384PP[source_well][1] >= dead_volume_dna + transfer_volume:
                                    level_1_384PP[source_well][1] -= transfer_volume
                                    row += 1
                                    uid += 1
                                    worksheet.write(row, 0, uid)
                                    worksheet.write(row, 1, "level 1 384 source plate (DNA components)")
                                    worksheet.write(row, 2, "384LDV_AQ_B")
                                    worksheet.write(row, 3, source_well)
                                    worksheet.write(row, 4, "384-Well Level 1 MoClo output plate")
                                    worksheet.write(row, 5, "Echo® Qualified 384-Well Polypropylene Source Microplate ("
                                                            "384PP)")
                                    worksheet.write(row, 6, destination_well)
                                    worksheet.write(row, 7, transfer_volume)
                                    worksheet.write(row, 8, part)
                                    break

    # Plasmid backbones
    for destination_well in level_1_output.keys():
        if level_1_output[destination_well][0].find("Transcription unit 1") == 0:
            for source_well in level_1_384PP:
                if level_1_384PP[source_well][0] == "pTU1-A-lacZ":
                    if level_1_output[destination_well][0].find("reaction 1:1") >= 0:
                        transfer_volume = EcoFlex_protocol.transfer_volume("level_1_backbone_1_1")
                    elif level_1_output[destination_well][0].find("reaction 1:2") >= 0:
                        transfer_volume = EcoFlex_protocol.transfer_volume("level_1_backbone_1_2")
                    elif level_1_output[destination_well][0].find("reaction 2:1") >= 0:
                        transfer_volume = EcoFlex_protocol.transfer_volume("level_1_backbone_2_1")
                    if level_1_384PP[source_well][1] >= dead_volume_dna + transfer_volume:
                        level_1_384PP[source_well][1] -= transfer_volume
                        row += 1
                        uid += 1
                        worksheet.write(row, 0, uid)
                        worksheet.write(row, 1, "level 1 384 source plate (DNA components)")
                        worksheet.write(row, 2, "384LDV_AQ_B")
                        worksheet.write(row, 3, source_well)
                        worksheet.write(row, 4, "384-Well Level 1 MoClo output plate")
                        worksheet.write(row, 5, "Echo® Qualified 384-Well Polypropylene Source Microplate ("
                                                "384PP)")
                        worksheet.write(row, 6, destination_well)
                        worksheet.write(row, 7, transfer_volume)
                        worksheet.write(row, 8, "pTU1-A-lacZ")
                        break

        elif level_1_output[destination_well][0].find("Transcription unit 2") >= 0:
            for source_well in level_1_384PP:
                if level_1_384PP[source_well][0] == "pTU1-B-lacZ":
                    if level_1_output[destination_well][0].find("reaction 1:1") >= 0:
                        transfer_volume = EcoFlex_protocol.transfer_volume("level_1_backbone_1_1")
                    elif level_1_output[destination_well][0].find("reaction 1:2") >= 0:
                        transfer_volume = EcoFlex_protocol.transfer_volume("level_1_backbone_1_2")
                    elif level_1_output[destination_well][0].find("reaction 2:1") >= 0:
                        transfer_volume = EcoFlex_protocol.transfer_volume("level_1_backbone_2_1")
                    if level_1_384PP[source_well][1] >= dead_volume_dna + transfer_volume:
                        level_1_384PP[source_well][1] -= transfer_volume
                        row += 1
                        uid += 1
                        worksheet.write(row, 0, uid)
                        worksheet.write(row, 1, "level 1 384 source plate (DNA components)")
                        worksheet.write(row, 2, "384LDV_AQ_B")
                        worksheet.write(row, 3, source_well)
                        worksheet.write(row, 4, "384-Well Level 1 MoClo output plate")
                        worksheet.write(row, 5, "Echo® Qualified 384-Well Polypropylene Source Microplate ("
                                                "384PP)")
                        worksheet.write(row, 6, destination_well)
                        worksheet.write(row, 7, transfer_volume)
                        worksheet.write(row, 8, "pTU1-B-lacZ")
                        break

        elif level_1_output[destination_well][0].find("Transcription unit 3") >= 0:
            for source_well in level_1_384PP:
                if level_1_384PP[source_well][0] == "pTU1-C-lacZ":
                    if level_1_output[destination_well][0].find("reaction 1:1") >= 0:
                        transfer_volume = EcoFlex_protocol.transfer_volume("level_1_backbone_1_1")
                    elif level_1_output[destination_well][0].find("reaction 1:2") >= 0:
                        transfer_volume = EcoFlex_protocol.transfer_volume("level_1_backbone_1_2")
                    elif level_1_output[destination_well][0].find("reaction 2:1") >= 0:
                        transfer_volume = EcoFlex_protocol.transfer_volume("level_1_backbone_2_1")
                    if level_1_384PP[source_well][1] >= dead_volume_dna + transfer_volume:
                        level_1_384PP[source_well][1] -= transfer_volume
                        row += 1
                        uid += 1
                        worksheet.write(row, 0, uid)
                        worksheet.write(row, 1, "level 1 384 source plate (DNA components)")
                        worksheet.write(row, 2, "384LDV_AQ_B")
                        worksheet.write(row, 3, source_well)
                        worksheet.write(row, 4, "384-Well Level 1 MoClo output plate")
                        worksheet.write(row, 5, "Echo® Qualified 384-Well Polypropylene Source Microplate ("
                                                "384PP)")
                        worksheet.write(row, 6, destination_well)
                        worksheet.write(row, 7, transfer_volume)
                        worksheet.write(row, 8, "pTU1-C-lacZ")
                        break

        elif level_1_output[destination_well][0].find("Transcription unit 4") == 0:
            if int(GUI.transcription_unit_quantity_combo.get()) == 4:
                for source_well in level_1_384PP:
                    if level_1_384PP[source_well][0] == "pTU1-D-lacZ":
                        if level_1_output[destination_well][0].find("reaction 1:1") >= 0:
                            transfer_volume = EcoFlex_protocol.transfer_volume("level_1_backbone_1_1")
                        elif level_1_output[destination_well][0].find("reaction 1:2") >= 0:
                            transfer_volume = EcoFlex_protocol.transfer_volume("level_1_backbone_1_2")
                        elif level_1_output[destination_well][0].find("reaction 2:1") >= 0:
                            transfer_volume = EcoFlex_protocol.transfer_volume("level_1_backbone_2_1")
                        if level_1_384PP[source_well][1] >= dead_volume_dna + transfer_volume:
                            level_1_384PP[source_well][1] -= transfer_volume
                            row += 1
                            uid += 1
                            worksheet.write(row, 0, uid)
                            worksheet.write(row, 1, "level 1 384 source plate (DNA components)")
                            worksheet.write(row, 2, "384LDV_AQ_B")
                            worksheet.write(row, 3, source_well)
                            worksheet.write(row, 4, "384-Well Level 1 MoClo output plate")
                            worksheet.write(row, 5, "Echo® Qualified 384-Well Polypropylene Source Microplate ("
                                                    "384PP)")
                            worksheet.write(row, 6, destination_well)
                            worksheet.write(row, 7, transfer_volume)
                            worksheet.write(row, 8, "pTU1-D-lacZ")
                            break

            elif int(GUI.transcription_unit_quantity_combo.get()) == 5:
                for source_well in level_1_384PP:
                    if level_1_384PP[source_well][0] == "pTU1-D1-lacZ":
                        if level_1_output[destination_well][0].find("reaction 1:1") >= 0:
                            transfer_volume = EcoFlex_protocol.transfer_volume("level_1_backbone_1_1")
                        elif level_1_output[destination_well][0].find("reaction 1:2") >= 0:
                            transfer_volume = EcoFlex_protocol.transfer_volume("level_1_backbone_1_2")
                        elif level_1_output[destination_well][0].find("reaction 2:1") >= 0:
                            transfer_volume = EcoFlex_protocol.transfer_volume("level_1_backbone_2_1")
                        if level_1_384PP[source_well][1] >= dead_volume_dna + transfer_volume:
                            level_1_384PP[source_well][1] -= transfer_volume
                            row += 1
                            uid += 1
                            worksheet.write(row, 0, uid)
                            worksheet.write(row, 1, "level 1 384 source plate (DNA components)")
                            worksheet.write(row, 2, "384LDV_AQ_B")
                            worksheet.write(row, 3, source_well)
                            worksheet.write(row, 4, "384-Well Level 1 MoClo output plate")
                            worksheet.write(row, 5, "Echo® Qualified 384-Well Polypropylene Source Microplate ("
                                                    "384PP)")
                            worksheet.write(row, 6, destination_well)
                            worksheet.write(row, 7, transfer_volume)
                            worksheet.write(row, 8, "pTU1-D1-lacZ")
                            break

        elif level_1_output[destination_well][0].find("Transcription unit 5") == 0:
            for source_well in level_1_384PP:
                if level_1_384PP[source_well][0] == "pTU1-E-lacZ":
                    if level_1_output[destination_well][0].find("reaction 1:1") >= 0:
                        transfer_volume = EcoFlex_protocol.transfer_volume("level_1_backbone_1_1")
                    elif level_1_output[destination_well][0].find("reaction 1:2") >= 0:
                        transfer_volume = EcoFlex_protocol.transfer_volume("level_1_backbone_1_2")
                    elif level_1_output[destination_well][0].find("reaction 2:1") >= 0:
                        transfer_volume = EcoFlex_protocol.transfer_volume("level_1_backbone_2_1")
                    if level_1_384PP[source_well][1] >= dead_volume_dna + transfer_volume:
                        level_1_384PP[source_well][1] -= transfer_volume
                        row += 1
                        uid += 1
                        worksheet.write(row, 0, uid)
                        worksheet.write(row, 1, "level 1 384 source plate (DNA components)")
                        worksheet.write(row, 2, "384LDV_AQ_B")
                        worksheet.write(row, 3, source_well)
                        worksheet.write(row, 4, "384-Well Level 1 MoClo output plate")
                        worksheet.write(row, 5, "Echo® Qualified 384-Well Polypropylene Source Microplate ("
                                                "384PP)")
                        worksheet.write(row, 6, destination_well)
                        worksheet.write(row, 7, transfer_volume)
                        worksheet.write(row, 8, "pTU1-E-lacZ")
                        break
    workbook.close()


def level_2_transcription_units():
    # 6RES reagents (deionised water) level 2
    workbook = xlsxwriter.Workbook("6res_2.xlsx")
    worksheet = workbook.add_worksheet()
    script_headers(worksheet)
    row = 0
    uid = 0
    for destination_well in level_2_output.keys():
        if level_2_output[destination_well][0].find("reaction 1:1") >= 0:
            transfer_volume = EcoFlex_protocol.transfer_volume("level_2_water_1_1")
        elif level_2_output[destination_well][0].find("reaction 1:2") >= 0:
            transfer_volume = EcoFlex_protocol.transfer_volume("level_2_water_1_2")
        elif level_2_output[destination_well][0].find("reaction 2:1") >= 0:
            transfer_volume = EcoFlex_protocol.transfer_volume("level_2_water_2_1")
        row += 1
        uid += 1
        worksheet.write(row, 0, uid)
        worksheet.write(row, 1, "level 2 6RES source plate")
        worksheet.write(row, 2, "6RES_AQ_BP")
        worksheet.write(row, 6, destination_well)
        worksheet.write(row, 5, "Echo® Qualified 384-Well Polypropylene Source Microplate (384PP)")
        worksheet.write(row, 4, "384-Well Level 2 MoClo output plate")
        worksheet.write(row, 8, "Deionised water")
        worksheet.write(row, 7, 2875)
        dead_volume_6res = 250000
        transfer_volume = 2875
        for well in level_2_6RES:
            if level_1_6RES[well][0] == "deionised water":
                if level_1_6RES[well][1] >= dead_volume_6res + transfer_volume:
                    level_1_6RES[well][1] -= transfer_volume
                    worksheet.write(row, 3, well)
                    break
    workbook.close()

    # LDV reagents (enzymes and buffers) level 2
    workbook = xlsxwriter.Workbook("ldv_2.xlsx")
    worksheet = workbook.add_worksheet()
    script_headers(worksheet)
    row = 0
    uid = 0
    # Transfers for DNA ligase buffer level 2
    for destination_well in level_2_output.keys():
        row += 1
        uid += 1
        worksheet.write(row, 0, uid)
        worksheet.write(row, 1, "level 2 LDV source plate")
        worksheet.write(row, 2, "384LDV_AQ_B")
        worksheet.write(row, 6, destination_well)
        worksheet.write(row, 5, "Echo® Qualified 384-Well Polypropylene Source Microplate (384PP)")
        worksheet.write(row, 4, "384-Well Level 2 MoClo output plate")
        worksheet.write(row, 8, "DNA ligase buffer")
        dead_volume_ldv_buffer = 3000
        transfer_volume = 500
        worksheet.write(row, 7, transfer_volume)
        for well in level_2_LDV:
            if level_2_LDV[well][0] == "10x DNA ligase buffer (Promega)":
                if level_2_LDV[well][1] >= dead_volume_ldv_buffer + transfer_volume:
                    level_2_LDV[well][1] -= transfer_volume
                    worksheet.write(row, 3, well)
                    break

    # Transfers for DNA ligase level 2
    for destination_well in level_2_output.keys():
        row += 1
        uid += 1
        worksheet.write(row, 0, uid)
        worksheet.write(row, 1, "level 2 LDV source plate")
        worksheet.write(row, 2, "384LDV_AQ_B")
        worksheet.write(row, 6, destination_well)
        worksheet.write(row, 5, "Echo® Qualified 384-Well Polypropylene Source Microplate (384PP)")
        worksheet.write(row, 4, "384-Well Level 2 MoClo output plate")
        worksheet.write(row, 8, "DNA ligase")
        dead_volume_ldv_enzyme = 6000
        transfer_volume = 125
        worksheet.write(row, 7, transfer_volume)
        for well in level_2_LDV:
            if level_2_LDV[well][0] == "1-3 units T4 DNA ligase (Promega)":
                if level_2_LDV[well][1] >= dead_volume_ldv_enzyme + transfer_volume:
                    level_2_LDV[well][1] -= transfer_volume
                    worksheet.write(row, 3, well)
                    break

    # Transfer for BsmBI (restriction enzyme) level 2
    for destination_well in level_2_output.keys():
        row += 1
        uid += 1
        worksheet.write(row, 0, uid)
        worksheet.write(row, 1, "level 2 LDV source plate")
        worksheet.write(row, 2, "384LDV_AQ_B")
        worksheet.write(row, 6, destination_well)
        worksheet.write(row, 5, "Echo® Qualified 384-Well Polypropylene Source Microplate (384PP)")
        worksheet.write(row, 4, "384-Well Level 2 MoClo output plate")
        worksheet.write(row, 8, "BsmBI (NEB)")
        dead_volume_ldv_enzyme = 6000
        transfer_volume = 250
        worksheet.write(row, 7, transfer_volume)
        for well in level_2_LDV:
            if level_2_LDV[well][0] == "BsmBI (NEB)":
                if level_2_LDV[well][1] >= dead_volume_ldv_enzyme + transfer_volume:
                    level_2_LDV[well][1] -= transfer_volume
                    worksheet.write(row, 3, well)
                    break
    workbook.close()

    # level 1 TU's and level 2 plasmid backbones level 2
    workbook = xlsxwriter.Workbook("dna_2.xlsx")
    worksheet = workbook.add_worksheet()
    script_headers(worksheet)

    # level 1 Transcription units (TU's) level 2
    dead_volume_dna = 15000
    transfer_volume = 500
    row = 0
    uid = 0

    for destination_well in level_2_output.keys():
        for construct_name in level_2_dictionary.keys():
            if level_2_output[destination_well][0] == construct_name:
                tu_list = level_2_dictionary[construct_name]
                for tu in tu_list:
                    for source_well in level_2_384PP.keys():
                        if tu == level_2_384PP[source_well][0]:
                            if level_2_output[destination_well][0].find("reaction 1:1") >= 0:
                                transfer_volume = EcoFlex_protocol.transfer_volume("level_2_tu_1_1")
                            elif level_2_output[destination_well][0].find("reaction 1:2") >= 0:
                                transfer_volume = EcoFlex_protocol.transfer_volume("level_2_tu_1_2")
                            elif level_2_output[destination_well][0].find("reaction 2:1") >= 0:
                                transfer_volume = EcoFlex_protocol.transfer_volume("level_2_tu_2_1")
                            if level_2_384PP[source_well][1] >= dead_volume_dna + transfer_volume:
                                level_2_384PP[source_well][1] -= transfer_volume
                                row += 1
                                uid += 1
                                worksheet.write(row, 0, uid)
                                worksheet.write(row, 1, "level 2 384 source plate (DNA components)")
                                worksheet.write(row, 2, "384LDV_AQ_B")
                                worksheet.write(row, 3, source_well)
                                worksheet.write(row, 4, "384-Well Level 2 MoClo output plate")
                                worksheet.write(row, 5, "Echo® Qualified 384-Well Polypropylene Source Microplate ("
                                                        "384PP)")
                                worksheet.write(row, 6, destination_well)
                                worksheet.write(row, 7, transfer_volume)
                                worksheet.write(row, 8, tu)
                                break

    # Plasmid backbones level 2
    transfer_volume = 250
    for destination_well in level_2_output.keys():
        if int(GUI.transcription_unit_quantity_combo.get()) == 2:
            for source_well in level_2_384PP.keys():
                if level_2_384PP[source_well][0] == "pTU2-a-RFP":
                    if level_2_output[destination_well][0].find("reaction 1:1") >= 0:
                        transfer_volume = EcoFlex_protocol.transfer_volume("level_2_backbone_1_1")
                    elif level_2_output[destination_well][0].find("reaction 1:2") >= 0:
                        transfer_volume = EcoFlex_protocol.transfer_volume("level_2_backbone_1_2")
                    elif level_2_output[destination_well][0].find("reaction 2:1") >= 0:
                        transfer_volume = EcoFlex_protocol.transfer_volume("level_2_backbone_2_1")
                    if level_2_384PP[source_well][1] >= dead_volume_dna + transfer_volume:
                        level_2_384PP[source_well][1] -= transfer_volume
                        row += 1
                        uid += 1
                        worksheet.write(row, 0, uid)
                        worksheet.write(row, 1, "level 2 384 source plate (DNA components)")
                        worksheet.write(row, 2, "384LDV_AQ_B")
                        worksheet.write(row, 3, source_well)
                        worksheet.write(row, 4, "384-Well Level 2 MoClo output plate")
                        worksheet.write(row, 5, "Echo® Qualified 384-Well Polypropylene Source Microplate ("
                                                "384PP)")
                        worksheet.write(row, 6, destination_well)
                        worksheet.write(row, 7, transfer_volume)
                        worksheet.write(row, 8, "pTU2-a-RFP")
                        break

        elif int(GUI.transcription_unit_quantity_combo.get()) == 3:
            for source_well in level_2_384PP.keys():
                if level_2_384PP[source_well][0] == "pTU2-b-RFP":
                    if level_2_output[destination_well][0].find("reaction 1:1") >= 0:
                        transfer_volume = EcoFlex_protocol.transfer_volume("level_2_backbone_1_1")
                    elif level_2_output[destination_well][0].find("reaction 1:2") >= 0:
                        transfer_volume = EcoFlex_protocol.transfer_volume("level_2_backbone_1_2")
                    elif level_2_output[destination_well][0].find("reaction 2:1") >= 0:
                        transfer_volume = EcoFlex_protocol.transfer_volume("level_2_backbone_2_1")
                    if level_2_384PP[source_well][1] >= dead_volume_dna + transfer_volume:
                        level_2_384PP[source_well][1] -= transfer_volume
                        row += 1
                        uid += 1
                        worksheet.write(row, 0, uid)
                        worksheet.write(row, 1, "level 2 384 source plate (DNA components)")
                        worksheet.write(row, 2, "384LDV_AQ_B")
                        worksheet.write(row, 3, source_well)
                        worksheet.write(row, 4, "384-Well Level 2 MoClo output plate")
                        worksheet.write(row, 5, "Echo® Qualified 384-Well Polypropylene Source Microplate ("
                                                "384PP)")
                        worksheet.write(row, 6, destination_well)
                        worksheet.write(row, 7, transfer_volume)
                        worksheet.write(row, 8, "pTU2-b-RFP")
                        break

        elif int(GUI.transcription_unit_quantity_combo.get()) > 3:
            for source_well in level_2_384PP.keys():
                if level_2_384PP[source_well][0] == "pTU2-A-RFP":
                    if level_2_output[destination_well][0].find("reaction 1:1") >= 0:
                        transfer_volume = EcoFlex_protocol.transfer_volume("level_2_backbone_1_1")
                    elif level_2_output[destination_well][0].find("reaction 1:2") >= 0:
                        transfer_volume = EcoFlex_protocol.transfer_volume("level_2_backbone_1_2")
                    elif level_2_output[destination_well][0].find("reaction 2:1") >= 0:
                        transfer_volume = EcoFlex_protocol.transfer_volume("level_2_backbone_2_1")
                    if level_2_384PP[source_well][1] >= dead_volume_dna + transfer_volume:
                        level_2_384PP[source_well][1] -= transfer_volume
                        row += 1
                        uid += 1
                        worksheet.write(row, 0, uid)
                        worksheet.write(row, 1, "level 2 384 source plate (DNA components)")
                        worksheet.write(row, 2, "384LDV_AQ_B")
                        worksheet.write(row, 3, source_well)
                        worksheet.write(row, 4, "384-Well Level 2 MoClo output plate")
                        worksheet.write(row, 5, "Echo® Qualified 384-Well Polypropylene Source Microplate ("
                                                "384PP)")
                        worksheet.write(row, 6, destination_well)
                        worksheet.write(row, 7, transfer_volume)
                        worksheet.write(row, 8, "pTU2-A-RFP")
                        break

    workbook.close()

