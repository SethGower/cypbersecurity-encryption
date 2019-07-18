def substitution_cipher(alphabet, key, message):
    """substitution_cipher
    This is a simple function to make a substitution cipher
    Parameters:
        alphabet: a list of the alphabet that is used
        key: the scrambled alphabet. Must have all of the same characters, just in different order. Each index in the
            key is mapped to the same index in the alphabet
        message: The message which is to be encrypted

    Returns:
        cipher_message: A string which is the result
    """
    cipher_message = ""
    for char in message:
        if char in alphabet:
            index = alphabet.index(char)
            cipher_message += key[index]
        else:
            cipher_message += char # if the char isn't in the alphabet (punctuation etc), just add it unecrypted
    return cipher_message


def shift_cipher(alphabet, key, message):
    """
    Simple shift cipher
    :param alphabet: alphabet which to shift
    :param key: key by which to shift
    :param message: message to encrypt
    :return cipher_message: encrypted message
    """
    cipher_message = ""
    shift_alph = alphabet[key:] + alphabet[:key]
    for char in message.lower():
        if char in alphabet:
            index = alphabet.index(char)
            cipher_message += shift_alph[index]
        else:
            cipher_message += char
    return cipher_message


def shift_brute_force(alphabet, message):
    """
    Shift brute force. Tries all possible shifts, based on length of alphabet in use
    :param alphabet: alphabet which is being tested
    :param message: message to break
    :return message_list: list of all of the attempts
    """
    message_list = []
    for i in range(len(alphabet)):
        attempt = ""
        new_alph = alphabet[i:] + alphabet[:i]
        for char in message:
            if char in alphabet:
                index = new_alph.index(char)
                attempt += alphabet[index]
            else:
                attempt += char
        message_list.append(attempt)
    return message_list


def frequency_decrypt(alphabet, frequency_list, cipher_message):
    """
    Attempt at frequency analysis to break cipher
    :param alphabet: alphabet to use
    :param frequency_list: the list of how the frequencies in sample set to test against
    :param cipher_message: message to decrypt
    :return message: the message that was "decrypted"
    """
    message = ""
    cipher_frequencies = analyze_frequencies(alphabet, cipher_message)

    cipher_frequencies.sort(key=lambda tup: tup[1], reverse=True)
    frequency_list.sort(key=lambda tup: tup[1], reverse=True)

    cipher_frequencies = [x[0] for x in cipher_frequencies]
    frequency_list = [x[0] for x in frequency_list]

    for char in cipher_message:
        if char in alphabet and char in cipher_frequencies:
            index = cipher_frequencies.index(char)
            message += frequency_list[index]
        elif char.lower() in alphabet:
            index = cipher_frequencies.index(char.lower())
            message += frequency_list[index].capitalize()
        else:
            message += char
    return message


def analyze_frequencies(alphabet, message):
    """
    Analyze the frequencies in a given sample. Stored in a list of lists, where each index has a 2 item list, with the
        letter and the number of times that letter occurs
    :param alphabet: alphabet against which to test
    :param message: sample to analyze
    :return frequencies: list of the frequencies
    """
    frequencies = []
    for char in message:
        if char.lower() in alphabet:
            keys = [i[0] for i in frequencies]
            if char.lower() in keys:
                index = keys.index(char.lower())
                frequencies[index][1] += 1
            else:
                frequencies.append([char.lower(), 1])
    frequencies.sort(key=lambda tup: tup[1], reverse=True)

    # total = 0
    # for letter in frequencies:
    #     print(letter[0] + ": " + str(letter[1]))
    #     total += letter[1]
    return frequencies


def vigenere(alphabet, codeword, message):
    """
    Simple vigenere cipher
    :param alphabet: alphabet which to use
    :param codeword: codeword with which to encrypt
    :param message: message to encrypt
    :return cipher_message:
    """
    cipher_message = ""
    codeword = codeword.lower()
    message = message.lower()
    counter = 0 # counter to keep track of where in the codeword
    for i in range(len(message)):
        if message[i] not in alphabet:
            cipher_message += message[i]
            pass

        if counter == len(codeword):  # if gotten to end of codeword, then restart in codeword
            counter = 0
        curr_key = alphabet.index(codeword[counter])
        if curr_key == 0:
            new_alph = alphabet
        else:
            new_alph = alphabet[curr_key:] + alphabet[:curr_key]

        index = alphabet.index(message[i])
        cipher_message += new_alph[index]
    return cipher_message


def xor_stream(message, key):
    """
    Function to perform an XOR stream cipher, given a key. This is the provided XOR stream cipher, I think it is
        terrible. See xor()

    :param message: Message to encrypt
    :param key: Key with which to encrypt
    :return cipher: Encrypted Message

    """
    code_ints = [int(i) for i in str(message)]
    key_ints = [int(i) for i in str(key)]
    cipher_ints = [code_ints[i] ^ key_ints[i] for i in range(len(code_ints))]
    cipher = "".join(str(b) for b in cipher_ints)
    return cipher


def xor(message, key):
    """
    Better xor cipher, uses binary data from given data.
    :param message: a string message to encrypt/decrypt
    :param key: a key with which to encrypt/decrypt
    :return: encrypted/decrypted message
    """
    message = message.encode('ascii') # encodes the strings as binary bytes in ASCII, not UTF-8
    key = key.encode('ascii')
    cipher = []
    counter = 0  # similar to vigenere, keep track in key
    for i in range(len(message)):
        if counter >= len(key):  # if end of key, restart
            counter = 0
        xor_byte = message[i] ^ key[counter]  # the integer value of the xor of the two bytes
        cipher.append((chr(xor_byte)))  # append the casted version of the xor output
        counter += 1
    return "".join(cipher)  # returns the list as a string
