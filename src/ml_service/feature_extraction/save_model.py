import numpy

from feature_extraction.pre_processing.pre_processing import PreProcessor
from util.file import Save
from util.constant import Global


def __get_tuple(precedent_dict, data_to_extract):
    """
    Creates a tuple from the dictionary values
    :param precedent_dict: dict['facts'/'decisions'] : dict['vectors']['sentence']['filenames']
    :param data_to_extract: String
    :return:tupple(vectors, sentence, filenames)
    """

    X = []
    labels = []
    precedence_files = []

    for fact in precedent_dict[data_to_extract]:
        X.append(precedent_dict[data_to_extract][fact].dict['vector'])
        labels += ([precedent_dict[data_to_extract][fact].dict['fact']])
        precedence_files.append(precedent_dict[data_to_extract][fact].dict['precedence'])

    X = numpy.matrix(X)
    labels = numpy.array(labels)
    precedence_files = numpy.array(precedence_files)

    return X, labels, precedence_files


def save(filename=None, nb_of_files=-1):
    """
    Gets all information from precedence and saves binary model
    :param data_to_extract: decision or facts
    :param nb_of_files: -1 reads all directory
    :return: None
    """

    parser = PreProcessor()
    precedent_dict = parser.parse_files(Global.precedent_directory, nb_of_files)
    fact_model = __get_tuple(precedent_dict, 'facts')
    decision_model = __get_tuple(precedent_dict, 'decisions')

    # deallocate memory
    precedent_dict = None

    s = Save(directory=r'preprocess_model/')
    if filename is None:
        s.binarize_model('processed_facts.bin', fact_model)
        s.binarize_model('processed_decisions.bin', decision_model)
    else:
        # this only exists to allow unittests
        s.binarize_model(filename + '.bin', fact_model)