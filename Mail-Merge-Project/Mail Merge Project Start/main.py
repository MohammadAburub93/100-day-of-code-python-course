PLACEHOLDER = "[name]"

with open("./Input/Names/invited_names.txt") as names:
    list_of_names = names.readlines()

with open("./Input/Letters/starting_letter.txt") as letter:
    letter_content = letter.read()
for name in list_of_names:
    stripped_name = name.strip()
    new_letter = letter_content.replace(PLACEHOLDER, stripped_name)

    with open(f"./Output/ReadyToSend/letter_for_{stripped_name}.txt", mode="w") as letter:
        letter.write(new_letter)

























#Hint1: This method will help you: https://www.w3schools.com/python/ref_file_readlines.asp
    #Hint2: This method will also help you: https://www.w3schools.com/python/ref_string_replace.asp
        #Hint3: THis method will help you: https://www.w3schools.com/python/ref_string_strip.asp