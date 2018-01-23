import unittest
import numpy
from feature_extraction.pre_processing.word_vector.french_vector import FrenchVector
from util.constant import Path
import os


class TestFrenchWordVector(unittest.TestCase):
    """
    the most crucial aspect of this unittest is to make sure
    that the words get vectorized and that the word vector"s
    memory allocation is deallocated when it is not needed anymore
    """

    def test_load_vector(self):
        Path.binary_directory = os.path.join(Path.root_directory, r'data/binary/')
        FrenchVector.unload_vector()
        self.assertIsNone(FrenchVector.word_vectors)
        FrenchVector.load_french_vector_bin()
        self.assertIsNotNone(FrenchVector.word_vectors)
        FrenchVector.unload_vector()

    def test_unload_vector(self):
        Path.binary_directory = os.path.join(Path.root_directory, r'data/binary/')
        FrenchVector.unload_vector()
        self.assertIsNone(FrenchVector.word_vectors)
        FrenchVector.load_french_vector_bin()
        self.assertIsNotNone(FrenchVector.word_vectors)
        FrenchVector.unload_vector()
        self.assertIsNone(FrenchVector.word_vectors)

    def test_stop_words(self):
        Path.binary_directory = os.path.join(Path.root_directory, r'data/binary/')
        stop_words = ["dehors", "depuis", "devrait", "doit", "donc", "dos", "début"]
        all_words_found = True
        for words in stop_words:
            all_words_found = words in FrenchVector.get_stop_tokens()
        self.assertTrue(all_words_found)

    def test_vectorize_sent(self):
        """
        The actual values of the vector are not tested because
        they are arbitrary from one model_training to another.
        """
        Path.binary_directory = os.path.join(Path.root_directory, r'data/binary/')
        FrenchVector.load_french_vector_bin()
        sentence = "Je suis trop beau."
        vec = FrenchVector.vectorize_sent(sentence)
        test_array = numpy.zeros(1)
        self.assertEqual(type(test_array), type(vec))
        self.assertEqual(len(vec), FrenchVector.word_vector_size)
        sentence = ["Je", "suis", "trop", "beau", "."]
        vec = FrenchVector.vectorize_sent(sentence)
        self.assertEqual(type(test_array), type(vec))
        self.assertEqual(len(vec), FrenchVector.word_vector_size)
        FrenchVector.unload_vector()
