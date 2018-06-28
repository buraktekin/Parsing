from collections import defaultdict

class CNF(object):
    """
    !! IMPORTANT NOTE !!:
    This part will be referenced in comments in the code base below. While referencing the symbol
    '@' will be in use.
    
    Rules to follow for chomsky normal form conversion are as follows:
    1. Define a start symbol. If there is Start Symbol on the right hand side (RHS), create 
    a new rule which derives Start Symbol (S).
    2. Get rid of ε-productions if any exists.
    3. Get rid of all productions with one non-terminal symbol on the RHS.
    4. Replace all long productions (which has more than 2 symbols) with the shorter ones.
    5. Move all terminals to productions.
    """


    def __init__(self):
        #-----------------------------------------------
        # CONSTANTS:
        self.EPSILON = "ε"
        self.start_symbol = None
        self.filename = "grammar.txt"
        #-----------------------------------------------
        
        #-----------------------------------------------
        # RULES: all productions as a list
        self.rules = defaultdict(list)
        #-----------------------------------------------
        
        #-----------------------------------------------
        # Load Grammar from text file...
        print(self.load_grammar("./grammar.txt"))
        print(self.find_epsilon_productions())
        #-----------------------------------------------

    def define_start_symbol(self, symbol):
        self.start_symbol = symbol
    
    def load_grammar(self, filename):
        self.filename = filename
        with open(self.filename, "r") as grammar:
            rules = grammar.readlines()
            for rule in rules:
                #-----------------------------------------------
                # Split lhs and rhs of the rules to
                # create a dictionary of rules
                lhs, rhs = rule.strip().split(" -> ")
                rhs_symbols = rhs.strip().split(" | ")
                if rules.index(rule) == 0:
                    self.start_symbol = lhs
                for r in rhs_symbols:
                    self.rules[lhs].append(r.split())
                #-----------------------------------------------
                
                #-----------------------------------------------
                # Check start symbol: Rule @1
                self.check_start_symbol_on_rhs(self.start_symbol, rhs_symbols)
                #-----------------------------------------------
        return self.rules

    def check_start_symbol_on_rhs(self, symbol, rhs):
        if symbol in rhs:
            new_symbol = symbol + "'"
            self.rules[new_symbol].append(symbol)
            self.start_symbol = new_symbol

    def find_epsilon_productions(self):
        for lhs in self.rules:
            if not self.start_symbol is None and lhs == self.start_symbol:
                continue
            for index, rhs in enumerate(self.rules[lhs]):
                if self.EPSILON in rhs:
                    return lhs, index # EPSILON found in index 'index'

        return None, None

    def _eliminate_epsilon_productions(self):
        while True:
            # Get the production rules have EPSILON in it.
            lhs, index = self.find_epsilon_productions()
            
            #-----------------------------------------------
            # NOTE:
            # if find_epsilon_productions returns nothing 
            # for LHS then break the loop.
            if lhs is None:
                break
            #-----------------------------------------------
            
            #-----------------------------------------------
            # Delete epsilon rule from RHS
            del self.rules[lhs][index]
            #-----------------------------------------------

if __name__ == '__main__':
    CNF()