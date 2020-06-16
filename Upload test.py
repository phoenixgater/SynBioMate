from sbol import*

doc = Document()
setHomespace('https://synbiohub.org/public/igem/')
igem = PartShop('https://synbiohub.org/public/igem')

r0010 = ComponentDefinition('r0010')
r0010.roles = SO_PROMOTER
doc.addComponentDefinition(r0010)


igem.login("phoenixgater@hotmail.com", "password")
doc.displayId = 'my_collection'
doc.name = 'my collection'
doc.description = 'a description of your collection'
igem.submit(doc)
