# This Python file uses the following encoding: utf-8
import transcoder
import codecs
import re

# ('प्राथमिक-लट्-कर्तरि-एकवचन-प्रथमपुरुष', '', '', 'tA ', '', 'hE'), this is the expected output of this program
def suffixlist():
	first = ['प्राथमिक', 'णिजन्त', 'यङन्त', 'सन्नन्त']
	second = ['लट्', 'लोट्', 'विधिलिङ्', 'लङ्', 'लृट्', 'लिट्', 'लुङ्', 'आगमाभावयुक्तलुङ्', 'लृङ्', 'आशीर्लिङ्', 'लुट्']
	third = ['कर्तरि', 'कर्मणि']
	fourth = [ 'एकवचन', 'द्विवचन', 'बहुवचन']
	fifth = ['उत्तमपुरुष', 'मध्यमपुरुष', 'प्रथमपुरुष']
	f = open("suffix.txt", "w")
	number = 1
	for one in first:
		for two in second:
			for three in third:
				f.write(str(number)+". "+one+"-"+two+"-"+three+"\n")
				#number += 1
				for four in fourth:
					for five in fifth:
						f.write( "('"+one+"-"+two+"-"+three+"-"+four+"-"+five+"', '', '', '', '', ''),\n")
	f.close()
#suffixlist()

def nounsuffixlist():
	first = ['प्रथमा', 'संबोधन', 'द्वितीया', 'तृतीया', 'चतुर्थी', 'पञ्चमी', 'षष्ठी', 'सप्तमी']
	second = ['एकवचन', 'द्विवचन', 'बहुवचन']
	third = ['पुंल्लिङ्ग', 'स्त्रीलिङ्ग', 'नपुंसकलिङ्ग', 'सङ्ख्या']
	f = open("nounsuffix.txt", "w")
	number = 1
	for one in first:
		for two in second:
			for three in third:
				f.write( "('"+one+"-"+two+"-"+three+"', '', '', '', '', ''),\n")
	f.close()
nounsuffixlist()

def dev(file):
	f = codecs.open(file, 'r+', 'utf-8-sig')
	data = f.read()
	data = transcoder.transcoder_processString(data,'slp1','deva')
	data = re.sub(u'ळ्ह्', '|', data)
	f.close()
	g = codecs.open("hindidevanagariverbform.txt", "w+", "utf-8-sig")
	g = codecs.open("skd_deva.txt", "w+", "utf-8-sig")
	g.write(data)
	g.close()
#dev('hindiverbform.txt')

def dev1(file):
	f = codecs.open(file, 'r+', 'utf-8-sig')
	g = codecs.open("skd_deva.txt", "w+", "utf-8-sig")
	data = f.readlines()
	for datum in data:
		datum = transcoder.transcoder_processString(datum,'slp1','deva')
		datum = re.sub(u'ळ्ह्', '|', datum)
		g.write(datum)
		print datum
	g.close()
	f.close()
#dev1('skd.txt')
