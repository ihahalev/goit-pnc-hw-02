import os

alphabet_upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
alphabet_lower = "abcdefghijklmnopqrstuvwxyz"

def transposition_col_encrypt(text: str, key: str) -> str:
    num_cols = len(key)
    num_rows = len(text) // num_cols + (1 if len(text) % num_cols else 0)
    padded_text = text.ljust(num_cols * num_rows)
    # for r in range(num_rows):
    #     print(padded_text[r*num_cols:(r+1)*num_cols])
    encrypted_text = ['']* num_cols
    for col in range(num_cols) :
        for row in range (num_rows):
            encrypted_text[col] += padded_text[row*num_cols + col]
    return ''.join(encrypted_text)

def transposition_col_decrypt(encrypted_text: str, key: str) -> str:
    num_cols = len(key)
    num_rows = len(encrypted_text) // num_cols + (1 if len(encrypted_text) % num_cols else 0)
    padded_text = encrypted_text.ljust(num_cols * num_rows)
    # for c in range(num_cols):
    #     print(padded_text[c*num_rows:(c+1)*num_rows])
    decrypted_text = [''] * num_rows
    for row in range (num_rows):
        for col in range(num_cols) :
            decrypted_text[row] += padded_text[col*num_rows + row]
    return ''.join(decrypted_text).strip()

def transposition_row_encrypt(text: str, key: str) -> str:
    num_rows = len(key)
    num_cols = len(text) // num_rows + (1 if len(text) % num_rows else 0)
    padded_text = text.ljust(num_rows * num_cols)
    # for c in range(num_cols):
    #     print(padded_text[c*num_rows:(c+1)*num_rows])
    encrypted_text = ['']* num_rows
    for row in range (num_rows):
        for col in range(num_cols) :
            encrypted_text[row] += padded_text[col*num_rows + row]
    return ''.join(encrypted_text)

def transposition_row_decrypt(encrypted_text: str, key: str) -> str:
    num_rows = len(key)
    num_cols = len(encrypted_text) // num_rows + (1 if len(text) % num_rows else 0)
    padded_text = encrypted_text.ljust(num_rows * num_cols)
    # for r in range(num_rows):
    #     print(encrypted_text[r*num_cols:(r+1)*num_cols])
    decrypted_text = [''] * num_cols
    for col in range(num_cols) :
        for row in range (num_rows):
            decrypted_text[col] += padded_text[row*num_cols + col]
    return ''.join(decrypted_text).strip()

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

if __name__ == "__main__":
    text = read_file('plain_text.txt')
    key = "SECRET"

    encrypted_text = transposition_col_encrypt(text, key)
    print(f"{os.path.basename(__file__)} Зашифрований текст:", encrypted_text, '\n')

    decrypted_text = transposition_col_decrypt(encrypted_text, key)
    print(f"{os.path.basename(__file__)} Розшифрований текст:", decrypted_text, '\n')

    key2 = "CRYPTO"

    encrypted_double = transposition_row_encrypt(encrypted_text, key2)
    print(f"{os.path.basename(__file__)} Подвійно зашифрований текст:", encrypted_double, '\n')

    decrypted_double = transposition_row_decrypt(encrypted_double, key2)
    print(f"{os.path.basename(__file__)} Розшифрований текст перший рівень:", decrypted_double, '\n')

    decrypted_text = transposition_col_decrypt(decrypted_double, key)
    print(f"{os.path.basename(__file__)} Розшифрований текст другий рівень:", decrypted_text, '\n')
