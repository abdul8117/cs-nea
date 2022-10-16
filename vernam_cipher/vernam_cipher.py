def encrypt(plaintext, key):
    """
    Pseudocode

    FUNCTION encrypt(plaintext, key)
        SET cipher_array = []
        
        FOR index IN RANGE(0, LENGTH(plaintext))
            SET cipher_char = plaintext[index] XOR key[index]
            cipher_array.APPEND(cipher_char)
    
        return <cipher_array as a binary object>
    """

    cipher_array = []

    for i in range(len(plaintext)):
        cipher_array.append(ord(plaintext[i]) ^ ord(key[i]))
        # print(cipher_array[i])

    return bytes(cipher_array)


def decrypt(cipher, key):
    """
    Pseudocode

    SET plaintext_array = []

    FUNCTION decrypt(cipher, key)
        FOR i IN RANGE(0, LENGTH(cipher))
            SET plaintext_letter = cipher[i] XOR key[i]
            plaintext_array.APPEND(plaintext_letter)
    
    return <plaintext_array as one string>
            
    """

    plaintext = []
    print(cipher)
    
    for i in range(len(cipher)):
        # print(i)
        plaintext.append(chr(cipher[i] ^ ord(key[i])))
    
    return ''.join(plaintext)



key = "stron2easdddsd"

cipher = encrypt("strongPassword", key)
# plaintext = decrypt(cipher, key)