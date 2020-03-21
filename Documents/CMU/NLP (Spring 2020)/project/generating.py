import spacy

nlp = spacy.load("en_core_web_sm")
string1st = "Autonomous cars shift insurance liability toward manufacturers"
string = "Germany invaded France in 1940"
doc = nlp(string)
save = ""
subj = ""
head = ""
label = ""
for chunk in doc.noun_chunks:
    print(chunk.text, chunk.root.text, chunk.root.dep_,
            chunk.root.head.text)
    if(chunk.root.dep_ == "nsubj"):
    	subj = chunk.text
    	head = chunk.root.head.text
for ent in doc.ents:
	if(subj == ent.text):
		label = ent.label_
save = string.replace(subj, "")
if(label == "ORG"):
	save = "which organization" + save + "?"
elif(label == "MONEY"):
	save = "how much" + save + "?"
elif(label == "GPE"):
	save = "which country" + save + "?"
elif(label == "PERSON"):
	save = "who" + save + "?"
elif(label == "LOC"):
	save = "where" + save + "?"
else:
	save = "what" + save + "?"
print(save)
