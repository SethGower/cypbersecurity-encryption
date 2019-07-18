from ciphers import *
def main():
    message = input("Please input a message to be encrypted: ")
    keyword = input("Please input a codeword: ")
    encrypted = xor(message, keyword)
    print(len(encrypted))
    print(encrypted)
    decrypted = xor(encrypted, keyword)
    print(decrypted)


if __name__ == "__main__":
    main()
