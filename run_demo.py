import tiktoken
import random

# ============================================================
# CONTEXT FREEZING DEMO
# ============================================================

enc = tiktoken.get_encoding("cl100k_base")

def count_tokens(text):
    return len(enc.encode(text))


# ----------------------------
# ARTIFACT (FULL CONTEXT)
# ----------------------------
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


# ----------------------------
# EXECUTION ENGINE
# ----------------------------
def run_iteration(volatility, volume):
    if volatility == "low" and volume == "low":
        return "regime=estable | variables=precio"
    elif volatility == "medium":
        return "regime=transicion | variables=precio,volumen"
    else:
        return "regime=inestable | variables=precio,volumen,volatilidad"


# ----------------------------
# SIMULATION
# ----------------------------
iterations = 5000
volatility_space = ["low", "medium", "high", "extreme"]
volume_space = ["low", "high"]

delta_tokens_total = 0
baseline_tokens_total = 0
outputs = set()


# ----------------------------
# INIT
# ----------------------------
print("\n=== INIT PHASE ===")
print(f"Artifact tokens (full context): {artifact_tokens}")
print("--------------------------------")


# ----------------------------
# EXECUTION
# ----------------------------
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


# ----------------------------
# SUMMARY
# ----------------------------
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
