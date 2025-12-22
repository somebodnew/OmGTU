# alphabet    -   алфавит
# length      -   мощность алфавита
# input_text  -   входные данные
# output_text -   выходные данные
# k           -   ключ
# flag        -   флажок: -1 значит расшифровку, 1 зашифровку
def CESARE(alphabet, length, input_text_unedited, output_text, k, flag = -1):
    input_text = input_edit(input_text_unedited)
    for x in range(len(input_text)):        # перебор индекса буковок в тексте
        for i in range(length):             # перебор индекса для буковок в алфавите
            if  input_text[x] == alphabet[i]:                   # сравнивает буковы и если они совпадают, мы
                output_text[x] = alphabet[(i+k*flag+length)%length]  # добавляем ключ и длину алфавита, а затем берем остаток от деления на длину
                break                                           # Т.О., мы по кругу вычетов перемещаемся туда или обратно
    if flag == 1:               # вывод если шифровали
        print(f"\nОткрытй текст - {input_text}\nШифрованный текст(ключ - {k}) - {"".join(output_text)}\n")
        with open("encrypted.txt", "a", encoding="utf-8") as f:
            f.write("".join(output_text))
            f.write(str(k)+"\n")
    elif flag == -1:            # вывод если не шифвроали
        print(f"\nЗашифрованный текст  - {input_text}\nОткрытый текст(ключ = {k}) - {"".join(output_text)}\n")
        with open("decrypted.txt", "a", encoding="utf-8") as f:
            f.write("".join(output_text))
            f.write(str(k)+"\n")


def input_edit(text):
    text = text.lower()
    text = text.replace("ё","е")
    return text # меняет регистр и заменяет ё на е

def choice(length = 32):  # Для меню, при выборе 1 и 2
    moreoptions = input("Чтение с файла? (Y/N) ").lower()
    if moreoptions == "y":
        filename = input("Введите полное имя файла ")
        with open(filename,"r", encoding="utf-8") as file:
            input_text = file.readline().rstrip('\n')
            key = int(file.readline().rstrip('\n'))
    elif moreoptions == "n":
        input_text = input("Ввод текста: ")
        key = int(input("Ввод ключа(в диапазоне 1-31): "))
    
    while key == 0 or key == length:
        key = int(input("Ключ не повлияет ни на что, введите другой в диапазоне 1-31: "))

    if not 1 <= key <= length - 1:
        key = key%32
        print("Ключ не входит в диапазон и будет сокращен до ",key)
                  
    return (input_text,key)

# создание или перезапись файлов при запуске программы
with open("encrypted.txt", "w", encoding="utf-8") as f:
    print()
with open("decrypted.txt", "w", encoding="utf-8") as f:
    print()
with open("var19.txt", "w", encoding="utf-8") as f:
    f.write("енуждимонуошфсврфкижклпчшиошлсвублулчэжчшвещйцбнлуолчфилчшоозфслнувочэжчшоллчшвшфсврффшчщшчшиолгшоыкищынфс")


# алфавит и его мощность
alphabet = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
length = len(alphabet)

menu = True
while(menu):
    print("Выберите пункт ","1 - Зашифровать ОТ","2 - Расшифровать ШТ","3 - Выполнить вариантное задание","4 - Завершить программу",sep="\n")
    assignment = input()
    if  assignment == "1":  # пользователь вводит ОТ и ключ, получает ШТ
        input_text, key = choice(length) # См. функцию выше
        CESARE(alphabet, length, input_text, list(input_text), int(key), 1)
        print("Сохранено в файле encrypted.txt\n\n")
    
    elif assignment == "2":  # пользователь вводит ШТ и ключ, получает ОТ
        input_text, key = choice(length) # См. функцию выше
        CESARE(alphabet, length, input_text, list(input_text), int(key))
        print("Сохранено в файле decrypted.txt")
    
    elif assignment == "3":  # выводятся попеременно варианты перебора
        choose_variant = "var" + input("Введите ваш вариант задания ") + ".txt"
        with open(choose_variant, encoding="utf-8") as file:
            input_text = file.readline()
        for i in range(1,length):
            CESARE(alphabet, length, input_text, list(input_text), i)
            accept = input("Правильно?  Y/N ").lower()
            if accept == "y":
                with open("ans"+choose_variant,'r', encoding="utf-8") as file:
                    for n in range(5):
                        print(file.readline())
                break
    elif assignment == "4":
        menu = False

#ans = ["язнаювжизнитолькодвадействительныенесчастьяугрызениесовестииболезньисчастиеестьтолькоотсутствиеэтихдвухзол","6",
#       "толстойвойнаимиртомвторойчастьвторая","шфсчшфпифпужотоцшфтишфцфпэжчшвишфцже"]

# Вывод ответа на задание, программой выведены были 
# все варианты ОТ, вручную затем найден тот, 
# что имеет смысл, в интернете по нему 
# найдена оставшаяся часть ответа
