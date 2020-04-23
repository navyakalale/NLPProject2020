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
    {'ORG':'who',
     'MONEY':'how much',
     'GPE':'who',
     'PERSON':'who',
     'LOC':'where',
     'DATE':'when'
    })


label2Rank = defaultdict(lambda:1,{'VERB':0})

labelRank = defaultdict(lambda:2,{'PERSON':0,'LOC':0,'DATE':0,'GPE':1,'MONEY':1,'ORG':1})

labels = {}

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

    return (start,end,reps[labels[entity]],labelRank[labels[entity]]) if entity else None

def searchToks(deps,doc):
    entity = None
    for i,tok in enumerate(doc):
        if tok.dep_ in deps:
            entity = tok.text
            index = i
            break
    return (index,reps[labels[entity]],labelRank[labels[entity]]) if entity else None

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
        start,end,rep,rank = a

        if words[start] in ('The','the'):
            rep = 'what'
        if start != 0 and end != (len(words) - 1):
            if(words[start - 1] == "[" or words[start - 1] == "("):
                words[start - 1] = ""
                words[end] = ""

        rank2 = 1
        if end < (len(words) - 1):
            if(len(nlp(words[end])) > 0):
                rank2 = label2Rank[nlp(words[end])[0].pos_]
        '''
        words[start:end] = [""]
        if end >= len(words):
            return None
        if(start==0):
            if(nlp(words[end])[0].pos_ == "CCONJ" or nlp(words[end])[0].pos_ == "ADP"):
                return None
        else:
            if(nlp(words[0])[0].pos_ == "CCONJ" or nlp(words[0])[0].pos_ == "ADP"):
                return None

        words = [rep] + words
        '''
        words[start:end] = [rep]
        return (words,rank,rank2)
    if b:
        i,rep,rank = b
        words[i] = rep
        rank2 = 1
        if i+1 < (len(words) - 1):
            if(len(nlp(words[i+1])) > 0):
                rank2 = label2Rank[nlp(words[i+1])[0].pos_]
        return (words,rank,rank2)

    return None

subj = ['nsubj','nsubjpass','csubj','csubjpass']
obj  = ['dobj','iobj','pobj']

replaceSubject = replace(subj)
replaceObject = replace(obj)

def sortingFunc(e):
  return len(e)

def applyReplace(rep,txts,n):
    arr = [(' '.join(x[0]),x[1],x[2]) for x in [rep(x) for x in txts] if x]
    arr.sort(key=lambda p:p[2]*1000+p[1]*100 + len(p[0]))
    #arr = [words for (words,rank) in arr]
    return arr[0:n]



with open(sys.argv[1]) as f:
    text = f.read()

parsed = nlp(text)
sents = [nlp(s.text) for s in parsed.sents]
sentstext = [s.text for s in parsed.sents]

labels = defaultdict(lambda:None,{x.text:x.label_ for x in parsed.ents})

for s in applyReplace(replaceSubject,sentstext,int(sys.argv[2])):
    (s,r,r2) = s
    s = s.strip()
    if s.count('\n') > 1 or '   ' in s:
        continue
    print(s)

