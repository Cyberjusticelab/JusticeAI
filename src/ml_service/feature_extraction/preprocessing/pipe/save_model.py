import numpy
from src.ml_service.feature_extraction.preprocessing.pipe.precedence_parse import Precedence_Parser
from src.ml_service.global_variables.global_variable import Global
from src.ml_service.outputs.output import Save


def save(data_to_extract, nb_of_files=-1):
    """
    Gets all information from precedence and saves binary model
    :param data_to_extract: decision or facts
    :param nb_of_files: -1 reads all directory
    :return: None
    """
    parser = Precedence_Parser()
    precedence_dict = parser.parse_files(Global.Precedence_Directory, nb_of_files)

    X = []
    labels = []
    precedence_files = []

    for fact in precedence_dict[data_to_extract]:
        X.append(precedence_dict[data_to_extract][fact].dict['vector'])
        labels += ([precedence_dict[data_to_extract][fact].dict['fact']])
        precedence_files += (precedence_dict[data_to_extract][fact].dict['precedence'])

    # deallocate memory
    precedence_dict = None

    X = numpy.matrix(X)
    labels = numpy.array(labels)
    precedence_files = numpy.array(precedence_files)

    data_tuple = (X, labels, precedence_files)

    s = Save(directory=r'preprocess_model/')
    s.binarize_model(data_to_extract + '.bin', data_tuple)