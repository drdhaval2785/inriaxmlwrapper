# This Python file uses the following encoding: utf-8
# Author - Dr. Dhaval patel - drdhaval2785@gmail.com - www.sanskritworld.in
# Written for Sanskrit Hindi translation tool for Nripendra Pathak's Ph.D.
# XML database of verbs taken from sanskrit.inria.fr site of Gerard Huet. For sample, please see SL_roots.xml
# Date - 21 August 2015
# Version - 1.0.0
from lxml import etree
from io import StringIO, BytesIO
import re
import transcoder
import codecs

def formscraper(datafile,outputfile):	
	tree = etree.parse(datafile) # Prepared an element tree in lxml
	xpathname = '/forms/f' # Defined the xpath to search
	r = tree.xpath(xpathname) # Created a list 'r' whose members are lines of XML file which correspond to the word form 'inputform'
	f = open(outputfile,'w')
	for member in r:
		f.write(member.get('form')+"\n")
	f.close()
formscraper('SL_nouns.xml','sanskritinput.txt')
