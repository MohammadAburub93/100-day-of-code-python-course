import pandas

nato_alphabet = pandas.read_csv("nato_phonetic_alphabet.csv")

letters_reference = {row.letter:row.code for (index, row) in nato_alphabet.iterrows()}


user_name = input("Enter the word: ").upper()
coded_word = [letters_reference[letter] for letter in user_name]
print(coded_word)