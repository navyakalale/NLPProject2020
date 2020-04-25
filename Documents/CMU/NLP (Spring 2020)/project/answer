#!/usr/bin/env python3
# coding: utf-8

import sys
import re
import nltk
#nltk.download('all-nltk')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')
from nltk import sent_tokenize, word_tokenize, pos_tag, ne_chunk
from nltk import ngrams
import numpy

def find_sentence_in_txt_by_question(text_sentences_list, question_sentence):
    question_sentence1 = question_sentence.lower()
    q_tokenize = nltk.word_tokenize(question_sentence1)
    q_onegrams = list(ngrams(q_tokenize, 1))
    q_bigrams = list(ngrams(q_tokenize, 2))
    q_trigrams = list(ngrams(q_tokenize, 3))
    q_fourgrams = list(ngrams(q_tokenize, 4))
    q_fivegrams = list(ngrams(q_tokenize, 5))
    q_sixgrams = list(ngrams(q_tokenize, 6))
    q_sevengrams = list(ngrams(q_tokenize, 7))

    # print(q_bigrams)

    best_sentence = ""
    best_num_matching = -1
    longest_matching_str = ""
    # print(text_sentences_list)
    for sentence in text_sentences_list:
        sentence1 = sentence.lower()
        txt_tokenize = nltk.word_tokenize(sentence1)
        txt_onegrams = list(ngrams(txt_tokenize, 1))
        txt_bigrams = list(ngrams(txt_tokenize, 2))
        txt_trigrams = list(ngrams(txt_tokenize, 3))
        txt_fourgrams = list(ngrams(txt_tokenize, 4))
        txt_fivegrams = list(ngrams(txt_tokenize, 5))
        txt_sixgrams = list(ngrams(txt_tokenize, 6))
        txt_sevengrams = list(ngrams(txt_tokenize, 7))

        curr_matching = 0
        curr_matching_str = ''
        sent_words = sentence.split()
        for onegram in txt_onegrams:
            if onegram in q_onegrams:
                curr_matching += .2
                curr_matching_str = onegram
        for bigram in txt_bigrams:
            if bigram in q_bigrams:
                curr_matching += 1
                curr_matching_str = bigram
        for trigram in txt_trigrams:
            if trigram in q_trigrams:
                curr_matching += 2
                curr_matching_str = trigram
        for fourgram in txt_fourgrams:
            if fourgram in q_fourgrams:
                curr_matching += 3
                curr_matching_str = fourgram
        for fivegram in txt_fivegrams:
            if fivegram in q_fivegrams:
                curr_matching += 3
                curr_matching_str = fivegram
        for sixgram in txt_sixgrams:
            if sixgram in q_sixgrams:
                curr_matching += 4
                curr_matching_str = sixgram
        for sevengram in txt_sevengrams:
            if sevengram in q_sevengrams:
                curr_matching += 5
                curr_matching_str = sevengram
        if curr_matching > best_num_matching:
            best_sentence = sentence
            best_num_matching = curr_matching
        if len(curr_matching_str) > len(longest_matching_str):
            longest_matching_str = curr_matching_str

    res_longest_matching_str = ''
    for s in longest_matching_str:
        res_longest_matching_str += " " + s

    #print(res_longest_matching_str)
    return (best_sentence, res_longest_matching_str)


def process_sentence(sentence):
    named_ent_list = []
    res = []
    question_ne_list = []
    tokenized = nltk.word_tokenize(sentence)
    tagged = nltk.pos_tag(tokenized)
    named_ent = nltk.ne_chunk(tagged, binary=True)

    # get named entities
    for chunk in named_ent:
        if hasattr(chunk, 'label'):
            question_ne_list.append((chunk.label(), ' '.join(c[0] for c in chunk)))

    # get full output
    named_ent_list += question_ne_list
    res = (str(named_ent).split("\n  "))
    new_res = []
    for i in range(len(res)):
        word = res[i]
        word = word.strip('()')

        if " " in word:
            l = word.split(" ")
            #print(l)
            for i in range(len(l)):
                if (i >= 1):
                    word = l[i]
                    #print(word)
                    if (word != '/' and word != ',/,' and word != './.'): new_res.append(word)
        else:
            if (word != '/' and word != ',/,' and word != './.'): new_res.append(word)

    #print("processed sent", (named_ent_list, new_res)[1])
    return (named_ent_list, new_res)



