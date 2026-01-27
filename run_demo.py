
#*   -------------------------------------------------------------------
#*                                                 r u n  d e m o . p y
#?                                                          v 1 . 0 . 0

#?   Ruta del módulo: /run_demo.py

#?   Dependencias del módulo:
#   - tiktoken
#   - random

#?   Input:
#   - Parámetros simulados de mercado:
#     - volatility: str ∈ {low, medium, high, extreme}
#     - volume: str ∈ {low, high}

#?   Output:
#   - Métricas de ejecución impresas por consola:
#     - Consumo total de tokens con y sin artifact
#     - Outputs únicos generados
#     - Porcentaje estimado de ahorro de tokens

#?   Descripción:
#   Demostración controlada de congelamiento de contexto (artifact)
#   para eliminar el costo de reenvío de reglas de decisión en
#   ejecuciones repetidas.

#*  --------------------------   A u t o r -  M a t í a s  G a l a r z a


import tiktoken
import random


#*  -----------------------   C O N T E X T   F R E E Z I N G   D E M O

enc = tiktoken.get_encoding("cl100k_base")

def count_tokens(text):
    return len(enc.encode(text))


#*  ---------------------   A R T I F A C T  ( F U L L   C O N T E X T )

ARTIFACT = """
REGIMES:
- estable
- transicion
- inestable

RULES:
1. volatility == low and volume == low
   -> estable | precio

2. volatility == medium
   -> transicion | precio, volumen

3. volatility in (high, extreme)
   -> inestable | precio, volumen, volatilidad
"""

artifact_tokens = count_tokens(ARTIFACT)


#*  ----------------------------------   E X E C U T I O N   E N G I N E

def run_iteration(volatility, volume):
    if volatility == "low" and volume == "low":
        return "regime=estable | variables=precio"
    elif volatility == "medium":
        return "regime=transicion | variables=precio,volumen"
    else:
        return "regime=inestable | variables=precio,volumen,volatilidad"


#*  ----------------------------------------------   S I M U L A T I O N

iterations = 5000
volatility_space = ["low", "medium", "high", "extreme"]
volume_space = ["low", "high"]

delta_tokens_total = 0
baseline_tokens_total = 0
outputs = set()


#*  ----------------------------------------------------------   I N I T

print("\n=== INIT PHASE ===")
print(f"Artifact tokens (full context): {artifact_tokens}")
print("--------------------------------")


#*  ------------------------------------------------   E X E C U T I O N

print("\n=== EXECUTION PHASE ===\n")

for i in range(iterations):
    vol = random.choice(volatility_space)
    volu = random.choice(volume_space)

    delta_context = f"volatility={vol}\nvolume={volu}"
    delta_tokens = count_tokens(delta_context)

    # Artifact-based system
    delta_tokens_total += delta_tokens

    # Baseline system (full context resent every time)
    baseline_tokens_total += artifact_tokens + delta_tokens

    output = run_iteration(vol, volu)
    outputs.add(output)

    if i < 5:
        print(f"Iteration {i+1}")
        print(delta_context)
        print("->", output)
        print()


#*  ----------------------------------------------------   S U M M A R Y

print("--------------------------------")
print("\n=== SUMMARY ===")
print(f"Iterations: {iterations}")
print(f"Unique outputs: {len(outputs)}\n")

print("WITH FROZEN ARTIFACT:")
print(f"- Artifact tokens (once):    {artifact_tokens}")
print(f"- Delta tokens total:        {delta_tokens_total}")
print(f"- TOTAL TOKENS USED:         {artifact_tokens + delta_tokens_total}\n")

print("WITHOUT ARTIFACT (baseline):")
print(f"- TOTAL TOKENS USED:         {baseline_tokens_total}\n")

savings = 100 * (1 - (artifact_tokens + delta_tokens_total) / baseline_tokens_total)

print("=== COST COMPARISON ===")
print(f"Estimated token savings: ~{round(savings, 2)}%")
print("\nThis demonstrates how freezing decision state")
print("converts repeated long-context cost into")
print("a one-time payment.\n")


#* ---------------------------------------------------------   N O T A S

#?  Notas de desarrollo:

# 1. El patrón es especialmente efectivo cuando se aplica primero a
#    contenido trivial y repetitivo. Al congelar estas capas básicas,
#    se reduce el ruido contextual y se libera presupuesto de tokens
#    para decisiones de mayor nivel.

# 2. El enfoque es escalable y compuesto: múltiples artifacts pueden
#    encadenarse o superponerse. Cada capa congelada reduce costo
#    marginal y estabiliza el sistema a medida que la complejidad crece.

#* -----------------------  A c t u a l i z a c i o n  -  2026 - 01 - 27
