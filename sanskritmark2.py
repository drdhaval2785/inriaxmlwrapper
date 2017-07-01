# This Python file uses the following encoding: utf-8
# Author - Dr. Dhaval patel - drdhaval2785@gmail.com - www.sanskritworld.in
# XML database of verbs taken from sanskrit.inria.fr site of Gerard Huet. For sample, please see SL_roots.xml
# Date - 23 October 2015
# Version - 1.0.1
from lxml import etree
from io import StringIO, BytesIO
import re
import transcoder
import codecs
import datetime

# Function to return timestamp
def timestamp():
	return datetime.datetime.now()

# Parsing the XMLs. We will use them as globals when need be.
print "Parsing of XMLs started at", timestamp()
roots = etree.parse('SL_roots.xml') # parses the XML file.
nouns = etree.parse('SL_nouns.xml')
adverbs = etree.parse('SL_adverbs.xml')
final = etree.parse('SL_final.xml')
parts = etree.parse('SL_parts.xml')
pronouns = etree.parse('SL_pronouns.xml')
#upasargas = etree.parse('SL_upasargas.xml')
# This filelist can include all or some files. By default it takes into account all XMLs of Gerard.
# If you need some specific database like roots, nouns etc you can keep them and remove the rest. It would speed up the process.
#filelist = [roots, nouns, adverbs, final, parts, pronouns, upasargas]
filelist = [roots, nouns, adverbs, final, parts, pronouns]
#filelist = [parts]
print "Parsing of XMLs completed at", timestamp()
#print "Will notify after every 100 words analysed."

# Returns first members of a compound. Gerard stores them as iic, iip and iiv tags, in final.xml file.
def firstmemberlist():
	global final # Calling global variable final
	# defining xpaths
	iic = final.xpath('/forms/f/iic')
	iip = final.xpath('/forms/f/iip')
	iiv = final.xpath('/forms/f/iiv')
	# fetched and added data
	firstmemberlist = [member.getparent().get('form') for member in iic]
	firstmemberlist += [member.getparent().get('form') for member in iip]
	firstmemberlist += [member.getparent().get('form') for member in iiv]
	return firstmemberlist
# Storing firstmembers for future use as global variable.
firstmembers = firstmemberlist()

# Secondmember of a compound. Gerard has stored them in noun and participles files.
def secondmemberlist():
	# Calling global variables nouns and parts
	global nouns, parts
	n = nouns.xpath('/forms/f')
	p = parts.xpath('/forms/f')
	# Storing data
	secondmemberlist = [member.get('form') for member in n]
	secondmemberlist += [member.get('form') for member in p]
	return secondmemberlist
# Storing secondmembers for future use as global variable.
secondmembers = secondmemberlist()

# Returns all the forms for XML files listed in variable 'filelist'.
def allmemberlist():
	global filelist # If you need to increase or decrease the database, change the filelist variable in the starting of the code.
	allmemberlist = [] # Initialising a list to store data.
	for file in filelist:
		allwords = file.xpath('/forms/f')
		allmemberlist += [member.get('form') for member in allwords] # Created an array of all forms in filelist.
	return allmemberlist # Returns the list.
# Storing allmembers for future use as global variable.
allmembers = set(allmemberlist())

# function findwordform searches in the XML file for line which matches the wordform we are interested in. e.g. findwordform("Bavati","SL_roots.xml") would find all lines of XML file which have word form "Bavati".
def findwordform(inputform):
	#print "importing filelist for findwordform started at", timestamp()
	global filelist, allmembers # Fetched global variable filelist.
	#print "importing filelist for findwordform ended at", timestamp()
	outputlist = [] # A list to store output.
	if inputform in allmembers:
		for file in filelist:
			tree = file # The etree to manipulate.
			xpathname = '/forms/f[@form="' + inputform + '"]' # Defined the xpath to search
			#print "xpath parsing for findwordform started at", timestamp() # After speed analysis, this function is the most time expensive. It takes around 0.10 sec per word form.
			r = tree.xpath(xpathname) # Created a list 'r' whose members are lines of XML file which correspond to the word form 'inputform'
			#print "xpath parsing for findwordform ended at", timestamp()
			for member in r:
				outputlist.append(etree.tostring(member).strip()) # Created a string out of element tree. strip() removes unnecessary white spaces around the string.
	#print "findwordform completed at", timestamp()
	if len(outputlist) == 0:
		return '????' # Error message.
	else:
		return "|".join(outputlist) # Else, return the list separated by '|'.

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
	if wordxml == "????":
		return "????" # Error message
	else:
		wordxml = unicode(wordxml) # Converted the word to unicode
		wordwithtags = [] # Empty list
		individualentries = wordxml.split('|')
		for individualentry in individualentries:
			tree = StringIO(individualentry) # Created XML from the worddata
			#print "parsing of iter started at", timestamp()
			context = etree.parse(tree) # Parsed the element tree.
			#print "parsing of iter ended at", timestamp()
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
			for member in outputlist:
				wordwithtags.append(baseword + "-" + "-".join(member) ) # Created a list wordwithtags where the first member is baseword and the rest of the members are attributes separated by '-'
		#print "postprocessing of iter ended at", timestamp()
		return "|".join(wordwithtags) # If there are more than one possible verb characteristics for a given form, they are shown separated by a '|'

