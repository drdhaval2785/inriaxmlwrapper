#!/usr/bin/env python
''' Convert SL_preverbs.txt to SL_upasargas.xml

    SL_preverbs.txt is searched for simple preverbs
    XML structure is created and output to SL_upasargas.xml
    Author: Karthik Madathil <kmadathil@gmail.com>
'''



import re
import lxml.etree as ET

# Regexp to match simple upasargas
lre=re.compile(r"^\s*(\w+)\s*=\s*\1\s*$")

with open("SL_preverbs.txt") as pf:
    # Root element <forms>
    fe=ET.Element("forms")
    for pfl in pf:
        m=lre.match(pfl)
        if m:
            up = m.group(1)
            # Create XML Elements
            # <f form=upasarga_name><upsrg /><stem=upasarga_name/></f>
            f=ET.SubElement(fe,"f",form=up)
            t=ET.SubElement(f,"upsrg")
            s=ET.SubElement(f,"s",stem=up)

# Write out
with open("SL_upasargas.xml","w") as xo:
   tree=ET.ElementTree(fe)
   tree.write(xo,pretty_print=True)
    
