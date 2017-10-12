from services.is_student_classifier import IsStudentClassifier


def test_classify_true():
    aa = IsStudentClassifier()
    inputList = list(aa.preprocess('I am a student at Mcgill University'))
    vector = aa.vectorize(inputList)
    b = aa.cl.classify(vector)
    aa.cl.show_most_informative_features()
    print(aa.cl.prob_classify(vector).__dict__)
    assert IsStudentClassifier().classify('I study at Mcgill University')['is_student'] == 'true'

def test_classify_false():
    assert IsStudentClassifier().classify('I have graduated')['is_student'] == 'false'
