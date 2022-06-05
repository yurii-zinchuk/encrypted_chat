import random


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
    message, p, q, g, y, r, s = message_packet
    if DSA_check_signature(message, p, q, g, y, r, s):
        return message


def DSA_example():
    message = 'Hello World'
    q = 1009
    p = 10091
    for h in range(p):
        if (h**((p-1)/q)) % p > 1:
            g = int((h**((p-1)/q)) % p)
            break
    x = random.randint(0, q)  # private_key
    y = (g**x) % p  # public_key

    # the private key package is {p,q,g,x}.
    # The public key package is {p,q,g,y}.

    r, s = DSA_encode(message, p, q, g, x)
    print("Encoded message signature:", r, s)
    print("Check signature:", DSA_check_signature(message, p, q, g, y, r, s))


DSA_example()
