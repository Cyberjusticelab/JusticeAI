from bllipparser import RerankingParser
from bllipparser.ModelFetcher import download_and_install_model
import nltk
import re

class Pipeline():
    sentence_match = re.compile('S|SQ|SBARQ')
    adj_phrase_match = re.compile('ADJP')
    prepositional_phrase_match = re.compile('PP')
    adverb_phrase_match = re.compile('ADVP')
    verb_phrase_match = re.compile('VB')
    phrase_match = re.compile('ADJP|PP|ADVP|NP')
    conjunction_match = re.compile('CC')
    verb_match = re.compile('VB')
    ignore_words = re.compile('POS')


    def __init__(self):
        model_dir = download_and_install_model('WSJ', '/tmp/models')
        # Loading the model is slow, but only needs to be done once
        self.__rpp = RerankingParser.from_unified_model_dir(model_dir)
        self.sentence = []
        self.raw_sentence = []

    def pipe(self, sentence):
        self.sentence.clear()
        self.raw_sentence.clear()
        nbest_list = self.__rpp.parse(sentence)
        nbest_list = nbest_list.fuse()
        tree = nbest_list.as_nltk_tree()
        self.__traverse_tree(tree)
        return self.sentence.copy()

    def tokenized_sent(self):
        return self.sentence

    def get_raw_sent(self):
        return self.raw_sentence

    def string_format(self):
        final_str = ''
        for word_phrase in self.sentence:
            final_str += (str(word_phrase[1]) + ' --> ')
        print(final_str)

    def __traverse_tree(self, tree):
        for subtree in tree:
            if type(subtree) == nltk.tree.Tree:
                label = subtree.label()

                if self.phrase_match.match(label):
                    if len(subtree.leaves()) > 0:
                        self.raw_sentence.append(subtree.leaves())

                    words = self.__label_leaves(subtree)
                    if len(words) == 0:
                        pass
                    else:
                        self.sentence.append([label, words])

                elif self.verb_phrase_match.match(label):
                    words = ([(label, subtree.leaves()[0])])
                    self.raw_sentence.append(subtree.leaves())
                    self.sentence.append([label, words])

                elif self.conjunction_match.match(label):
                    words = subtree.leaves()
                    self.raw_sentence.append(subtree.leaves())
                    self.sentence.append([label, words])

                self.__traverse_tree(subtree)

    def remove_punctuation(self, sentence):
        to_remove = ".?!\"\'"
        table = {ord(char): None for char in to_remove}

        for words in sentence:
            words.translate(table)

    def __label_leaves(self, subtree):
        lst = []
        for s in subtree:
            if self.prepositional_phrase_match.match(s.label()):
                continue
            elif self.ignore_words.match(s.label()):
                continue

            elif type(s[0]) == nltk.tree.Tree:
                tmp_lst = self.__label_leaves(s)
                for t in tmp_lst:
                    lst.append(t)
            else:
                lst.append((s.label(), s[0]))
            try:
                s.clear()
            except:
                pass
        return lst

if __name__ == '__main__':
    pipe = Pipeline()

    pipe.pipe("The handball team played badly last Saturday.")
    pipe.string_format()

    print(pipe.tokenized_sent())

    pipe.pipe(" It was an extremely bad match.")
    print(pipe.tokenized_sent())

    pipe.pipe(" The handball team played extremely badly last Wednesday.")
    print(pipe.tokenized_sent())

    pipe.pipe("There are quite a lot of people here.")
    print(pipe.tokenized_sent())

    pipe.pipe("Unfortunately, the flight to Dallas had been cancelled.")
    print(pipe.tokenized_sent())
