from src.nlp_service.preprocessing.French.NerTraining import Ner

'''
Look at /French/GlobalVariables/ to set your models directory
'''
if __name__ == '__main__':
    ner = Ner()
    ner.train_named_entity(window=1)
