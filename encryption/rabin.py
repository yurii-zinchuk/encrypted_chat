"""
module with Rabin cryptography
technique implementation
"""
import math
from random import randint


NUMS_DICT = {
    "Q": "10",
    "W": "11",
    "E": "12",
    "R": "13",
    "T": "14",
    "Y": "15",
    "U": "16",
    "I": "17",
    "O": "18",
    "P": "19",
    "A": "20",
    "S": "21",
    "D": "22",
    "F": "23",
    "G": "24",
    "H": "25",
    "J": "26",
    "K": "27",
    "L": "28",
    "Z": "29",
    "X": "30",
    "C": "31",
    "V": "32",
    "B": "33",
    "N": "34",
    "M": "35",
    "q": "36",
    "w": "37",
    "e": "38",
    "r": "39",
    "t": "40",
    "y": "41",
    "u": "42",
    "i": "43",
    "o": "44",
    "p": "45",
    "a": "46",
    "s": "47",
    "d": "48",
    "f": "49",
    "g": "50",
    "h": "51",
    "j": "52",
    "k": "53",
    "l": "54",
    "z": "55",
    "x": "56",
    "c": "57",
    "v": "58",
    "b": "59",
    "n": "60",
    "m": "61",
    " ": "62",
    ",": "63",
    ".": "64",
    "!": "65",
    "?": "66",
    "-": "67",
    "`": "68",
    "'": "69",
    '"': "70",
    ";": "71",
    ":": "72",
    "(": "73",
    ")": "74",
    "/": "75",
    "|": "76",
    "_": "77",
    "1": "78",
    "2": "79",
    "3": "80",
    "4": "81",
    "5": "82",
    "6": "83",
    "7": "84",
    "8": "85",
    "9": "86",
    "0": "87",
}


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

    def p_q_gener(the_range=(8,20)):
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



def encrypt(n, message, server):
    'encrypting the message'

    def get_id():
        'gets the id for current operation'
        id = randint(1, 1000000000000000)
        return id

    def message_to_num(message):
        """turns message to num"""
        num = int(NUMS_DICT[str(message)])
        # return m
        return num

    def formula_encryption(m, n):
        'formula for encryption'
        c = m**2 % n
        return c

    id_val = get_id()
    server.register(message, id_val)
    the_num = message_to_num(message)
    encr = formula_encryption(the_num, n)
    return encr, id_val

def decrypt(c, p, q, server):
    'decrypting the message'


    def eucl_alg(val1, val2):
        'recursive euclidian algorithm'
        if val1 == 0:
            return (val2, 0, 1)
        else:
            st1_val, st2_val, st3_val = eucl_alg(val2 % val1, val1)
            val3 = st3_val - (val2 // val1) * st2_val
            return (st1_val, val3, st2_val)


    def inverse(val1, val2):
        'finds the modular inverse number'
        st1_val, st2_val, st3_val = eucl_alg(val1, val2)
        return st2_val % val2
    
    
    def chinese_remainder_count(val1:list, val2:list):
        'chinese remainder theorem for calculations'
        while True:
            inv1, inv2 = inverse(val1[1],val1[0]), inverse(val1[0],val1[1])
            st1_def1 = inv1 * val2[0] * val1[1]
            st2_def2 = inv2 * val2[1] * val1[0]
            st1 = st1_def1 + st2_def2
            st2 = val1[0] * val1[1]
            # val1_2' * val1_2 * val2_1 + val1_1' * val1_1 * val2_2
            # modify val2 and val1 lists
            val2.remove(val2[0])
            val2.remove(val2[0])
            val1.remove(val1[0])
            val1.remove(val1[0])
            val1, val2 = [st2] + val1, [st1 % st2] + val2
            # if only one elem left - break
            if len(val2) == 1:
                break
        return val2[0]

    def chinese_theorem(tuple1, tuple2):
        'chinese theorem for 2 components'
        mod_num_ls = [tuple1[1], tuple2[1]]
        gen_num_ls = [tuple1[0], tuple2[0]]
        result = chinese_remainder_count(mod_num_ls, gen_num_ls)
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
    
    ls = define_answ(int(c), p, q)
    return ls


class ServerData:
    """class for a final set of values;
    is used to verify them on server"""
    def __init__(self) -> None:
        self.dct = dict()

    def register(self, datum, id):
        'registers the datum on the server side'
        self.dct[id] = datum

    def check_data(self, data, id):
        'checks the final data'
        if self.dct[id] in data:
            return self.dct[id]



def get_input(n, server):
    'gets input from the user'
    message = input('please, write your message:   ')
    to_send = ''
    id_ls = []
    for symb in message:
        enc, id_val = encrypt(n, symb, server)
        id_ls.append(id_val)
        add_str = '*' + str(enc)
        to_send += add_str
    to_send = to_send[1:]
    return to_send, id_ls

def get_data(data, p, q, server, nums_dict, id_ls):
    'gets the data and decrypts it'
    final_result = ''
    to_decrypt = data.split('*')
    for idx, datum in enumerate(to_decrypt):
        id_val = id_ls[idx]
        decr = decrypt(datum, p, q, server)
        # to_check.append(result)

        
        answ_ls = []
        for el in decr:
            try:
                check_dict = {i: j for j, i in nums_dict.items()}
                elem = check_dict[str(el)]
                answ_ls.append(elem)
            except:
                pass

        result = server.check_data(answ_ls, id_val)
        # print(result)
        final_result += result
    return final_result




if __name__ == '__main__':
    # ------ single character encoding/decoding test ------\

    # server = ServerData()
    # n, (p, q) = keys_generation()
    # # n, (p, q) = 161, (23, 7)

    # print(f'n:{n}, p, q:{p},{q}')

    # message = 'd'
    # encr, id_val = encrypt(n, message, server)
    # print(encr, '  encr')
    # decr = decrypt(encr, p, q, server)
    # print(decr, '   chinese theorem decr')
    # answ_ls = []
    # for el in decr:
    #     try:
    #         check_dict = {i: j for j, i in NUMS_DICT.items()}
    #         elem = check_dict[str(el)]
    #         answ_ls.append(elem)
    #     except:
    #         pass

    # result = server.check_data(answ_ls, id_val)
    # print(result)





    # words encoding/decoding test
    server = ServerData()
    n, (p, q) = keys_generation()
    to_send, id_ls = get_input(n, server)
    final_result = get_data(to_send, p, q, server, NUMS_DICT, id_ls)
    print(final_result)

