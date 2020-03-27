import spacy
from collections import defaultdict

nlp = spacy.load("en_core_web_sm")
txt1 = "Autonomous cars shift insurance liability toward manufacturers"
txt2 = "Pittsburgh is a city in the state of Pennsylvania in the United States, and is the county seat of Allegheny County."
txt3 = "1999 is the year Matthew McQuaid was born"
txt4 = "Matthew McQuaid was born in 1999"
doc = nlp(txt4)


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


@curry2
def replace(deps,doc):
    words = toWords(doc)
    entity = None
    for chunk in doc.noun_chunks:
        if chunk.root.dep_ in deps:
            entity = chunk.text
            start,end = chunk.start,chunk.end
    if entity:
        words[start:end] = [reps[getLabel(entity)]]
        return words
    else:
        for i,tok in enumerate(doc):
            if tok.dep_ in deps:
                entity = tok.text
        if entity:
            words[i] = reps[getLabel(entity)]
            return words

        else:
            return None

subj = ['nsubj','nsubjpass','csubj','csubjpass']
obj  = ['dobj','iobj','pobj']

replaceSubject = replace(subj)
replaceObject = replace(obj)


