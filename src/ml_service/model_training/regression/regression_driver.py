from model_training.regression.multi_output.multi_output_regression import MultiOutputRegression
from util.log import Log


def run(command_list, dataset):
    if len(command_list) > 0:
        Log.write('Command not recognized')
        return False

    Log.write('Training multi output regression')
    svr = MultiOutputRegression(dataset)
    svr.train()
    return True
