import random


class RSA:
    def __init__(self, size, text):
        self.size = size
        self.text = text
        self.generate_rsa_keys()

    # Szyfrowanie
    def encrypt(self):
        cipher = ''

        for character in self.text:
            cipher += str(pow(ord(character), self.e, self.n)) + ' '

        return cipher

    # Deszyfrowanie
    def decrypt(self, cipher):
        text = ''

        for x in cipher.split():
            if x:
                text += chr(pow(int(x), self.d, self.n))

        return text

    # Test Millera-Rabina do sprawdzenia czy liczba jest pierwsza
    def miller_rabin_test(self, n, d):
        j = random.randint(2, (n - 2) - 2)
        x = pow(j, int(d), n)

        if x == 1 or x == n - 1:
            return True

        while d != n - 1:
            x = pow(x, 2, n)
            d *= 2

            if x == 1:
                return False
            elif x == n - 1:
                return True

        return False

    # Czy liczba jest liczbą pierwszą
    def check_is_prime(self, n):
        if n < 2:
            return False

        c = n - 1
        while c % 2 == 0:
            c /= 2

        for i in range(128):
            if not self.miller_rabin_test(n, c):
                return False

        return True

    def egcd(self, x, y):
        s = 0
        t = 1
        r = y

        old_s = 1
        old_t = 0
        old_r = x

        while r != 0:
            quot = old_r // r
            old_r, r = r, old_r - quot * r
            old_s, s = s, old_s - quot * s
            old_t, t = t, old_t - quot * t

        return old_r, old_s, old_t

    def modular_inverse(self, x, y):
        gcd, a, b = self.egcd(x, y)

        if a < 0:
            a += y

        return a

    # Wygeneruj klucze RSA
    def generate_rsa_keys(self):
        self.p = self.generate_primes()
        self.q = self.generate_primes()
        self.n = self.p * self.q
        self.phi = (self.p - 1) * (self.q - 1)

        while True:
            self.e = random.randrange(2 ** (self.size - 1), 2 ** self.size - 1)
            if self.find_gcd(self.e, self.phi) == 1:
                break

        self.d = self.modular_inverse(self.e, self.phi)

    # Wygeneruj dwie duże liczby pierwsze
    def generate_primes(self):
        while True:
            num = random.randrange(2 ** (self.size - 1), 2 ** self.size - 1)

            if self.check_is_prime(num):
                return num

    # Wyznacz NWD za pomocą algorytmu Euklidesa
    def find_gcd(self, a, b):
        while b:
            a, b = b, a % b

        return a


def script():
    text = input('Wpisz tekst do zaszyfrowania: ')

    rsa = RSA(32, text)
    encrypted_text = rsa.encrypt()
    decrypted_text = rsa.decrypt(encrypted_text)

    print(f'Wygenerowane liczby pierwsze to: {rsa.p} i {rsa.q}')
    print('Zaszyfrowany tekst: ', encrypted_text)
    print('Odszyfrowany tekst: ', decrypted_text)


script()

