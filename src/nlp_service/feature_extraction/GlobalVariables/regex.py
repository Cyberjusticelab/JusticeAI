import re


class Regex:
    phrase_match = re.compile('ADJP|PP|ADVP|NP|S|SQ|SBARQ|VP')
    noun_match = re.compile('NN|PRP|CD')
    noun_phrase_match = re.compile('NP')
    verb_match = re.compile('VB|TO|IN')
    w_word_match = re.compile('WRB')
    verb_phrase_match = re.compile('VP|WHADVP')
    adjective_match = re.compile('JJ|\$')
    determiner_match = re.compile('DT|EX')
    adjective_phrase_match = re.compile('ADJP')
    prepositoinal_phrase_match = re.compile('PP')
    conjunction_match = re.compile('CC')
    adverb_match = re.compile('RB')
    adverb_phrase_match = re.compile('ADVP')
    rp_match = re.compile('RP')
    key_word_match = re.compile('RP|NN|PRP|JJ|\$|CD')
    relevant_word_match = re.compile('NN|JJ')
