README for SynBioMate v0.1
Software GitHub repository: https://github.com/phoenixgater/SynBioMate

######## Installing and running this software #############
The entirety of this software can be downloaded from the github repository: https://github.com/phoenixgater/SynBioMate
This software is known to be compatible with Python version 3.6.0 windows 64 bit

This software is dependent on the following third-party libraries, all of which are contained within the softwares local "venv" folder:
-PySBOL version 2.3.2 for windows 64 bit python version 3.6.0 
-requests library v.2.3.20 
-python-docx v.0.8.10 
-openpyxl v.3.0.4
-xlsxwriter v.1.2.9

To run this software, run the file "Main.py" in your chosen IDE (Please ensure your interpreter is set to python v.3.6.0)

######## Notes on this software ############
SynBioMate is a protocol generation software for MoClo assembly that uses SBOL-encoded parts and designs.
This software is currently compatible with the EcoFlex MoClo toolkit, and can produce automated assembly scripts for an Echo 525 acoustic liquid handler.
More details on the EcoFlex MoClo toolkit can be found here: http://www.addgene.org/kits/freemont-ecoflex-moclo/


######## Basic guide to software functionality #######################
This software has 3 basic functionalities:
-Creating SBOL parts
-Creating SBOL designs
-MoClo protocol generation with liquid handling scripts for automated assembly

######## Part creation #############
Part creation is accessed via the "Create part" tab.
-For part creation, enter your chosen values, and press the "create part" button
-You can convert a genbank file into the SBOL format using the "Create from genbank file" button. The converted file will be in the same directory as
the genbank file that was selected (Please note that the other input on the create part tab will not affect the SBOL file produced)

######## Genetic Design Creation #############
Genetic design creation can be accessed via the "Create design" tab.
-This software does not currently support the incorporation of existing designs that have primary structures, and on attempt will show an error message
-This software does, however, support parts with sub-components
-Parts can be imported via the "Import SBOL file" button
-Parts can be queried via the "import from synbiohub" interface. Enter the search term, and click the "Submit" button (this may take
some time to load, and the software may appear to crash during this query) Queried parts will be displayed, and you can click these parts to add them to the design.
-Once all parts have been imported, enter a name into the lower text entry box, and click "Assemble Design"

######## MoClo protocol generation with liquid handling scripts for automated assembly ############
MoClo protocol generation can be accessed via the "MoClo assembly" tab

Creating a level 0 library:
-Designs or individual parts can be imported using the "Import SBOL file" button.
-Individual parts will be added directly to the level 0 library
-Designs will be displayed, and the part descriptions and restriction sites can be seen by clicking the "Show part descriptions" and "Show design analysis" buttons,
respectively. Designs can then be imported into the level 0 library by clicking the "Import design parts to level 0 library" button.
-Parts are allocated keys, based on their detected role, these are; promoters (p), ribosome binding sites (r), signal peptides (s), coding regions (c),
terminators (t), and other (o). Parts can be moved to a different group through the interface by specifying the key (e.g p1) and their desired destination group.
********* The group that parts belong to will affect how they are designed to be compatible with the MoClo protocol ***********

Selecting protocol paramaters:
Specifications for the generated protocol can be set via the options under the "Protocol design" sub-title.
-Include signal peptide? - allows you to select whether you desire a signal peptide part between rbs and coding region parts. **Currently, if one transcription unit
has a signal peptide, all transcription units must have a signal peptide ******
- Toolkit - Allows selection of the MoClo toolkit to be used, and will affect the plasmid backbones, fusion sites, and restriction sites that are used
- Transcription unit quantity - Specifies the amount of level 1 transcription units that will be present in level 2 constructs ***If "1" is selected, the protocol and scripts
for level 2 assembly will not be produced ***
- Assembly method - Manual will produce the designs for the parts and assembled constructs, and include a standard EcoFlex protocol. Automatic will produce a protocol
 and scripts for automated assembly
- Substitute CDS restriction sites? - Selecting "Yes" will remove forbidden EcoFlex restriction sites from CDS parts ***Do not select this if using an EcoFlex ready part***
- Add fusion sites to parts? - Selecting "Yes" will add appropriate flanking restriction sites, fusion sites, and overhangs to parts.
- Reaction ratio selection - This will specify the volumetric ratio of backbones to parts for the reaction mixtures, multiple selection is allowed
- Once all parameters have been fulfilled, click the "Create" button

Selecting parts in transcription units:
Once protocol parameters have been selected and the "create" button has been pressed, you will be prompted to enter the parts included in each transcription unit variant
- To specify the part variations that will occur in each transcription unit, enter the parts key in the level 0 library (e.g p1). To specify further variations
seperate entries by a comma, e.g for three promoter variations in one transcription unit, you may enter "p1, p2, p3"
- Any parts in the level 0 library that are not included in any transcription unit variation will be discarded

Final entry:
- Once parts have been specified, if "automated" assembly was selected, you will be asked to select a liquid handler
- The protocol name is entered in the lower text entry box
- Once all transcription units have been specified, a liquid handler has been selected, and a protocol name entered, press "Create protocol"
- A final prompt will appear, noting the amount of variants produced, and any detected restriction sites. ***If more than 384 level 1 transcription unit variants,
or more than 384 level 2 transcription unit variants are produced, then liquid handling scripts will be invalid******
-The protocol and scripts will be saved to the "protocols_and_scripts" folder in the SynBioMate software directory












