sequence = "atttgcaaagtaaaaaaggeagaaaagaaacttttcactggagagcatgcgggagggggcaattcttgttgaattaaaagatggtgatgttaatgggcacaaattttgcatgcctgtcagtggagagggtgaaggtgatgcaacatacggaaaacttacccttaaatttatttgcactactggaaaactacctgttccatggccaacacttgtcactactttcggttatggtgttcaatgctttgcgagatacccagatcatatgaaacagcatgactttttcaagagtgccatgcccgaaggttatgtacaggaaagaactatatttttcaaagatgacgggaactacaagacacgtgctgaagtcaagtttgaaggtgatacccttgttaatagaatcgagttaaaaggtattgattttaaagaagatggaaacattcttggacacaaattggaatacaactataactcacacaatgtatacatcatggcagacaaacaaaagaatggaatcaaagttaacttcaaaattagacacaacattgaagatggaagcgttcaactagcagaccattatcaacaaaatactccaattggcgatggccctgtccttttaccagacaaccattacctgtccacacaatctgccctttcgaaagatcccaacgaaaagagagaccacatggtccttcttgagtttgtaacagctgctgggattacacatggcatggatgaactatacaaataataa"

'''sequence_list= []
for base in sequence:
    sequence_list.append(base)'''

location = (sequence.find("gcatgc"))
codon_list = ([sequence[i:i + 3] for i in range(0, len(sequence), 3)])
codon_list[int((location / 3) + 1)] = "ggg"
codon_string = (", ".join(codon_list))
modified_sequence = codon_string.replace(", ", "")
print(sequence)

dictionary_test = {}

dictionary_test["test"] = 1

print(sequence.count("poo"))

