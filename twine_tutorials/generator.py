#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed May 24 11:26:36 2017

@author: james
"""

from re import compile
from nltk import word_tokenize, pos_tag

regexp = compile(r'\(.*\)')

CMUDICT = {}

def read_dict():
    with open('sphinx4-data/src/main/resources/edu/cmu/sphinx/models/en-us/cmudict-en-us.dict',
              'r') as f:
        for line in f.readlines():
            dictline = line.strip().split()
            pronunciation = ' '.join(dictline[1:]).lower()
            if '(' in dictline[0]:
                headword = regexp.sub('', dictline[0], 1).lower()
            else:
                headword = dictline[0].lower()
            if headword in CMUDICT:
                CMUDICT[headword].append(pronunciation)
            else:
                CMUDICT[headword] = [pronunciation]


read_dict()

#print CMUDICT['the']

punct = compile(r'[,.?!]')

with open('AROWF-npov.txt', 'r') as f:
    done = {}
    num_lines = 1
    for line in f.readlines():
        if line[0]!='[':
            continue
        length = len(line)
        ccline = ''
        for i in range (length):
            #check = isalpha(line[i])
            if (line[i] == '.'):
                break
            if ((line[i].isalpha()) or (line[i].isspace())):
                ccline+=line[i]


        words = punct.sub('', ccline.strip().lower()).split()
        f = open('Prompts/Line'+str(num_lines)+'.txt','a' )
        #print(words)
        num_lines = num_lines + 1
        f.write(ccline+'\n')

        for word in words:
            n_tag = ""
            try:
                tag = (pos_tag(word_tokenize(word)))
                tag= tag[0][1]
                if tag[:2] == "CC":
                    n_tag = "c" #conjunction
                elif tag[:2] == "DT":
                    n_tag = "a" #article
                elif tag[:2] == "IN" or tag[:2] == "TO":
                    n_tag = "p" #preposition
                elif tag[:2] == "NN":
                    n_tag = "n" #noun
                elif tag[:2] == "VB" or tag[:2] == "MD" or tag[:2]=="RP":
                    n_tag = "v" #verb
                elif tag[:2] == "FW":
                    n_tag = "x" #negative
                elif tag[:2] == "RB" or tag[:2] == "WRB":
                    n_tag = "w" #adverb
                elif tag[:2] == "JJ":
                    n_tag = "m"
                elif tag[:2] == "PR" or tag[:3] == "WDT" or tag[:2] == "WP" or tag[:3] == "WP$":
                    n_tag = "o" #pronoun
                elif tag[:3] == "POS":
                    n_tag = "s" #possessive
                elif tag[:2] == "CD":
                    n_tag = "q"  #quantifier
                else:
                    print(tag + " " + word)
                prons = CMUDICT[word]
                # print(prons)
                # print(word)
                for pron in prons:
                    f.write(word+" "+str(n_tag)+" "+pron+'\n')
                #done[word] = True ### bad idea: context matters

            except:
                print ( word + '" out of vocabulary\n')
        f.close()
