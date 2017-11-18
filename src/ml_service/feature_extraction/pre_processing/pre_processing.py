import numpy

from feature_extraction.pre_processing.pre_processor import PreProcessor
from util.file import Save
from util.constant import Path


def __get_tuple(precedent_dict, data_to_extract):
    """
    Creates a tuple from the dictionary values
    :param precedent_dict: dict['facts'/'decisions'] : dict['vectors']['sentence']['filenames']
    :param data_to_extract: String
    :return:tupple(vectors, sentence, filenames)
    """
    X = []
    labels = []
    precedent_files = []

    for sentence in precedent_dict[data_to_extract]:
        X.append(precedent_dict[data_to_extract][sentence].dict['vector'])
        labels += ([precedent_dict[data_to_extract][sentence].dict['sentence']])
        precedent_files.append(precedent_dict[data_to_extract][sentence].dict['precedent'])

    X = numpy.matrix(X)
    labels = numpy.array(labels)
    precedent_files = numpy.array(precedent_files)

    return X, labels, precedent_files

def save(filename=None, nb_of_files=-1):
    """
    Gets all information from precedent and saves binary model
    :param data_to_extract: decision or facts
    :param nb_of_files: -1 reads all directory
    :return: None
    """
    parser = PreProcessor()
    precedent_dict = parser.parse_files(Path.raw_data_directory, nb_of_files)
    fact = __get_tuple(precedent_dict, 'facts')
    decision = __get_tuple(precedent_dict, 'decisions')

    # deallocate memory
    precedent_dict = None

    s = Save(directory=r'pre_processing')
    if filename is None:
        s.save_binary('pre_processed_facts.bin', fact)
        s.save_binary('pre_processed_decisions.bin', decision)
    else:
        # this only exists to allow unittests
        s.save_binary(filename + '.bin', fact)