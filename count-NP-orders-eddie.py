# -*- coding: utf-8 -*-

import pandas as pd
import os, re, pickle, sys
from itertools import permutations, combinations
import numpy as np


##########

def countNPs(language):

    orders = {''.join(i):{} for i in permutations(els)}
    orders.update({''.join(perm):{} for combo in combinations(els, 3) for perm in permutations(combo) if 'n' in perm})

    df = pd.read_csv(language)
    # print 'Loaded CSV file for {}'.format(language.split('.')[2].split('-')[0])
    nounSample = df[df.UPOSTAG=='NOUN'].sample(100)

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
                # print sortedNP
                order = ''.join([labels[i] for i in sortedNP])
                if order in orders.keys():
                    comboCount +=1
                    orders[order].update({lg+str(sent_id): comboCount})

    return orders

#####

# dems = {
#     'en': ['this', 'that', 'these', 'those']
# }

els = ['n', 'D', 'N', 'A']
labels = {
    'NOUN':'n',
    'ADJ':'A',
    'NUM':'N',
    'DEM':'D',
    'DET':'D'
}

deps = [
    'det',
    'nummod',
    'amod'
]

modifiers = [
    'DET',
    'NUM',
    'ADJ'
]

cheminEddie = '/exports/eddie/scratch/amarti16/'

cheminTreebanks = cheminEddie + 'treebankCSVs'
cheminTreebanks = '../treebankCSVs/'

treebankCSVs = os.listdir(cheminTreebanks)
# regexUD = re.compile('UD_.*')
regexCONLL = re.compile('.*ud-train\.csv')

treebankFiles = [f for f in treebankCSVs if regexCONLL.match(f)] 
# print treebankFiles

treebankIndex = int(sys.argv[1]) - 1 
        
        
#####

thisLgFile = treebankFiles[treebankIndex]
# print thisLgFile
lg = thisLgFile.split('-')[0]

orders = countNPs(cheminTreebanks+thisLgFile)

cheminOut = cheminEddie + 'output/{}-order-frequencies.pickle'.format(lg)
cheminOut = '../output/{}-order-frequencies.pickle'.format(lg)

pickle.dump(orders, open(cheminOut, 'w+'))