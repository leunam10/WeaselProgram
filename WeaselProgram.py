
import numpy as np
import random
import string
import time
import copy


class Weasel:

    def __init__(self, n_copies=100, p_mutation=0.05):

        # set seed by using time
        np.random.seed(seed=int(time.time()))

        # get the random seed
        self.current_seed = np.random.get_state()[1][0]
        
        # Number of copies of the string for each generation (default value:100)
        self.n_copies = n_copies

        # Probability of mutation: replace a character with a new random character (default value: 5%)
        self.p_mutation = p_mutation

        # number of generation
        self.n_generation = 0
        
        # when the random generated string is the target string the program ends
        # the comparison of the two strings is done character by character, white
        # space included
        self.target_string = "METHINKS IT IS LIKE A WEASEL"
#        self.target_string = "CIAO SONO MANUEL"

        # total number of characters (white space included)
        self.n_char = int(len(self.target_string))

        # all ascii uppercase letters list
        self.ascii_uppercase_letters_list = list(string.ascii_uppercase)

        # all ascii uppercase letters list with white space
        self.ascii_uppercase_letters_list.append(" ")

        # this dictionary contains the copies of the string for each generation
        self.string_copies_dict = {}

        # this dictionary contains the score of the generated string
        self.score_dict = {}
        self.score_dict_init()

        # this list is used to select which character will mutate
        # a list of N 0 and 1 is created with a p=1-p_mutation for 0 and p=p_mutation for  
        self.if_mutation = [0,1]

        # it is true only for the first generation
        self.first_generation = True

        # print the general information 
        self.print_init()

    def print_init(self):

        '''
        
        This function prints the initialization info 

        '''
        print("")
        print("*"*100)
        print(f"SEED: {self.current_seed}")
        print(f"COPIES FOR GENERATION: {self.n_copies}")
        print(f"MUTATION PROBABILITY: {self.p_mutation*100}%")
        print(f"TARGET: {self.target_string}")
        
        
        print("*"*100)
        print("")
        

    def score_dict_init(self):

        '''
        
        This function is used to initialize the score dictionary

        '''
        
        for n in range(self.n_copies):
            copy_name = "copy_"+str(n+1)
            self.score_dict[copy_name] = 0
        
        
    def string_init(self):

        '''
        
        This function is used to initialize the initial 28 random characters string
        
        '''
        
        random_string_list = list(np.random.choice(self.ascii_uppercase_letters_list,
                                                   size=self.n_char))

        
        return random_string_list



    def make_string_copy(self):

        '''
        
        This function is used to make N copies of the string (string generated in each generation). The copies are saved in a dictionary

        '''

        if(self.first_generation):
            string_list = self.string_init()
        else:
            string_list = self.string_copies_dict[self.copy_with_high_score]
            
        for n in range(self.n_copies):
            copy_name = "copy_"+str(n+1)            
            self.string_copies_dict[copy_name] = copy.copy(string_list)
        

    def mutation(self):

        '''
        
        This function is used to randomly mutate the characters in the generated string

        '''

        for n in range(self.n_copies):
            copy_name = "copy_"+str(n+1)
            
            mutation_list = np.random.choice(self.if_mutation,
                                             size=self.n_char,
                                             p=[1-self.p_mutation, self.p_mutation])
            
            id_mutation_list = np.where(mutation_list==1)[0]
            if(len(id_mutation_list)==1):
                _id = id_mutation_list[0]                

                self.string_copies_dict[copy_name][_id] = np.random.choice(self.ascii_uppercase_letters_list)
            else:
                for _id in id_mutation_list:
                    self.string_copies_dict[copy_name][_id] = np.random.choice(self.ascii_uppercase_letters_list)
        
    def string_comparison(self):

        '''
    
        This function compares all the strings for the i-th generation with the target string

        '''

        for n in range(self.n_copies):
            copy_name = "copy_"+str(n+1)
            string_test = self.string_copies_dict[copy_name]

            for char1, char2 in zip(string_test, self.target_string):
                if(char1 == char2):
                    self.score_dict[copy_name] += 1
        

    def generation(self):

        '''
        
        '''

        self.score_dict_init()
        target_condition = len(self.target_string)
        best_score = self.select_best_string()

        while(best_score != target_condition):
            self.make_string_copy()
            self.mutation()
            self.string_comparison()
           
            best_score  = self.select_best_string()
            self.print_result(self.n_generation, best_score)
            
            if(self.n_generation == 0):
                self.first_generation = False
                        
            self.score_dict_init()
            self.n_generation += 1
            
    def select_best_string(self):

        '''
        
        This function is used to select the generated string with the highest score

        '''

        keys_list = list(self.score_dict.keys())
        values_list = list(self.score_dict.values())

        id_target_max = np.argmax(values_list)
        best_score = values_list[id_target_max]
        self.copy_with_high_score = keys_list[id_target_max]

        return best_score
        
    def print_result(self, n_generation, best_score):

        '''
        '''
        best_string = "".join(self.string_copies_dict[self.copy_with_high_score])
        print(f"{n_generation}: {best_string} -- score: {best_score}")

        

            
def main():

    wp = Weasel()
    wp.generation()
    
if(__name__ == "__main__"):
    
    main()
