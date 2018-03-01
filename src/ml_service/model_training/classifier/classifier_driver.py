from util.log import Log
from model_training.classifier.multi_output.multi_class_svm import MultiClassSVM


class CommandEnum:
    WEIGHTS = '--weights'
    command_list = [WEIGHTS]


def run(command_list, dataset):
    for command in command_list:
        if '--' == command[:2]:
            if command not in CommandEnum.command_list:
                Log.write(command + " not recognized")
                return False

    if CommandEnum.WEIGHTS in command_list:
        Log.write('Obtaining weights')
        svm = MultiClassSVM(None)
        svm.weights_to_csv()

    else:
        Log.write('Training SVM classifier')
        svm = MultiClassSVM(dataset)
        svm.train()
        svm.save()
    return True