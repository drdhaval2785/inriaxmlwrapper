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

# function findwordform searches in the XML file for line which matches the wordform we are interested in. e.g. findwordform("BavAmi","SL_roots.xml") would find all lines of XML file which have word form "Bavati".
def findwordform(inputform, datafile):	
	tree = etree.parse(datafile) # Prepared an element tree in lxml
	xpathname = '/forms/f[@form="' + inputform + '"]' # Defined the xpath to search
	r = tree.xpath(xpathname) # Created a list 'r' whose members are lines of XML file which correspond to the word form 'inputform'
	for member in r:
		return etree.tostring(member).strip() # Created a string out of element tree. strip() removes unnecessary white spaces around the string.

# function converttodevanagari is used to translate the short forms used by Gerard Huet to their Sanskrit Devanagari counterpart.
def converttodevanagari(attributeslist):
	# Abbreviations used by Gerard.
	gerardwords = ['nom', 'acc', 'ins', 'dat', 'abl', 'gen', 'loc', 'voc', 'mas', 'fem', 'neu', 'dei', 'sg', 'du', 'pl', 'fst', 'snd', 'trd', 'iic', 'iiv', 'iip', 'avyaya', 'na', 'uf', 'conj']
	# Their counterparts in Sanskrit
	devawords =   ['प्रथमा', 'द्वितीया', 'तृतीया', 'चतुर्थी', 'पञ्चमी', 'षष्ठी', 'सप्तमी', 'संबोधन', 'पुंल्लिङ्ग', 'स्त्रीलिङ्ग', 'नपुंसकलिङ्ग', 'सङ्ख्या', 'एकवचन', 'द्विवचन', 'बहुवचन', 'प्रथमपुरुष', 'मध्यमपुरुष', 'उत्तमपुरुष', 'समासपूर्वपद', 'सहायकधातुपूर्व', 'कृदन्तपूर्वपद', 'अव्यय', '', 'अव्यय', '']
	outputlist = [] # initiated a blank list.
	for member in attributeslist:
		alist = [] # initiated a blank list.
		for mem1 in member:
			alist.append(devawords[gerardwords.index(mem1)]) # appended the Devanagari words for Gerard's abbreviations.
		outputlist.append(alist) # appended alist to outputlist
	return outputlist # returned outputlist which has everything converted to Sanskrit in Devanagari.

# function iter is to iterate over the XML file and get following from a given word form - Base root and attributes
# Default strength is "Full". "deva" converts the output to Devanagari, which is not advisable to use for any other use than testing. 
def iter(wordxml, strength="Full"):
	wordxml = unicode(wordxml) # Converted the word to unicode
	tree = StringIO(wordxml) # Created XML from the worddata
	context = etree.parse(tree) # Parsed the element tree.
	root = context.getroot() # got the root of element tree e.g. 'f'
	# The next two steps require explanation. In Gerard's XML files, All possible attributes are given as children of 'f'. The last child is always 's' which stores the stem. All other children are the various possible word attributes. Given as 'na' or 'v' etc. Gio
	children = root.getchildren()[:-1] # attributes
	basedata = root.getchildren()[-1] # 's' stem
	basewordslp = basedata.get('stem').strip() # Base word in SLP1 encoding.
	if strength == "deva":
		baseword = transcoder.transcoder_processString(basewordslp,'slp1','deva') # If the user wants output in Devanagari rather than SLP1, this code converts it to Devanagari.
	else:
		baseword = basewordslp # Otherwise in SLP1.
	attributes = [] # An empty list to store attributes.
	for child in children:
		taglist = child.xpath('.//*') # Fetches all elements (abbreviations) of a particular verb / word characteristics.
		output = [child.tag] # The first member of output list is the tag of element 'v', 'na' etc.
		output = output + [ tagitem.tag for tagitem in taglist] # Other tags (abbreviations) and add it to output list.
		# The following section is commented out right now. But it would be needed for situation where we need to konw the gaNa of a verb or 7 kinds of aorist derivation.
		"""if len(child.xpath('.//prs[@gn]')) > 0:
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
			output.append(injgana)"""
		attributes.append(output) # output list is appended to attributes list.
	if (strength == "deva"):
		outputlist = converttodevanagari(attributes) # Devanagari
	else:
		outputlist = attributes # SLP1
	wordwithtags = [] # Empty list
	for member in outputlist:
		wordwithtags.append(baseword + "-" + "-".join(member) ) # Created a list wordwithtags where the first member is baseword and the rest of the members are attributes separated by '-'
	return "|".join(wordwithtags) # If there are more than one possible verb characteristics for a given form, they are shown separated by a '|'

# function analyser analyses all the XML files and gets matching details from all XMLs e.g. 'Bavati' may be a verb form, but it can also be a noun form of 'Bavat' locative singular. Therefore it is needed to traverse all XML files.
def analyser(word, strength="Full"):
	filelist = ['SL_roots.xml', 'SL_nouns.xml', 'SL_adverbs.xml', 'SL_final.xml', 'SL_parts.xml', 'SL_pronouns.xml']
	outputlist = []
	for file in filelist:
		if findwordform(word, file) is not None: # If there is a line in XML matching the searched word
			outputlist.append(iter(findwordform(word, file), strength)) # Append the base word with its attributes to outputlist
	return "|".join(outputlist) # Show the data separated by '|' in case there are more than one datum.

#print analyser("gamyate")

