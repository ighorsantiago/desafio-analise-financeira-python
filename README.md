# Análise Financeira com Python — ClearBank

Projeto desenvolvido como parte de um desafio prático de pós-graduação. Simula o trabalho de um analista de dados júnior em uma fintech fictícia chamada **ClearBank**.

## Objetivo

Ler um CSV de transações bancárias com erros intencionais, limpar os dados, calcular métricas financeiras mensais, sinalizar movimentações suspeitas e exportar o resultado em JSON — usando exclusivamente a biblioteca nativa `csv` do Python.

## Estrutura do repositório

```
clearbank/
├── analise_financeira.ipynb   # Notebook principal (obrigatório) — todas as células executadas
├── transacoes.csv             # Base de dados com 17 linhas válidas e 5 inválidas
├── relatorio.json             # Saída gerada automaticamente ao executar o notebook
├── analise_pandas.py          # Opcional RO1 — reimplementação com pandas
├── grafico.png                # Opcional RO2 — gráfico de crédito/débito por mês
└── README.md
```

## Requisitos

- Python 3.8+
- `pandas` (somente para `analise_pandas.py`)
- `matplotlib` e `numpy` (somente para a célula de gráfico no notebook)

Instale as dependências opcionais:

```bash
pip install pandas matplotlib numpy
```

## Como executar

### Notebook principal (obrigatório)

```bash
jupyter notebook analise_financeira.ipynb
```

Ou via JupyterLab:

```bash
jupyter lab analise_financeira.ipynb
```

O notebook já está entregue com **todas as células executadas** e os outputs visíveis. Para reproduzir do zero: `Kernel → Restart & Run All`.

> O arquivo `transacoes.csv` deve estar no mesmo diretório que o notebook ao executar.

### Script pandas (opcional RO1)

```bash
python analise_pandas.py
```

Compara os resultados do agrupamento mensal com a solução nativa e imprime `✓ OK` ou `✗ DIVERGENTE` para cada mês.

## Dados de entrada — `transacoes.csv`

| Campo | Tipo esperado | Regra de validação |
|---|---|---|
| `id` | inteiro | não vazio e numérico |
| `data` | `AAAA-MM-DD` | formato exato |
| `cliente_id` | string | não vazio |
| `tipo` | `credito` ou `debito` | somente esses dois valores |
| `valor` | float | numérico e maior que zero |
| `descricao` | string | livre |
| `categoria` | string | livre |

O CSV contém **22 linhas de dados** (17 válidas em 4 meses, 5 inválidas cobrindo todos os cenários de validação).

## Lógica de validação

Linhas descartadas silenciosamente quando:

- `id` vazio ou não numérico
- `cliente_id` vazio
- `data` fora do formato `AAAA-MM-DD`
- `tipo` diferente de `credito` ou `debito`
- `valor` não numérico ou ≤ 0

## Transações suspeitas

Qualquer transação com `valor > 10000.00` (constante `LIMITE_SUSPEITO`) é marcada como suspeita e listada separadamente no relatório.

No conjunto de dados de exemplo há duas transações suspeitas:

| ID | Cliente | Data | Valor |
|---|---|---|---|
| 7 | CLI003 | 2026-02-10 | R$ 15.000,00 |
| 12 | CLI002 | 2026-03-15 | R$ 12.500,00 |

## Saída — `relatorio.json`

```json
{
  "gerado_em": "AAAA-MM-DD",
  "total_transacoes_validas": 17,
  "total_transacoes_invalidas": 5,
  "periodo": { "inicio": "...", "fim": "...", "dias": 110 },
  "resumo_mensal": {
    "2026-01": {
      "quantidade": 5,
      "total_credito": 4700.0,
      "total_debito": 590.4,
      "saldo": 4109.6,
      "media": 1058.08,
      "maior_valor": 3500.0,
      "menor_valor": 89.9
    }
  },
  "transacoes_suspeitas": [...]
}
```

## Gráfico — `grafico.png`

Barras agrupadas (verde = crédito, vermelho = débito) por mês, gerado com `matplotlib`. Produzido pela última célula do notebook.

## Funções implementadas

| Função | Célula | Descrição |
|---|---|---|
| `fmt_brl(valor)` | 3 | Formata float para `R$ 1.234,56` |
| `ler_transacoes(caminho)` | 3 | Lê CSV com `csv.DictReader`; trata `FileNotFoundError` |
| `validar_transacao(linha)` | 3 | Valida cada linha; usa `try/except` para `int`, `float` e `datetime` |
| `gerar_relatorio(transacoes_validas)` | 4 | Agrupamento mensal e cálculo de métricas |
| `exibir_relatorio(...)` | 4 | Exibe relatório formatado no terminal |
| `salvar_json(...)` | 4 | Exporta `relatorio.json` com `json.dump` |
