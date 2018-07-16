# -*- coding: utf-8 -*-

import os, re

pickleFiles = os.listdir('../output/')
m = re.compile('.*\.pickle')

pickles = [pickle.load(open(f, 'r+')) for f in pickleFiles if m.match(f)]

orders = [
    'ANDn',
    'NAn',
    'DAn',
    'nAND',
    'DAnN',
    'AnDN',
    'NDAn',
    'DNAn',
    'NnAD',
    'NnDA',
    'AnND',
    'DnA',
    'NADn',
    'nAD',
    'DnN',
    'nAN',
    'nNDA',
    'ADNn',
    'DnNA',
    'AnD',
    'nDAN',
    'AnN',
    'NnD',
    'nND',
    'NAnD',
    'DANn',
    'nNA',
    'ANn',
    'ANnD',
    'NnA',
    'nNAD',
    'nADN',
    'nDN',
    'nDA',
    'nDNA',
    'NDn',
    'NDnA',
    'ADn',
    'DNn',
    'ADnN',
    'DNnA',
    'DnAN'
]

out = {k:{} for k in orders}

out = {out[k].update(v) for dico in pickles for k,v in dico.items()}

for p in pickles:
    for k,v in p.items():
        out[k].update(v)

