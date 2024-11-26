import os
alphabet_upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
alphabet_lower = "abcdefghijklmnopqrstuvwxyz"

def extend_key(text, key) -> str:
    key = list(key)
    if len(text) <= len(key):
        return key
    else:
        for i in range(len(text) - len(key)):
            key.append(key[i % len(key)])
    return ''.join(key)

def vigenere_encrypt(plain_text: str, key: str) -> str:
    key = extend_key(plain_text, key)
    k_low = key.lower()
    ciphered_text = []
    for i in range(len(plain_text)):
        if plain_text[i] in alphabet_upper:
            shift = ord(key[i]) - ord('A')
            x = (alphabet_upper.index(plain_text[i]) + shift) % 26
            x += ord('A')
        elif plain_text[i] in alphabet_lower:
            shift = ord(k_low[i]) - ord('a')
            x = (alphabet_lower.index(plain_text[i]) + shift) % 26
            x += ord('a')
        else:
            x = ord(plain_text[i])
        ciphered_text.append(chr(x))
    return ''.join(ciphered_text)

def vigenere_decrypt(cipher_text, key) -> str:
    key = extend_key(cipher_text, key)
    k_low = key.lower()
    original_text = []
    for i in range(len(cipher_text)):
        if cipher_text[i] in alphabet_upper:
            shift = ord(key[i]) - ord('A')
            x = (alphabet_upper.index(cipher_text[i]) - shift) % 26
            x += ord('A')
        elif cipher_text[i] in alphabet_lower:
            shift = ord(k_low[i]) - ord('a')
            x = (alphabet_lower.index(cipher_text[i]) - shift) % 26
            x += ord('a')
        else:
            x = ord(cipher_text[i])
        original_text.append(chr(x))
    return ''.join(original_text)

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

if __name__ == "__main__":
    text = read_file('plain_text.txt')
    key = "CRYPTOGRAPHY"

    encrypted_text = vigenere_encrypt(text, key)
    print(f"{os.path.basename(__file__)} Зашифрований текст:", encrypted_text)

    decrypted_text = vigenere_decrypt(encrypted_text, key)
    print(f"{os.path.basename(__file__)} Розшифрований текст:", decrypted_text)
