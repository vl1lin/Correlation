# Корреляции давления точки пузырьков (Bubble Point Pressure Correlations)

> **Формат файла**: Markdown с LaTeX-формулами
> **Кодировка**: UTF-8
> **Назначение**: Машиночитаемый файл с формулами корреляций для распознавания и вычислений

---

## METADATA

```json
{
  "document_type": "correlation_formulas",
  "version": "1.0",
  "total_correlations": 9,
  "units": {
    "pb": "psi",
    "Rs": "scf/STB",
    "gamma_g": "dimensionless",
    "gamma_API": "degrees API",
    "T": "degrees Fahrenheit"
  }
}
```

---

## VARIABLES

| Символ | LaTeX | Описание | Единицы |
|--------|-------|----------|---------|
| $p_b$ | `p_b` | Давление точки пузырьков | psi |
| $R_s$ | `R_s` | Растворимость газа в нефти | scf/STB |
| $\gamma_g$ | `\gamma_g` | Относительная плотность газа | безразмерная |
| $\gamma_{API}$ | `\gamma_{API}` | Гравитация API нефти | °API |
| $T$ | `T` | Температура | °F |
| $\gamma_o$ | `\gamma_o` | Относительная плотность нефти | безразмерная |
| $M_o$ | `M_o` | Молярная масса нефти | lb/lbmol |
| $T_{sp}$ | `T_{sp}` | Температура сепарации | °F |
| $p_{sp}$ | `p_{sp}` | Давление сепарации | psi |
| $x_g$ | `x_g` | Мольная доля газа в жидкой фазе | безразмерная |

---

## CORRELATIONS

### CORRELATION_001

```yaml
name: "Standing (1947)"
region: "California, USA"
id: "standing"
```

**Formula**:

$$p_b = 18.2 \left[ \left( \frac{R_s}{\gamma_g} \right)^{0.83} \cdot 10^{(0.00091T - 0.0125\gamma_{API})} - 1.4 \right]$$

**LaTeX**:
```latex
p_b = 18.2 \left[ \left( \frac{R_s}{\gamma_g} \right)^{0.83} \cdot 10^{(0.00091T - 0.0125\gamma_{API})} - 1.4 \right]
```

**Input parameters**: `Rs`, `gamma_g`, `T`, `gamma_API`

**Output**: `pb`

**Validity**:
```json
{
  "Rs": {"min": 20, "max": 1425, "unit": "scf/STB"},
  "gamma_g": {"min": 0.59, "max": 0.95, "unit": "dimensionless"},
  "gamma_API": {"min": 16.5, "max": 63.8, "unit": "degrees API"},
  "T": {"min": 100, "max": 258, "unit": "degrees Fahrenheit"}
}
```

---

### CORRELATION_002

```yaml
name: "Elam (1957)"
region: "Texas, USA"
id: "elam"
```

**Formula**:

$$p_b = \frac{R_s^{0.702}}{\gamma_g^{0.514}} \cdot e^{(0.00348T - 0.0282\gamma_{API} + 3.58)}$$

**LaTeX**:
```latex
p_b = \frac{R_s^{0.702}}{\gamma_g^{0.514}} \cdot e^{(0.00348T - 0.0282\gamma_{API} + 3.58)}
```

**Input parameters**: `Rs`, `gamma_g`, `T`, `gamma_API`

**Output**: `pb`

**Validity**:
```json
{
  "Rs": {"min": 100, "max": 2000, "unit": "scf/STB"},
  "gamma_g": {"min": 0.6, "max": 1.2, "unit": "dimensionless"},
  "gamma_API": {"min": 20, "max": 50, "unit": "degrees API"},
  "T": {"min": 120, "max": 280, "unit": "degrees Fahrenheit"}
}
```

---

### CORRELATION_003

```yaml
name: "Lasater (1958)"
region: "Midcontinent U.S."
id: "lasater"
```

**Formulas**:

$$x_g = \left[ 1 + \frac{\gamma_o}{7.521 \times 10^{-6} R_s M_o} \right]^{-1}$$

$$p_f = e^{\left( \frac{x_g - 0.15649}{0.33705} \right)} - 0.59162$$

$$p_b = \frac{p_f (T + 459.67)}{\gamma_g}$$

**LaTeX**:
```latex
x_g = \left[ 1 + \frac{\gamma_o}{7.521 \times 10^{-6} R_s M_o} \right]^{-1}
p_f = e^{\left( \frac{x_g - 0.15649}{0.33705} \right)} - 0.59162
p_b = \frac{p_f (T + 459.67)}{\gamma_g}
```

**Input parameters**: `Rs`, `gamma_g`, `T`, `gamma_API` (for gamma_o calculation)

