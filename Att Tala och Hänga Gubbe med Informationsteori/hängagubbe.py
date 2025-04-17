import math
from ordlista import data



word_dict = {}

for line in data.split("\n"):
    word, number = line.split(",")
    word_dict[word] = int(number)

total_count_of_frequency = sum(word_dict.values())

word_list = {word: count / total_count_of_frequency for word, count in word_dict.items()}

best_first_guesses = {1: 'a', 2: 'o', 3: 'e', 4: 'e', 5: 'e', 6: 'e', 7: 'e', 8: 'e', 9: 'e', 10: 'e', 11: 'e', 12: 'i', 13: 'i', 14: 'i', 15: 't', 16: 'e', 17: 'e', 18: 'e', 19: 'e', 20: 'e', 21: 'e', 22: 'e', 23: 'e', 24: 'e', 25: 'a', 26: 's', 
27: 'u', 28: 'a', 29: 'e', 30: 'a', 31: 'e', 32: 'a', 33: 'a', 34: 'e', 35: 'a', 36: 'a', 38: 'a'}



def approximate_y(x):
    y = 0.61 * x
    return y



def can_convert_to_int(input_string):
    try:
        int(input_string)
        return True
    except ValueError:
        return False



def first_question():
    while True:
        yes_or_no = input("Do you want to make sure your word exists? ").lower().strip()
        if yes_or_no == "yes":
            print("You chose yes!")
            check_if_word_exist()
            break
        elif yes_or_no == "no":
            print("You chose no!")
            break
        else:
            print("Invalid input. Please answer with 'yes' or 'no'.")



def check_if_word_exist():
    while True:
        word_chosen_by_player = input("What is the word you think of so we can make sure it exists? ").lower().strip()
        word_exists = (word_chosen_by_player in word_list)
        if word_exists == True:
            print("Your word exists.")
            break
        else:
            print("Your word does not exist. Please try another one.")



def creating_word_list_according_to_lenght():
    while True:
        lenght_of_word = input("What is the length of your word (number of letters)? ")
        if can_convert_to_int(lenght_of_word):
            lenght_of_word = int(lenght_of_word)
            word_list_according_to_lenght_in_funtion = {word: count for word, count in word_list.items() if len(word) == lenght_of_word}
            if len(word_list_according_to_lenght_in_funtion) == 0:
                print("There exists no word with that many letters. Please try again.")
            else:
                break
        else:
            print("Invalid input. Please answer with a number")
    return word_list_according_to_lenght_in_funtion



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



def hangman_using_informationtheory(word_list_according_to_information):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    checking_number = 0


    while True:
        if len(word_list_according_to_information) > 1:
            total_probability_according_to_information = sum(word_list_according_to_information.values())
            word_list_according_to_information = {word: count / total_probability_according_to_information for word, count in word_list_according_to_information.items()}



            if checking_number == 1:
                list_of_best_guesses_in_order = find_the_best_guess_with_informationtheory(word_list_according_to_information, alphabet)
                letter_in_word = list(list_of_best_guesses_in_order.keys())[0]
            else:
                letter_in_word = best_first_guesses[len(list(word_list_according_to_information.keys())[0])]
                checking_number = 1
            


            alphabet = alphabet.replace(letter_in_word, '')



            list_of_places_of_letter = []
            while True:
                yes_or_no = input("Does your word contain the letter " + letter_in_word + "? ").lower().strip()
                if yes_or_no == "yes":
                    print("You chose yes!")



                    while True:
                        place_of_letter = input("In which place is " + letter_in_word + " in your word (answer one place at a time)? ").lower().strip()
                        if can_convert_to_int(place_of_letter):
                            place_of_letter = int(place_of_letter)



                            if place_of_letter <= len(next(iter(word_list_according_to_information))):
                                if place_of_letter not in list_of_places_of_letter:
                                    list_of_places_of_letter.append(place_of_letter)
                                else:
                                    print("You have already said your word has " + letter_in_word + " in place " + str(place_of_letter))



                                word_list_according_to_information = {word: count for word, count in word_list_according_to_information.items() if word[place_of_letter-1] == letter_in_word}



                                while True:
                                    any_more_letters = input("Are there any more " + letter_in_word + ":s in your word? ").lower().strip()
                                    if any_more_letters == "yes" or any_more_letters == "no":
                                        break
                                    else:
                                        print("Invalid input. Please answer with 'yes' or 'no'.")



                                if any_more_letters == "no":
                                    break
                            else:
                                print("There exists no word with that many letters. Please try again.")
                        else:
                            print("Invalid input. Please answer with a number.")
                    


                    list_of_places_of_letter = [pos -1 for pos in list_of_places_of_letter]
                    word_list_according_to_information = {word: count for word, count in word_list_according_to_information.items() if has_letter_only_at_positions(word, list_of_places_of_letter, letter_in_word)}
                    break
                elif yes_or_no == "no":
                    print("You chose no!")
                    word_list_according_to_information = {word: count for word, count in word_list_according_to_information.items() if letter_in_word not in word}
                    break
                else:
                    print("Invalid input. Please answer with 'yes' or 'no'.")
            if len(word_list_according_to_information) == 1:
                end_of_game(word_list_according_to_information)
                break
            elif len(word_list_according_to_information) == 0:
                print("Your word does not exist.")
                break
        else:
            if len(word_list_according_to_information) == 1:
                end_of_game(word_list_according_to_information)
                break
            elif len(word_list_according_to_information) == 0:
                print("Your word does not exist.")
                break



def has_letter_only_at_positions(word, positions, letter_in_word):
    for i, char in enumerate(word):
        if char == letter_in_word and i not in positions:
            return False
        if i in positions and char != letter_in_word:
            return False
    return True



def end_of_game(word_list_according_to_information):
    print("Your word is: " + str(next(iter(word_list_according_to_information))))



def structure_of_hangman():
    print("Welcome to Hangman using Information-theory")
    first_question()
    word_list_according_to_information = creating_word_list_according_to_lenght()
    hangman_using_informationtheory(word_list_according_to_information)



structure_of_hangman()