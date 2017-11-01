from is_student_classifier import IsStudentClassifier


def test_classify_true():
    assert IsStudentClassifier().classify('I study at Mcgill University')[
               'is_student'] == 'true'


def test_classify_false():
    assert IsStudentClassifier().classify('I have graduated')[
               'is_student'] == 'false'