def mapiter(input):
	return iter(findwordform(input))

# function analyser analyses all the XML files and gets matching details from all XMLs e.g. 'Bavati' may be a verb form, but it can also be a noun form of 'Bavat' locative singular. Therefore it is needed to traverse all XML files.
def analyser(word, strength="Full"):
	global secondmembers
	foundform = findwordform(word)
	if not foundform == '????': # If the output is not an error
		return iter(foundform, strength) # Return the output
	elif not strength == "low":
		samasa = sss(word) # Try to split the word for samAsa / sandhi.
		output = []
		if samasa is not 'error': # If the word can be split as a samAsa / sandhi,
			indsamasa = samasa.split('|') # Separate all possible splits.
			for indsam in indsamasa:
				indsamcomponents = indsam.split('+') # Separate members of the compound / sandhi
				analy = map(mapiter, indsamcomponents) # Apply mapiter function to all components of indsamcomponents.
				prefix = indsamcomponents[:-1]
				lastword = indsamcomponents[-1]
				lastwordanalysed = iter(findwordform(lastword), strength)
				for lastwordan in lastwordanalysed.split('|'):
					output.append('+'.join(prefix) + '+' + lastwordan)
				output.append('$'.join(analy)) # Appended the solution to output list.
			return '%'.join(output) # Return the output joined by '%'.
		else:
			return '????' # Return error.
	else:
		return word
# Don't know ther reason, but findrootword and generator are taking too long. They used to work well earlier.
# Functions findrootword and generator are for generating the word form from given attributes and root.
def findrootword(checkedrootword):
	listing = [] # Initialised a list.
	filelist = ['SL_roots.xml', 'SL_nouns.xml', 'SL_adverbs.xml', 'SL_final.xml', 'SL_parts.xml', 'SL_pronouns.xml'] # list of Gerard's xml files.
	for datafile in filelist:
		tree = etree.parse(datafile) # Parsed a tree.
		entries = tree.xpath('.//f') # All entries of that file.
		for entry in entries:
			parts = entry.getchildren() # Got all the children of that tree.
			s = parts[-1] # Fetched tag 's'.
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
	if len(word) > 1:
		if word[-1] == 'H':
			word = word[:-1]+"s" # A word ending with a visarga are converted to sakArAnta, because this is how Gerard has stored his data.
		elif word[-1] == 'M':
			word = word[:-1]+"m"
	# If there are tags which are not enumerated here, they can be added as and when there is a need.
	database = [('v-cj-prim', 'प्राथमिकः'),
    ('v-cj-ca', 'णिजन्तः'),
    ('v-cj-int', 'यङन्तः'),
    ('v-cj-des', 'सन्नन्तः'),
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
    ('np-sg', 'एकवचनम्'),
    ('np-du', 'द्विवचनम्'),
    ('np-pl', 'बहुवचनम्'),
    ('fst', 'उत्तमपुरुषः'),
    ('snd', 'मध्यमपुरुषः'),
    ('trd', 'प्रथमपुरुषः'),
    ('na-nom', 'प्रथमाविभक्तिः'),
    ('na-voc', 'संबोधनविभक्तिः'),
    ('na-acc', 'द्वितीयाविभक्तिः'),
    ('na-ins', 'तृतीयाविभक्तिः'),
    ('na-dat', 'चतुर्थीविभक्तिः'),
    ('na-abl', 'पञ्चमीविभक्तिः'),
    ('na-gen', 'षष्ठीविभक्तिः'),
    ('na-loc', 'सप्तमीविभक्तिः'),
    ('sg', 'एकवचनम्'),
    ('du', 'द्विवचनम्'),
    ('pl', 'बहुवचनम्'),
    ('mas', 'पुंल्लिङ्गम्'),
    ('fem', 'स्त्रीलिङ्गम्'),
    ('neu', 'नपुंसकलिङ्गम्'),
    ('dei', 'सङ्ख्या'),
    ('uf', 'अव्ययम्'),
    ('ind', 'क्रियाविशेषणम्'),
    ('interj', 'उद्गारः'),
    ('parti', 'निपातम्'),
    ('prep', 'चादिः'),
    ('conj', 'संयोजकः'),
    ('tasil', 'तसिल्'),
    ('vu-cj-prim', 'अव्ययधातुरूप-प्राथमिकः'),
    ('vu-cj-ca', 'अव्ययधातुरूप-णिजन्तः'),
    ('vu-cj-int', 'अव्ययधातुरूप-यङन्तः'),
    ('vu-cj-des', 'अव्ययधातुरूप-सन्नन्तः'),
    ('iv-inf','तुमुन्'),
    ('iv-abs','क्त्वा'),
    ('iv-per','per'),
    ('ab-cj-prim', 'क्त्वा-प्राथमिकः'),
    ('ab-cj-ca', 'क्त्वा-णिजन्तः'),
    ('ab-cj-int', 'क्त्वा-यङन्तः'),
    ('ab-cj-des', 'क्त्वा-सन्नन्तः'),
    ('kr-cj-prim-no', 'प्राथमिकः'),
    ('kr-cj-ca-no', 'णिजन्तः'),
    ('kr-cj-int-no', 'यङन्तः'),
    ('kr-cj-des-no', 'सन्नन्तः'),
    ('kr-vb-no', ''),
    ('ppp', 'कर्मणिभूतकृदन्तः'),
    ('ppa', 'कर्तरिभूतकृदन्तः'),
    ('pprp', 'कर्मणिवर्तमानकृदन्तः'),
    ('ppr-para', 'कर्तरिवर्तमानकृदन्त-परस्मैपदी'),
    ('ppr-atma', 'कर्तरिवर्तमानकृदन्त-आत्मनेपदी'),
    ('ppft-para', 'पूर्णभूतकृदन्त-परस्मैपदी'),
    ('ppft-atma', 'पूर्णभूतकृदन्त-आत्मनेपदी'),
    ('pfutp', 'कर्मणिभविष्यत्कृदन्तः'),
    ('pfut-para', 'कर्तरिभविष्यत्कृदन्त-परस्मैपदी'),
    ('pfut-atma', 'कर्तरिभविष्यत्कृदन्त-आत्मनेपदी'),
    ('gya', 'य'),
    ('iya', 'ईय'),
    ('tav', 'तव्य'),
    ('para', 'कर्तरि'),
    ('atma', 'कर्तरि'),
    ('pass', 'कर्मणि'),
    ('pa', 'कृदन्तः'),
	('iic', 'समासपूर्वपदनामपदम्'),
	('iip', 'समासपूर्वपदकृदन्तः'),
	('iiv', 'समासपूर्वपदधातुः'),
	('upsrg', 'उपसर्गः')
				]
	#print "analysis of word started", timestamp()
	datafetched = analyser(word,strength='low') # Analyse the input word.
	#print "analysis of word ended", timestamp()
	if datafetched == "????": # If error
		return "????" # Return error
	else:
		individual = datafetched.split("|") # create a list of all possible splits.
		outputlist = []
		for ind in individual:
			split = ind.split('-') # Separate the tags.
			root = split[0].decode('utf-8') # Base root.
			#root = root.split('#')[0] # In case you want to remove '#1' etc kept by Gerard, uncomment it.
			root = transcoder.transcoder_processString(root, "slp1", "deva") # Conversion to Devanagari.
			output = "-".join(split[1:]) # All Devanagari attributs joined with '-'.
			output = output.decode('utf-8') # UTF-8
			for member in database:
				output = re.sub(member[0], member[1].decode('utf-8'), output) # Changed attributes strings with their Sanskrit Devanagari counterparts.
			output = transcoder.transcoder_processString(output, "slp1", "deva") # This code creates some issue in windows setting. Therefore not converting to Devanagari right now. Will do that later.
			outputlist.append(root + "-" + output)
		#print "Postprocessing of word ended", timestamp()
		return "|".join(outputlist) # Return output
