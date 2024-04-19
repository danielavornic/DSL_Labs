import unittest

from Grammar import Grammar
from constants import EPSILON


class TestGrammar(unittest.TestCase):
    def setUp(self):
        # variant 29 grammar
        non_terminals = ['S', 'A', 'B', 'C', 'D']
        terminals = ['a', 'b']
        rules = {
            'S': ['aB', 'DA'],
            'A': ['a', 'BD', 'aDADB'],
            'B': ['b', 'ASB'],
            'C': ['BA'],
            'D': ['BA', EPSILON]
        }
        self.grammar = Grammar(non_terminals, terminals, rules)

    def test_initial_grammar(self):
        self.assertEqual(self.grammar.non_terminals, ['S', 'A', 'B', 'C', 'D'])
        self.assertEqual(self.grammar.terminals, ['a', 'b'])
        self.assertIn('S', self.grammar.rules)
        self.assertIn('A', self.grammar.rules)
        self.assertIn('B', self.grammar.rules)
        self.assertIn('C', self.grammar.rules)
        self.assertIn('D', self.grammar.rules)

    def test_eliminate_epsilon_productions(self):
        self.grammar.eliminate_epsilon_productions()
        self.assertNotIn(EPSILON, self.grammar.rules['D'])

    def test_eliminate_renaming_productions(self):
        self.grammar.eliminate_epsilon_productions()
        self.grammar.eliminate_renaming()
        for prods in self.grammar.rules.values():
            for prod in prods:
                self.assertNotIn(prod, self.grammar.non_terminals)

    def test_eliminate_inaccessible_symbols(self):
        self.grammar.eliminate_epsilon_productions()
        self.grammar.eliminate_renaming()
        self.grammar.eliminate_inaccessible_symbols()
        for nt in self.grammar.non_terminals:
            self.assertIn(nt, self.grammar.rules)

    def test_eliminate_non_productive_symbols(self):
        self.grammar.eliminate_epsilon_productions()
        self.grammar.eliminate_renaming()
        self.grammar.eliminate_inaccessible_symbols()
        self.grammar.eliminate_non_productive_symbols()
        for prods in self.grammar.rules.values():
            for prod in prods:
                self.assertTrue(all(
                    symbol in self.grammar.terminals or symbol in self.grammar.non_terminals for symbol in prod))

    def test_is_cnf(self):
        self.assertFalse(self.grammar.is_cnf())
        self.grammar.to_cnf(print_steps=False)
        self.assertTrue(self.grammar.is_cnf())

    def test_to_cnf(self):
        self.grammar.to_cnf(print_steps=False)
        for nt, prods in self.grammar.rules.items():
            for prod in prods:
                self.assertTrue(len(prod) <= 2)
                if len(prod) == 2:
                    self.assertTrue(
                        all(symbol in self.grammar.non_terminals for symbol in prod))
                if len(prod) == 1:
                    self.assertTrue(
                        prod in self.grammar.terminals or prod == EPSILON)


if __name__ == '__main__':
    unittest.main()
