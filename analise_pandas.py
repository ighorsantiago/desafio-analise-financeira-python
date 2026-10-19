"""
Análise Financeira com pandas — ClearBank (Requisito Opcional RO1)
Reimplementa a leitura e o agrupamento mensal usando pandas,
comparando os resultados com a solução nativa (csv module).
"""

import pandas as pd
from datetime import datetime

ARQUIVO_CSV = "transacoes.csv"
LIMITE_SUSPEITO = 10000.00


def fmt_brl(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


# ── Leitura e limpeza ──────────────────────────────────────────────────────────

df = pd.read_csv(ARQUIVO_CSV, dtype=str)

total_lidas = len(df)

# Remover linhas inválidas (mesmas regras da solução nativa)
df = df.dropna(subset=["id", "cliente_id"])
df = df[df["id"].str.strip() != ""]
df = df[df["cliente_id"].str.strip() != ""]
df = df[df["tipo"].str.strip().str.lower().isin(["credito", "debito"])]

df["valor"] = pd.to_numeric(df["valor"], errors="coerce")
df = df[df["valor"].notna() & (df["valor"] > 0)]

df["data"] = pd.to_datetime(df["data"], format="%Y-%m-%d", errors="coerce")
df = df[df["data"].notna()]

total_validas = len(df)
total_invalidas = total_lidas - total_validas

df["mes"] = df["data"].dt.strftime("%Y-%m")
df["tipo"] = df["tipo"].str.strip().str.lower()

# ── Agrupamento mensal ─────────────────────────────────────────────────────────

creditos = df[df["tipo"] == "credito"].groupby("mes")["valor"].sum().rename("total_credito")
debitos  = df[df["tipo"] == "debito"].groupby("mes")["valor"].sum().rename("total_debito")
qtd      = df.groupby("mes")["valor"].count().rename("quantidade")
media    = df.groupby("mes")["valor"].mean().rename("media")
maximo   = df.groupby("mes")["valor"].max().rename("maior_valor")
minimo   = df.groupby("mes")["valor"].min().rename("menor_valor")

resumo = pd.concat([qtd, creditos, debitos, media, maximo, minimo], axis=1).fillna(0)
resumo["saldo"] = resumo["total_credito"] - resumo["total_debito"]
resumo = resumo.sort_index()

# ── Exibição ───────────────────────────────────────────────────────────────────

print("=" * 50)
print(" ANÁLISE COM PANDAS — ClearBank")
print("=" * 50)
print(f"\nTotal lidas:   {total_lidas}")
print(f"Válidas:       {total_validas}")
print(f"Inválidas:     {total_invalidas}")

print("\n" + "=" * 50)
print(" RESUMO MENSAL (pandas)")
print("=" * 50)

for mes, row in resumo.iterrows():
    print(f"\nMês: {mes}")
    print(f"  Transações:    {int(row['quantidade'])}")
    print(f"  Total crédito: {fmt_brl(row['total_credito'])}")
    print(f"  Total débito:  {fmt_brl(row['total_debito'])}")
    print(f"  Saldo:         {fmt_brl(row['saldo'])}")
    print(f"  Média:         {fmt_brl(row['media'])}")
    print(f"  Maior valor:   {fmt_brl(row['maior_valor'])}")
    print(f"  Menor valor:   {fmt_brl(row['menor_valor'])}")

# ── Comparação com a solução nativa ───────────────────────────────────────────

print("\n" + "=" * 50)
print(" COMPARAÇÃO COM SOLUÇÃO NATIVA (csv module)")
print("=" * 50)

referencia = {
    "2026-01": {"total_credito": 4700.00, "total_debito": 590.40, "saldo": 4109.60},
    "2026-02": {"total_credito": 18500.00, "total_debito": 700.00, "saldo": 17800.00},
    "2026-03": {"total_credito": 16000.00, "total_debito": 699.90, "saldo": 15300.10},
    "2026-04": {"total_credito": 3500.00, "total_debito": 2030.50, "saldo": 1469.50},
}

todos_iguais = True
for mes, ref in referencia.items():
    if mes not in resumo.index:
        print(f"  {mes}: MÊS AUSENTE no resultado pandas")
        todos_iguais = False
        continue
    row = resumo.loc[mes]
    ok = (
        round(row["total_credito"], 2) == ref["total_credito"]
        and round(row["total_debito"], 2) == ref["total_debito"]
        and round(row["saldo"], 2) == ref["saldo"]
    )
    status = "✓ OK" if ok else "✗ DIVERGENTE"
    print(f"  {mes}: {status}")
    if not ok:
        todos_iguais = False

if todos_iguais:
    print("\nResultados idênticos à solução nativa.")
else:
    print("\nAtenção: há divergências entre as soluções.")
