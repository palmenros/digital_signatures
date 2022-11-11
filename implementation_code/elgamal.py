import random
import utils


# Devuelve (p, H, g)
def asignar_parametros(p, H, g):
    # Devuelve los parámetros
    return (p, H, g)


# Devuelve (privada, publica)
def asignar_claves(parametros, privada):
    p, _, g = parametros
    publica = pow(g, privada, p)
    return (privada, publica)


# Devuelve (r, s)
def firmar(parametros, clave_privada, mensaje, k = None):
    m = mensaje
    p, H, g = parametros
    x = clave_privada

    k_ya_seleccionada = k is not None

    s = 0
    while s == 0:
        gcd = 0
        while gcd != 1:
            if not k_ya_seleccionada:
                k = random.randint(2, p-1)

            (gcd, k_inv, _) = utils.extended_gcd(k, p-1)
        r = pow(g, k, p)
        s = ( ((H(m) - x * r) % (p-1)) * k_inv) % (p-1)

    return r, s


def verifica(parametros, clave_publica, firma, mensaje):
    m = mensaje
    p, H, g = parametros
    y = clave_publica
    r, s = firma

    if not (0 < r < p) or not (0 < s < p-1):
        return False

    return pow(g, H(m), p) == ((pow(y, r, p) * pow(r, s, p)) % p)


# Genera aleatoriamente parámetros (g) dados el numero de bits de p y H
# devuelve (p, H, g)
def generar_parametros(n_bits, H):
    p, g = utils.primo_aleatorio_generador(n_bits)
    return p, H, g


def generar_claves(parametros):
    p, _, _ = parametros
    privada = random.randint(1, p-2)
    return asignar_claves(parametros, privada)