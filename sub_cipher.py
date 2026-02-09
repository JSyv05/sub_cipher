# TODO:
# - Add in different key generators (shift, rotation)
# - Implement cracker functionality
# - Implement secure key generation
# - Allow alphabets and common words to be controlled in a
# config file
# - Have the iteration loop break when a near match is found

import argparse
import os
import random
import re

# from thefuzz import fuzz, process

# Common words like it, is, in, a, and I are not
# included because they are either too similar to
# eachother and/or are too short to reliably perform
# swaps based on them
alphabet = "abcdefghijklmnopqrstuvwxyz"
most_common_letters = "etaoinsrhdlucmfywgpbvkxqjz"
common_english_words = [
    " the ",
    " be ",
    " to ",
    " of ",
    " and ",
    " that ",
    " have ",
    " you ",
]

folder_path = "output"

plain_text_path = folder_path + "/plain_text.txt"
cipher_text_path = folder_path + "/cipher_text.txt"
key_path = folder_path + "/key.txt"
freq_table_path = folder_path + "/freq_table.txt"
crack_path = folder_path + "/crack_iterations.txt"


def write_file(content, path):
    file = open(path, "w")
    file.write(repr(content))
    file.close()


# this function will accept a file, a key, and an alphabet.
# The function will create a map of the original key to the
# alphabet, then replace each instance of a letter in the
# plain text with the key letter associated with it
def sub_encrypt(plain_text, key, alphabet):
    key_map = dict(zip(alphabet, key))
    print(f"Alphabet: {alphabet}\n")
    print(f"Key: {key}\n")
    print(f"Cipher text: {plain_text}\n")
    print(f"Map: {key_map}\n")
    print("Encrypting...")
    result = [key_map.get(letter.lower(), letter) for letter in plain_text]
    joined_result = "".join(result)
    print(f"Encrypted text: {joined_result}\n")
    return joined_result


# this function operates in the same way, but rather than mapping
# the key to the alphabet, it maps the alphabet to the key
def sub_decrypt(cipher_text, key, alphabet):
    alpha_map = dict(zip(key, alphabet))
    print(f"Alphabet: {alphabet}\n")
    print(f"Key: {key}\n")
    print(f"Cipher text: {cipher_text}\n")
    print(f"Map: {alpha_map}\n")
    print("Decrypting...")
    result = [alpha_map.get(letter.lower(), letter) for letter in cipher_text]
    joined_result = "".join(result)
    print(f"Decrypted text: {joined_result}\n")
    return joined_result


# gen_key will take the english alphabet, break it into a list,
# shuffle the list, join the list into a string, and return the
# result
def gen_key(alphabet):
    print("Generating key...")
    letter_list = list(alphabet)
    random.shuffle(letter_list)  # this isn't secure, but works :P
    result = "".join(letter_list)
    print(f"Generated key: {result}\n")
    return result


def gen_shift_key(shift_count, alphabet):
    print("Generating shift key...")
    chars_to_shift = alphabet[:shift_count]
    shift_chars = alphabet[shift_count:]
    shift_key = shift_chars + chars_to_shift
    print(f"Generated shift key: {shift_key}\n")
    return shift_key


# This function first generates a dictionary based on how
# many of a letter there are, add in any letters that are
# missing from the string, and then return a sorted list
# of the letters and their frequency
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

    print(f"Frequency table: {freq_table}\n")
    print("Sorting...")
    sorted_freq_table = sorted(
        freq_table.items(), key=lambda item: item[1], reverse=True
    )
    print(f"Sorted frequency table: {sorted_freq_table}\n")
    return sorted_freq_table


# Removes all non-alphabetical characters from a string,
# preserves spaces
def remove_special_chars(text):
    return re.sub(r"[^a-zA-Z\s]", "", text)


# Removes all non-alphabetical characters from a string,
# does not preserve spacing
def remove_special_chars_sub_space(text):
    return re.sub(r"[^a-zA-Z]", "", text)


