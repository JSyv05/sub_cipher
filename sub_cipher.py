# TODO:
# add in different key generators (shift, rotation)
# Implement cracker functionality

import argparse
import os
import random

alphabet = "abcdefghijklmnopqrstuvwxyz"
most_common_letter = "etaoinsrhdlucmfywgpbvkxqjz"
common_english_words = [
    " the ",
    " be ",
    " to ",
    " of ",
    " and ",
    " a ",
    " in ",
    " that ",
    " have ",
    " i ",
]

folder_path = "output"

plain_text_path = folder_path + "/plain_text.txt"
cipher_text_path = folder_path + "/cipher_text.txt"
key_path = folder_path + "/key.txt"
freq_table_path = folder_path + "/freq_table.txt"

alphabet_length = len(alphabet)


# this function will accept a file, a key, and an alphabet.
# The function will create a map of the original key to the
# alphabet, then replace each instance of a letter in the
# plain text with the key letter associated with it
def sub_encrypt(plain_text, key, alphabet):
    key_map = dict(zip(alphabet, key))
    print(f"Alphabet: {alphabet}")
    print(f"Key: {key}")
    print(f"Cipher text: {plain_text}")
    print(f"Map: {key_map}")
    print("Encrypting...")
    result = [key_map.get(letter.lower(), letter) for letter in plain_text]
    joined_result = "".join(result)
    print(f"Encrypted text: {joined_result}")
    return joined_result


# this function operates in the same way, but rather than mapping
# the key to the alphabet, it maps the alphabet to the key
def sub_decrypt(cipher_text, key, alphabet):
    alpha_map = dict(zip(key, alphabet))
    print(f"Alphabet: {alphabet}")
    print(f"Key: {key}")
    print(f"Cipher text: {cipher_text}")
    print(f"Map: {alpha_map}")
    print("Decrypting...")
    result = [alpha_map.get(letter.lower(), letter) for letter in cipher_text]
    joined_result = "".join(result)
    print(f"Decrypted text: {joined_result}")
    return joined_result


# gen_key will take the english alphabet, break it into a list,
# shuffle the list, join the list into a string, and return the
# result

# TODO: Implement secure key generation


def gen_key():
    letter_list = list(alphabet)
    print("Generating key...")
    random.shuffle(letter_list)  # this isn't secure, but works :P
    result = "".join(letter_list)
    print(f"Generated key: {result}", "\n")
    return result


def gen_freq_table(text, alphabet):
    print(f"Cipher text: {text}")
    print("Generating frequency table...")
    freq_table = {}
    for char in text:
        if char.isalpha():
            if char in freq_table:
                freq_table[char] += 1
            else:
                freq_table[char] = 1
    alphabet_set = set(alphabet)
    input_chars = set(text.lower())
    missing_letters_set = sorted(alphabet_set - input_chars)
    missing_letters = "".join(missing_letters_set)
    for char in missing_letters:
        freq_table[char] = 0

    print(f"Frequency table: {freq_table}")
    print("Sorting...")
    sorted_freq_table = sorted(
        freq_table.items(), key=lambda item: item[1], reverse=True
    )
    print(f"Sorted frequency table: {sorted_freq_table}")
    return sorted_freq_table


def crack():
    pass


def main():
    parser = argparse.ArgumentParser(
        description="a cli tool for encrypting and decrypting text files using the substitution cipher"
    )

    parser.add_argument(
        "-e", "--encrypt", help="enables encryption mode", action="store_true"
    )
    parser.add_argument(
        "-d", "--decrypt", help="enables decryption mode", action="store_true"
    )

    parser.add_argument(
        "textfile", help="a file containing either plaintext or ciphertext"
    )

    parser.add_argument(
        "key",
        nargs="?",
        default=None,
        help="your key that you want to use, either as a file or argument",
    )

    parser.add_argument(
        "--nokey",
        help="generates a random key when encrypting, generates freq. table when decrypting",
        action="store_true",
    )

    parser.add_argument(
        "--crack",
        help="attempts to crack text with patterns. generates possible keys and solutions",
        action="store_true",
    )

    args = parser.parse_args()

    if not bool(args.encrypt) ^ bool(args.decrypt):
        print("ERR: Must select either encryption or decryption")

    if not (os.path.isfile(args.textfile) and os.access(args.textfile, os.R_OK)):
        print(f"ERR: Text file {args.textfile} does not exist")
        return

    elif args.encrypt:
        with open(args.textfile, "r") as text_file:
            os.makedirs(folder_path, exist_ok=True)
            if bool(not args.key) ^ bool(args.nokey):
                print("ERR: Must specify key or no key")
                return
            elif args.nokey:
                key = gen_key()
            elif args.key:
                if os.path.isfile(args.key) and os.access(args.key, os.R_OK):
                    key_file = open(args.key, "r")
                    key = key_file.read()
                    key = (
                        key.replace("'", "")
                        .replace("[", "")
                        .replace("]", "")
                        .replace("\n", "")
                    )
                    key_file.close()
                else:
                    key = args.key
            else:
                print("ERR: Unhandled error occured")
                return

            if len(key) != alphabet_length:
                print(f"ERR: Key must be {alphabet_length} letters long ({len(key)})")
                return

            for char in key:
                if key.count(char) > 1:
                    print(
                        f"ERR: Key cannot contain duplicate letters ({char}, {key.count(char)})"
                    )
                    return

            plain_text = text_file.read().replace("\n", "")

            cipher_output = sub_encrypt(plain_text, key, alphabet)

            cipher_file = open(cipher_text_path, "w")
            cipher_file.write(repr(cipher_output))
            cipher_file.close()

            key_file = open(key_path, "w")
            key_file.write(repr(key))
            key_file.close()

    elif args.decrypt:
        with open(args.textfile, "r") as text_file:
            os.makedirs(folder_path, exist_ok=True)
            if not bool(args.key) ^ bool(args.nokey):
                print("ERR: Must specify key or no key")
                return
            elif args.nokey:
                cipher_text = text_file.read().replace("'", "").lower()
                freq_table = gen_freq_table(cipher_text, alphabet)
                freq_table_file = open(freq_table_path, "w")
                freq_table_file.write(repr(freq_table))
                freq_table_file.close()
                return
            elif args.key:
                if os.path.isfile(args.key) and os.access(args.key, os.R_OK):
                    key_file = open(args.key, "r")
                    key = key_file.read()
                    key = (
                        key.replace("'", "")
                        .replace("[", "")
                        .replace("]", "")
                        .replace("\n", "")
                    )
                    key_file.close()
                else:
                    key = args.key

            else:
                print("ERR: Unhandled error occured")
                return

            if len(key) != alphabet_length:
                print(f"ERR: Key must be {alphabet_length} letters long ({len(key)})")
                print(str(key))
                return

            for char in key:
                if key.count(char) > 1:
                    print(
                        f"ERR: Key cannot contain duplicate letters ({char}, {key.count(char)})"
                    )
                    return

            cipher_text = text_file.read().replace("'", "").replace("\n", "")
            plain_output = sub_decrypt(cipher_text, key, alphabet)
            plain_text_file = open(plain_text_path, "w")
            plain_text_file.write(repr(plain_output))
            plain_text_file.close()

            key_file = open(key_path, "w")
            key_file.write(repr(key))
            key_file.close()


if __name__ == "__main__":
    main()
