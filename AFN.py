"""AFN validador: acepta solo cadenas de exactamente 36 símbolos de {b, e, o, d, m}.

Actúa como filtro sintáctico antes de la Máquina de Turing (MT.py):
garantiza que la cadena represente una captura íntegra del inventario.

    M_afn = (Q_afn, Σ, δ_afn, q0, F_afn)
    Q_afn = {q0, q1, ..., q36}
    Σ     = {b, e, o, d, m}
    F_afn = {q36}
    δ_afn(qi, x) = {q(i+1)} para todo x en Σ, i = 0..35
    Desde q36 no hay transiciones (no hay estado basura).
"""
from typing import List

from automata.base.exceptions import RejectionException
from automata.fa.nfa import NFA

LONGITUD_INVENTARIO = 36
ALFABETO = {'b', 'e', 'o', 'd', 'm'}
ESTADO_INICIAL = 'q0'
ESTADO_FINAL = f'q{LONGITUD_INVENTARIO}'


def _construir_afn() -> NFA:
    estados = {f'q{i}' for i in range(LONGITUD_INVENTARIO + 1)}
    transiciones = {}
    for i in range(LONGITUD_INVENTARIO):
        transiciones[f'q{i}'] = {simbolo: {f'q{i + 1}'} for simbolo in ALFABETO}
    transiciones[ESTADO_FINAL] = {}  # q36 no tiene transiciones

    return NFA(
        states=estados,
        input_symbols=ALFABETO,
        transitions=transiciones,
        initial_state=ESTADO_INICIAL,
        final_states={ESTADO_FINAL},
    )


AFN_VALIDADOR = _construir_afn()


def validar_cadena(cadena: str) -> bool:
    """True si la cadena tiene exactamente 36 símbolos de {b, e, o, d, m}."""
    return AFN_VALIDADOR.accepts_input(cadena)


def recorrido(cadena: str) -> List[str]:
    """Estados por los que pasa el AFN; termina en '∅' si la ruta muere."""
    estados = []
    try:
        for actuales in AFN_VALIDADOR.read_input_stepwise(cadena):
            estados.append(next(iter(actuales)) if actuales else '∅')
    except RejectionException:
        pass
    return estados


if __name__ == '__main__':
    casos = [
        ('cadena vacía', ''),
        ('35 símbolos', 'eodmbd' * 5 + 'eodmb'),
        ('36 símbolos', 'eodmbd' * 6),
        ('inventario vacío (36 b)', 'b' * 36),
        ('37 símbolos', 'eodmbd' * 6 + 'e'),
        ('símbolo inválido (x)', 'eodmbd' * 5 + 'eodmbx'),
    ]
    for nombre, cadena in casos:
        estados = recorrido(cadena)
        resultado = 'ACEPTA' if validar_cadena(cadena) else 'RECHAZA'
        final = estados[-1] if estados else '-'
        print(f'{nombre:<26} longitud {len(cadena):>2} | último estado: {final:<4} | {resultado}')

    # Comprobación: el AFN reconoce el mismo lenguaje que la expresión regular.
    afn_regex = NFA.from_regex('(b|e|o|d|m){36}', input_symbols=ALFABETO)
    print('\n¿Equivale a (b+e+o+d+m)^36?', AFN_VALIDADOR == afn_regex)
