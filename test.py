import unittest 
from wt import *

def esep(text,words = ''):
    return SEPARATOR+text+SEPARATOR+words

class _WtTestCase(unittest.TestCase):
    
    def setUp(self):
        self.wt = WeirdText()
    
    def tearDown(self):
        self.wt = None
    
class EncodeTestCase(_WtTestCase):
    
    def test_empty(self):
        self.assertEqual(self.wt.encode(''),esep(''))
        self.assertEqual(self.wt.encode(' '*10),esep(' '*10))
        self.assertEqual(self.wt.encode('.'),esep('.'))
        self.assertEqual(self.wt.encode('. . .'),esep('. . .'))
        
    def test_single(self):
        self.assertEqual(self.wt.encode('t e s t'),esep('t e s t'))
        self.assertEqual(self.wt.encode('T E S T'),esep('T E S T'))
        self.assertEqual(self.wt.encode('te st'),esep('te st'))
        self.assertEqual(self.wt.encode('tes t tes t'),esep('tes t tes t'))
        self.assertEqual(self.wt.encode('te\nst'),esep('te\nst'))
    
    def test_4_and_sort(self):
        self.assertEqual(self.wt.encode('test'),esep('tset','test'))
        #sort
        self.assertEqual(self.wt.encode('Vita auam.'),esep('Vtia aaum.','auam Vita'))
    
    def test_type(self):
        with self.assertRaises(TypeError):
            self.wt.encode(1)
    
    def unique(self):
        self.assertEqual(self.wt.encode('ab cde fghi'), esep('ab cde fghi','fhgi'))
        self.assertEqual(self.wt.encode('abcd fghi abcd'), esep('abcd fghi abcd','abcd fghi'))
        

        
    
class DecodeTestCase(_WtTestCase):
    
    def test_empty(self):
        self.assertEqual(self.wt.decode(esep('')),'')
        self.assertEqual(self.wt.decode(esep(' '*10)),' '*10)
        self.assertEqual(self.wt.decode(esep('.')),'.')
        self.assertEqual(self.wt.decode(esep('. . .')),'. . .')

    def test_text(self):
        self.assertEqual(self.wt.decode(esep('t e s t')),'t e s t')
        self.assertEqual(self.wt.decode(esep('T E S T')),'T E S T')
        self.assertEqual(self.wt.decode(esep('te st')),'te st')
        self.assertEqual(self.wt.decode(esep('tes t tes t')),'tes t tes t')
        self.assertEqual(self.wt.decode(esep('te\nst')),'te\nst')
        
    
    def test_4(self):
        self.assertEqual(self.wt.decode(esep('tset','test')),'test')
        self.assertEqual(self.wt.decode(esep('Aaum vtia.','vtia Auam')),'Auam vtia.')
        
    def test_incorect_empty(self):
        with self.assertRaises(DecodeError):
            self.wt.decode('')
    
    def test_incorect_text(self):
        with self.assertRaises(DecodeError):
            self.wt.decode(esep('test'))
        
        with self.assertRaises(DecodeError):
            self.wt.decode(esep('abcd efgh','abcd'))
        
    
    def test_incorect_type(self):
        with self.assertRaises(TypeError):
            self.wt.decode(1)
            
    def test_ambiguous(self):
        text = 'Ambiguous: abcd and acbd'
        decoded = self.wt.decode(self.wt.encode(text))
        self.assertNotEqual(text,decoded)
        self.assertEqual('Ambiguous: abcd|acbd and abcd|acbd',decoded)
        

class CompexTestCase(_WtTestCase):
    def test_simple(self):
        text = 'This is a long looong test sentence,\nwith some big (biiiiig) words!'
        encoded_text = self.wt.encode(text)
        
        self.assertNotEqual(text, encoded_text)
        self.assertEqual(self.wt.decode(encoded_text),text)
    
    def test_more_complex(self):
        self.maxDiff = 3000
        text = """The standard Lorem Ipsum passage, used since the 1500s\n\n"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."\nSection 1.10.32 of "de Finibus Bonorum et Malorum", written by Cicero in 45 BC\n"Sed ut perspiciatis unde omnis iste natus error sit , eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem. Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur? Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur, vel illum qui dolorem eum fugiat quo voluptas nulla pariatur?"""
        encoded_text = self.wt.encode(text)
        
        self.assertNotEqual(text, encoded_text)
        self.assertEqual(self.wt.decode(encoded_text),text)
        
def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(EncodeTestCase, 'test'))
    suite.addTest(unittest.makeSuite(DecodeTestCase, 'test'))
    suite.addTest(unittest.makeSuite(CompexTestCase, 'test'))
    return suite
        
if __name__ == '__main__':
    unittest.main(defaultTest='suite')