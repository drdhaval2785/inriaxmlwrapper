# SanskritMark

A specification guideline for using the benifits of Sanskrit tools available at http://sanskrit.inria.fr.

The guideline is important to maintain uniformity.

#####Transliteration - SLP1



# Noun form

## Suggested format

```
noun.gender.case.vacana
```

where

'gender' takes 'm' for musculine, 'f' for feminine, 'n' for neuter and 'a' for any gender.

'case' takes '1' for nominative, '2' for accusative, '3' for instrumental, '4' for dative, '5' for ablative, '6' for genitive, '7' for locative and '0' for sambodhana.

'vacana' takes '1' for ekavacana, '2' for dvivacana and '3' for bahuvacana respectively.

e.g. `Davala.m.1.1` signifies that the noun 'Davala' has to be declined with musculine, nominative ekavacana i.e. DavalaH

# Verb form

## Suggested format

```
verb.gana.pada.lakara.vacya.purusa.vacana
```

where

'gana' takes '1' to '10' where they are usual gaNas in pANini's grammar. Use '0' for secondary verbs.

'pada' takes 'p'/'a' for parasmaipada and Atmanepada respectively.

'lakara' takes 'law'/'laN'/'viliN'/'low'/'lfw'/'lfN'/'luw'/'liw'/'luN'/'aluN'/'AliN'. viliN stands for viDiliN. aluN stands for AgamAbhAvayuktaluN, AliN stands for ASIrliN. All others have their usual notations in pANini's grammar.

'vacya' takes 't' / 'm' for kartari and karmaNi respectively.

'purusa' takes 'p'/'m'/'u' for prathama, madhyama, uttama respectively.

'vacana' takes '1'/'2'/'3' for ekavacana, dvivacana and bahuvacana respectively.

e.g. `BU.1.p.low.t.1.1` signifies that the verb 'BU' has to be declined with 1st gana, parasmaipada, low lakara, kartari vacya, prathama purusa, ekavacana e.g. aBUt

# kRdanta form

## Suggested format

```
verb.gana.kridanta.gender.case.vacana
```

where

'gana' takes '1' to '10' where they are usual gaNas in pANini's grammar. Use '0' for secondary verbs.

'kridanta' takes '1' for 'kta', '2' for 'ktavat', '3' for 'Satf', '4' for 'SAnac', '5' for 'SAnac Atmanepada', '6' for 'luwAdeSa parasmaipada', '7' for 'luwAdeSa Atmanepada', '8' for 'tavya', '9' for 'yat', '10' for 'anIyar', '11' for 'Ryat', '12' for 'liqparasmai' and '13' for 'liqAtmane'.

'gender' takes 'm' for musculine, 'f' for feminine and 'n' for neuter.

'case' takes '1' for nominative, '2' for accusative, '3' for instrumental, '4' for dative, '5' for ablative, '6' for genitive, '7' for locative and '0' for sambodhana.

'vacana' takes '1' for ekavacana, '2' for dvivacana and '3' for bahuvacana respectively.

# adverbial form

## Suggested format

```
adverb.adv
```

where

'adverb' is the adverb concerned.

'adv' is constant string.


# SanskritMark to Devanagari

If a SanskritMark description gives more than one form, they will be shown separated by '|'. Note that there would be no space around the separator.

# Devanagari to SanskritMark

If a given Sanskrit word can stand for more than one SanskritMark description, they will be shown separated by '|'. Note that there would be no space around the separator.
