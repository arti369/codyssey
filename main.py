filename = 'mission_computer_main.log'

with open(filename, 'r', encoding='utf-8') as file:
    contents = file.read()
    print(contents)