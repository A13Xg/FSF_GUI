import unittest
import os
import json
import sys
from forgesteel_converter import main

class TestIntegration(unittest.TestCase):
    def test_full_conversion(self):
        """Tests the full conversion process from .ds-hero to Foundry VTT .json."""
        input_file = 'Quelialis.ds-hero'
        output_file = 'test_output.json'
        
        # Run the conversion
        sys.argv = ['forgesteel_converter.py', input_file, output_file, '--compendium', 'draw_steel_repo/src/packs']
        main()
        
        # Check that the output file was created
        self.assertTrue(os.path.exists(output_file))
        
        # Load the generated file and the reference file
        with open(output_file, 'r', encoding='utf-8') as f:
            generated_char = json.load(f)
        
        with open('fvtt-Actor-test-yS2hB07JR2QR8oS7.json', 'r', encoding='utf-8') as f:
            reference_char = json.load(f)
            
        # Compare some key fields
        self.assertEqual(generated_char['name'], 'Quelialis')
        self.assertEqual(generated_char['type'], reference_char['type'])
        self.assertTrue(len(generated_char['items']) > 0)
        
        # Clean up the generated file
        os.remove(output_file)

if __name__ == '__main__':
    unittest.main()