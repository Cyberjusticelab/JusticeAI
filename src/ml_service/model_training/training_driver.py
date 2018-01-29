from model_training.classifier.multi_class_svm import MultiClassSVM
from model_training.regression.tenant_pays_landlord_regressor import TenantPaysLandlordRegressor
from model_training.similar_finder.similar_finder import SimilarFinder
from util.file import Load
from util.log import Log


def __dictionary_to_list():
    """

    Converts the binarize structured_data_dict to a list format

    precedent_vectors:{
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
    precedent_vector = Load.load_binary("precedent_vectors.bin")
    if precedent_vector is None:
        return []
    Log.write("Formatting data")
    data_list = []
    for precedent_file in precedent_vector:
        data_list.append(precedent_vector[precedent_file])
    return data_list


class CommandEnum:
    SVM = "--svm"
    SIMILARITY_FINDER = "--sf"
    SVR = "--svr"
    EVALUATE = "--evaluate"
    WEIGHTS = '--weights'
    command_list = [SVM, SIMILARITY_FINDER, SVR, EVALUATE, WEIGHTS]


def run(command_list):
    """
    1) Converts dictionary a precedent vectors to a list of dictionaries
    2) Train the support vector machine model
    3) train the similarity finder model

    :param command_list: List of command line arguments. Not used yet since there is only 1 training technique
    :return: boolean
    """

    # ------------------- COMMAND LINE SYNTAX --------------------------
    for command in command_list:
        if '--' == command[:2]:
            if command not in CommandEnum.command_list:
                Log.write(command + " not recognized")
                return False

    precedent_vector = __dictionary_to_list()
    if len(precedent_vector) == 0:
        return False
    try:
        data_size = command_list[-1]
        precedent_vector = precedent_vector[:int(data_size)]

    except IndexError:
        pass

    except ValueError:
        pass

    except TypeError:
        Log.write("create the precedent vector model first.\nCommand: python main.py -post")
        return False

    # ------------------- TRAINING --------------------------
    Log.write("Executing train model.")
    if CommandEnum.SVM in command_list:
        linear_svm = MultiClassSVM(precedent_vector)
        if CommandEnum.WEIGHTS in command_list:
            linear_svm.display_weights()
        else:
            linear_svm.train()
            linear_svm.save()

    if CommandEnum.SVR in command_list:
        regression_svr = TenantPaysLandlordRegressor(precedent_vector)
        regression_svr.train()
        regression_svr.save()

    if CommandEnum.SIMILARITY_FINDER in command_list:
        SimilarFinder(train=True, dataset=precedent_vector)

    precedent_vector = None  # deallocate memory

    return True
