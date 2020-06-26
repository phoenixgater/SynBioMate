from sbol import*

doc = Document()

doc.read("BBa_K208005.xml")
for obj in doc.componentDefinitions:
    print(obj.type)
