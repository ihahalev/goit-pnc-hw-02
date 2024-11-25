vigenere = __import__('01_vigenere')

"""За два століття до нашої ери, грецький літератор та історик Полібій створив так званий полібіанський квадрат розмірами 5 на 5,
    заповнений літерами алфавіту у випадковому порядку.
    Для кодування повідомлень за допомогою цього квадрата знаходили літеру з тексту та заміняли її літерою,
    розташованою нижче у тому ж стовпці, або верхньою літерою, якщо вона знаходилася в останньому рядку.
"""
def create_matrix(key: str) -> list[list[str]]:
    matrix = []
    key = ''.join(sorted(set(key), key=lambda x: key.index(x))) # remove repeats
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for char in key:
        if char not in matrix:
            matrix.append(char)
    for char in alphabet:
        if char not in matrix:
            matrix.append(char)
    return [matrix[i:i + 5] for i in range(0, len(matrix), 5)]

def table_encrypt(text: str, key: str) -> str:
    matrix = create_matrix(key)
    for r in matrix:
        print(r)
    encrypted_text = []
    for char in text:
        if char.isalpha():
            for col in range(len(matrix)):
                col_check = []
                for i in range(len(matrix)):
                    try:
                        col_check.append(matrix[i][col])
                    except IndexError:
                        break
                if char.upper() in col_check:
                    row_index = col_check.index(char.upper())
                    row = (row_index + 1) % len(col_check)
                    if char.isupper():
                        encrypted_char = matrix[row][col]
                    else:
                        encrypted_char = matrix[row][col].lower()
                    encrypted_text.append(encrypted_char)
                    break
        else:
            encrypted_text.append(char)
    return ''.join(encrypted_text)

def table_decrypt(encrypted_text: str, key: str) -> str:
    matrix = create_matrix(key)
    decrypted_text = []
    for char in encrypted_text:
        if char.isalpha():
            for col in range(len(matrix)):
                col_check = []
                for i in range(len(matrix)):
                    try:
                        col_check.append(matrix[i][col])
                    except IndexError:
                        break
                if char.upper() in col_check:
                    row_index = col_check.index(char.upper())
                    row = (row_index - 1) % len(col_check)
                    if char.isupper():
                        decrypted_char = matrix[row][col]
                    else:
                        decrypted_char = matrix[row][col].lower()
                    decrypted_text.append(decrypted_char)
                    break
        else:
            decrypted_text.append(char)
    return ''.join(decrypted_text)

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

if __name__ == "__main__":
    text = read_file('plain_text.txt')
    key = "MATRIX"

    encrypted_text = table_encrypt(text, key)
    print("Зашифрований текст:", encrypted_text, '\n')

    decrypted_text = table_decrypt(encrypted_text, key)
    print("Розшифрований текст:", decrypted_text, '\n')

    key2 = "CRYPTO"

    encrypted_vigenere = vigenere.vigenere_encrypt(text, key)
    print("Зашифрований текст Віженером:", encrypted_vigenere, '\n')

    encrypted_double = table_encrypt(encrypted_vigenere, key2)
    print("Подвійно зашифрований текст:", encrypted_double, '\n')

    decrypted_double = table_decrypt(encrypted_double, key2)
    print("Розшифрований текст перший рівень:", decrypted_double, '\n')

    decrypted_text =  vigenere.vigenere_decrypt(decrypted_double, key)
    print("Розшифрований текст другий рівень:", decrypted_text, '\n')
