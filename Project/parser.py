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
        # Memory // history 
        self.mem = defaultdict(list)
        #-----------------------------------------------
        # Initialization
        self.load_sentences(self.filename)
        self._generate_strings()
        self.bottom_up()
        print(f"\n#--------------------\n{self.cnf_rules}\n#--------------------\n")

    
    def load_sentences(self, filename):
        self.filename = filename
        with open(self.filename, "r") as sentences:
            lines = sentences.readlines()
            for line in lines:
                self.set_of_tokens.append(line.split())
    
    def _generate_row_productions(self, row, sentence):
        result = list()
        sentence = [[x] for x in sentence]
        for index, item in enumerate(sentence):
            new_string = sentence[index:index + row]
            if len(new_string) == row:
                if row < 3:
                    result.append(new_string)
                else:
                    for num in range(len(new_string) - 1):
                        temp_string = [new_string[:num + 1], new_string[num+1:]]
                        result.append(temp_string)
        return result

    #-----------------------------------------------
    # NOTE:
    # mutual with the method _find_cells()
    #-----------------------------------------------
    def _generate_strings(self):
        for sentence in self.set_of_tokens:
            for index in range(len(sentence)):
                row = self._generate_row_productions(index + 1, sentence)
                self.strings_of_rows[index + 1] = row
    #-----------------------------------------------

    def _cartesian_product(self, first, second):
        result = list()
        for i in first:
            for j in second:
                result.append([i,j])

        return result

    def _find_lhs_from_rhs(self, rules, rhs_rule):
        temp_lhs = list()
        for lhs in rules:
            if rhs_rule in rules[lhs]:
                temp_lhs.append(lhs)
        return temp_lhs
    
    def _address_element(self, row, strings, index):
        print(row, " -> ", strings, " -> ", index)
        print(self.mem)
        factors = list()
        for col, string in enumerate(strings):
            row_number = len(string)
            factor = self.table_rows[row_number][index:index+1]
            factors.append(factor)
            print("STRING: ", string, "ROW: ", row_number, " COL: ", col, " INDEX: ", index)

        print("FACTORS: ", factors)
        cartesian = self._cartesian_product(factors[0], factors[1])
        print("CARTES:", cartesian)
        result = list()
        for product in cartesian:
            lhs = self._find_lhs_from_rhs(self.cnf_rules, product)
            print("PRODUCT: ", product, " LHS: ", lhs)
            #print("Product: ", product, " ---> LHS: ", lhs, "\n")
            if lhs not in result:
                result += lhs
            result = list(set(result))
        self.table_rows[row].insert(index, result)
        
        print(self.table_rows)

    def bottom_up(self):
        print(self.strings_of_rows)
        for row in self.strings_of_rows:
            for index, strings in enumerate(self.strings_of_rows[row]):
                column = index
                if(row == 1):
                    lhs = self._find_lhs_from_rhs(self.cnf_rules, strings[0])
                    self.table_rows[row].append(lhs)
                else:
                    self._address_element(row, strings, index)
                    #if(len(symbol) == 1):
                    #    lhs = self._find_lhs_from_rhs(self.cnf_rules, symbol)
                    #    self.table_rows[row].append(lhs)

if __name__ == '__main__':
    Parser()