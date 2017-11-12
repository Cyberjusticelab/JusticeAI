from word_vectors import vectors
import numpy
import unittest


class TestStringMethods(unittest.TestCase):

    def test_load_vector(self):
        self.assertIsNone(vectors.FrenchVectors.word_vectors)
        vectors.FrenchVectors.load_french_vector_bin()
        self.assertIsNotNone(vectors.FrenchVectors.word_vectors)
        vectors.FrenchVectors.unload_vector()

    def test_unload_vector(self):
        self.assertIsNone(vectors.FrenchVectors.word_vectors)
        vectors.FrenchVectors.load_french_vector_bin()
        self.assertIsNotNone(vectors.FrenchVectors.word_vectors)
        vectors.FrenchVectors.unload_vector()
        self.assertIsNone(vectors.FrenchVectors.word_vectors)

    def test_stop_words(self):
        stop_words = ['dehors', 'depuis', 'devrait', 'doit', 'donc', 'dos', 'début']
        all_words_found = True
        for words in stop_words:
            all_words_found = words in vectors.FrenchVectors.get_stop_words()
        self.assertTrue(all_words_found)

    def test_vectorize_sent(self):
        vectors.FrenchVectors.load_french_vector_bin()
        sentence = "Je suis trop beau."
        vec = vectors.FrenchVectors.vectorize_sent(sentence)
        test_array = numpy.zeros(1)
        self.assertEqual(type(test_array), type(vec))
        self.assertEqual(len(vec), vectors.FrenchVectors.Word_Vector_Size)
        sentence = ['Je', 'suis', 'trop', 'beau', '.']
        vec = vectors.FrenchVectors.vectorize_sent(sentence)
        self.assertEqual(type(test_array), type(vec))
        self.assertEqual(len(vec), vectors.FrenchVectors.Word_Vector_Size)
        vectors.FrenchVectors.unload_vector()
