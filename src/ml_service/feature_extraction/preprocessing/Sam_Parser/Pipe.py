from pattern3.fr import singularize, conjugate, parsetree, tag, predicative
from nltk.tokenize import word_tokenize
from nltk.tokenize.moses import MosesDetokenizer
import re


class PipeSent():
    filter_match = re.compile('NN|VB')

    def __init__(self):
        pass

    '''
    ------------------------------------------------------
    PIPE
    ------------------------------------------------------
    Main method for splitting sentence
    sent <string>: full sentence
    return <list, list>: sub sentences, full sentences
    '''

    def pipe(self, sent):
        s = self.filter_words(sent)
        sub_sent = parsetree(s, relations=True)
        return self.sub_sent(sub_sent, sent)

    '''
    ------------------------------------------------------
    FILTER WORDS
    ------------------------------------------------------
    Remove unecessary words from a sentence
    sent <string>: full sentence
    return <string>: sentence without useful words
    '''

    def filter_words(self, sent):
        word_list = tag(sent)
        new_string = ""
        for word in word_list:
            if self.filter_match.match(word[1]):
                new_string += word[0] + " "
            elif '$' in word[0]:
                new_string += 'argent '
        word_list = word_tokenize(new_string, language='french')
        detokenizer = MosesDetokenizer()
        return detokenizer.detokenize(word_list, return_str=True)

    '''
    ------------------------------------------------------
    SUB SENT
    ------------------------------------------------------
    Creates sub sentence from full sentence
    tagged_sent<pattern.parsetree>
    s<string>: original sentence

    returns: sub sentence list, original sentence list
    '''

    def sub_sent(self, tagged_sent, s):
        original_sent = []
        sentence_list = []
        for sentence in tagged_sent:
            dict = {}
            for relation in (sentence.relations['SBJ']):
                for words in sentence.relations['SBJ'][relation]:
                    try:
                        dict[relation] += " " + words.string
                    except KeyError:
                        dict[relation] = words.string

            for relation in (sentence.relations['VP']):
                for words in sentence.relations['VP'][relation]:
                    try:
                        dict[relation] += " " + words.string
                    except KeyError:
                        dict[relation] = words.string

            for relation in (sentence.relations['OBJ']):
                for words in sentence.relations['OBJ'][relation]:
                    try:
                        dict[relation] += " " + words.string
                    except KeyError:
                        dict[relation] = words.string

            for sent in dict:
                sentence_list.append(dict[sent])
                original_sent.append(s)
            return sentence_list, original_sent


if __name__ == '__main__':
    from src.ml_service.feature_extraction.preprocessing.Sam_Parser.PrecedenceParse import Precedence_Parser
    from src.ml_service.global_variables.global_variable import Global
    p = PipeSent()
    parser = Precedence_Parser()
    tpl = parser.parse_files(Global.Precedence_Directory, 50)
    original_sent = tpl[2]
    file = open('sub.txt', 'a')
    for s in original_sent:
        lst = p.pipe(s)
        for l in lst[0]:
            file.write("SUB SENTENCES: \n")
            file.write(l + '\n\n')
        file.write("ORIGINAL SENTENCE: \n")
        file.write(s + '\n\n')
        file.write("------------------------------------------\n\n")