def get_question_word(tagged_question_sentence):
    q_tags = {'WDT', 'WP', 'WP$', 'WRB'}
    tagged_list = tagged_question_sentence[1]
    question_word = ""
    q_tag_word = ""
    for word in tagged_list:
        # print(word.split("/"))
        # print(word)
        word = word.strip('()')
        if " " in word:
            l = word.split(" ")
            word = l[1]

        wlist = word.split("/")
        if len(wlist) >= 2:
            w = wlist[0]
            tag = wlist[1]

        wlist = word.split("/")
        if len(wlist) >= 2:
            w = wlist[0]
            tag = wlist[1]
            if tag in q_tags:
                question_word = w
                q_tag_word = tag
    #print("question word", question_word, q_tag_word)
    return (question_word.lower(), q_tag_word)



def find_sentence_words_by_question(question_word, question_tag, question, sentence_txt, longest_phrase):
    qword_dict = {'who': ['NNP', 'NNS'], 'which': ['JJ', 'NNP', 'NNS'], 'what': ['NNP', 'NNS'],
                  'when': ['NNP','CD'], 'where': ['NNP'], 'how': ['CD'],
                  'why': ['IN'], '':['NNP']}

    if (len(question) == 0 or len(question_word) == 0): return (['idk'], ['CD'])
    qlower = question.lower()
    #print(qlower)
    #print(question_word)
    if "?" in qlower: question_words = qlower.split("?")[0].split()
    else: question_words = qlower.split()

    #remove commas
    for i in range(len(question_words)):
        word = question_words[i]
        if "," in word:
            l = word.split(",")
            word = l[0]
            question_words[i] = word

    tags_to_find = qword_dict.get(question_word, '')
    processed_sent = process_sentence(sentence_txt)[1]
    sentence_words = []
    sentence_tag_words = []

    prevw, prevtag  = ",", ","
    nextw, nexttag = ",", ", "
    next_nextw, next_nexttag = ",", ","
    next3_w, next3_tag = ",", ","

    for i in range(len(processed_sent)):
        #get prev and next word
        if i >= 1:
            prevword = processed_sent[i - 1]
            prevwlist = prevword.split("/")
            if len(prevwlist) >= 2:
                prevw = prevwlist[0]
                prevtag = prevwlist[1].split(" ")[0]

        if i < (len(processed_sent) - 1):
            nextword = processed_sent[i + 1]
            nextwlist = nextword.split("/")
            if len(nextwlist) >= 2:
                nextw = nextwlist[0]
                nexttag = nextwlist[1].split(" ")[0]

        if i < (len(processed_sent) - 2):
            next_nextword = processed_sent[i + 2]
            next_nextwlist = next_nextword.split("/")
            if len(next_nextwlist) >= 2:
                next_nextw = next_nextwlist[0]
                next_nexttag = next_nextwlist[1].split(" ")[0]

        if i < (len(processed_sent) - 3):
            next3_word = processed_sent[i + 3]
            next3_wlist = next3_word.split("/")
            if len(next3_wlist) >= 2:
                next3_w = next3_wlist[0]
                next3_tag = next3_wlist[1].split(" ")[0]

        if question_word.lower() == 'which':
            w_to_find = ''
            #print(question_words)
            if question_word.lower() in question_words:
                idx = question_words.index(question_word.lower())
                if (idx < len(question_words) - 1):
                    w_to_find_idx = idx + 1
                    w_to_find = question_words[w_to_find_idx]

            w_to_find_is_plural = False
            if w_to_find[-1] == 's':
                # print("isplural")
                w_to_find_is_plural = True
            # print(w_to_find)

            word = processed_sent[i]
            wlist = word.split("/")
            # print(word)
            if len(wlist) >= 2:
                w = wlist[0].lower()
                tag = wlist[1]
                if w == w_to_find:
                    if prevtag in tags_to_find:
                        if (not w_to_find_is_plural):
                            return ([prevw], [prevtag])
                        else:
                            for word in processed_sent[:i]:
                                wlist = word.split("/")
                                if len(wlist) >= 2:
                                    w = wlist[0]
                                    tag = wlist[1]
                                    # print(tag)
                                    if tag == 'NNP' and w.lower() not in question_words:
                                        sentence_words.append(w)
                                        sentence_tag_words.append(tag)
                            # print("sentence words", sentence_words, sentence_tag_words)
                            return (sentence_words, sentence_tag_words)

                    elif nexttag in tags_to_find or nexttag == 'DT':
                        if (not w_to_find_is_plural):
                            return ([nextw], [nexttag])
                        else:
                            sent_portion = processed_sent[i:]
                            if len(sent_portion) >= 5: sent_portion = processed_sent[i:i+5]
                            for word in sent_portion:
                                wlist = word.split("/")
                                if len(wlist) >= 2:
                                    w = wlist[0]
                                    tag = wlist[1]
                                    # print(tag)
                                    if tag == 'NNP' and w.lower() not in question_words:
                                        sentence_words.append(w)
                                        sentence_tag_words.append(tag)
                            # print("sentence words", sentence_words, sentence_tag_words)
                            return (sentence_words, sentence_tag_words)


        if question_word.lower() == 'who':
            if question_word.lower() in question_words:
                idx = question_words.index(question_word.lower())
                if (idx < len(question_words) - 1):
                    w_to_find_idx = idx + 1
                    w_to_find = question_words[w_to_find_idx]
                    #print(w_to_find)
                    #print(processed_sent[i])
                    wlist = processed_sent[i].split("/")
                    if len(wlist) >= 2:
                        w = wlist[0]
                        tag = wlist[1]
                        if w.lower() == w_to_find:
                            if (nexttag in tags_to_find):
                                return ([nextw], [nexttag])
                            elif prevtag in tags_to_find:
                                return ([prevw], [prevtag])
                            else: continue

        if question_word.lower() == 'what':
            w_to_find = ''
            if question_word.lower() in question_words:
                idx = question_words.index(question_word.lower())
                if (idx < len(question_words)-1):
                    w_to_find_idx = idx + 1
                    w_to_find = question_words[w_to_find_idx]

                    # print(processed_sent[i])
                    wlist = processed_sent[i].split("/")
                    if len(wlist) >= 2:
                        w = wlist[0]
                        tag = wlist[1]
                        if w.lower() == w_to_find:
                            if (nexttag in tags_to_find and nextword not in question_words):
                                return ([nextw], [nexttag])
                            elif prevtag in tags_to_find and prevw not in question_words:
                                return ([prevw], [prevtag])
                            else:
                                continue

        if question_word.lower() == 'when' or question_word.lower() == 'where':
            wlist = processed_sent[i].split("/")
            if len(wlist) >= 2:
                w = wlist[0]
                tag = wlist[1]
                if tag in tags_to_find and prevtag == 'IN' and w.lower() not in question_words:
                    if nexttag in tags_to_find and nextw.lower() not in question_words:
                        if next_nexttag in tags_to_find and next_nextw.lower() not in question_words:
                            return ([w, nextw, ",", next_nextw], [tag, nexttag, ",", next_nexttag])
                        else: return ([w, nextw], [tag, nexttag])
                    else: return ([w], [tag])

        if question_word.lower() == 'why':
            wlist = processed_sent[i].split("/")
            if len(wlist) >= 2:
                w = wlist[0]
                tag = wlist[1]
                if (w == 'because' or w == 'since' or w == 'for'):
                        return ([w, nextw, next_nextw, next3_w], [tag, nexttag, next_nexttag, next3_tag])


    sentence_words = []
    sentence_tag_words = []

    for i in range(len(processed_sent)):
        word = processed_sent[i]
        word = word.strip('()')
        if " " in word:
            l = word.split(" ")
            word = l[1]
        wlist = word.split("/")
        if len(wlist) >= 2:
            w = wlist[0]
            tag = wlist[1]
            #print(longest_phrase)
            if (tag in tags_to_find) and (w.lower() not in question_words) and (w not in sentence_words):
                sentence_words.append(w)
                sentence_tag_words.append(tag)

    #print("sentence words", sentence_words, sentence_tag_words)
    if len(sentence_words) <= 6 and len(sentence_words) > 0: return (sentence_words, sentence_tag_words)
    elif len(sentence_words) > 6: return (sentence_txt.split(), [])
    else: return (['idk'], ['CD'])