**Output**: `pb`

**Validity**:
```json
{
  "Rs": {"min": 50, "max": 1500, "unit": "scf/STB"},
  "gamma_g": {"min": 0.55, "max": 1.3, "unit": "dimensionless"},
  "gamma_API": {"min": 15, "max": 55, "unit": "degrees API"},
  "T": {"min": 80, "max": 300, "unit": "degrees Fahrenheit"}
}
```

---

### CORRELATION_004

```yaml
name: "Vazquez and Beggs (1976)"
region: "Worldwide"
id: "vazquez"
```

**Formulas**:

$$\gamma_{gc} = \gamma_g \left[ 1 + 5.912 \times 10^{-5} \gamma_{API} T_{sp} \log\left( \frac{p_{sp}}{114.7} \right) \right]$$

$$p_b = \left[ A \left( \frac{R_s}{\gamma_{gc}} \right) 10^{\left( \frac{B\gamma_{API}}{T + 459.67} \right)} \right]^C$$

**LaTeX**:
```latex
\gamma_{gc} = \gamma_g \left[ 1 + 5.912 \times 10^{-5} \gamma_{API} T_{sp} \log\left( \frac{p_{sp}}{114.7} \right) \right]
p_b = \left[ A \left( \frac{R_s}{\gamma_{gc}} \right) 10^{\left( \frac{B\gamma_{API}}{T + 459.67} \right)} \right]^C
```

**Coefficients**:

| Condition | A | B | C |
|-----------|-------|---------|--------|
| $\gamma_{API} \leq 30$ | 27.64 | -11.172 | 0.9143 |
| $\gamma_{API} > 30$ | 56.06 | -10.393 | 0.8425 |

**Input parameters**: `Rs`, `gamma_g`, `T`, `gamma_API`, `T_sp`, `p_sp`

**Output**: `pb`

**Validity**:
```json
{
  "Rs": {"min": 50, "max": 2500, "unit": "scf/STB"},
  "gamma_g": {"min": 0.5, "max": 1.5, "unit": "dimensionless"},
  "gamma_API": {"min": 15, "max": 55, "unit": "degrees API"},
  "T": {"min": 100, "max": 350, "unit": "degrees Fahrenheit"}
}
```

---

### CORRELATION_005

```yaml
name: "Glasø (1980)"
region: "North Sea"
id: "glaso"
```

**Formulas**:

$$X = \left( \frac{R_s}{\gamma_g} \right)^{0.816} \left( \frac{T^{0.172}}{\gamma_{API}^{0.989}} \right)$$

$$p_b = 10^{(1.7669 + 1.7447 \log X - 0.30218 (\log X)^2)}$$

**LaTeX**:
```latex
X = \left( \frac{R_s}{\gamma_g} \right)^{0.816} \left( \frac{T^{0.172}}{\gamma_{API}^{0.989}} \right)
p_b = 10^{(1.7669 + 1.7447 \log X - 0.30218 (\log X)^2)}
```

**Input parameters**: `Rs`, `gamma_g`, `T`, `gamma_API`

**Output**: `pb`

**Validity**:
```json
{
  "Rs": {"min": 100, "max": 2000, "unit": "scf/STB"},
  "gamma_g": {"min": 0.6, "max": 1.3, "unit": "dimensionless"},
  "gamma_API": {"min": 20, "max": 50, "unit": "degrees API"},
  "T": {"min": 120, "max": 320, "unit": "degrees Fahrenheit"}
}
```

---

### CORRELATION_006

```yaml
name: "Labedi (1982)"
region: "Libya, Nigeria, Angola"
id: "labedi"
```

**Formula**:

$$p_b = \frac{6.0001}{\gamma_{g_{sp}}} \left[ \frac{R_s^{0.6714} \left( \frac{T}{\gamma_{API}} \right)^{0.7097} T_{sp}^{0.08929}}{10^{(7.995 \times 10^{-5} R_s)}} \right]$$

**LaTeX**:
```latex
p_b = \frac{6.0001}{\gamma_{g_{sp}}} \left[ \frac{R_s^{0.6714} \left( \frac{T}{\gamma_{API}} \right)^{0.7097} T_{sp}^{0.08929}}{10^{(7.995 \times 10^{-5} R_s)}} \right]
```

**Input parameters**: `Rs`, `gamma_g_sp`, `T`, `gamma_API`, `T_sp`

**Output**: `pb`

**Validity**:
```json
{
  "Rs": {"min": 100, "max": 3000, "unit": "scf/STB"},
  "gamma_g": {"min": 0.55, "max": 1.2, "unit": "dimensionless"},
  "gamma_API": {"min": 25, "max": 50, "unit": "degrees API"},
  "T": {"min": 150, "max": 350, "unit": "degrees Fahrenheit"}
}
```

