from model_training.similar_finder.similar_finder import SimilarFinder
import pytest
import numpy as np


def test_init_train_without_data():
    with pytest.raises(ValueError):
        SimilarFinder(train=True)


def test_get_most_similar():
    # Test Data
    similar = SimilarFinder.__new__(SimilarFinder)
    similar.case_numbers = ['a', 'b', 'c', 'd', 'e']

    # Mock
    class MockModel(object):

        def kneighbors(self, any):
            return (np.array([[1., 2., 3., 4., 5.]]), np.array([[1, 2, 4, 0, 3]]))

    class MockScaler(object):

        def transform(self, any):
            return any

    similar.model = MockModel()
    similar.scaler = MockScaler()

    # Execute
    result = similar.get_most_similar({'demands_vector': np.zeros(
        1), 'outcomes_vector': np.zeros(1), 'facts_vector': np.zeros(1)})

    # Verify
    assert result[0] == ('b', 1.)
    assert result[1] == ('c', 2.)
    assert result[2] == ('e', 3.)
    assert result[3] == ('a', 4.)
    assert result[4] == ('d', 5.)
