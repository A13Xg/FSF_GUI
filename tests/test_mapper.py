import unittest
import json
from converter.mapper import convert_character

class TestMapper(unittest.TestCase):
    def setUp(self):
        with open('Quelialis.ds-hero', 'r', encoding='utf-8') as f:
            self.forgesteel_char = json.load(f)
        
        self.compendium_items = {
            "catch-breath": {
                "name": "Catch Breath",
                "type": "ability",
                "system": {
                    "_dsid": "catch-breath"
                }
            }
        }

        self.foundry_char = convert_character(self.forgesteel_char, self.compendium_items)

    def test_convert_character_core_attributes(self):
        """Tests the conversion of core character attributes."""
        self.assertEqual(self.foundry_char['name'], 'Quelialis')
        self.assertEqual(self.foundry_char['type'], 'hero')
        self.assertEqual(self.foundry_char['system']['stamina']['value'], 0)
        self.assertEqual(self.foundry_char['system']['characteristics']['might']['value'], -1)
        self.assertEqual(self.foundry_char['system']['hero']['wealth'], 1)

    def test_feature_conversion(self):
        """Tests that features are converted to items."""
        self.assertTrue(len(self.foundry_char['items']) > 0)
        
        # Check for a specific ancestry feature
        ancestry_item = next((item for item in self.foundry_char['items'] if item['name'] == 'Memonek'), None)
        self.assertIsNotNone(ancestry_item)
        self.assertEqual(ancestry_item['type'], 'ancestry')

        # Check for a specific class feature
        class_item = next((item for item in self.foundry_char['items'] if item['name'] == 'Elementalist'), None)
        self.assertIsNotNone(class_item)
        self.assertEqual(class_item['type'], 'class')
    
    def test_ability_conversion(self):
        """Tests that abilities are converted to items."""
        # Check for a specific ability that is in the character data
        bifurcated_incineration = next((item for item in self.foundry_char['items'] if item['name'] == 'Bifurcated Incineration'), None)
        self.assertIsNotNone(bifurcated_incineration)
        self.assertEqual(bifurcated_incineration['type'], 'ability')

        # Check for a specific class feature that is an ability
        hurl_element_item = next((item for item in self.foundry_char['items'] if item['name'] == 'Hurl Element'), None)
        self.assertIsNotNone(hurl_element_item)
        self.assertEqual(hurl_element_item['type'], 'feature')

    def test_inventory_conversion(self):
        """Tests that inventory items are converted."""
        # The sample character has no inventory, so we'll add a mock item
        self.forgesteel_char['state']['inventory'] = [{'id': 'test-item', 'name': 'Test Item', 'description': 'A test item.'}]
        self.foundry_char = convert_character(self.forgesteel_char, self.compendium_items)
        
        test_item = next((item for item in self.foundry_char['items'] if item['name'] == 'Test Item'), None)
        self.assertIsNotNone(test_item)
        self.assertEqual(test_item['type'], 'treasure')


if __name__ == '__main__':
    unittest.main()