---

### CORRELATION_007

```yaml
name: "Owolabi (1984) - Cook Inlet"
region: "Alaska, Cook Inlet"
id: "owolabi1"
```

**Formula**:

$$p_b = 55.0 + 0.8643 \left[ \left( \frac{R_s}{\gamma_g} \right)^{1.255} \frac{T^{0.172}}{\gamma_{API}^{0.178}} \right]$$

**LaTeX**:
```latex
p_b = 55.0 + 0.8643 \left[ \left( \frac{R_s}{\gamma_g} \right)^{1.255} \frac{T^{0.172}}{\gamma_{API}^{0.178}} \right]
```

**Input parameters**: `Rs`, `gamma_g`, `T`, `gamma_API`

**Output**: `pb`

**Validity**:
```json
{
  "Rs": {"min": 50, "max": 1500, "unit": "scf/STB"},
  "gamma_g": {"min": 0.6, "max": 1.1, "unit": "dimensionless"},
  "gamma_API": {"min": 20, "max": 45, "unit": "degrees API"},
  "T": {"min": 100, "max": 250, "unit": "degrees Fahrenheit"}
}
```

---

### CORRELATION_008

```yaml
name: "Owolabi (1984) - North Slope"
region: "Alaska, North Slope"
id: "owolabi2"
```

**Formula**:

$$p_b = -987.56359 + 179.58816 \left[ \left( \frac{R_s}{\gamma_g} \right)^{0.48088266} \frac{T^{0.093538150}}{\gamma_{API}^{0.16648326}} \right]$$

**LaTeX**:
```latex
p_b = -987.56359 + 179.58816 \left[ \left( \frac{R_s}{\gamma_g} \right)^{0.48088266} \frac{T^{0.093538150}}{\gamma_{API}^{0.16648326}} \right]
```

**Input parameters**: `Rs`, `gamma_g`, `T`, `gamma_API`

**Output**: `pb`

**Validity**:
```json
{
  "Rs": {"min": 100, "max": 2000, "unit": "scf/STB"},
  "gamma_g": {"min": 0.55, "max": 1.0, "unit": "dimensionless"},
  "gamma_API": {"min": 15, "max": 40, "unit": "degrees API"},
  "T": {"min": 80, "max": 220, "unit": "degrees Fahrenheit"}
}
```

---

### CORRELATION_009

```yaml
name: "Al-Marhoun (1985)"
region: "Saudi Arabia"
id: "almarhoun"
```

**Formulas**:

$$X = R_s^{0.722569} \frac{\gamma_o^{3.046590}}{\gamma_g^{1.879109}} (T + 459.67)^{1.302347}$$

$$p_b = -64.13891 + 7.02362 \times 10^{-3} X - 2.278475 \times 10^{-9} X^2$$

**LaTeX**:
```latex
X = R_s^{0.722569} \frac{\gamma_o^{3.046590}}{\gamma_g^{1.879109}} (T + 459.67)^{1.302347}
p_b = -64.13891 + 7.02362 \times 10^{-3} X - 2.278475 \times 10^{-9} X^2
```

**Input parameters**: `Rs`, `gamma_g`, `T`, `gamma_API` (for gamma_o calculation)

**Output**: `pb`

**Validity**:
```json
{
  "Rs": {"min": 50, "max": 2500, "unit": "scf/STB"},
  "gamma_g": {"min": 0.7, "max": 1.3, "unit": "dimensionless"},
  "gamma_API": {"min": 20, "max": 50, "unit": "degrees API"},
  "T": {"min": 120, "max": 300, "unit": "degrees Fahrenheit"}
}
```

---

## PARSING GUIDE

Для программного распознавания и парсинга формул:

### Структура документа

1. **METADATA** — JSON-блок с метаданными документа
2. **VARIABLES** — таблица с описанием всех переменных
3. **CORRELATIONS** — секция с корреляциями, каждая начинается с `### CORRELATION_XXX`

### Формат каждой корреляции

```
### CORRELATION_XXX
```yaml
name: "Название"
region: "Регион"
id: "идентификатор"
```
**Formula**: визуальная формула в $$...$$
**LaTeX**: код LaTeX в блоке ```latex ... ```
**Input parameters**: список входных параметров
**Output**: выходной параметр
**Validity**: JSON с границами применимости
```

### Рекомендации по парсингу

1. Используйте YAML-блок для извлечения name, region, id
2. LaTeX-код из блока ```latex可以直接 передавать в парсер LaTeX
3. Validity содержит структурированные данные о границах в JSON формате
4. Все параметры используют единые единицы измерения из METADATA

---

## END OF DOCUMENT
