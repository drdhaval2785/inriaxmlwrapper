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
import editdistance

# Function to return timestamp
def printtimestamp():
	return datetime.datetime.now()

# Parsing the XMLs. We will use them as globals when need be.
print "Parsing of XMLs started at", printtimestamp()
roots = etree.parse('SL_roots.xml') # parses the XML file.
nouns = etree.parse('SL_nouns.xml')
adverbs = etree.parse('SL_adverbs.xml')
final = etree.parse('SL_final.xml')
parts = etree.parse('SL_parts.xml')
pronouns = etree.parse('SL_pronouns.xml')
upasargas = etree.parse('SL_upasargas.xml')
# This filelist can include all or some files. By default it takes into account all XMLs of Gerard.
# If you need some specific database like roots, nouns etc you can keep them and remove the rest. It would speed up the process.
filelist = [roots, nouns, adverbs, final, parts, pronouns, upasargas]
#filelist = [parts]
print "Parsing of XMLs completed at", printtimestamp()
#print "Will notify after every 100 words analysed."

# function to create the verbformlist from XML file SL_roots.xml. Output stored as verbformlist.txt.
# The database can be put into many uses e.g. in https://github.com/drdhaval2785/SanskritVerb/ I use it to compare my output against Gerard's database and note the errors in my output for correction.
def verbformlist():
	global roots # fetched parsed XML.
	g = codecs.open('verbformlist.txt', 'w', 'utf-8') # Opened the file to store data.
	# Typical line in XML file is in `<forms><f form="aMSaya"><v><cj><prim/></cj><sys><prs gn="11"><md><ip/></md><para/></prs></sys><np><sg/><snd/></np></v><s stem="aMSa"/></f></forms>` format.
	# Therefore, the data which we want e.g. 'aMSaya' is in /forms/f-get('form') location. Fetching it below.
	roo = roots.xpath('/forms/f') # Returns a list of all /forms/f in the database.
	verbformlist = [member.get('form') for member in roo] # For all /forms/f in database, we get its attribute 'forms' e.g. 'aMSaya'.
	g.write(','.join(verbformlist)) # The list verbformlist is stored as comma separated data in the outputfile.
	g.close() # Closed the file.
#verbformlist()

# function to create verblist from XML file SL_roots.xml.
def verblist():
	global roots # Fetched parsed XML.
	g = codecs.open('verblist.txt', 'w', 'utf-8') # Opened the file to store data.
	# Typical line in XML file is in `<forms><f form="aMSaya"><v><cj><prim/></cj><sys><prs gn="11"><md><ip/></md><para/></prs></sys><np><sg/><snd/></np></v><s stem="aMSa"/></f></forms>` format.
	# Therefore, the data which we want e.g. 'aMSa' is in /forms/f/s-get('stem') location. Fetching it below.
	roo = roots.xpath('/forms/f/s') # Returns a list of all /forms/f/s in the database.
	verbformlist = [member.get('stem') for member in roo] # For all /forms/f/s in the databae, we get its attribute 'stem' e.g. 'aMSa'.
	verbformlist = list(set(verbformlist)) # Keeping only unique entries, because for a stem can give a lot of verb forms.
	outputlist = [] # Initialising a list to store data for return.
	for member in verbformlist:
		member = re.sub(r'[0-9]',r'',member) # Removed all digits, because Gerard names its verbs like 'BU#1' sometimes. If you want such output, comment these lines out.
		member = re.sub('#','',member) # Removed '#'.
		outputlist.append(member) # Added in the outputlist.
	outputlist = list(set(outputlist)) # Keeping only unique items.
	print len(outputlist) # Just to get an idea of the number of verbs returned. Can comment out if not needed.
	g.write(','.join(outputlist)) # The list is stored as comma separated data in the outputfile.
	g.close() # Closed the file.
#verblist();

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
allmembers = allmemberlist() 

#print "Starting analysis at", printtimestamp()

# Function makestring converts a list of list into all possible strings e.g. [['p','b'],['A'],['g','u']] would give pAg,bAg,pAu,bAu as output.
# Default joiner is a blank. You can specify conj='+' etc to join the strings with a '+'.
# The function is used as subroutine in function 'sss'.
def makestring(listoflist, conj=''):
	# by default the least number of members of the output list would be equal to the first member e.g. len(['p','b']) = 2. 
	outputstore = listoflist[0]
	# For rest of the members, we run a for loop.
	for i in range(1,len(listoflist)):
		out2 = []
		for member in outputstore:
			# All strings of the listoflist[i] are joined to the member (the strings generated so far). e.g. pA,bA would become pAg,bAg,pAu,gAu in our example
			for j in listoflist[i]:
				out2.append(member + conj + j)
			outputstore = out2
	out3 = []
	for love in outputstore:
		out3.append(love)
	return out3

