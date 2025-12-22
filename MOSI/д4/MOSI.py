import random
from math import gcd


RUSSIAN_ALPHABET = {
    'А': 10, 'Б': 11, 'В': 12, 'Г': 13, 'Д': 14, 'Е': 15, 'Ж': 16, 'З': 17, 'И': 18, 'Й': 19,
    'К': 20, 'Л': 21, 'М': 22, 'Н': 23, 'О': 24, 'П': 25, 'Р': 26, 'С': 27, 'Т': 28, 'У': 29,
    'Ф': 30, 'Х': 31, 'Ц': 32, 'Ч': 33, 'Ш': 34, 'Щ': 35, 'Ъ': 36, 'Ы': 37, 'Ь': 38, 'Э': 39,
    'Ю': 40, 'Я': 41, ' ': 99
}
REVERSE_ALPHABET = {v: k for k, v in RUSSIAN_ALPHABET.items()}

    #Расширенный алгоритм Евклида для нахождения НОД и коэффициентов
def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0
    d, x1, y1 = extended_gcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return d, x, y


    #Нахождение обратного элемента по модулю m
def mod_inverse(a, m):
    d, x, y = extended_gcd(a, m)
    if d != 1:
        raise ValueError(f"Обратный элемент не существует для a={a}, m={m}")
    return x % m


    #Бинарное возведение в степень по модулю (быстрое возведение в степень)
def binary_pow(base, exponent, modulus):
    result = 1
    base = base % modulus
    
    while exponent > 0:
        if exponent & 1:
            result = (result * base) % modulus
        base = (base * base) % modulus
        exponent >>= 1
    
    return result


    #Проверка, являются ли числа взаимно простыми
def is_coprime(a, b):
    return gcd(a, b) == 1


    #Генерация пар открытых/закрытых ключей
def generate_keys(p, q, num_keys=3):
    n = p * q
    phi = (p - 1) * (q - 1)
    
    keys = []
    
    for _ in range(num_keys):
        while True:
            e = random.randint(2, phi - 1)
            if is_coprime(e, phi):
                break
        
        d = mod_inverse(e, phi)
        
        keys.append({
            'public': (e, n),
            'private': (d, n),
            'p': p,
            'q': q,
            'phi': phi
        })
    
    return keys



def text_to_numbers(text):
    text = text.upper()
    numbers = []
    for char in text:
        if char in RUSSIAN_ALPHABET:
            numbers.append(RUSSIAN_ALPHABET[char])
        else:
            numbers.append(99)
    return numbers

def numbers_to_text(numbers):
    text = ""
    for num in numbers:
        if num in REVERSE_ALPHABET:
            text += REVERSE_ALPHABET[num]
        else:
            text += ' '
    return text


def split_into_blocks(numbers, n):
    n_str = str(n)
    max_len = len(n_str) - 1  
    
    blocks = []
    current_block = ""
    
    for num in numbers:
        num_str = str(num)
        
        if current_block and int(current_block + num_str[0]) == 0:
            if current_block:
                blocks.append(int(current_block))
            current_block = num_str
        else:
            test_block = current_block + num_str
            
            if int(test_block) < n and len(test_block) <= max_len:
                current_block = test_block
            else:
                if current_block:
                    blocks.append(int(current_block))
                current_block = num_str
    if current_block:
        blocks.append(int(current_block))
    
    return blocks

def combine_blocks(blocks):
    numbers = []
    for block in blocks:
        block_str = str(block)
        i = 0
        while i < len(block_str):
            if i + 2 <= len(block_str):
                two_digit = int(block_str[i:i+2])
                if 10 <= two_digit <= 99:
                    numbers.append(two_digit)
                    i += 2
                    continue            
            i += 1
    return numbers


def encrypt_blocks(blocks, public_key):
    e, n = public_key
    encrypted_blocks = []
    
    for block in blocks:
        if block >= n:
            raise ValueError(f"Блок {block} больше или равен модулю n={n}")
        
        encrypted_block = binary_pow(block, e, n)
        encrypted_blocks.append(encrypted_block)
    
    return encrypted_blocks

def decrypt_blocks(encrypted_blocks, private_key):
    d, n = private_key
    decrypted_blocks = []
    
    for block in encrypted_blocks:
        decrypted_block = binary_pow(block, d, n)
        decrypted_blocks.append(decrypted_block)
    
    return decrypted_blocks



