import random
import utils


# Devuelve (p, q, H, g)
def asignar_parametros(p, q, H, g):
    # Devuelve los parámetros
    return p, q, H, g


# Devuelve (privada, publica)
def asignar_claves(parametros, privada):
    p, q, _, g = parametros
    publica = pow(g, privada, p)
    return privada, publica


# Genera aleatoriamente parámetros (g) dados H, el numero de bits de p y el de q
# devuelve (p, H, g)
def generar_parametros(p_bits, q_bits, H):
    p, q = utils.primos_aleatorios_divisores(p_bits, q_bits)

    g = 1
    while g == 1:
        h = random.randint(2, p-2)
        g = pow(h, (p-1) // q, p)

    return asignar_parametros(p, q, H, g)


def generar_claves(parametros):
    _, q, _, _ = parametros
    privada = random.randint(1, q - 1)
    return asignar_claves(parametros, privada)


# Devuelve (r, s)
def firmar(parametros, clave_privada, mensaje, k = None):
    m = mensaje
    p, q, H, g = parametros
    x = clave_privada

    k_ya_seleccionada = k is not None

    s = 0
    r = 0
    while s == 0 or r == 0:
        if not k_ya_seleccionada:
            k = random.randint(2, q-1)

        (gcd, k_inv, _) = utils.extended_gcd(k, q)

        r = pow(g, k, p) % q
        s = (k_inv * ((H(m) + x * r) % q)) % q

    return r, s


def verifica(parametros, clave_publica, firma, mensaje):
    m = mensaje
    p, q, H, g = parametros
    y = clave_publica
    r, s = firma

    if not (0 < r < q) or not (0 < s < q):
        return False

    # w = s^-1 mod q
    (_, w, _) = utils.extended_gcd(s, q)

    u1 = (H(m) * w) % q
    u2 = (r * w) % q

    v = ((pow(g, u1, p) * pow(y, u2, p)) % p) % q
    return v == r