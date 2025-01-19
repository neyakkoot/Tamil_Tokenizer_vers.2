import unittest
from pathlib import Path
import json
from advanced_tamil_analyzer import AdvancedTamilAnalyzer

class TestAdvancedTamilAnalyzer(unittest.TestCase):
    def setUp(self):
        """Test setup"""
        self.analyzer = AdvancedTamilAnalyzer()
        self.test_text = """
        தமிழ் இலக்கியம் தொன்மையானது. 
        சங்க இலக்கியம், பக்தி இலக்கியம், காப்பிய இலக்கியம் என
        பல்வேறு வகைகள் உண்டு.
        """
        
    def test_init(self):
        """Test initialization"""
        self.assertIsNotNone(self.analyzer.tamil_letters)
        self.assertIsNotNone(self.analyzer.uyir_letters)
        self.assertIsNotNone(self.analyzer.mei_letters)
        self.assertIsNotNone(self.analyzer.uyirmei_letters)
        self.assertIsNotNone(self.analyzer.agaram_letters)

    def test_load_text_direct(self):
        """Test direct text loading"""
        text = self.analyzer.load_text("தமிழ்", source_type='text')
        self.assertEqual(text, "தமிழ்")

    def test_load_text_file(self):
        """Test file loading"""
        # Create test file
        test_file = Path('test.txt')
        test_file.write_text(self.test_text, encoding='utf-8')
        
        loaded_text = self.analyzer.load_text(test_file, source_type='file')
        self.assertEqual(loaded_text.strip(), self.test_text.strip())
        
        # Cleanup
        test_file.unlink()

    def test_detailed_analysis(self):
        """Test text analysis"""
        results = self.analyzer.detailed_analysis(self.test_text)
        
        # Check basic structure
        self.assertIn('அடிப்படை_தகவல்', results)
        self.assertIn('எழுத்து_வகைகள்', results)
        self.assertIn('அதிக_பயன்பாட்டு_சொற்கள்', results)
        self.assertIn('அதிக_பயன்பாட்டு_எழுத்துகள்', results)
        
        # Check basic info
        basic_info = results['அடிப்படை_தகவல்']
        self.assertGreater(basic_info['மொத்த_சொற்கள்'], 0)
        self.assertGreater(basic_info['மொத்த_எழுத்துகள்'], 0)
        
        # Check letter types
        letter_types = results['எழுத்து_வகைகள்']
        self.assertIn('உயிர்', letter_types)
        self.assertIn('மெய்', letter_types)
        self.assertIn('உயிர்மெய்', letter_types)
        self.assertIn('அகரம்', letter_types)

    def test_generate_visualizations(self):
        """Test visualization generation"""
        results = self.analyzer.detailed_analysis(self.test_text)
        visualizations = self.analyzer.generate_visualizations(
            results,
            output_dir='test_output'
        )
        
        # Check visualization objects
        self.assertIn('word_frequency', visualizations)
        self.assertIn('letter_types', visualizations)
        self.assertIn('char_frequency', visualizations)
        self.assertIn('dashboard', visualizations)
        
        # Check output files
        output_dir = Path('test_output')
        self.assertTrue((output_dir / 'word_frequency.html').exists())
        self.assertTrue((output_dir / 'letter_types.html').exists())
        self.assertTrue((output_dir / 'char_frequency.html').exists())
        self.assertTrue((output_dir / 'dashboard.html').exists())
        
        # Cleanup
        import shutil
        shutil.rmtree(output_dir)

    def test_save_results(self):
        """Test results saving"""
        results = self.analyzer.detailed_analysis(self.test_text)
        output_file = 'test_results.json'
        
        self.analyzer.save_results(results, output_file)
        
        # Check if file exists and is valid JSON
        self.assertTrue(Path(output_file).exists())
        with open(output_file, 'r', encoding='utf-8') as f:
            loaded_results = json.load(f)
        
        # Check basic structure of saved results
        self.assertIn('அடிப்படை_தகவல்', loaded_results)
        self.assertIn('எழுத்து_வகைகள்', loaded_results)
        self.assertIn('அதிக_பயன்பாட்டு_சொற்கள்', loaded_results)
        self.assertIn('அதிக_பயன்பாட்டு_எழுத்துகள்', loaded_results)
        
        # Cleanup
        Path(output_file).unlink()

    def test_empty_text(self):
        """Test handling of empty text"""
        results = self.analyzer.detailed_analysis("")
        self.assertEqual(results['அடிப்படை_தகவல்']['மொத்த_சொற்கள்'], 0)
        self.assertEqual(results['அடிப்படை_தகவல்']['மொத்த_எழுத்துகள்'], 0)

    def test_non_tamil_text(self):
        """Test handling of non-Tamil text"""
        results = self.analyzer.detailed_analysis("Hello World")
        self.assertEqual(results['அடிப்படை_தகவல்']['மொத்த_சொற்கள்'], 0)
        self.assertEqual(results['அடிப்படை_தகவல்']['மொத்த_எழுத்துகள்'], 0)

    def test_mixed_text(self):
        """Test handling of mixed Tamil and English text"""
        mixed_text = "தமிழ் Language மொழி"
        results = self.analyzer.detailed_analysis(mixed_text)
        # Should only count Tamil words
        self.assertEqual(results['அடிப்படை_தகவல்']['மொத்த_சொற்கள்'], 2)

if __name__ == '__main__':
    unittest.main()
