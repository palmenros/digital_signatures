import random
import functools
import math

LEN_CRIBA = 500
lista_primos = set()


def eratostenes(n):
    l = [1] * (n+1)
    l[0] = 0
    l[1] = 0

    num = 1

    while num <= n:
        if l[num] == 1:
            # primo
            i = 2 * num
            while i <= n:
                l[i] = 0
                i += num
        num += 1

    return l


# Devuelve (gcd, x, y)
# (x, y) tales que gcd = x * a + b * y
def extended_gcd(a, b):
    (viejo_r, r) = (a, b)
    (viejo_s, s) = (1, 0)
    (viejo_t, t) = (0, 1)

    while r != 0:
        q = viejo_r // r
        (viejo_r, r) = (r, viejo_r - q * r)
        (viejo_s, s) = (s, viejo_s - q * s)
        (viejo_t, t) = (t, viejo_t - q * t)

    return viejo_r, viejo_s, viejo_t


def rellenar_lista_primos():
    global lista_primos

    criba = eratostenes(LEN_CRIBA)
    lista_primos = [i for i in range(1, LEN_CRIBA) if criba[i] == 1 and i > 1]


def numero_aleatorio_n_bits(n):
    return random.randrange(2**(n-1) + 1, 2**n - 1)


def es_primo_eratostenes(n):
    for divisor in lista_primos:
        if n % divisor == 0 and divisor * divisor <= n:
            return False
    return True


def es_primo_miller_rabin(n, num_iteraciones = 20):
    if n == 2 or n == 3:
        return True

    # s, d satisfacen
    # n = 2 ** s * d + 1,
    # d impar
    s = 0
    d = n - 1
    while d & 1 == 0:
        d >>= 1
        s += 1

    for _ in range(num_iteraciones):
        a = random.randint(2, n-2)
        x = pow(a, d, n)
        if x == 1 or x == n-1:
            continue

        compuesto = True

        for _ in range(s-1):
            x = (x * x) % n
            if x == n - 1:
                compuesto = False
                break

        if compuesto:
            return False

    return True


def es_primo(n):
    return es_primo_eratostenes(n) and es_primo_miller_rabin(n)


def primo_aleatorio(n_bits):
    n = numero_aleatorio_n_bits(n_bits)

    # Convertimos n en impar si no lo era
    n |= 1

    while not es_primo(n):
        n = numero_aleatorio_n_bits(n_bits)

        # Convertimos n en impar si no lo era
        n |= 1
    return n


# Devuelve (p, g), donde p es un primo de n_bits bits y g es un generador del grupo multiplicativo (Z/pZ)*
def primo_aleatorio_generador(n_bits):
    # Primero buscamos un primo p de la forma 2*q + 1, con q primo
    p = 0
    while True:
        q = primo_aleatorio(n_bits - 1)
        p = 2 * q + 1
        if es_primo(p):
            break

    # Los posibles ordenes de los elementos de (Z/pZ)* son 1, 2, q, p-1
    # El único elemento de orden 2 es p-1 = -1 mod p
    # El único elemento de orden 1 es 1

    g = 0
    while True:
        g = random.randint(2, p-2)

        # Solo necesitamos checkear que no es de orden q
        if pow(g, q, p) != 1:
            break
    return p, g


# Devuelve dos primos (p, q) tal que q tiene q_bits, p tiene p_bits +- 1bit y q | (p-1)
# p_bits debe ser al menos mayor que igual q_bits + 3
def primos_aleatorios_divisores(p_bits, q_bits):
    while True:
        q = primo_aleatorio(q_bits)

        num_intentos = 0
        num_bits_multiplo = p_bits - q_bits

        while num_intentos < 2 ** num_bits_multiplo:
            mult = numero_aleatorio_n_bits(num_bits_multiplo)
            p = mult * q + 1
            if es_primo(p):
                return (p, q)
            num_intentos += 1


# Calcula el orden del elemento e en el grupo (Z/pZ)*
def orden(e, p):
    o = 1
    e = e % p
    x = e
    while x != 1:
        x = (x * e) % p
        o += 1
    return o


def num_bits(n):
    return math.floor(math.log2(n)) + 1


rellenar_lista_primos()
print(lista_primos)