#print devanagaridisplay("aMSakatas")

# This is the most important function.
# It analyses the words in inputfile and gives the analysed version in outputfile.
def convertfromfile(inputfile,outputfile):
	f = codecs.open(inputfile, 'r', 'utf-8') # Opened inputfile with UTF-8 encoding.
	data = f.readlines() # Read the lines into a list.
	f.close() # Closed the inputfile.
	g = codecs.open(outputfile, 'w', 'utf-8') # Opened the outputfile with UTF-8 encoding.
	for datum1 in data: # For each member of data,
		datum1 = datum1.strip() # Removed unnecessary whitespaces.
		datum1 = transcoder.transcoder_processString(datum1, "deva", "slp1") # Converted from Devanagari to SLP1.
		dat = re.split('(\W+)',datum1) # Created a word list by exploding the sentence at word boundaries.
		for i in xrange(len(dat)):
			datum = dat[i].strip() # Clean whitespaces.
			if i % 2 == 0 and i != len(dat): # Even members of datum are the words and odd members are word boundaries. Therefore, processing only even members. 
				#print "analysis of word started", timestamp()
				x = devanagaridisplay(datum) # Analysed the even members.
				#print "analysis of word ended", timestamp()
				g.write(transcoder.transcoder_processString(datum, "slp1", "deva")+"("+x+")") # Wrote to the outputfile.
				print datum, timestamp()
				#print transcoder.transcoder_processString(datum, "slp1", "deva")+"("+x+")" # printed to the screen for the user.
				#print "wrote to the file", timestamp()
			else:
				g.write(transcoder.transcoder_processString(dat[i], "slp1", "deva")) # For odd members, converted the word boundaries to their Devanagari counterparts.
		g.write('\n') # Newline character added
		print # Newline character printed on terminal.
	g.close() # Closed outputfile.

if __name__=="__main__":
	convertfromfile('sanskritinput.txt','analysedoutput.txt')
