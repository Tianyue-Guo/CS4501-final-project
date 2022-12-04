import random

# generate a list of prime numbers
def generate_prime_list(upper_value):
    primeList = []
    for number in range(0, upper_value + 1):
        if number > 1:
            for i in range(2, number):
                if (number % i) == 0:
                    break
            else:
                primeList.append(number)
    return primeList

# get the low primes for RSA
def get_low_prime(n):
    while True:
        x = random.randrange(2 ** (n - 1) + 1, 2 ** n - 1)
        #  prime number in range(0,1000)
        max_prime = 1000
        for p in generate_prime_list(max_prime):
            if x % p == 0 and x >= p ** 2:
                break
            else:
                return x


#  Reference: http://stackoverflow.com/questions/6325576/how-many-iterations-of-rabin-miller-should-i-use-for-cryptographic-safe-primes
def miller_rabin(p, k):
    # determines whether a given number is likely to be prime
    # Test if generated p and q are prime
    # p: prime number generated
    # k: number  of trails
    if p == 2:
        return True

    if p % 2 == 0:
        return False

    r, s = 0, p - 1
    while s % 2 == 0:
        r += 1
        s //= 2
    for i in range(k):
        a = random.randrange(2, p - 1)
        x = pow(a, s, p)
        if x == 1 or x == p - 1:
            continue
        for j in range(r - 1):
            x = pow(x, 2, p)
            if x == p - 1:
                break
        else:
            return False
    return True


def get_prime_num(length):
    # generate p, q
    # length: length of the prime number

    while True:
        p = get_low_prime(length)
        # Miller-Rabin Primality test
        if miller_rabin(p, 18):
            return p


# Reference: https://www.geeksforgeeks.org/rsa-algorithm-cryptography/
def gcd(a, h):
    # find the largest positive integer that divides each of the integers
    temp = 0
    while True:
        temp = a % h
        if temp == 0:
            return h
        a = h
        h = temp


def get_e(phi):
    # e should be greater than 1 and less than phi n
    e = random.randrange(2, phi)
    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(2, phi)
        g = gcd(e, phi)
    return e


def get_d(e, phi):
    # d is the mod inverse of e
    return pow(e, -1, phi)


def key_pair(p, q):
    # Generate p and q
    n = p * q
    phi = (p - 1) * (q - 1)
    e = get_e(phi)
    d = get_d(e, phi)
    #  Get public and private key
    public = (e, n)
    private = (d, n)
    return public, private


def encrypt(M, public):
    e, n = public
    # convert char to ASCII,  M^e mod n
    cipher_M = [int(ord(x) ** e) % n for x in M]
    C_message = '#'.join([str(x) for x in cipher_M])

    return C_message


def decrypt(C_message, private):
    d, n = private
    print("before decrypt:",C_message)
    C = C_message.split('#')
    #  decrypt C, each character is equal to C^e mod n
    decrypt_M_list = [chr((int(x) ** d) % n) for x in C]

    decrypt_M_message = ''.join(decrypt_M_list)
    return decrypt_M_message


if __name__ == "__main__":

    primeLength = 9 # change prime number length to get greater p and q
    # generate random p and q values < 1,000,000
    # p = 379
    # q = 1517//19
    # # make sure p != q
    # # output the values of p, q, e, and d

    # while p == q:
    #     p = get_prime_num(primeLength)
    # print("p = {:}".format(p))
    # print("q = {:}".format(q))
    public, private = ((379,1517),(19, 1517))
    e, d = 379, 19


    # message M
    M = input("Enter Message: ")

    C = encrypt(M, public)

    print("Encrypted message = {:}".format(C))
    decrypt_M = decrypt(C, private)
    print("Decrypted message = {:}".format(decrypt_M))
