from src.ml_service.feature_extraction.preprocessing.Sam_Parser.PrecedenceParse import Precedence_Parser
from src.ml_service.global_variables.global_variable import Global
from src.ml_service.word_vectors.FrenchVectors import FrenchVectors
import joblib
import os
import numpy

if __name__ == '__main__':
    parser = Precedence_Parser()
    precedence_dict = parser.parse_files(Global.Precedence_Directory, 10)
    # deallocate memory
    FrenchVectors.word_vectors = None
    data_to_extract = 'decisions'

    X = []
    labels = []
    precedence_files = []
    piped_fact = []

    for fact in precedence_dict[data_to_extract]:
        X.append(precedence_dict[data_to_extract][fact].dict['vector'])
        labels += ([precedence_dict[data_to_extract][fact].dict['fact']])
        precedence_files += (precedence_dict[data_to_extract][fact].dict['precedence'])
        piped_fact += ([precedence_dict[data_to_extract][fact].dict['piped_fact']])

    X = numpy.matrix(X)
    labels = numpy.array(labels)
    precedence_files = numpy.array(precedence_files)
    piped_fact = numpy.array(piped_fact)

    # deallocate memory
    precedence_dict = None

    data_tuple = (X, labels, precedence_files, piped_fact)

    print('Saving binary')
    __script_dir = os.path.abspath(__file__ + r"/../../../")
    __rel_path = r'ml_models/processed_decisions.bin'
    model_path = os.path.join(__script_dir, __rel_path)
    joblib.dump(data_tuple, model_path)