# Functions findrootword and generator are for generating the word form from given attributes and root.
# The approach 
def findrootword(checkedrootword):
	listing = []
	filelist = ['SL_roots.xml', 'SL_nouns.xml', 'SL_adverbs.xml', 'SL_final.xml', 'SL_parts.xml', 'SL_pronouns.xml']
	for datafile in filelist:
		tree = etree.parse(datafile)
		entries = tree.xpath('.//f')
		for entry in entries:
			parts = entry.getchildren()
			s = parts[-1] # Fetched tag 's' till this section.
			if s.get('stem') == checkedrootword: # If the stem is the same as checkedrootword
				children = parts[:-1] # Removed the last because it has only stem data.
				for child in children:
					taglist = child.xpath('.//*')
					output = [ child.tag ] + [ tagitem.tag for tagitem in taglist]
					if output[-1] in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'] and output[-2] in ['verbgana', 'aoristgana', 'injunctivegana']: # Remove the last two data, because they are not part of Gerard's scheme.
						output = output[:-2] 
					output += [ entry.get('form') ] # Added the entered word form at the last.
					listing.append(output) # Added output to listing list
	return listing # Return listing list.

def generator(analysedword, translit="slp1"):
	analysedword = unicode(analysedword) # unicode
	data = re.split('|',analysedword) # There may be cases where the data may have been analysed by our analyser. They would be separated by '|'.
	for datum in data:
		separate = re.split('-', datum) # split the whole string by '-'
		rootword = separate[0] # Base word
		taglist = separate[1:] # attributes
		if taglist[-1] in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'] and taglist[-2] in ['verbgana', 'aoristgana', 'injunctivegana']:
			taglist = taglist[:-2] # Removed artificially added attributes
		datahavingroot = findrootword(rootword) # Created a list of possible items
		outlist = []
		for rootdatum in datahavingroot:
			if set(taglist) < set(rootdatum): # If the tags supplied are a subset of the data from XML file,
				outlist.append(rootdatum[-1]) # Add the word form to outlist
		if translit == "deva":
			return transcoder.transcoder_processString("|".join(outlist),'slp1','deva') # Devanagari
		else:
			return "|".join(outlist) # SLP1

#print generator('Davala-sg-mas-abl', 'deva')

# devangaridisplay and translator functions are created for Nripendra Pathak, so that he may provide necessary data for extending the code.
# function devanagaridisplay will show the attribute list from XML files in a format which a traditional Sanskrit scholar may understand easily.
def devanagaridisplay(word):
	if word[-1] == 'H':
		word = word[:-1]+"s" # A word ending with a visarga are converted to sakArAnta, because this is how Gerard has stored his data.
	datafetched = analyser(word)
	# If there are tags which are not enumerated here, they can be added as and when there is a need.
	database = [('v-cj-prim', 'प्राथमिक'),
				('v-cj-ca', 'णिजन्त'),
				('v-cj-int', 'यङन्त'),
				('v-cj-des', 'सन्नन्त'),
				('sys-prs-md-pr', 'लट्'),
				('sys-prs-md-ip', 'लोट्'),
				('sys-prs-md-op', 'विधिलिङ्'),
				('sys-prs-md-im', 'लङ्'),
				('sys-pas-md-pr', 'लट्-कर्मणि'),
				('sys-pas-md-ip', 'लोट्-कर्मणि'),
				('sys-pas-md-op', 'विधिलिङ्-कर्मणि'),
				('sys-pas-md-im', 'लङ्-कर्मणि'),
				('sys-tp-fut', 'लृट्'),
				('sys-tp-prf', 'लिट्'),
				('sys-tp-aor', 'लुङ्'),
				('sys-tp-inj', 'आगमाभावयुक्तलुङ्'),
				('sys-tp-cnd', 'लृङ्'),
				('sys-tp-ben', 'आशीर्लिङ्'),
				('sys-pef', 'लुट्'),
				('para', 'कर्तरि'),
				('atma', 'कर्तरि'),
				('pass', 'कर्मणि'),
				('np-sg', 'एकवचन'),
				('np-du', 'द्विवचन'),
				('np-pl', 'बहुवचन'),
				('fst', 'उत्तमपुरुष'),
				('snd', 'मध्यमपुरुष'),
				('trd', 'प्रथमपुरुष'),
				('na-nom', 'प्रथमा'),
				('na-voc', 'संबोधन'),
				('na-acc', 'द्वितीया'),
				('na-ins', 'तृतीया'),
				('na-dat', 'चतुर्थी'),
				('na-abl', 'पञ्चमी'),
				('na-gen', 'षष्ठी'),
				('na-loc', 'सप्तमी'),
				('sg', 'एकवचन'),
				('du', 'द्विवचन'),
				('pl', 'बहुवचन'),
				('mas', 'पुंल्लिङ्ग'),
				('fem', 'स्त्रीलिङ्ग'),
				('neu', 'नपुंसकलिङ्ग'),
				('dei', 'सङ्ख्या'),
				]
	output = datafetched
	for member in database:
		output = re.sub(member[0], member[1], output) # Changed attributes strings with their Sanskrit Devanagari counterparts.
	root1 = output.split("-")[0]
	root2 = root1.split("#")[0] # Gerard sometimes adds # to denote number of verb in his dictionary. Removed the number for our usage.
	output = re.sub(root1, root2, output)
	#output = transcoder.transcoder_processString(output, "slp1", "deva") # This code creates some issue in windows setting. Therefore not converting to Devanagari right now. Will do that later.
	return output

