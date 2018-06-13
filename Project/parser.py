# -----------------------------------------------------------------
# :: Author :: Burak Tekin
# :: Lecture :: Parsing - SuSe 2018, University of Stuttgart
# :: Parsing ::
#
# ::Design Recipe::
# PURPOSE: Generating parsing tree for the given sentence by applying 
# the rules defined in given grammar.
#
# ::Contract::
# parser( list_of_rules::List, sentence::String ) --> parse_tree::String
# -----------------------------------------------------------------

import sys, os

class Parser:
    # -----------------------------------------------------------------
    # create dictionaries to hold the rules to make it easier to reach
    # them, while the production is on going.
    # -----------------------------------------------------------------
    def __init__(self):
        self.rules = {}
        # derivations: all productions as a key, value pairs
        self.derivations = {} 
        # List of terminals
        self.terminals = []
        # List of non-terminals
        non_terminals = []
        self.load_grammar("./grammar.cfg")


    # -----------------------------------------------------------------
    # Split terminals and non-terminals
    # -----------------------------------------------------------------
    def find_terminals(self, rhs, non_terminals):
        temp_array = list()
        for symbols in rhs:
            for symbol in symbols:
                for s in symbol:
                    if( s not in non_terminals 
                    and s not in temp_array ):
                        temp_array.append( s )
        return temp_array


    # -----------------------------------------------------------------
    # Get LHS and RHS of the rule
    # -----------------------------------------------------------------
    def lhs_rhs(self, rule):
        rule_string = rule.strip().split("->")
        lhs = rule_string[0].strip()
        rhs = [ r.split() for r in rule_string[1].strip().split(" | ") ]
        self.derivations[lhs] = rhs
        return rule_string


    # -----------------------------------------------------------------
    # Load grammar from a file
    # -----------------------------------------------------------------
    def load_grammar(self, filename):
        with open(filename) as grammar:
            unit_rules = grammar.readlines()
        list_of_rules = list(map(self.lhs_rhs, unit_rules))
        rhs = list(self.derivations.values())
        non_terminals = list(set(self.derivations.keys()))
        terminals = self.find_terminals(rhs, non_terminals)

        print("Terminals: ", terminals)
        print("Non terminals: ", non_terminals)

        self.is_cnf(self.derivations)

        return list_of_rules


    # -----------------------------------------------------------------
    # Detect whether the given grammar is in CNF form or not?
    # Every rule in the grammar has to be in the form of:
    # I) (non−terminal) -> (non−terminal)(non−terminal)
    #                  ~ OR ~
    # II) (non−terminal) -> (terminal)
    # -----------------------------------------------------------------
    def is_cnf(self, derivations):
        for derivation in list(derivations.values()):
            for rhs in derivation:
                # (non-terminal) -> (non-terminal) (non-terminal)
                [(index, symbol) for symbol, index in rhs if( len(rhs) == 2 )]:


    # -----------------------------------------------------------------
    # Converts a given CFG formatted grammar into the form of CNF.
    # (non−terminal) -> (non−terminal)(non−terminal) :: n - 1
    # (non−terminal) -> (terminal) :: n
    # Totally :: 2n + 1 rules applied where n is the length of string
    # 
    # Elimiate ε-Rules
    # However CNF reduces complexity by constraining the number of LHS
    # to 2 and it gives us the complexity of O(n^3).
    # -----------------------------------------------------------------
    def converter(self, grammar):
        ''' deneme '''


if __name__ == '__main__':
    Parser()