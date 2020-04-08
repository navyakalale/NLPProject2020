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

q = questions_txt_sentences[0]


# In[4]:


def find_sentence_in_txt_by_question(text_sentences_list, question_sentence):
    
    q_tokenize = nltk.word_tokenize(question_sentence)
    q_bigrams = list(ngrams(q_tokenize,2))
    q_trigrams = list(ngrams(q_tokenize,3))
    q_fourgrams = list(ngrams(q_tokenize,4))
    q_fivegrams = list(ngrams(q_tokenize,5))
    q_sixgrams = list(ngrams(q_tokenize,6))
    q_sevengrams = list(ngrams(q_tokenize,7))
    
    #print(q_bigrams)
    
    best_sentence = ""
    best_num_matching = -1
    #print(text_sentences_list)
    for sentence in text_sentences_list:
        txt_tokenize = nltk.word_tokenize(sentence)
        txt_bigrams = list(ngrams(txt_tokenize,2))
        txt_trigrams = list(ngrams(txt_tokenize,3))
        txt_fourgrams = list(ngrams(txt_tokenize,4))
        txt_fivegrams = list(ngrams(txt_tokenize,5))
        txt_sixgrams = list(ngrams(txt_tokenize,6))
        txt_sevengrams = list(ngrams(txt_tokenize,7))
        
        curr_matching = 0
        sent_words = sentence.split()
        for bigram in txt_bigrams:
            if bigram in q_bigrams:
                curr_matching += 1
        for trigram in txt_trigrams:
            if trigram in q_trigrams:
                curr_matching += 1
        for fourgram in txt_fourgrams:
            if fourgram in q_fourgrams:
                curr_matching += 2
        for fivegram in txt_fivegrams:
            if fivegram in q_fivegrams:
                curr_matching += 2
        for sixgram in txt_sixgrams:
            if sixgram in q_sixgrams:
                curr_matching += 3
        for sevengram in txt_sevengrams:
            if sevengram in q_sevengrams:
                curr_matching += 3
        if curr_matching > best_num_matching:
            best_sentence = sentence
            best_num_matching = curr_matching
            
    return best_sentence


# In[5]:


find_sentence_in_txt_by_question(sample_txt_sentences, q)


# In[6]:


print(q)


# In[7]:


def process_sentence(sentence):
    named_ent_list = []
    res = []
    question_ne_list = []
    tokenized = nltk.word_tokenize(sentence)
    tagged = nltk.pos_tag(tokenized)
    named_ent = nltk.ne_chunk(tagged, binary=True)
        
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


# In[8]:


tagged_q_sentence = process_sentence(q)


# In[9]:


txt_answer = find_sentence_in_txt_by_question(sample_txt_sentences, q)
process_sentence(txt_answer)


# In[10]:


q_tags = {'WDT', 'WP', 'WP$', 'WRB'}

def get_question_word(tagged_question_sentence):
    tagged_list = tagged_question_sentence[1]
    question_word = ""
    q_tag_word = ""
    for word in tagged_list:
        #print(word.split("/"))
        #print(word)
        wlist = word.split("/")
        if len(wlist) >= 2:
            w = wlist[0]
            tag = wlist[1]
            if tag in q_tags:
                question_word = w
                q_tag_word = tag
    return (question_word, q_tag_word)
        #w = word.split("/")[0]
        #tag = word.split('/')[1]
        #print(w,tag)
    


# In[11]:


get_question_word(tagged_q_sentence)


# In[12]:


tag_dict = {'WP' : ['NNP'], 'WDT' : ['JJ', 'NNP']}
def find_sentence_words_by_question(question_word, question_tag, question, sentence_txt):
    #print(question_tag)
    question_words = question.split("?")[0].split()
    #print(question_words)
    tags_to_find = tag_dict[question_tag]
    processed_sent = process_sentence(sentence_txt)[1]
    #print(processed_sent)
    sentence_words = []
    sentence_tag_words = []
    if question_word.lower() == 'which':
        w_to_find_idx = question_words.index('which') + 1
        w_to_find = question_words[w_to_find_idx]
        w_to_find_is_plural = False
        if w_to_find[-1] == 's':
            #print("isplural")
            w_to_find_is_plural = True
        #print(w_to_find)

        for i in range(len(processed_sent)):
            if i >= 1:
                prevword = processed_sent[i-1]
                prevwlist = prevword.split("/")
                if len(prevwlist) >= 2:
                    prevw = prevwlist[0].lower()
                    prevtag = prevwlist[1].split(" ")[0]
            if i < (len(processed_sent)-1):
                nextword = processed_sent[i+1]
                nextwlist = nextword.split("/")
                if len(nextwlist) >= 2:
                    nextw = nextwlist[0].lower()
                    nexttag = nextwlist[1].split(" ")[0]
                    #print(nexttag)
                
            word = processed_sent[i]
            wlist = word.split("/")
            #print(word)
            if len(wlist) >= 2:
                w = wlist[0].lower()
                tag = wlist[1]
                if w == w_to_find:
                    if prevtag in tags_to_find:
                        if (not w_to_find_is_plural):
                            return ([prevw], [prevtag])
                        else:
                            res_words = [prevw]
                            res_tags = [prevtag]
                            j = 2
                            prev_prevtag = prevtag
                            while (prevtag == prev_prevtag):
                                if (i - j >= 0):
                                    prev_prevw = processed_sent[i-j]
                                    prev_prevwlist = prevword.split("/")
                                    if len(prev_prevwlist) >= 2:
                                        prev_prevw = prevwlist[0].lower()
                                        prev_prevtag = prevwlist[1]
                                        res_words = [prev_prevw]+res_words
                                        res_tags = [prev_prevtag]+res_tags
                                    j+=1
                            return (res_words, res_tags)
                    
                    elif nexttag in tags_to_find:
                        #print("herenexttag")
                        if (not w_to_find_is_plural):
                            return ([nextw], [nexttag])
                        else:
                            res_words = [nextw]
                            res_tags = [nexttag]
                            j = 2
                            next_nexttag = nexttag
                            while (nexttag == next_nexttag):
                                #print("here")
                                if (i + j < len(processed_sent)):
                                    next_nextw = processed_sent[i+j]
                                    next_nextwlist = prevword.split("/")
                                    if len(next_nextwlist) >= 2:
                                        next_nextw = nextwlist[0].lower()
                                        next_nexttag = nextwlist[1]
                                        res_words = [next_nextw]+res_words
                                        res_tags = [next_nexttag]+res_tags
                                    j+=1
                            return (res_words, res_tags)

                    else:
                         return ([prevw], [prevtag])
                        #break
    
    for word in processed_sent:
        #print(word.split("/"))
        #print(word)
        wlist = word.split("/")
        if len(wlist) >= 2:
            w = wlist[0]
            tag = wlist[1]
            #print(tag)
            if tag in tags_to_find and w not in question_words:
                sentence_words.append(w)
                sentence_tag_words.append(tag)
    return (sentence_words, sentence_tag_words)
    


# In[13]:


res = find_sentence_words_by_question(get_question_word(tagged_q_sentence)[0], get_question_word(tagged_q_sentence)[1], q, txt_answer)


# In[14]:


def convertListToString(L):
    res = ""
    for i in range(len(L)):
        if i == 0:
            res = L[i]
        else:
            res += " " + L[i]
    return res
        


# In[15]:


convertListToString(res[0])

