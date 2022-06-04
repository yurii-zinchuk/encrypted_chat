"""
module with Rabin cryptography
technique implementation
"""
import math
from functools import reduce


def keys_generation():
    'generates the keys'

    def is_prime(num):
        'checks if the number is prime'
        if num> 1:
            # check for num2 < num if num can be divided
            for num2 in range(2,num):
                if (num % num2) == 0:
                    # if so, num is not prime
                    return False
            # if not, num is prime
            return True
        else:
            return False

    def are_coprime(a, b):
        'checks if the numbers are coprime'
        return math.gcd(a, b) == 1

    def p_q_gener(the_range=(6,15)):
        'generates p and q values'
        for elem in range(the_range[0], the_range[1]):
            if is_prime(elem) and elem % 4 == 3:
                p = elem
        for elem in range(the_range[0], the_range[1]):
            if is_prime(elem) and elem % 4 == 3:
                if p != elem:
                    q = elem
        return p, q

    def n_count(p, q):
        'defines the n value'
        return p*q


    p, q = p_q_gener()
    n = n_count(p, q)
    # return open key (n) and secret key (p,q)
    return n, (p, q)



def encrypt(n, message):
    'encrypting the message'

    def message_to_ascii(message):
        """turns message to ASCII,
        then to binary"""
        # right now, use just an ordinary number
        # return m
        return message

    def formula_encryption(m, n):
        'formula for encryption'
        c = m**2 % n
        return c

    # message = message_to_ascii(message)
    encr = formula_encryption(message_to_ascii(message), n)
    return encr

def decrypt(c, p, q):
    'decrypting the message'

# function that implements Extended euclidean
# algorithm
    def extended_euclidean(a, b):
        if a == 0:
            return (b, 0, 1)
        else:
            g, y, x = extended_euclidean(b % a, a)
            return (g, x - (b // a) * y, y)
    
    # modular inverse driver function
    def modinv(a, m):
        g, x, y = extended_euclidean(a, m)
        return x % m
    
    # function implementing Chinese remainder theorem
    # list m contains all the modulii
    # list x contains the remainders of the equations
    def crt(m, x):
    
        # We run this loop while the list of
        # remainders has length greater than 1
        while True:
            
            # temp1 will contain the new value
            # of A. which is calculated according
            # to the equation m1' * m1 * x0 + m0'
            # * m0 * x1
            temp1 = modinv(m[1],m[0]) * x[0] * m[1] + \
                    modinv(m[0],m[1]) * x[1] * m[0]
    
            # temp2 contains the value of the modulus
            # in the new equation, which will be the
            # product of the modulii of the two
            # equations that we are combining
            temp2 = m[0] * m[1]
    
            # we then remove the first two elements
            # from the list of remainders, and replace
            # it with the remainder value, which will
            # be temp1 % temp2
            x.remove(x[0])
            x.remove(x[0])
            x = [temp1 % temp2] + x
    
            # we then remove the first two values from
            # the list of modulii as we no longer require
            # them and simply replace them with the new
            # modulii that  we calculated
            m.remove(m[0])
            m.remove(m[0])
            m = [temp2] + m
    
            # once the list has only one element left,
            # we can break as it will only  contain
            # the value of our final remainder
            if len(x) == 1:
                break
    
        # returns the remainder of the final equation
        return x[0]

    def chinese_theorem(tuple1, tuple2):
        'chinese theorem for 2 components'
        mod_num_ls = [tuple1[1], tuple2[1]]
        gen_num_ls = [tuple1[0], tuple2[0]]
        result = crt(mod_num_ls, gen_num_ls)
        return result

    def normal_form(tuple_val):
        """turn coefficients in mod expression
        to smaller positive ones"""
        times = tuple_val[0]//tuple_val[1]
        first_elem = tuple_val[0] - tuple_val[1]*times
        # keeps sign the same
        if first_elem < 0:
            first_elem = tuple_val[1] + first_elem
        return (int(first_elem), tuple_val[1])


    def define_answ(c, p, q):
        'defines the plain text from encrypted message'
        a1 = ((c**((p+1)/4)), p)
        a2 = ((-c**((p+1)/4)), p)
        b1 = ((c**((q+1)/4)), q)
        b2 = ((-c**((q+1)/4)), q)
        print([a1,a2,b1,b2], '   temp values')

        print(f'{a1}: {a1[0]} (mod)  {p}')
        print(f'{a2}: {a2[0]} (mod)  {p}')
        print(f'{b1}: {a2[0]} (mod)  {p}')
        print(f'{b2}: {a2[0]} (mod)  {p}')
        print()
        a1 = normal_form(a1)
        print(f'|a1|  {a1[0]} (mod) {a1[1]}')
        a2 = normal_form(a2)
        print(f'|a2|  {a2[0]} (mod) {a2[1]}')
        b1 = normal_form(b1)
        print(f'|b1|  {b1[0]} (mod) {b1[1]}')
        b2 = normal_form(b2)
        print(f'|b2|  {b2[0]} (mod) {b2[1]}')

        result1 = chinese_theorem(a1, b1)
        result2 = chinese_theorem(a1, b2)
        result3 = chinese_theorem(a2, b1)
        result4 = chinese_theorem(a2, b2)

        return [result1, result2, result3, result4]
    
    ls = define_answ(c, p, q)
    return ls


class Datum:
    """class for a final set of values;
    is used to verify them on server"""
    def __init__(self, pt1, pt2, pt3, pt4) -> None:
        self.pt1 = pt1
        self.pt2 = pt2
        self.pt3 = pt3
        self.pt4 = pt4


def get_input(n):
    'gets input from the user'
    message = input('please, write your message:   ')
    to_send = ''
    for symb in message:
        enc = encrypt(n, ord(symb))
        to_send = to_send + '_' + str(enc)
    return to_send

def get_data(data, p, q):
    'gets the data and decrypts it'
    to_check = []
    to_decrypt = data.split('_')
    for datum in to_decrypt:
        result = decrypt(datum, p, q)
        to_check.append(result)
    return to_check





if __name__ == '__main__':
    n, (p, q) = keys_generation()
    # n, (p, q) = 161, (23, 7)

    print(f'n:{n}, p, q:{p},{q}')

    message = 24
    encr = encrypt(n, message)
    print(encr, '  encr')
    decr = decrypt(encr, p, q)  
    print(decr, '   final decr')
