def translate_word(string):
    temp = string[0]
    k = n = len(string)
    if n % 2 == 0:
        string = string[1:]
        k -= 1
    new_string = string[k//2]
    for i in range(1, k//2 + 1):
        new_string += string[k//2-i]
        new_string += string[k//2+i]
    if n % 2 == 0:
        new_string += temp
    return new_string


def translate_phrase(phrase):
    phrase = phrase.split()
    temp = phrase[0]
    k = n = len(phrase)
    if n % 2 == 0:
        phrase = phrase[1:]
        k -= 1
    new_phrase = [phrase[k//2]]
    for i in range(1, k//2 + 1):
        new_phrase.append(phrase[k//2-i])
        new_phrase.append(phrase[k//2+i])
    if n % 2 == 0:
        new_phrase.append(temp)
    return new_phrase


for i in range(1, 10):
    file1 = open(f"C:\\Users\\Admin\\Downloads\\Тау-Кита1\\Тау-Кита\\input_s1_0{i}.txt")
    file2 = open(f"C:\\Users\\Admin\\Downloads\\Тау-Кита1\\Тау-Кита\\output_s1_0{i}.txt")
    string = file1.readline()
    string = translate_phrase(string)
    new_string = ""
    for word in string:
        new_string += (translate_word(word) + " ")
    new_string = new_string[:-1]
    test = file2.readline()
    print(f"Тест{i}: {new_string == test}")
