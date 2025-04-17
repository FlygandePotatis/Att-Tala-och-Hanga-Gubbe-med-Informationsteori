import math
from ordlista import data
from metod5förberäkning import PreCalculations3_best_first_guesses



word_dict = {}

for line in data.split("\n"):
    word, number = line.split(",")
    word_dict[word] = int(number)

total_count_of_frequency = sum(word_dict.values())

word_list = {word: count / total_count_of_frequency for word, count in word_dict.items()}

best_first_guesses = PreCalculations3_best_first_guesses



def approximate_y(x):
    y = 0.61 * x
    return y



def find_the_best_guess_with_informationtheory(word_list_according_to_information, alphabet):
    letters_and_their_corresponding_expected_wrong_guesses =  {letter: 0 for letter in alphabet}



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



def hangman_using_informationtheory(the_current_word):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    word_list_according_to_information = {word: count for word, count in word_list.items() if len(word) == len(the_current_word)}
    wrong_guesses = 0
    checking_number = 0



    while True:
        if len(word_list_according_to_information) > 1:
            total_probability_according_to_information = sum(word_list_according_to_information.values())
            word_list_according_to_information = {word: count / total_probability_according_to_information for word, count in word_list_according_to_information.items()}



            if checking_number == 1:
                list_of_best_guesses_in_order = find_the_best_guess_with_informationtheory(word_list_according_to_information, alphabet)
                letter_in_word = list(list_of_best_guesses_in_order.keys())[0]
            else:
                letter_in_word = best_first_guesses[len(the_current_word)]
                checking_number = 1
            


            alphabet = alphabet.replace(letter_in_word, '')



            if letter_in_word in the_current_word:
                list_of_places_of_letter = [i for i, char in enumerate(the_current_word) if char == letter_in_word]
                word_list_according_to_information = {word: count for word, count in word_list_according_to_information.items() if has_letter_only_at_positions(word, list_of_places_of_letter, letter_in_word)}
            else:
                wrong_guesses += 1
                word_list_according_to_information = {word: count for word, count in word_list_according_to_information.items() if letter_in_word not in word}

            

            if len(word_list_according_to_information) == 1:
                break
        else:
            if len(word_list_according_to_information) == 1:
                break
    
    

    return wrong_guesses



def has_letter_only_at_positions(word, positions, letter_in_word):
    for i, char in enumerate(word):
        if char == letter_in_word and i not in positions:
            return False
        if i in positions and char != letter_in_word:
            return False
    return True



def structure_of_hangman_statistics():
    wrong_guesses_statistics = {}



    n=1
    for word in word_list:
        wrong_guesses = hangman_using_informationtheory(word)



        if wrong_guesses in wrong_guesses_statistics:
            wrong_guesses_statistics[wrong_guesses] +=  word_list[word]
        else:
            wrong_guesses_statistics[wrong_guesses] =  word_list[word]
        print(n)
        n+=1
    


    wrong_guesses_statistics = dict(sorted(wrong_guesses_statistics.items()))

    print(wrong_guesses_statistics)



structure_of_hangman_statistics()