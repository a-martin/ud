# -*- coding: utf-8 -*-

import pandas as pd
import os, re


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
    return sentences

def makeDf(fileName):
    sentences = read_conll(fileName)

    
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
    df['lg'] = fileName.split('-')[0].split('/')[-1]

    return df


cheminTreebanks = '../treebanks/'
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
        
for tb in treebankFiles:
    df = makeDf(tb)
    csvName = '..' + tb.split('.')[2] + '.csv'
    print csvName
    df.to_csv(csvName, index=None)



