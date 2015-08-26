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
	gerardwords = ['nom', 'acc', 'ins', 'dat', 'abl', 'gen', 'loc', 'voc', 'mas', 'fem', 'neu', 'dei', 'sg', 'du', 'pl', 'fst', 'snd', 'trd', 'iic', 'iiv', 'iip', 'avyaya', 'na', 'uf', 'conj']
	devawords =   [u'प्रथमा', u'द्वितीया', u'तृतीया', u'चतुर्थी', u'पञ्चमी', u'षष्ठी', u'सप्तमी', u'संबोधन', u'पुंल्लिङ्ग', u'स्त्रीलिङ्ग', u'नपुंसकलिङ्ग', u'सङ्ख्या', u'एकवचन', u'द्विवचन', u'बहुवचन', u'प्रथमपुरुष', u'मध्यमपुरुष', u'उत्तमपुरुष', u'समासपूर्वपद', u'सहायकधातुपूर्व', u'कृदन्तपूर्वपद', u'अव्यय', u'', u'अव्यय', u'']
	outputlist = []
	for member in attributeslist:
		alist = []
		for mem1 in member:
			alist.append(devawords[gerardwords.index(mem1)])
		outputlist.append(alist)
	return outputlist

def iter(wordxml, strength="Full"):
	wordxml = unicode(wordxml)
	tree = StringIO(wordxml)
	context = etree.parse(tree)
	root = context.getroot()
	children = root.getchildren()[:-1] # attributes
	basedata = root.getchildren()[-1] # s stem
	basewordslp = basedata.get('stem').strip()
	if strength == "deva":
		baseword = transcoder.transcoder_processString(basewordslp,'slp1','deva')
	else:
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
	if (strength == "deva"):
		outputlist = converttodevanagari(attributes)
	else:
		outputlist = attributes
	wordwithtags = []
	for member in outputlist:
		wordwithtags.append(baseword + "-" + "-".join(member) )
	return "|".join(wordwithtags)
			
def analyser(word, strength="Full"):
	filelist = ['SL_roots.xml','SL_nouns.xml','SL_adverbs.xml','SL_parts.xml','SL_pronouns.xml']
	outputlist = []
	for file in filelist:
		if findwordform(word, file) is not None:
			outputlist.append(iter(findwordform(word, file), strength))
	return "|".join(outputlist)

#print analyser("gamyate")

def findrootword(checkedrootword):
	listing = []
	filelist = ['SL_roots.xml','SL_nouns.xml','SL_adverbs.xml','SL_parts.xml','SL_pronouns.xml']
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

def generator(analysedword, translit="slp1"):
	analysedword = unicode(analysedword)
	data = re.split('|',analysedword)
	for datum in data:
		separate = re.split('-', datum)
		rootword = separate[0]
		taglist = separate[1:]
		if taglist[-1] in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'] and taglist[-2] in ['verbgana', 'aoristgana', 'injunctivegana']:
			taglist = taglist[:-2]
		datahavingroot = findrootword(rootword)
		outlist = []
		for rootdatum in datahavingroot:
			if set(taglist) < set(rootdatum):
				outlist.append(rootdatum[-1])
		if translit == "deva":
			return transcoder.transcoder_processString("|".join(outlist),'slp1','deva')
		else:
			return "|".join(outlist)
#print generator('Davala-sg-mas-abl', 'deva')

sanskritverb = ['BU', 'gam']
hindiverb = ['हो', 'जा']
def devanagaridisplay(word):
	if word[-1] == 'H':
		word = word[:-1]+"s"
	datafetched = analyser(word)
	database = [(u'v-cj-prim', u'प्राथमिक'),
				(u'v-cj-ca', u'प्रेरक'),
				(u'v-cj-int', u'intensive'),
				(u'v-cj-des', u'desiderative'),
				(u'sys-prs-md-pr', u'लट्'),
				(u'sys-prs-md-ip', u'लोट्'),
				(u'sys-prs-md-op', u'विधिलिङ्'),
				(u'sys-prs-md-im', u'लङ्'),
				(u'sys-pas-md', u'कर्मणि'),
				(u'sys-tp-fut', u'लृट्'),
				(u'sys-tp-prf', u'लिट्'),
				(u'sys-tp-aor', u'लुङ्'),
				(u'sys-tp-inj', u'आगमाभावयुक्तलुङ्'),
				(u'sys-tp-cnd', u'लृङ्'),
				(u'sys-tp-ben', u'आशीर्लिङ्'),
				(u'sys-pef', u'लुट्'),
				(u'para', u'परस्मैपद'),
				(u'atma', u'आत्मनेपद'),
				(u'pass', u'कर्मणि'),
				(u'np-sg', u'एकवचन'),
				(u'np-du', u'द्विवचन'),
				(u'np-pl', u'बहुवचन'),
				(u'fst', u'उत्तमपुरुष'),
				(u'snd', u'मध्यमपुरुष'),
				(u'trd', u'प्रथमपुरुष'),
				(u'-verbgana', u''),
				(u'-aoristgana', u''),
				(u'-injunctivegana', u''),
				(u'-1', u''),
				(u'-2', u''),
				(u'-3', u''),
				(u'-4', u''),
				(u'-5', u''),
				(u'-6', u''),
				(u'-7', u''),
				(u'-8', u''),
				(u'-9', u''),
				(u'-10', u''),
				]
	output = datafetched
	for member in database:
		output = re.sub(member[0], member[1], output)
	root1 = output.split("-")[0]
	root2 = root1.split("#")[0]
	output = re.sub(root1, root2, output)
	output = transcoder.transcoder_processString(output, "slp1", "deva")
	return output

print analyser("Bavati")