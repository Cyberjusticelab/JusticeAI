import sys

try:
    from src.ml_service.preprocessing.French.DecisionParse import Parser
except:
    print("Train NER model first")
    sys.exit(1)
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
        if 'AZ-51205' in i and j < 5:
            j += 1
            model = parser.parse(i)
            t = model.topics
            for j in range(len(t)):
                print(model.core_topic[j])
                print(model.topics[j])
                print()
