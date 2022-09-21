import spacy
import pandas as pd
from nltk.stem import WordNetLemmatizer
import string

wnl = WordNetLemmatizer()

def get_lemma(text):
    splitted_text = text.split()
    lemmas = []
    for token in splitted_text:
        lemmas.append(wnl.lemmatize(token).lower())
    return lemmas

def remove_unicode(text):
    text = text.strip()
    text = text.translate(str.maketrans('', '', string.punctuation))
    strencode = text.encode("ascii", "ignore")
    return strencode.decode()

def get_rationale(lemma):
    rationale = []
    for elem in lemma:
        if elem in lexicon_list:
            rationale.append(0)
        else:
            rationale.append(1)
    return rationale

def remove_spesh_chars(token, splitted_text, rationale):
    while token in splitted_text:
        index = splitted_text.index(token)
        del splitted_text[index]
        if len(rationale)!=0:    
            del rationale[index]
    return splitted_text, rationale


# Set path here which contains the lexixon and the train,dev,test splits

PATH = "data/stf/stf_raw/"

lexicon = pd.read_csv(PATH+'lexicon.csv', header=None)
lexicon['lemma'] = lexicon[0].apply(lambda x: get_lemma(x)[0])
lexicon_list = lexicon['lemma'].values

splits = ['train','dev','test']
df_list = {}
for split in splits:
    dfx = pd.read_csv(PATH+split+".tsv", sep='\t')
    dfx['text'] = dfx['text'].apply(remove_unicode)
    dfx['lemma'] = dfx['text'].apply(get_lemma)
    dfx['rationale'] = dfx['lemma'].apply(get_rationale)
    
    count = 0
    for idx, row in dfx.iterrows():
        r = row['rationale']
        if 0 in r:
            count +=1
    print(split, count)
    print(dfx['is_hate'].value_counts())
    
    df_list[split] = dfx
    if split == 'dev':
        split = 'val'
    dfx[['text','rationale','is_hate']].reset_index(drop=True).to_json(PATH+"processed_"+split+".json", orient='records', lines=True)
    