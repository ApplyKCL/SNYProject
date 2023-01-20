import random


# function that to generate random number
def get_number_string(char_num=6):
    random_str = ''
    for number in range(char_num):
        random_str += str(random.randrange(0, 9))
    return random_str


# Funtion that used to file the employee load str
def fill_string(num_str=5, char_num=6, string='{},{},{},{},{}'):
    str_list = []
    for number in range(num_str):
        str_list.append(get_number_string(char_num=char_num))

    string = string.format(str_list[0], str_list[1], str_list[2], str_list[3], str_list[4])
    return string