# Crack will create a frequency table, then generate
# a key based on the frequency of the letters. That
# key will be mapped onto a dict based on the most
# common letters. From there we will iterate through
# the cipher text, generating a key and the text
# based on that key.
def crack(text, alphabet, common_letters):
    print("Cracking...")
    freq_table = str(gen_freq_table(text, alphabet))

    print("Creating key based on frequency table...")
    freq_key = remove_special_chars_sub_space(freq_table)
    print(f"Frequency key: {freq_key}\n")

    print("Generating frequency map...")
    freq_key_map = dict(zip(common_letters, freq_key))
    print(f"Frequency mapping: {freq_key_map}\n")

    print("performing initial swaps...")

    mod_text = text
    mod_key = alphabet
    with open(crack_path, "w") as f:
        f.write("")
    crack_file = open(crack_path, "a")
    for key, value in freq_key_map.items():
        char_to_swap = value + key
        print(f"Chars to swap out: {char_to_swap}")
        crack_file.write(f"Chars to swap out: {char_to_swap}\n")
        swap_char = key + value
        print(f"Chars to swap in: {swap_char}\n")
        crack_file.write(f"Chars to swap out: {swap_char}\n\n")
        translation_table = str.maketrans(char_to_swap, swap_char)
        mod_text = mod_text.translate(translation_table)
        mod_key = mod_key.translate(translation_table)
        print(f"Modified key: {mod_key}")
        crack_file.write(f"Modified key: {mod_key}\n")
        print(f"Modified text: {mod_text}\n")
        crack_file.write(f"Modified text: {mod_text}\n\n")

    crack_file.close()


def crack_shift(text, alphabet):
    print("Cracking using shift cipher...")
    with open(crack_path, "w") as f:
        f.write("")
    crack_file = open(crack_path, "a")
    for i in range(len(alphabet)):
        chars_to_shift = alphabet[:i]
        shift_chars = alphabet[i:]
        mod_key = shift_chars + chars_to_shift
        key_map = dict(zip(alphabet, mod_key))

        mod_list = [key_map.get(letter.lower(), letter) for letter in text]
        mod_text = "".join(mod_list)
        print(f"Shift: {i}")
        crack_file.write(f"Shift: {i}\n")
        print(f"Modified key: {mod_key}")
        crack_file.write(f"Modified key: {mod_key}\n")
        print(f"Modified text: {mod_text}\n")
        crack_file.write(f"Modified text: {mod_text}\n\n")

    crack_file.close()


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

    parser.add_argument(
        "--shift",
        help="generates a shift key when encrypting, shifts iterively when cracking",
        type=int,
        nargs="?",
        const=1,
        default=0,
        dest="shift_value",
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
                if args.shift_value:
                    key = gen_shift_key(args.shift_value, alphabet)
                else:
                    key = gen_key(alphabet)
            elif args.key:
                if os.path.isfile(args.key) and os.access(args.key, os.R_OK):
                    key_file = open(args.key, "r")
                    key = remove_special_chars(key_file.read())
                    key_file.close()
                else:
                    key = args.key
            else:
                print("ERR: Unhandled error occured")
                return

            if len(key) != len(alphabet):
                print(f"ERR: Key must be {len(alphabet)} letters long ({len(key)})")
                return

            for char in key:
                if key.count(char) > 1:
                    print(
                        f"ERR: Key cannot contain duplicate letters ({char}, {key.count(char)})"
                    )
                    return

            plain_text = text_file.read().replace("\n", "")
            cipher_output = sub_encrypt(plain_text, key, alphabet)
            write_file(cipher_output, cipher_text_path)
            write_file(key, key_path)

    elif args.decrypt:
        with open(args.textfile, "r") as text_file:
            os.makedirs(folder_path, exist_ok=True)
            if not bool(args.key) ^ bool(args.nokey):
                print("ERR: Must specify key or no key")
                return
            elif args.nokey:
                cipher_text = remove_special_chars(text_file.read()).lower()
                if args.crack and args.shift_value:
                    crack_shift(cipher_text, alphabet)
                    return
                elif args.crack:
                    crack(cipher_text, alphabet, most_common_letters)
                    return
                else:
                    freq_table = gen_freq_table(cipher_text, alphabet)
                    write_file(freq_table, freq_table_path)
                    return
            elif args.key:
                if os.path.isfile(args.key) and os.access(args.key, os.R_OK):
                    key_file = open(args.key, "r")
                    key = remove_special_chars(key_file.read())
                    key_file.close()
                else:
                    key = args.key

            else:
                print("ERR: Unhandled error occured")
                return

            if len(key) != len(alphabet):
                print(f"ERR: Key must be {len(alphabet)} letters long ({len(key)})")
                return

            for char in key:
                if key.count(char) > 1:
                    print(
                        f"ERR: Key cannot contain duplicate letters ({char}, {key.count(char)})"
                    )
                    return

            cipher_text = remove_special_chars(text_file.read())
            plain_output = sub_decrypt(cipher_text, key, alphabet)
            write_file(plain_output, plain_text_path)
            write_file(key, key_path)


if __name__ == "__main__":
    main()
