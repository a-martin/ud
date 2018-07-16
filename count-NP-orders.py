# -*- coding: utf-8 -*-

import pandas as pd
import os, re
from itertools import permutations, combinations
import numpy as np
from multiprocessing import Pool

vs_file = 'very_small_en.txt'
s_file = 'small_en.txt'
en_file = 'en_ewt-ud-train.conllu'

cheminTreebanks = '../treebanks_sandbox/'
treebankFolders = os.listdir(cheminTreebanks)
regexUD = re.compile('UD_.*')
regexCONLL = re.compile('.*ud-train\.conllu')

treebankFiles = []

for dirname in treebankFolders:
    if regexUD.match(dirname):
        localFiles = os.listdir(cheminTreebanks+dirname)
        for f in localFiles:
            if regexCONLL.match(f):
                treebankFiles.append(cheminTreebanks+dirname+'/'+f)
            else:
                continue
    else:
        continue

# print treebankFiles


ID,FORM,LEMMA,UPOS,XPOS,FEATS,HEAD,DEPREL,DEPS,MISC=range(10)

def read_conll(filename):
    """
        returns list of sentences
        sentence = list of tokens
        token = list of fields

        ex: sentences[0][0][FORM] is the word form of the first token of the first sentence
    """
    with open(filename) as f :
        sentences = [[line.split("\t") for line in sen.split("\n") if line and line[0] != "#"] for sen in f.read().split("\n\n") if sen.strip()]

    for i in range(len(sentences)):
        # la ligne suivante retire les amalgames
        #sentences[i] = [t for t in sentences[i] if "-" not in t[ID]]
        s = sentences[i]
        # for tok in s:
            # tok[ID] = int(tok[ID])
            # tok[HEAD] = int(tok[HEAD])
    return sentences

def makeDf(file):
    sentences = read_conll(file)

    
    for n,i in enumerate(sentences):
        for j in range(len(i)):
            sentences[n][j] += [n]

    ss = []
    for s in sentences:
        ss += s


    cols = [
        'ID',
        'FORM',
        'LEMMA',
        'UPOSTAG',
        'XPOSTAG',
        'FEATS',
        'HEAD',
        'DEPREL',
        'DEPS',
        'MISC',
        'sent_id'
    ]
    df = pd.DataFrame(ss, columns=cols)
    df['lg'] = file.split('-')[0].split('/')[-1]

    return df

dfs = [makeDf(i) for i in treebankFiles]

df = pd.concat(dfs, ignore_index=True)

# df = makeDf(s_file)

# df['sent_uni'] = df.index.map(lambda x: df.loc[x].lg + str(df.loc[x].sent_id))


def findSentence(sentId):
    sentence = df[(df.lg==sentId[:2]) & (df.sent_id==int(sentId[2:]))]
    return ' '.join(list(sentence.FORM))

#####

dems = {
    'en': ['this', 'that', 'these', 'those']
}

els = ['n', 'D', 'N', 'A']
labels = {
    'NOUN':'n',
    'ADJ':'A',
    'NUM':'N',
    'DEM':'D',
    'DET':'D'
}

orders = {''.join(i):{} for i in permutations(els)}
orders.update({''.join(perm):{} for combo in combinations(els, 3) for perm in permutations(combo) if 'n' in perm})


deps = [
    # 'det',
    'nummod',
    'amod'
]

modifiers = [
    'DET',
    'NUM',
    'ADJ'
]

#####




# first find nouns

nouns = len(df[df.UPOSTAG=='NOUN'])
nPCount = 0

print "There are {} noun phrases to examine.".format(nouns)

nounSample = df[df.UPOSTAG=='NOUN'].sample(10000)


for nounIndex in nounSample.index:
    nPCount += 1
    if nPCount % 100 == 0:
        print "Examined {} nouns out of a total of {}.".format(nPCount, nouns)
    nounId = df.loc[nounIndex].ID
    sent_id = df.loc[nounIndex].sent_id
    lg = df.loc[nounIndex].lg
    sentence = df[(df.sent_id==sent_id) & (df.lg==lg)]
    
    nP = []
    for index, row in sentence.iterrows():
        if row.HEAD == nounId and row.DEPREL in deps and row.UPOSTAG in labels.keys():
            # print row
            nP.append(index)

    if len(nP) > 1:
        comboCount = 0
        for combo2 in combinations(nP, 2):
            sortedNP = list(df.loc[np.sort(list(combo2) + [nounIndex])].UPOSTAG)
            print sortedNP
            order = ''.join([labels[i] for i in sortedNP])
            if order in orders.keys():
                comboCount +=1
                orders[order].update({lg+str(sent_id): comboCount})
        comboCount = 0
        for combo3 in combinations(nP, 3):
            sortedNP = list(df.loc[np.sort(list(combo3) + [nounIndex])].UPOSTAG)
            print sortedNP
            order = ''.join([labels[i] for i in sortedNP])
            if order in orders.keys():
                comboCount +=1
                orders[order].update({lg+str(sent_id): comboCount})




# pool = Pool()
# results = pool.map(func, list)
# pool.close()
        
