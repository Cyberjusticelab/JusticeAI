from model_training.svm.svm import LinearSVM
from numpy.testing import assert_array_equal


def test_get_weights_without_training():
    # Execute
    result = LinearSVM([]).get_weights()

    # Verify
    assert result is None


def test_predict_without_training():
    # Execute
    result = LinearSVM([]).predict([])

    # Verify
    assert result is None


def test__reshape_dataset():
    # Test Data
    precedent1 = {'facts_vector': [1, 2, 3], 'outcomes_vector': [0, 14]}
    precedent2 = {'facts_vector': [4, 6, 8], 'outcomes_vector': [0, 1114]}
    precedent3 = {'facts_vector': [5, 7, 9], 'outcomes_vector': [0, 114]}
    precedents = [precedent1, precedent2, precedent3]

    # Execute
    (x_total, y_total) = LinearSVM(precedents)._reshape_dataset()

    # Verify
    assert_array_equal(x_total[0], [1, 2, 3])
    assert_array_equal(x_total[1], [4, 6, 8])
    assert_array_equal(x_total[2], [5, 7, 9])

    assert_array_equal(y_total[0], [14])
    assert_array_equal(y_total[1], [1114])
    assert_array_equal(y_total[2], [114])
