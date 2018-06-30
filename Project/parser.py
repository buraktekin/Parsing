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

# -*- coding: utf-8 -*-

import sys, os
from collections import defaultdict
from CNF_converter import CNF

class Parser:
    def __init__(self):
        #-----------------------------------------------
        # Grammar in CNF
        self.cnf_rules = CNF().rules
        #-----------------------------------------------
        # CONSTANTS:
        self.set_of_tokens = list()
        self.filename = "sentence.txt"
        self.strings_of_rows = defaultdict(list)
        self.table_rows = defaultdict(list)
        #-----------------------------------------------
        # Initialization
        self.load_sentences(self.filename)
        self._generate_strings()
        print(f"\n#--------------------\n{self.cnf_rules}\n#--------------------\n")
        self._find_cells()

    
    def load_sentences(self, filename):
        self.filename = filename
        with open(self.filename, "r") as sentences:
            lines = sentences.readlines()
            for line in lines:
                self.set_of_tokens.append(line.split())
    
    def _generate_row_productions(self, row, sentence):
        result = list()
        for index, item in enumerate(sentence):
            new_string = sentence[index:index + row]
            if len(new_string) == row:
                if row < 3:
                    result.append([new_string])
                else:
                    for num in range(len(new_string) - 1):
                        temp_string = [new_string[:num + 1], new_string[num+1:]]
                        result.append(temp_string)
        return result

    def _generate_strings(self):
        for sentence in self.set_of_tokens:
            for index in range(len(sentence)):
                row = self._generate_row_productions(index + 1, sentence)
                self.strings_of_rows[index + 1] = row

    def _find_cells(self):
        for string in self.strings_of_rows:
            for substring in self.strings_of_rows[string]:
                for symbols in substring:
                    print(string, symbols, " -> ", CNF()._find_lhs_from_rhs(symbols))
                    

if __name__ == '__main__':
    Parser()