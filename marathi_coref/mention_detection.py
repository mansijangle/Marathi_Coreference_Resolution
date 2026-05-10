import stanza

nlp = stanza.Pipeline(
    'mr',
    processors='tokenize,mwt,pos,lemma,depparse,ner'
)

def extract_mentions(sentence):

    doc = nlp(sentence)

    mentions = []

    for sent in doc.sentences:

        for word in sent.words:

            mentions.append(word.text)

    return mentions