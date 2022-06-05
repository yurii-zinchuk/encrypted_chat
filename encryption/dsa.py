import random

import time

def DSA_encode(message, p, q, g, x):
    """
    Encodes a message using DSA
    :param message: message to be encoded
    :param p: prime number
    :param q: prime number
    :param g: generator
    :return: encoded message
    """
    h = hash(message)
    r = 0

    while r == 0:
        k = random.randint(1, q-1)
        r = ((g ** k) % p) % q
        s = (modular_multiplicative_inverse(k, q)*(h+x*r)) % q
    return r, s


def modular_multiplicative_inverse(number, module):
    """Finds modular multiplicative inverse"""
    number_inversed = 0
    while (number * number_inversed) % module != 1:
        number_inversed += 1
    return number_inversed


def DSA_check_signature(message, p, q, g, y, r, s):
    """
    Decodes a message using DSA
    :param r: encoded message
    :param s: encoded message
    :param p: prime number
    :param q: prime number
    :param g: generator
    :return: decoded message
    """

    w = modular_multiplicative_inverse(s, q) % q
    u1 = (hash(message) * w) % q
    u2 = (r*w) % q
    v = ((((g**u1) * (y**u2)) % p) % q)
    return v == r


def encode(message):
    """Creates signature for message

    Args:
        message (str): message which is going to be sent

    Returns:
        tuple: message and packet with signature
    """
    p = 10091       # It should be bigger for better secure(e.g. 512 bit - 1024 bit) *prime number
    q = 1009        # p = q*k + 1 (p is also prime)
    for h in range(p):
        if (h**((p-1)/q)) % p > 1:
            g = int((h**((p-1)/q)) % p)
            break
    x = random.randint(0, q)  # private_key
    y = (g**x) % p  # public_key
    # the private key package is {p,q,g,x}.
    # The public key package is {p,q,g,y}.
    r, s = DSA_encode(message, p, q, g, x)
    return message, (p, q, g, y, r, s)


def check_signature(message_packet):
    """Checks signature validity

    Args:
        message_packet (tuple): message and packet with signature

    Returns:
        str: message
    """
    message, (p, q, g, y, r, s) = message_packet
    if DSA_check_signature(message, p, q, g, y, r, s):
        return message
    else:
        return False


def DSA_example():
    message = input('Please, type your message: ')
    for i in range(12):
        if i == 11:
            print(f"\rencoding{'.'*(i%4)}    ")
        else:
            print(f"\rencoding{'.'*(i%4)}    ", end='')
        time.sleep(0.2)
    
    message_packet = encode(message)

    for i in range(12):
        if i == 11:
            print(f"\rsending packet{'.'*(i%4)}   ")
        else:
            print(f"\rsending packet{'.'*(i%4)}   ", end='')
        time.sleep(0.2)

    print('Message packet:', message_packet)
    print("Encoded message signature:", message_packet[1][-2], message_packet[1][-1])
    time.sleep(3)
    # the private key package is {p,q,g,x}.
    # The public key package is {p,q,g,y}.
    print('\n\n(Another user)\nNow lets check signature validity')
    
    for i in range(12):
        if i == 11:
            print(f"\rChecking{'.'*(i%4)}   ")
        else:
            print(f"\rChecking{'.'*(i%4)}   ", end='')
        time.sleep(0.2)

    if check_signature(message_packet) is not False:
        print("Signature is valid!")
        print("Your message:", check_signature(message_packet))
    else:
        print('Signature is not valid!')


if __name__=='__main__':
    DSA_example()
