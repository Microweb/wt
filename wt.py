'''

This module contains the core classes and variables

Created on 18-05-2012
@author: smialy

Simple usage:

    from wt import WeirdText

    if __name__ == '__main__':
        wt = WeirdText
        orginal_text = 'Sample text...'
        encoded_text = wt.encode(orginal_text)
        ...
        orginal_text = wt.decode(encoded_text)        
'''
import re
import random

__all__ = ['WeirdText', 'SEPARATOR', 'DecodeError']

SEPARATOR = '\n---weird---\n'

#not need check len(word) < 4
tokenize_re = re.compile(r'(\w{4,})')

class DecodeError(Exception):
    pass

class _Encoder():
    '''
    Encoded for text
    '''
    def _hash(self, part):
        """Shuffle part"""
        #optimialization
        if len(part) == 2:
            return part[1] + part[0]
        l = list(part)
        random.shuffle(l)
        return ''.join(l)
        
    def process(self, text):
        #unique dictionary of words
        unique = set()
        def _replace(m):
            token = m.group(0)
            unique.add(token)
            return token[0] + self._hash(token[1:-1]) + token[-1]
            
        text = tokenize_re.sub(_replace, text)
        unique = list(unique)
        unique.sort(key=str.lower)
        return SEPARATOR + text + SEPARATOR + ' '.join(unique)
    
class _Decoder():
    '''
    Decoder for text
    '''
    def _unhash(self, token, words):
        #ambiguous result
        result = []
        for word in words:
            if len(word) == len(token) and word.startswith(token[0]) and word.endswith(token[-1]):
                #optimialization
                if len(word) == 4 and token[2] == word[1] and token[1] == word[2]:
                    result.append(word)
                else:
                    wl = list(word[1:-1])
                    tl = list(token[1:-1])
                    wl.sort()
                    tl.sort()
                    if tl == wl:
                        result.append(word)
        if not len(result):
            raise DecodeError('Not found corect word in dictionary')
        
        #ambiguous
        return '|'.join(result)
    
    def _revert(self, text, words):
        def _replace(m):
            return self._unhash(m.group(0),words)
        return tokenize_re.sub(_replace, text)
    
    def process(self, text):
        parts = text.split(SEPARATOR)
        if len(parts) != 3:
            raise DecodeError('Incorect text format to decode.')
        
        text = parts[1]
        words = set(parts[2].split(' '))
        text = self._revert(text, words)
        return text
    
class WeirdText():
    """
    Encode and decode text
    """
    def __init__(self):
        self._encoder = _Encoder()
        self._decored = _Decoder()
        
    def _check_text(self, text):
        if not isinstance(text, str):
            raise TypeError('Expected string')
        
    def encode(self, text):
        self._check_text(text)
        return self._encoder.process(text)
    
    def decode(self, text):
        self._check_text(text)
        return self._decored.process(text)


    