# This function splits a long word into its constituent words (If you want to change the dictionary, change the parameter 'words'. By default, they are fetched data from Gerard's XMLs above)
# http://stackoverflow.com/questions/8870261/how-to-split-text-without-spaces-into-list-of-words
#def find_words(instring, prefix = '', words = firstmembers + secondmembers):
def find_words(instring, prefix = '', words = allmembers):
    if not instring:
        return [] # Return a blank list
    if (not prefix) and (instring in words):
        return [instring] # The instring is in our 'words' i.e. the input is in our dictionary. Therefore, there is no need to break it. It would be returned.
    prefix, suffix = prefix + instring[0], instring[1:]
    solutions = []
    # Case 1: prefix in solution
    if prefix in words:
        try:
            solutions.append([prefix] + find_words(suffix, '', words)) # A recursive function. This is very slow for long words. Will have to find out some more efficient way.
        except ValueError:
            pass
    # Case 2: prefix not in solution
    try:
        solutions.append(find_words(suffix, prefix, words)) # A recursive function.
    except ValueError:
        pass
    if solutions:
        return sorted(solutions,
                      key = lambda solution: [len(word) for word in solution],
                      reverse = True)[0] # Returns the split with maximum possibility.
    else:
        return 'error'

# A subroutine to main function 'sss' to remove impossible splits i.e. when any split is less than expectedlength or when the terminal split is <= 4.
def leng(x, expectedlength, wordlist=allmembers):
	output = []
	y = x.split('+')
	for mem in y:
		if len(mem) <= expectedlength: # if there is any member in the split which is less than specified length, there are low chances that the split is good, so removing such splits.
			return False
	else:
		if y[-1] <= 4: # The last member of the split is an inflected form. So it is very rare to see them less than 4 letters. Excluding them.
			return False
		elif re.search(r'[aAiIuUfFeEoO][aAiIuUfFeEoO]', x): # Sanskrit has very less chances of two consecutive vowels. Excluding them.
			return False
		else: # Returning the rest as true.
			return True

# A subroutine to main function 'sss' to remove splits of find_words which don't parse the full word i.e. which didn't get the correct parse.
def find_word_exact(inputword):
	findwordoutput = find_words(inputword)
	if ''.join(findwordoutput) == inputword: # If the split matches with the inputword
		return '+'.join(findwordoutput) # Return the split with '+' in between
	else:
		return 'error' # Return error.

# sss stands for sandhisamasasplitting. It works well, but too slow. We need some restrictions while making sandhi splits.
def sss(inputword):
	# Some premodifications in the inputwords, because Gerard stores them with terminal s or m.
	if len(inputword) > 1:
		if inputword[-1] == 'H':
			inputword = inputword[:-1]+"s" # A word ending with a visarga are converted to sakArAnta.
		elif inputword[-1] == 'M':
			inputword = inputword[:-1]+"m" # A word ending with an anusvAra is converted to makArAnta.
	global firstmembers, secondmembers
	# A rough sandhi data for vowel sandhi. It can be extended to consonant sandhis and visarga sandhis, rutva sandhis etc by the same logic. Pending as of now.
	voweldata = [('A','a+a'),('A','a+A'),('A','A+a'),('A','A+A'),('I','i+i'),('I','i+I'),('I','I+i'),('I','I+I'),('U','u+u'),('U','u+U'),('U','U+u'),('U','U+U'),('F','f+f'),('e','e+a'),('e','a+i'),('e','A+i'),('e','a+I'),('e','A+I'),
				  ('o','o+a'),('o','a+u'),('o','A+u'),('o','a+U'),('o','A+U'),('E','a+e'),('E','A+e'),('E','a+E'),('E','A+E'),('O','a+o'),('O','A+o'),('O','a+O'),('O','A+O'),('y','i+'),('y','I+'),('v','u+'),('v','U+'),]
	consonantdata = [(r'([aAiIuUfFxXeEoO])([M])([S])([c])','\1n\4')]
	out2 = []
	for i in xrange(len(inputword)): # For each member of the list inputword
		out3 = [inputword[i]]
		for (x,y) in voweldata: # For each tuple in list voweldata
			out3.append(inputword[i].replace(x, y)) # Replaced the vowels with their possible splits e.g. A->a+a,a+A,A+a,A+A.
		out3 = list(set(out3)) # Unique entries.
		out2.append(out3) 
	sandhisplitdata = makestring(out2) # Returns the list in form of string.
	out4 = []
	for san in sandhisplitdata:
		if leng(san,2) or san.split('+')[-1] in ['ca']:
			#print printtimestamp()
			san = re.sub('[+]', '', san) # Removed '+' sign.
			for (a,b) in consonantdata: 
				san = re.sub(a, b, san) # Replaced consonantdata with their corresponding changes.
			#print printtimestamp()
			q = find_word_exact(san) # Return the splits which are proper splits of the inputword, filtering out unnecessary splits.
			#print printtimestamp()
			if q is not 'error':
				out4.append(q) # store in out4 list.
	if len(out4) > 0 and type(out4) == list:
		return '|'.join(out4) # Return the split separated by '|' in case there are more than one possible splits.
	else:
		return 'error' # Return error.

