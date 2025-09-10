import re
import math
import os

funciones = {}

def dividir_args(arg_str):
    args, nivel, actual = [], 0, ''
    for c in arg_str + ',':
        if c == ',' and nivel == 0:
            args.append(actual)
            actual = ''
        else:
            if c == '(': nivel += 1
            elif c == ')': nivel -= 1
            actual += c
    return args

def definir_funcion(linea):
    match = re.match(r'func (\w+)\((.*?)\) = (.*);', linea)
    if match:
        nombre, parametros, cuerpo = match.groups()
        funciones[nombre] = {
            'params': [p.strip() for p in parametros.split(',') if p],
            'body': cuerpo.strip()
        }
    else:
        print(f"Error de sintaxis en definición: {linea}")

def evaluar(expr, contexto):
    expr = expr.replace('^', '**')
    for var in contexto:
        expr = expr.replace(var, str(contexto[var]))
    return eval(expr)

def resolver_llamada(llamada):
    match = re.match(r'(\w+)\((.*)\)', llamada)
    if not match:
        return llamada
    nombre, args = match.groups()
    if nombre not in funciones:
        return f"Error: función no definida '{nombre}'"
    args = dividir_args(args)
    valores = [resolver_llamada(arg.strip()) for arg in args]
    if len(valores) != len(funciones[nombre]['params']):
        return f"Error: número incorrecto de parámetros en {nombre} (esperado {len(funciones[nombre]['params'])}, recibido {len(valores)})"
    contexto = dict(zip(funciones[nombre]['params'], valores))
    return evaluar(funciones[nombre]['body'], contexto)

def ejecutar_print(linea):
    match = re.match(r'print (.+);', linea)
    if match:
        llamada = match.group(1)
        resultado = resolver_llamada(llamada)
        print(resultado)
    else:
        print(f"Error de sintaxis en print: {linea}")

print("Directorio actual:", os.getcwd())

with open('codigo.txt') as f:
    for linea in f:
        linea = linea.strip()
        if linea.startswith('func'):
            definir_funcion(linea)
        elif linea.startswith('print'):
            ejecutar_print(linea)