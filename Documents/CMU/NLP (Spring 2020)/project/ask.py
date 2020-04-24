#!/usr/bin/env python3

import spacy
import sys
from collections import defaultdict

nlp = spacy.load("en_core_web_sm")

def curry2(f):
    return lambda x:lambda y:f(x,y)

#Maps word types to the apprioate question wh-word
reps = defaultdict(lambda:'What',
    {'ORG':'Who',
     'MONEY':'How much',
     'GPE':'Who',
     'PERSON':'Who',
     'LOC':'Where',
     'DATE':'When'
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
            rep = 'What'
        if start != 0 and end != (len(words) - 1):
            if(words[start - 1] == "[" or words[start - 1] == "("):
                words[start - 1] = ""
                words[end] = ""

        rank2 = 1
        if end < (len(words) - 1):
            last = nlp(words[end])
            if(len(last) > 0):
                rank2 = label2Rank[last[0].pos_]

        words[start:end] = [rep]
        return (words,rank,rank2)
    if b:
        i,rep,rank = b
        words[i] = rep
        rank2 = 1
        if i+1 < (len(words) - 1):
            last = nlp(words[i+1])
            if(len(last) > 0):
                rank2 = label2Rank[last[0].pos_]
        return (words,rank,rank2)

    return None

subj = ['nsubj','nsubjpass','csubj','csubjpass']
obj  = ['dobj','iobj','pobj']

replaceSubject = replace(subj)
replaceObject = replace(obj)

def whFront(s):
    for w in reps.values():
        if s.startswith(w):
            return True
    return False

def applyReplace(rep,txts,n):
    arr = []
    for x in [rep(x) for x in txts]:
        if x:
            if x[0][-1] == '.':
                x[0][-1] = '?'
            arr += [(' '.join(x[0]),x[1],x[2])]
    #arr = [(' '.join(x[0]),x[1],x[2]) for x in [rep(x) for x in txts] if x]
    arr.sort(key=lambda p:p[2]*1000+p[1]*100 + len(p[0]))
    arr = [p for p in arr if p[0].count('\n') < 1 and '   ' not in p[0] and whFront(p[0])]
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
    print(s)

