from model_training.svm.svm import LinearSVM
from model_training.similar_finder.similar_finder import SimilarFinder
from util.file import Load
from util.log import Log


def __dictionary_to_list():
    """
    TODO: Refactor regex_tagger to this format

    Converts the binarize structured_data_dict to a list format

    structured_data_dict:{
        filename:{
            name: 'AZ-XXXXXXX.txt',
            demands_vector: [...],
            facts_vector: [...],
            outcomes_vector: [...]
        }
    }

    :return: data_list: [{
        name: 'AZ-XXXXXXX.txt',
        demands_vector: [...],
        facts_vector: [...],
        outcomes_vector: [...]
    },
    {
        ...
    }]
    """
    structured_data_dict = Load.load_binary("structured_data_dict.bin")
    Log.write("Formatting data")
    data_list = []
    for precedent_file in structured_data_dict:
        data_list.append(structured_data_dict[precedent_file])
    return data_list


def run(command_list):
    """
    1) Converts dictionary a precedent vectors to a list of dictionaries
    2) Train the support vector machine model
    3) train the similarity finder model

    :param command_list: List of command line arguments. Not used yet since there is only 1 training technique
    :return: None
    """
    Log.write("Executing train model.")

    # Taking a subset since I don't want to wait forever
    precedent_vector = __dictionary_to_list()
    linear_svm = LinearSVM(precedent_vector)
    linear_svm.train()
    SimilarFinder(train=True, dataset=precedent_vector)
