import json
from src.fact_extraction.Models import clause, compliment, predicate

'''
CODE MEANT TO EXTRACT FEATURES FROM TRAINING DATA
NOT USED YET
'''
with open('clause_finder.json') as data_file:
    data = json.load(data_file)

model = data['data']

for sentence in model:
    pipe.pipe(sentence['sentence'])
    print()
    print(sentence['sentence'])
    print()
    word_dict = pipe.get_word_dict()
    answers = sentence['answer']
    for answer in answers:
        mc = answer['clause']
        pd = answer['predicate']
        cp = answer['compliment']
        for main_clause in mc:
            clause_model = clause.Clause()
            value_dict = main_clause['word']
            for values in value_dict:
                clause_model.set_word(word_dict[values['value']])
            value_dict = main_clause['quantifier']
            clause_model.set_quantifier(word_dict[value_dict])
            value_dict = main_clause['qualifier']
            for values in value_dict:
                clause_model.add_qualifier(word_dict[values['value']])
            print(clause_model)

        for pred_clause in pd:
            predicate_model = predicate.Predicate()
            value_dict = pred_clause['word']
            for values in value_dict:
                predicate_model.set_word(word_dict[values['value']])

            value_dict = pred_clause['qualifier']
            for values in value_dict:
                predicate_model.add_qualifier(word_dict[values['value']])
            print(predicate_model)

        for comp_clause in cp:
            compliment_model = compliment.compliment()
            value_dict = comp_clause['word']
            for values in value_dict:
                compliment_model.set_word(word_dict[values['value']])
            value_dict = comp_clause['quantifier']
            compliment_model.set_quantifier(word_dict[value_dict])
            value_dict = comp_clause['qualifier']
            for values in value_dict:
                compliment_model.add_qualifier(word_dict[values['value']])
            print(compliment_model)

        print('-------------------------------')
    print('-------------------------------')