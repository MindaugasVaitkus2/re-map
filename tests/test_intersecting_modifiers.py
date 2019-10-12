from sys import path
path.append('..')

from unittest import TestCase, main
from re_map import process, core, utils

core.__verbose__ = True

class IntersectingModifierTestCase(TestCase):
    def test_chain_1(self):
        text = 'C AAA C'

        modifiers = [
            ( r'(AAA)',  { 1: 'BBBBB' } ),
            ( r'(C BBBBB C)',  { 1: 'DD' } ),
        ]

        text_processed, span_map = process(text, modifiers)

        self.assertEqual( text_processed, 'DD' )
        self.assertEqual( span_map, [ ((0, 7), (0, 2)) ] )

        text_decorated, text_processed_decorated = utils.decorate(text, text_processed, span_map)

        self.assertEqual( text_decorated, '0000000' )
        self.assertEqual( text_processed_decorated, '00' )

    def test_chain_2(self):
        text = 'C AAA C'

        modifiers = [
            ( r'(AAA)',  { 1: 'BBBBB' } ),
            ( r'(C BBBBB)',  { 1: 'DD' } ),
        ]

        text_processed, span_map = process(text, modifiers)

        self.assertEqual( text_processed, 'DD C' )
        self.assertEqual( span_map, [ ((0, 5), (0, 2)) ] )

        text_decorated, text_processed_decorated = utils.decorate(text, text_processed, span_map)

        self.assertEqual( text_decorated, '00000 C' )
        self.assertEqual( text_processed_decorated, '00 C' )

    def test_chain_3(self):
        text = 'C AAA C'

        modifiers = [
            ( r'(AAA)',  { 1: 'BBBBB' } ),
            ( r'(BBBBB C)',  { 1: 'DD' } ),
        ]

        text_processed, span_map = process(text, modifiers)

        self.assertEqual( text_processed, 'C DD' )
        self.assertEqual( span_map, [ ((2, 7), (2, 4)) ] )

        text_decorated, text_processed_decorated = utils.decorate(text, text_processed, span_map)

        self.assertEqual( text_decorated, 'C 00000' )
        self.assertEqual( text_processed_decorated, 'C 00' )

    def test_chain_4(self):
        text = 'C AAA C'

        modifiers = [
            ( r'(AAA)',  { 1: 'BBEBB' } ),
            ( r'(BBEBB)',  { 1: 'DD' } ),
        ]

        text_processed, span_map = process(text, modifiers)

        self.assertEqual( text_processed, 'C DD C' )
        self.assertEqual( span_map, [ ((2, 5), (2, 4)) ] )

        text_decorated, text_processed_decorated = utils.decorate(text, text_processed, span_map)

        self.assertEqual( text_decorated, 'C 000 C' )
        self.assertEqual( text_processed_decorated, 'C 00 C' )

if __name__ == '__main__':
    main()