def main():
    
    variant = 19
    p = 181
    q = 331
    
    print(f"\nВариант {variant}: p = {p}, q = {q}")
    print(f"n = p * q = {p} * {q} = {p * q}")
    print(f"φ(n) = (p-1)*(q-1) = {p-1} * {q-1} = {(p-1)*(q-1)}")
    
    # 2.1 Генерация ключей
    print("\n" + "=" * 60)
    print("2.1 ГЕНЕРАЦИЯ ПАР ОТКРЫТЫХ/ЗАКРЫТЫХ КЛЮЧЕЙ")
    print("=" * 60)
    
    keys = generate_keys(p, q, num_keys=3)
    
    for i, key_pair in enumerate(keys, 1):
        print(f"\n--- Пара ключей #{i} ---")
        print(f"Открытый ключ (e, n): ({key_pair['public'][0]}, {key_pair['public'][1]})")
        print(f"Закрытый ключ (d, n): ({key_pair['private'][0]}, {key_pair['private'][1]})")
        print(f"Проверка: e * d mod φ(n) = {key_pair['public'][0]} * {key_pair['private'][0]} mod {key_pair['phi']} = "
              f"{(key_pair['public'][0] * key_pair['private'][0]) % key_pair['phi']}")
    
    # 2.2 Шифрование и расшифрование текста
    print("\n" + "=" * 60)
    print("2.2 ШИФРОВАНИЕ И РАСШИФРОВАНИЕ ТЕКСТА")
    print("=" * 60)
    
    # Ввод текста
    text = input("\nВведите текст для шифрования: ")
    
    # Преобразование текста в числа
    numbers = text_to_numbers(text)
    print(f"\nТекст в числовом представлении: {numbers}")
    
    # Выбор ключа для шифрования
    print("\nДоступные ключи:")
    for i, key_pair in enumerate(keys, 1):
        print(f"{i}. Открытый ключ: ({key_pair['public'][0]}, {key_pair['public'][1]})")
    
    key_choice = int(input("\nВыберите ключ для шифрования (1-3): ")) - 1
    
    if key_choice < 0 or key_choice >= len(keys):
        print("Неверный выбор, используется ключ #1")
        key_choice = 0
    
    selected_key = keys[key_choice]
    public_key = selected_key['public']
    private_key = selected_key['private']
    
    # Разбиение на блоки
    blocks = split_into_blocks(numbers, public_key[1])
    print(f"\nБлоки для шифрования (меньше n={public_key[1]}): {blocks}")
    
    # Шифрование
    encrypted_blocks = encrypt_blocks(blocks, public_key)
    print(f"\nЗашифрованные блоки: {encrypted_blocks}")
    
    # Расшифрование
    decrypted_blocks = decrypt_blocks(encrypted_blocks, private_key)
    print(f"\nРасшифрованные блоки: {decrypted_blocks}")
    
    # Проверка совпадения блоков
    if blocks == decrypted_blocks:
        print("Блоки совпадают после расшифрования!")
    else:
        print("Ошибка: блоки не совпадают после расшифрования!")
    
    # Объединение блоков обратно в числа
    decrypted_numbers = combine_blocks(decrypted_blocks)
    print(f"\nРасшифрованные числа: {decrypted_numbers}")
    
    # Преобразование чисел обратно в текст
    decrypted_text = numbers_to_text(decrypted_numbers)
    print(f"\nРасшифрованный текст: {decrypted_text}")
    
    # Проверка совпадения текста
    if text.upper() == decrypted_text:
        print("Текст успешно расшифрован!")
    else:
        print("Ошибка: текст не совпадает после расшифрования!")
    
    # Демонстрация с другими ключами
    print("\n" + "=" * 60)
    print("ДЕМОНСТРАЦИЯ С ДРУГИМИ КЛЮЧАМИ")
    print("=" * 60)
    
    for i, key_pair in enumerate(keys, 1):
        if i-1 != key_choice:
            print(f"\n--- Шифрование с ключом #{i} ---")
            print(f"Открытый ключ: ({key_pair['public'][0]}, {key_pair['public'][1]})")
            
            blocks_i = split_into_blocks(numbers, key_pair['public'][1])
            encrypted_i = encrypt_blocks(blocks_i, key_pair['public'])
            decrypted_i = decrypt_blocks(encrypted_i, key_pair['private'])
            
            print(f"Зашифровано: {encrypted_i[:3]}..." if len(encrypted_i) > 3 else f"Зашифровано: {encrypted_i}")
            print(f"Расшифровано: {decrypted_i == blocks_i}")
    

main()