# function findwordform searches in the XML file for line which matches the wordform we are interested in. e.g. findwordform("Bavati","SL_roots.xml") would find all lines of XML file which have word form "Bavati".
def findwordform(inputform):
	#print "importing filelist for findwordform started at", printtimestamp()
	global filelist # Fetched global variable filelist.
	#print "importing filelist for findwordform ended at", printtimestamp()
	outputlist = [] # A list to store output.
	for file in filelist:
		tree = file # The etree to manipulate.
		xpathname = '/forms/f[@form="' + inputform + '"]' # Defined the xpath to search
		#print "xpath parsing for findwordform started at", printtimestamp() # After speed analysis, this function is the most time expensive. It takes around 0.10 sec per word form.
		r = tree.xpath(xpathname) # Created a list 'r' whose members are lines of XML file which correspond to the word form 'inputform'
		#print "xpath parsing for findwordform ended at", printtimestamp()
		for member in r:
			outputlist.append(etree.tostring(member).strip()) # Created a string out of element tree. strip() removes unnecessary white spaces around the string.
	#print "findwordform completed at", printtimestamp()
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
			#print "parsing of iter started at", printtimestamp()
			context = etree.parse(tree) # Parsed the element tree.
			#print "parsing of iter ended at", printtimestamp()
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
		#print "postprocessing of iter ended at", printtimestamp()
		return "|".join(wordwithtags) # If there are more than one possible verb characteristics for a given form, they are shown separated by a '|'

def mapiter(input):
	return iter(findwordform(input))

# function analyser analyses all the XML files and gets matching details from all XMLs e.g. 'Bavati' may be a verb form, but it can also be a noun form of 'Bavat' locative singular. Therefore it is needed to traverse all XML files.
def analyser(word, strength="Full"):
	global secondmembers
	if not findwordform(word) == '????': # If the output is not an error
		return iter(findwordform(word), strength) # Return the output
	else:
		samasa = sss(word) # Try to split the word for samAsa / sandhi.
		output = []
		if samasa is not 'error': # If the word can be split as a samAsa / sandhi,
			indsamasa = samasa.split('|') # Separate all possible splits.
			for indsam in indsamasa:
				indsamcomponents = indsam.split('+') # Separate members of the compound / sandhi
				analy = map(mapiter, indsamcomponents) # Apply mapiter function to all components of indsamcomponents.
				"""prefix = indsamcomponents[:-1]
				lastword = indsamcomponents[-1]
				lastwordanalysed = iter(findwordform(lastword), strength)
				for lastwordan in lastwordanalysed.split('|'):
					output.append('+'.join(prefix) + '+' + lastwordan)"""
				output.append('$'.join(analy)) # Appended the solution to output list.
			return '%'.join(output) # Return the output joined by '%'.
		else:
			return '????' # Return error.

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
	#print "analysis of word started", printtimestamp()
	datafetched = analyser(word) # Analyse the input word.
	#print "analysis of word ended", printtimestamp()
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
		#print "Postprocessing of word ended", printtimestamp()
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
				#print "analysis of word started", printtimestamp()
				x = devanagaridisplay(datum) # Analysed the even members.
				#print "analysis of word ended", printtimestamp()
				g.write(transcoder.transcoder_processString(datum, "slp1", "deva")+"("+x+")") # Wrote to the outputfile.
				print transcoder.transcoder_processString(datum, "slp1", "deva")+"("+x+")" # printed to the screen for the user.
				#print "wrote to the file", printtimestamp()
			else:
				g.write(transcoder.transcoder_processString(dat[i], "slp1", "deva")) # For odd members, converted the word boundaries to their Devanagari counterparts.
				print transcoder.transcoder_processString(dat[i], "slp1", "deva") # For odd members, converted the word boundaries to their Devanagari counterparts.
		g.write('\n') # Newline character added
		print # Newline character printed on terminal.
	g.close() # Closed outputfile.
	
if __name__ == "__main__":
        convertfromfile('sanskritinput.txt','analysedoutput.txt')
