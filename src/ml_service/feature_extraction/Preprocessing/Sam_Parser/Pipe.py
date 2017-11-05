from pattern3.fr import singularize, conjugate, parsetree, tag, predicative
from nltk.tokenize import word_tokenize
from nltk.tokenize.moses import MosesDetokenizer
import re


class PipeSent():
    filter_match = re.compile('NN|PRP|VB')

    def __init__(self):
        pass

    def pipe(self, sent):
        sentence_list = []
        sent = self.filter_words(sent)
        tagged_sent = parsetree(sent, relations=True)
        self.sub_sent(tagged_sent, sentence_list)
        return sentence_list

    def filter_words(self, sent):
        word_list = tag(sent)
        new_string = ""
        for word in word_list:
            if self.filter_match.match(word[1]):
                new_string += word[0] + " "
        word_list = word_tokenize(new_string, language='french')
        detokenizer = MosesDetokenizer()
        return detokenizer.detokenize(word_list, return_str=True)

    def sub_sent(self, tagged_sent, sentence_list):
        for sentence in tagged_sent:
            dict = {}
            for relation in (sentence.relations['SBJ']):
                for words in sentence.relations['SBJ'][relation]:
                    try:
                        dict[relation] += " " + self.format_noun(words.string)
                    except KeyError:
                        dict[relation] = self.format_noun(words.string)

            for relation in (sentence.relations['VP']):
                for words in sentence.relations['VP'][relation]:
                    try:
                        dict[relation] += " " + self.format_verb(words.string)
                    except KeyError:
                        dict[relation] = self.format_verb(words.string)

            for relation in (sentence.relations['OBJ']):
                for words in sentence.relations['OBJ'][relation]:
                    try:
                        dict[relation] += " " + self.format_noun(words.string)
                    except KeyError:
                        dict[relation] = self.format_noun(words.string)

            for sent in dict:
                sentence_list.append(dict[sent])

    def format_noun(self, word):
        return singularize(word)


    def format_verb(self, word):
        return conjugate(word)

if __name__ == '__main__':
    p = PipeSent()
    sentence = '''Le locateur déclare que les locataires ont quitté le logement en date.'''
    lst = p.pipe(sentence)
    print(lst)