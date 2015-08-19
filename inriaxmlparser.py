#!usr/bin/python
# -*- coding: UTF-8 -*-
from lxml import etree
from io import StringIO, BytesIO
import re
import transcoder
import codecs

	
def findwordform(inputform, datafile):	
	tree = etree.parse(datafile)
	xpathname = '/forms/f[@form="' + inputform + '"]'
	r = tree.xpath(xpathname)
	for member in r:
		return etree.tostring(member).strip() # This works for output of the chunk of xml

def converttodevanagari(attributeslist):
	gerardwords = ['nom', 'acc', 'ins', 'dat', 'abl', 'gen', 'loc', 'voc', 'mas', 'fem', 'neu', 'dei', 'sg', 'du', 'pl', 'fst', 'snd', 'trd', 'iic', 'iiv', 'iip', 'avyaya',]
	devawords =   [u'प्रथमा', u'द्वितीया', u'तृतीया', u'चतुर्थी', u'पञ्चमी', u'षष्ठी', u'सप्तमी', u'संबोधन', u'पुंल्लिङ्ग', u'स्त्रीलिङ्ग', u'नपुंसकलिङ्ग', u'सङ्ख्या', u'एकवचन', u'द्विवचन', u'बहुवचन', u'प्रथमपुरुष', u'मध्यमपुरुष', u'उत्तमपुरुष', u'समासपूर्वपद', u'सहायकधातुपूर्व', u'कृदन्तपूर्वपद', u'अव्यय']
	outputlist = []
	for member in attributeslist:
		alist = []
		for mem1 in member:
			alist.append(devawords[gerardwords.index(mem1)])
		outputlist.append(alist)
	return outputlist

def iter(wordxml):
	wordxml = unicode(wordxml)
	tree = StringIO(wordxml)
	context = etree.parse(tree)
	root = context.getroot()
	children = root.getchildren()[:-1] # attributes
	basedata = root.getchildren()[-1] # s stem
	basewordslp = basedata.get('stem').strip()
	#baseword = transcoder.transcoder_processString(basewordslp,'slp1','deva')
	baseword = basewordslp
	attributes = []
	for child in children:
		taglist = child.xpath('.//*')
		output = [child.tag]
		output = output + [ tagitem.tag for tagitem in taglist]
		if len(child.xpath('.//prs[@gn]')) > 0:
			prsgana = child.xpath('.//prs')[0].get('gn')
			output.append('verbgana')
			output.append(prsgana)
		elif len(child.xpath('.//aor[@gn]')) > 0:
			aorgana = child.xpath('.//aor')[0].get('gn')
			output.append('aoristgana')
			output.append(aorgana)
		elif len(child.xpath('.//inj[@gn]')) > 0:
			injgana = child.xpath('.//inj')[0].get('gn')
			output.append('injunctivegana')
			output.append(injgana)
		attributes.append(output)
	#outputlist = converttodevanagari(attributes)
	outputlist = attributes # testing for verbs.
	wordwithtags = []
	for member in outputlist:
		wordwithtags.append(baseword + "-" + "-".join(member) )
	return "|".join(wordwithtags)
			
def iteroverfiles(word):
	filelist = ['SL_nouns.xml', 'SL_roots.xml','SL_adverbs.xml', 'SL_final.xml', 'SL_parts.xml', 'SL_pronouns.xml', ]
	outputlist = []
	for file in filelist:
		if findwordform(word, file) is not None:
			outputlist.append(iter(findwordform(word, file)))
	return "|".join(outputlist)

#print iteroverfiles("ajIgamat")
def findrootword(checkedrootword):
	listing = []
	filelist = ['SL_nouns.xml', 'SL_roots.xml','SL_adverbs.xml', 'SL_final.xml', 'SL_parts.xml', 'SL_pronouns.xml', ]
	for datafile in filelist:
		tree = etree.parse(datafile)
		entries = tree.xpath('.//f')
		for entry in entries:
			parts = entry.getchildren()
			s = parts[-1]
			if s.get('stem') == checkedrootword:
				children = parts[:-1]
				for child in children:
					taglist = child.xpath('.//*')
					output = [ child.tag ] + [ tagitem.tag for tagitem in taglist]
					if output[-1] in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'] and output[-2] in ['verbgana', 'aoristgana', 'injunctivegana']:
						output = output[:-2]
					output += [ entry.get('form') ]
					listing.append(output)
	return listing

def constructor(analysedword):
	data = re.split('|',analysedword)
	for datum in data:
		separate = re.split('-', datum)
		rootword = separate[0]
		taglist = separate[1:]
		if taglist[-1] in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'] and taglist[-2] in ['verbgana', 'aoristgana', 'injunctivegana']:
			taglist = taglist[:-2]
		#print rootword
		#print taglist
		datahavingroot = findrootword(rootword)
		outlist = []
		for rootdatum in datahavingroot:
			if set(taglist) < set(rootdatum):
				outlist.append(rootdatum[-1])
		return "|".join(outlist)

print constructor(u'gam-v-cj-prim-sys-tp-aor-para-np-sg-trd-aoristgana-3')

def connripa():
	f = open("nripadata1.csv", "r")
	data = f.read()
	f.close()
	g = codecs.open("nripadeva.csv", 'w', 'utf-8')
	data = transcoder.transcoder_processString(data, "slp1", "deva")
	g.write(data)
	g.close()
