# -*- coding: utf-8 -*-

import pandas as pd
import os, re, pickle
from itertools import permutations, combinations
import numpy as np
from multiprocessing import Pool
from collections import Counter


##########

def countNPs(language):

    orders = {''.join(i):{} for i in permutations(els)}
    orders.update({''.join(perm):{} for combo in combinations(els, 3) for perm in permutations(combo) if 'n' in perm})

    # for corpus in languages:

    # df = makeDf(language)
    df = pd.read_csv(language)
    print 'Loaded CSV file for {}'.format(language.split('.')[2].split('-')[0])
    nounSample = df[df.UPOSTAG=='NOUN']

    nPCount = 0

    for nounIndex in nounSample.index:
        nPCount += 1
        # if nPCount % 100 == 0:
            # print "Examined {} nouns out of a total of {}.".format(nPCount, nouns)
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
                # print sortedNP
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

    return orders

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

cheminTreebanks = '../treebanks_sandbox/'
treebankFolders = os.listdir(cheminTreebanks)
regexUD = re.compile('UD_.*')
regexCONLL = re.compile('.*ud-train\.csv')

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

print treebankFiles

def findSentence(lg, sent_id):
    sentence = df[(df.lg==sentId[:2]) & (df.sent_id==int(sentId[2:]))]
    return ' '.join(list(sentence.FORM))
        
#####

pool = Pool()
results = pool.imap(countNPs, treebankFiles)
pool.close()

out = {}
for i in results:
    out.update(i)

pickle.dump(out, open('order-frequencies.pickle', 'w+'))