# This Python file uses the following encoding: utf-8
# ('प्राथमिक-लट्-कर्तरि-एकवचन-प्रथमपुरुष', '', '', 'tA ', '', 'hE'), this is the expected output of this program
first = ['प्राथमिक', 'णिजन्त', 'यङन्त', 'सन्नन्त']
second = ['लट्', 'लोट्', 'विधिलिङ्', 'लङ्', 'लृट्', 'लिट्', 'लुङ्', 'आगमाभावयुक्तलुङ्', 'लृङ्', 'आशीर्लिङ्']
third = ['कर्तरि', 'कर्मणि']
fourth = [ 'एकवचन', 'द्विवचन', 'बहुवचन']
fifth = ['उत्तमपुरुष', 'मध्यमपुरुष', 'प्रथमपुरुष']
f = open("suffix.txt", "w")
for one in first:
	for two in second:
		for three in third:
			for four in fourth:
				for five in fifth:
					f.write( "('"+one+"-"+two+"-"+three+"-"+four+"-"+five+"', '', '', '', '', ''),\n")
f.close
