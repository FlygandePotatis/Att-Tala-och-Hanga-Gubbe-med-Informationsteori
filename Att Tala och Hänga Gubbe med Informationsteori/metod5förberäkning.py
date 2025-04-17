import math
import pandas as pd
import numpy as np
from ordlista import data



word_dict = {}

for line in data.split("\n"):
    word, number = line.split(",")
    word_dict[word] = int(number)

total_count_of_frequency = sum(word_dict.values())

word_list = {word: count / total_count_of_frequency for word, count in word_dict.items()}

word_list_only_with_words = list(word_list.keys())

lengths = list(set([len(word) for word in word_list_only_with_words]))


alphabet = "abcdefghijklmnopqrstuvwxyz"



def approximate_y(x):
    y = 0.61 * x
    return y



def find_the_best_guess_with_informationtheory(word_list_according_to_information):
    letters_and_their_corresponding_expected_wrong_guesses = {letter: 0 for letter in alphabet}
    total_probability_according_to_information = sum(word_list_according_to_information.values())
    word_list_according_to_information = {word: count / total_probability_according_to_information for word, count in word_list_according_to_information.items()}



    for letter in alphabet:
        word_list_with_no_letter = {word: probability for word, probability in word_list_according_to_information.items() if letter not in word}
        probability_of_no_letter = sum(word_list_with_no_letter.values())
        word_list_with_no_letter = {word: probability / probability_of_no_letter for word, probability in word_list_with_no_letter.items()}

        entropy_of_the_list_with_no_letter = 0
        for word, probability in word_list_with_no_letter.items():
            if probability != 0:
                entropy_of_the_list_with_no_letter -= probability * (math.log2(probability))
        
        entropy_after_no_letter_guess = entropy_of_the_list_with_no_letter
        


        word_list_with_letter = {word: probability for word, probability in word_list_according_to_information.items() if letter in word}
        probability_of_letter = 1 - probability_of_no_letter
        word_list_with_letter = {word: probability / probability_of_letter for word, probability in word_list_with_letter.items()}

        entropy_of_the_list_with_letter = 0
        for word, probability in word_list_with_letter.items():
            if probability !=0:
                entropy_of_the_list_with_letter -= probability * (math.log2(probability))



        probability_distribution_of_letter_in_local_wordlist = {}



        for word, probability in word_list_with_letter.items():
            list_of_places_of_letter = tuple([i for i, char in enumerate(word) if char == letter])



            if list_of_places_of_letter in probability_distribution_of_letter_in_local_wordlist:
                probability_distribution_of_letter_in_local_wordlist[list_of_places_of_letter] += word_list_with_letter[word]
            else:
                probability_distribution_of_letter_in_local_wordlist[list_of_places_of_letter] = word_list_with_letter[word]



        entropy_of_information_from_result_letter = 0
        for word, probability in probability_distribution_of_letter_in_local_wordlist.items():
            if probability != 0:
                entropy_of_information_from_result_letter -= probability * (math.log2(probability))

        entropy_after_letter_guess = entropy_of_the_list_with_letter - entropy_of_information_from_result_letter



        expected_wrong_guesses_of_letter = probability_of_letter * approximate_y(entropy_after_letter_guess) + probability_of_no_letter * (1 + approximate_y(entropy_after_no_letter_guess))



        letters_and_their_corresponding_expected_wrong_guesses[letter] = expected_wrong_guesses_of_letter
        

    
    sorted_letters = dict(sorted(letters_and_their_corresponding_expected_wrong_guesses.items(), key=lambda item: item[1]))



    return sorted_letters



def structure_of_hangman_best_first_guesses():
    best_first_guesses = {x: "" for x in lengths}



    for x in lengths:
        word_list_according_to_information = {word: count for word, count in word_list.items() if len(word) == x}
        list_of_best_guesses_in_order = find_the_best_guess_with_informationtheory(word_list_according_to_information)
        best_guess = list(list_of_best_guesses_in_order.keys())[0]
        best_first_guesses[x] = best_guess
    


    return(best_first_guesses)



PreCalculations3_best_first_guesses = structure_of_hangman_best_first_guesses()