def convertListToString(L):
    res = ""
    for i in range(len(L)):
        if i == 0:
            res = L[i]
        else:
            if L[i] == ",":
                res += L[i]
            else: res += " " + L[i]
    return res



if __name__ == "__main__":
    # Files
    DATA_FILE = sys.argv[1]
    QUESTION_FILE = sys.argv[2]

    data = open(DATA_FILE, "r")
    questions = open(QUESTION_FILE, "r")

    sample_txt = data.read()
    sample_txt_sentences = nltk.sent_tokenize(sample_txt)

    questions_txt = questions.read()
    questions_txt_sentences = nltk.sent_tokenize(questions_txt)

    for i in range(len(questions_txt_sentences)):
        q = questions_txt_sentences[i]


        tagged_q_sentence = process_sentence(q)
        qword = get_question_word(tagged_q_sentence)[0]
        qtag = get_question_word(tagged_q_sentence)[1]

        txt_answer = find_sentence_in_txt_by_question(sample_txt_sentences, q)[0]
        longest_phrase = find_sentence_in_txt_by_question(sample_txt_sentences, q)[1]

        res = find_sentence_words_by_question(qword,
                                              qtag,
                                              q, txt_answer, longest_phrase)

        res_str = (convertListToString(res[0]))

        #print(res_str)
        if res_str != "": print(res_str)
        else: print("idk")

