import unittest
from util.parse_dataset import CreateJson


class TestMain(unittest.TestCase):
    text = """
[meta]
() = money,ner_duckling

[regex_features]
money: $\d(.)?+|\d(.)?+$

[entity_synonyms]
entity: synonym1, synonym2

[common_examples: true]
my landlord increased my rent by ($500)
i owe my landlord (40 dollars)

[common_examples: false]
i don't owe my landlord any (money)    
    """

    def test_find_meta_characters(self):
        parser = CreateJson()
        text = "() = money,ner_duckling"
        result = parser.find_meta_characters(text)
        expected_result = {
            'open': '(',
            'close': ')',
            'entity': 'money',
            'extractor': 'ner_duckling'
        }
        self.assertTrue(result, expected_result)

    def test_find_regex(self):
        parser = CreateJson()
        text = "money: $\d(.)?+|\d(.)?+$"
        result = parser.find_regex(text)
        expected_result = {
            'name': 'money',
            'pattern': '$\\d(.)?+|\\d(.)?+$'
        }
        self.assertEqual(result, expected_result)

    def test_find_synonyms(self):
        parser = CreateJson()
        text = "entity: synonym1, synonym2"
        result = parser.find_synonyms(text)
        expected_result = {
            'entity': 'entity',
            'synonyms': [
                'synonym1',
                'synonym2'
            ]
        }
        self.assertEqual(result, expected_result)

    def test_find_text(self):
        parser = CreateJson()
        parser.parse_file(self.text)

        current_intent = parser.current_intent
        meta_list = parser.meta_list
        regex_list = parser.regex_list
        synonym_list = parser.synonym_list
        intent_list = parser.intent_list

        expected_current_intent = 'false'

        expected_meta_list = [
            {
                'close': ')',
                'extractor': 'ner_duckling',
                'entity': 'money',
                'open': '('
            }
        ]

        expected_regex_list = [
            {
                'pattern': '$\\d(.)?+|\\d(.)?+$',
                'name': 'money'
            }
        ]

        expected_synonym_list = [
            {
                'synonyms': [
                    'synonym1',
                    'synonym2'
                ],
                'entity': 'entity'
            }
        ]

        expected_intent_list = [
            {
                'intent': 'true',
                'text': 'my landlord increased my rent by $500',
                'entities': [
                    {
                        'extractor': 'ner_duckling',
                        'end': 37,
                        'value': '$500',
                        'start': 33,
                        'entity': 'money'
                    }
                ]
            },
            {'intent': 'true',
             'text': 'i owe my landlord 40 dollars',
             'entities': [
                 {
                     'extractor': 'ner_duckling',
                     'end': 28,
                     'value': '40 dollars',
                     'start': 18,
                     'entity': 'money'
                 }
             ]
             },
            {
                'intent': 'false',
                'text': "i don't owe my landlord any money    ",
                'entities': [
                    {
                        'extractor': 'ner_duckling',
                        'end': 33,
                        'value': 'money',
                        'start': 28,
                        'entity': 'money'
                    }
                ]
            }
        ]

        self.assertEqual(current_intent, expected_current_intent)
        self.assertEqual(meta_list, expected_meta_list)
        self.assertEqual(regex_list, expected_regex_list)
        self.assertEqual(synonym_list, expected_synonym_list)
        self.assertEqual(intent_list, expected_intent_list)

