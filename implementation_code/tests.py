import random
import dsa
import elgamal


def elgamal_ejemplo_presentacion():
    p = 13
    H = lambda m: m
    g = 2
    parametros = elgamal.asignar_parametros(p, H, g)
    privada = 3
    privada, publica = elgamal.asignar_claves(parametros, privada)

    mensaje = 11
    k = 5
    firma = elgamal.firmar(parametros, privada, mensaje, k)

    print(f'////////////////////////////')
    print(f'    Ejemplo ElGamal')
    print(f'////////////////////////////')

    print(f'Clave publica: {publica}')
    print(f'Firma: {firma}')
    print(f'Firma valida: {elgamal.verifica(parametros, publica, firma, mensaje)}')
    print(f'Firma alterada valida: {elgamal.verifica(parametros, publica, firma, mensaje + 1)}\n')


def elgamal_caso_prueba_aleatorio(n_bits_primo, H):
    parametros = elgamal.generar_parametros(n_bits_primo, H)
    privada, publica = elgamal.generar_claves(parametros)

    p, _, _ = parametros

    mensaje = random.randint(0, p - 1)
    firma = elgamal.firmar(parametros, privada, mensaje)

    r, s = firma
    firma_alterada_1 = (r + random.randint(1, p - 1)) % p, s
    firma_alterada_2 = r, (s + random.randint(1, p - 1)) % p

    mensaje_alterado = (mensaje + random.randint(1, p - 1)) % p
    return elgamal.verifica(parametros, publica, firma, mensaje) \
        and not elgamal.verifica(parametros, publica, firma, mensaje_alterado) \
        and not elgamal.verifica(parametros, publica, firma_alterada_1, mensaje) \
        and not elgamal.verifica(parametros, publica, firma_alterada_2, mensaje)


def elgamal_probar_aleatorios(num_casos):
    H = lambda m: m
    n_bits_primo = 40

    for it in range(num_casos):
        if not elgamal_caso_prueba_aleatorio(n_bits_primo, H):
            raise ValueError('Error en un test aleatorio de ElGamal!')
        if it % 500 == 0:
            print(f'Finished ElGamal iteration {it}')

    print('Terminados tests aleatorios ElGamal')


def dsa_ejemplo_presentacion():
    p = 283
    q = 47
    H = lambda m: m
    g = 60
    parametros = dsa.asignar_parametros(p, q, H, g)

    privada = 24
    privada, publica = dsa.asignar_claves(parametros, privada)

    mensaje = 41
    k = 15
    firma = dsa.firmar(parametros, privada, mensaje, k)

    print(f'////////////////////////////')
    print(f'    Ejemplo DSA')
    print(f'////////////////////////////')

    print(f'Clave publica: {publica}')
    print(f'Firma: {firma}')
    print(f'Firma valida: {dsa.verifica(parametros, publica, firma, mensaje)}')
    print(f'Firma alterada valida: {dsa.verifica(parametros, publica, firma, mensaje + 1)}\n')


def dsa_caso_prueba_aleatorio(p_bits, q_bits, H):
    parametros = dsa.generar_parametros(p_bits, q_bits, H)
    privada, publica = dsa.generar_claves(parametros)

    p, q, _, _ = parametros

    mensaje = random.randint(0, q - 1)
    firma = dsa.firmar(parametros, privada, mensaje)

    mensaje_alterado = (mensaje + random.randint(1, q - 1)) % q

    r, s = firma
    firma_alterada_1 = (r + random.randint(1, q - 1)) % q, s
    firma_alterada_2 = r, (s + random.randint(1, q - 1)) % q

    return dsa.verifica(parametros, publica, firma, mensaje) \
        and not dsa.verifica(parametros, publica, firma, mensaje_alterado) \
        and not dsa.verifica(parametros, publica, firma_alterada_1, mensaje) \
        and not dsa.verifica(parametros, publica, firma_alterada_2, mensaje)


def dsa_probar_aleatorios(num_casos):
    H = lambda m: m
    p_bits = 100
    q_bits = 50

    for it in range(num_casos):
        if not dsa_caso_prueba_aleatorio(p_bits, q_bits, H):
            raise ValueError('Error en un test aleatorio de DSA!')
        if it % 500 == 0:
            print(f'Finished iteration {it}')

    print('Terminados tests aleatorios DSA')


def suite_tests_aleatorios():
    elgamal_probar_aleatorios(5000)
    dsa_probar_aleatorios(5000)


if __name__ == '__main__':
    elgamal_ejemplo_presentacion()
    dsa_ejemplo_presentacion()
    suite_tests_aleatorios()
