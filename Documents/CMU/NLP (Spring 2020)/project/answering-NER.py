#!/usr/bin/env python
# coding: utf-8

# In[1]:


import nltk
from nltk import sent_tokenize, word_tokenize, pos_tag, ne_chunk
from nltk import ngrams


# In[2]:


datafile = "Development_data/set1/a1.txt"
datafile2 = "Development_data/set1/a2.txt"
questionfile = "Development_data/set1/a1q.txt"

data = open(datafile, "r")
data2 = open(datafile2, "r")
questions = open(questionfile, "r") 


# In[3]:


sample_txt = data.read()
sample_txt_sentences = nltk.sent_tokenize(sample_txt)

questions_txt = questions.read()
questions_txt_sentences = nltk.sent_tokenize(questions_txt)


# In[7]:


def find_sentence_in_txt_by_question(text_sentences_list, question_sentence):
    
    q_tokenize = nltk.word_tokenize(question_sentence)
    q_bigrams = list(ngrams(q_tokenize,2))
    q_trigrams = list(ngrams(q_tokenize,3))
    
    #print(q_bigrams)
    
    best_sentence = ""
    best_num_matching = -1
    #print(text_sentences_list)
    for sentence in text_sentences_list:
        txt_tokenize = nltk.word_tokenize(sentence)
        txt_bigrams = list(ngrams(txt_tokenize,2))
        txt_trigrams = list(ngrams(txt_tokenize,3))
        
        curr_matching = 0
        sent_words = sentence.split()
        for bigram in txt_bigrams:
            if bigram in q_bigrams:
                curr_matching += 1
                #print(curr_matching)
        for trigram in txt_trigrams:
            if trigram in q_trigrams:
                curr_matching += 1
        if curr_matching > best_num_matching:
            best_sentence = sentence
            best_num_matching = curr_matching
            
    return best_sentence


# In[8]:


find_sentence_in_txt_by_question(sample_txt_sentences, questions_txt_sentences[3])


# In[9]:


print(questions_txt_sentences[3])


# In[18]:


def process_sentence(sentence):
    named_ent_list = []
    res = []
    question_ne_list = []
    tokenized = nltk.word_tokenize(sentence)
    tagged = nltk.pos_tag(tokenized)
    named_ent = nltk.ne_chunk(tagged)
        
    #get named entities
    for chunk in named_ent:
        if hasattr(chunk, 'label'):
            question_ne_list.append((chunk.label(), ' '.join(c[0] for c in chunk)))
    
    #get full output
    named_ent_list += question_ne_list
    res = (str(named_ent).split("\n  "))
    
    #print((named_ent_list, res))
    return (named_ent_list, res)
        
    #return named_ent_list


# In[19]:


process_sentence(questions_txt_sentences[3])


# In[20]:


txt_answer = find_sentence_in_txt_by_question(sample_txt_sentences, questions_txt_sentences[3])
process_sentence(txt_answer)


# In[ ]:




