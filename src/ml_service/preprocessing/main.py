from src.ml_service.preprocessing.French.DecisionParse import Parser
from src.ml_service.preprocessing.French.GlobalVariable import Global
import os

'''
Look at /French/GlobalVariables/ to set your models directory
'''

# #######################################
# DEMO
if __name__ == '__main__':
    parser = Parser()
    j = 0
    for i in os.listdir(Global.Precedence_Directory):
        if 'AZ-51210' in i and j < 5:
            j += 1
            model = parser.parse(i)
            t = model.topics
            for j in range(len(t)):
                print(model.training_output())
