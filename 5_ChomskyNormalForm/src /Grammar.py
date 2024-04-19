from constants import EPSILON


class Grammar:
    def __init__(self, non_terminals, terminals, rules, start='S'):
        self.non_terminals = non_terminals
        self.terminals = terminals
        self.rules = rules
        self.start = start

    def print_rules(self):
        """
        Print the rules of the grammar in a human-readable format.
        """
        for non_terminal in self.rules:
            print(f'{non_terminal} -> {" | ".join(self.rules[non_terminal])}')

    def is_cnf(self):
        """
        Check if the grammar is in Chomsky Normal Form (CNF).
        """
        for non_terminal in self.rules:
            for production in self.rules[non_terminal]:
                if len(production) == 0 or len(production) > 2:
                    return False
                if len(production) == 1 and production not in self.terminals:
                    return False
                if len(production) == 2 and any(symbol in self.terminals for symbol in production):
                    return False

        return True

    def eliminate_epsilon_productions(self):
        """
        Eliminate epsilon productions from the grammar.
        """
        nullable = set()

        # Find all nullable non-terminals
        for non_terminal in self.non_terminals:
            for production in self.rules[non_terminal]:
                if production == EPSILON:
                    nullable.add(non_terminal)

        # Check for indirect nullable non-terminals
        changes = True
        while changes:
            changes = False
            for non_terminal in self.non_terminals:
                if non_terminal not in nullable:
                    for production in self.rules[non_terminal]:
                        if all(symbol in nullable for symbol in production):
                            nullable.add(non_terminal)
                            changes = True
                            break

        # Eliminate epislon-productions
        new_rules = {}
        for non_terminal in self.rules:
            new_prods = []
            for production in self.rules[non_terminal]:
                if production != EPSILON:
                    new_prods.extend(
                        self._expand_nullable_prod(production, nullable))
            # Remove duplicates
            new_rules[non_terminal] = list(set(new_prods))

        self.rules = new_rules

    def _expand_nullable_prod(self, production, nullable):
        """
        Expand a production by replacing nullable non-terminals with epsilon.
        """
        expansions = ['']

        for symbol in production:
            new_expansions = []
            if symbol in nullable:
                for expansion in expansions:
                    new_expansions.append(expansion + symbol)
                    new_expansions.append(expansion)
            else:
                for expansion in expansions:
                    new_expansions.append(expansion + symbol)
            expansions = new_expansions

        return [expansion for expansion in expansions if expansion]

    def eliminate_renaming(self):
        """
        Eliminate renaming productions (unit productions) from the grammar.
        """

        # Track the changes to avoid re-processing unit productions
        changes = True
        while changes:
            changes = False
            for non_terminal in self.non_terminals:
                # Filter out unit productions
                unit_productions = [
                    p for p in self.rules[non_terminal] if p in self.non_terminals]
                for unit in unit_productions:
                    # Add the productions of the unit non-terminal, replacing the unit production
                    new_productions = self.rules[unit]
                    if new_productions:
                        self.rules[non_terminal].extend(new_productions)
                        self.rules[non_terminal].remove(unit)
                        # Make sure to remove any duplicates
                        self.rules[non_terminal] = list(
                            set(self.rules[non_terminal]))
                        changes = True

                # After processing the unit productions for a non-terminal, filter them out
                self.rules[non_terminal] = [
                    p for p in self.rules[non_terminal] if p not in self.non_terminals]

    def eliminate_inaccessible_symbols(self):
        """
        Eliminate inaccessible symbols from the grammar.
        """
        accessible = {self.start}
        changes = True  # Flag to check if there were changes in the last iteration
        old_rules = self.rules.copy()

        while changes:
            changes = False
            for non_terminal in accessible.copy():
                for production in self.rules[non_terminal]:
                    for symbol in production:
                        if symbol in self.non_terminals and symbol not in accessible:
                            accessible.add(symbol)
                            changes = True

        self.non_terminals = list(accessible)
        self.rules = {nt: old_rules[nt] for nt in accessible}

    def eliminate_non_productive_symbols(self):
        """
        Eliminate non-productive symbols from the grammar.
        """
        productive = {self.start}
        changes = True

        while changes:
            changes = False
            for non_terminal in self.non_terminals:
                if non_terminal not in productive:
                    for production in self.rules[non_terminal]:
                        if all(symbol in self.terminals or symbol in productive for symbol in production):
                            productive.add(non_terminal)
                            changes = True
                            break

        self.non_terminals = list(productive)

        # Create a new dictionary to store the updated rules
        updated_rules = {}
        for nt in productive:
            productive_rules = []

            # Check each production for this non-terminal
            for production in self.rules[nt]:
                # Verify if every symbol in the production is either a terminal
                # or a productive non-terminal (i.e., it leads to a terminal string)
                if all(symbol in self.terminals or symbol in productive for symbol in production):
                    productive_rules.append(production)

            updated_rules[nt] = productive_rules

        self.rules = updated_rules

    def _create_new_non_terminal(self):
        alphabet = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZαβγδζηθικλμνξοπρστυφχψω'

        # First, try to find a single unused letter from the Latin alphabet
        for letter in alphabet:
            if letter not in self.non_terminals:
                self.non_terminals.append(letter)
                return letter

        # If all single letters are used, start combining them with numbers
        for letter in alphabet:
            for num in range(100):  # Assuming 100 is enough to avoid conflicts
                new_symbol = f'{letter}{num}'
                if new_symbol not in self.non_terminals:
                    self.non_terminals.append(new_symbol)
                    return new_symbol

        # If all combinations are exhausted, raise an error
        raise ValueError("Exhausted all possible non-terminal symbols.")

    def to_cnf(self, print_steps=True):
        """
        Convert the grammar to Chomsky Normal Form (CNF).
        """
        if self.is_cnf():
            return

        self.eliminate_epsilon_productions()
        if print_steps:
            print('1. After eliminating epsilon productions:')
            self.print_rules()
            print()

        self.eliminate_renaming()
        if print_steps:
            print('2. After eliminating renaming productions:')
            self.print_rules()
            print()

        self.eliminate_inaccessible_symbols()
        if print_steps:
            print('3. After eliminating inaccessible symbols:')
            self.print_rules()
            print()

        self.eliminate_non_productive_symbols()
        if print_steps:
            print('4. After eliminating non-productive symbols:')
            self.print_rules()
            print()

        # Additional steps to convert to CNF
        rhs_to_non_terminal = {}
        old_non_terminals = list(self.rules)

        new_rules = {}
        for non_terminal in list(self.rules):
            new_rules[non_terminal] = set()
            for production in self.rules[non_terminal]:
                # Case for productions with more than 2 symbols
                while len(production) > 2:
                    # Extract the first two symbols
                    first_two_symbols = production[:2]

                    if first_two_symbols in rhs_to_non_terminal:
                        new_non_terminal = rhs_to_non_terminal[first_two_symbols]
                    else:
                        new_non_terminal = self._create_new_non_terminal()
                        new_rules[new_non_terminal] = {first_two_symbols}
                        rhs_to_non_terminal[first_two_symbols] = new_non_terminal
                    # Replace the first two symbols with the new non-terminal
                    production = new_non_terminal + production[2:]

                new_rules[non_terminal].add(production)

        # Handle mixed productions
        for non_terminal, productions in list(new_rules.items()):
            temp_productions = productions.copy()
            for production in temp_productions:
                if len(production) == 2 and any(symbol in self.terminals for symbol in production):
                    new_production = []
                    for symbol in production:
                        if symbol in self.terminals:
                            if symbol in rhs_to_non_terminal:
                                new_non_terminal = rhs_to_non_terminal[symbol]
                            else:
                                new_non_terminal = self._create_new_non_terminal()
                                new_rules[new_non_terminal] = {symbol}
                                rhs_to_non_terminal[symbol] = new_non_terminal
                            new_production.append(new_non_terminal)
                        else:
                            new_production.append(symbol)
                    productions.remove(production)
                    productions.add(''.join(new_production))

        # Reorder the rules to match the original order + new non-terminals
        self.rules = {nt: new_rules[nt] for nt in old_non_terminals +
                      list(set(new_rules) - set(old_non_terminals))}

        if print_steps:
            print('5. After converting to CNF:')
            self.print_rules()
            print()
