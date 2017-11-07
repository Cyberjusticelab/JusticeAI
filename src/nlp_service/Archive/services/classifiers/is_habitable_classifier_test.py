from Archive.services import IsHabitableClassifier


def test_classify_false():
    assert IsHabitableClassifier().classify('There are rats in the apartment')[
        'is_habitable'] == 'false'


def test_classify_true():
    assert IsHabitableClassifier().classify('The apartment is nice')[
        'is_habitable'] == 'true'
