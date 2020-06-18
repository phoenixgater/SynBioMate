from sbol import*
doc = Document()

doc.read("test_design.xml")

primarystructure_cd = doc.getComponentDefinition("https://synbiohub.org/public/igem//ComponentDefinition/test_design/1")
primary_structure = primarystructure_cd.getPrimaryStructure()

for obj in primary_structure:
    print(obj)

print(primarystructure_cd.sequence.elements)







