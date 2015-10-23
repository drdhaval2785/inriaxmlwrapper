# What to expect
This code analyses a given Sanskrit text and gives its possible wordform analysis.
e.g. `किन्तु` would be analysed as `किन्तु(किन्तु-अव्ययम्-क्रियाविशेषणम्)`, `शृगालः` would be analysed as `शृगालः(शृगाल-प्रथमाविभक्तिः-एकवचनम्-पुंल्लिङ्गम्)` and `चिन्तयेत्` would be analysed as `चिन्तयेत्(चिन्त्-प्राथमिकः-विधिलिङ्-कर्तरि-एकवचनम्-प्रथमपुरुषः)`.

# Requirements
1. [python2.7](https://www.python.org/downloads/)

2. [lxml](http://lxml.de/)

# Installation and Usage
1. Download ZIP from the [repository](https://github.com/drdhaval2785/inriaxmlwrapper).

2. Extract the content to your favourite folder.

3. Put the file you want to analyse in `sanskritinput.txt`.

4. Open Terminal / cmd.exe.

5. cd to your folder.

6. Type `python sanskritmark.py` and press enter.

7. After the execution is over, check `analysedoutput.txt` for analysis of the text.

# Limitations
Currently support for sandhi and samAsas is quite premitive. We are working on its improvement.

# Keeping updated
If you want to update your database (in case [Gerard](http://sanskrit.rocq.inria.fr/DATA/XML/) updates his list), please download data from http://sanskrit.inria.fr/DATA/XML/SL_morph.tar.gz

Put the extracted XML data into the code directory. (SL\_parts.xml is bigger than what github allows). If there are any preexisting XML files, overwrite.

# Programs in repository
1. sanskritmark.py is the curent code under development.

2. SL_adverbs.xml, SL_final.xml, SL_morph.dtd, SL_nouns.xml, SL_parts.xml, SL_preverbs.txt, SL_pronouns.xml and SL_roots.xml are files taken from Gerard's database.

3. suffixentryfile.py is a file for generating data entry template for various parameters in code sanskritmark.py.

4. inriaxmlparser.py was the premitive version of the code. Now abandoned.


