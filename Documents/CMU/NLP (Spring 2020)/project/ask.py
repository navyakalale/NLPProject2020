#!/usr/bin/env python3

import spacy
import sys
from collections import defaultdict

nlp = spacy.load("en_core_web_sm")
txt1 = "Autonomous cars shift insurance liability toward manufacturers"
txt2 = "Pittsburgh is a city in the state of Pennsylvania in the United States, and is the county seat of Allegheny County."
txt3 = "1999 is the year Matthew McQuaid was born"
txt4 = "Matthew McQuaid was born in 1999"

txts = [nlp(x) for x in (txt1,txt2,txt3,txt4)]

def curry2(f):
    return lambda x:lambda y:f(x,y)

#Maps word types to the apprioate question wh-word
reps = defaultdict(lambda:'what',
    {'ORG':'which organization',
     'MONEY':'how much',
     'GPE':'what',
     'PERSON':'who',
     'LOC':'where',
     'DATE':'when'
    })


def toWords(doc):
    return [tok.text for tok in doc]

def getLabel(word):
    ents = nlp(word).ents

    return ents[0].label_ if len(ents) > 0 else None

def searchChunks(deps,chunks):
    entity = None
    for chunk in chunks:
        if chunk.root.dep_ in deps:
            entity = chunk.text
            start,end = chunk.start,chunk.end
            break

    return (start,end,reps[getLabel(entity)]) if entity else None

def searchToks(deps,doc):
    entity = None
    for i,tok in enumerate(doc):
        if tok.dep_ in deps:
            entity = tok.text
            index = i
            break
    return (index,reps[getLabel(entity)]) if entity else None

@curry2
def replace(deps,doc):
    splitatcommas = doc.split(',')
    if(len(splitatcommas) > 1):
        return None
    splitatcommasnlp = nlp(splitatcommas[0])
    words = toWords(splitatcommasnlp)
    entity = None
    a,b = searchChunks(deps,splitatcommasnlp.noun_chunks),searchToks(deps,splitatcommasnlp)
    if a:
        start,end,rep = a
        words[start:end] = [""]
        if(start==0):
            if(nlp(words[end])[0].pos_ == "CCONJ" or nlp(words[end])[0].pos_ == "ADP"):
                return None
        else:
            if(nlp(words[0])[0].pos_ == "CCONJ" or nlp(words[0])[0].pos_ == "ADP"):
                return None
        words = [rep] + words
        return words
    if b:
        i,rep = b
        words[i] = rep
        return words

    return None

subj = ['nsubj','nsubjpass','csubj','csubjpass']
obj  = ['dobj','iobj','pobj']

replaceSubject = replace(subj)
replaceObject = replace(obj)

def sortingFunc(e):
  return len(e)

def applyReplace(rep,txts,n):
    arr = [' '.join(x) for x in [rep(x) for x in txts] if x]
    arr.sort(key=sortingFunc)
    return arr[0:n]

with open(sys.argv[1]) as f:
    text = f.read()

sents = [nlp(s.text) for s in nlp(text).sents]
sentstext = [s.text for s in nlp(text).sents]

for s in applyReplace(replaceSubject,sentstext,int(sys.argv[2])):
    print(s.strip())

