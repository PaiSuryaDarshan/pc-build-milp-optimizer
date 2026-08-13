# PC Build Optimizer

An Excel-driven Python application for finding high-utility, compatible PC
builds under a configurable budget. It supports AI, animation, gaming, and value
priorities; new and used parts; hard hardware constraints; Top-N results; budget
sweeps; and Pareto analysis.

The project includes both a transparent brute-force reference implementation and
a scalable Google OR-Tools CP-SAT solver. For the market context and motivation
behind the project, see [background.md](background.md).

## Features

- Excel database designed for manual maintenance
- Input validation with part-specific error messages
- CPU/socket, RAM, clearance, power, budget, and capacity constraints
- Configurable workload profiles and minimum requirements
- Transparent used-component risk penalties
- Best-build and Top-N optimisation
- Exact brute-force baseline and CP-SAT solver
- Configurable budget sweeps
- Pareto-optimal build detection
- Excel reports containing the actual selected components
- Performance-versus-budget and Pareto plots

## How it works

```text
data/pc_parts.xlsx
        │
        ▼
Input validation
        │
        ▼
Compatibility and minimum requirements
        │
        ▼
Workload scoring and used-part risk
        │
        ▼
Brute force or OR-Tools CP-SAT
        │
        ├── Top-N builds
        ├── Budget sweep
        └── Pareto frontier
        │
        ▼
output/optimised_builds.xlsx + output/plots/
```

## Requirements

- Python 3.11 or newer
- Microsoft Excel, LibreOffice, or another `.xlsx` editor for maintaining parts
- macOS, Linux, or Windows

## Installation

Clone or download the repository, enter its directory, and create an isolated
environment:

```bash
python -m venv .venv
```

Activate it on macOS or Linux:

```bash
source .venv/bin/activate
```

Activate it on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Install the package and test dependencies:

```bash
python -m pip install --upgrade pip
pip install -e ".[dev]"
```

The editable installation makes both commands available:

```bash
python -m pc_optimizer --help
pc-optimizer --help
```

The examples below use `python -m pc_optimizer` because it is explicit and works
consistently across platforms.

## Quick start

The repository includes a ready-to-edit database at `data/pc_parts.xlsx` and an
untouched reference copy at `data/example_pc_parts.xlsx`.

```bash
python -m pc_optimizer validate
python -m pc_optimizer optimise --budget 1250 --profile ai
```

The result is written to:

```text
output/optimised_builds.xlsx
```

The bundled rows and scores are synthetic examples only. Replace them with
parts and evidence-based scores relevant to your market before making a purchase.

## Creating and maintaining `pc_parts.xlsx`

### Recommended method

1. Open `data/pc_parts.xlsx` in Excel.
2. Delete the synthetic example rows you do not want.
3. Add one row for every purchasing option you could actually buy.
4. Keep the existing column names unchanged.
5. Extend the Excel table to include newly added rows if Excel does not do so
   automatically.
6. Copy the `Effective_Price_GBP` formula into every new row.
7. Save the file as `data/pc_parts.xlsx`.
8. Run validation before optimisation.

```bash
python -m pc_optimizer validate
```

To regenerate both workbook templates from code:

```bash
python scripts/create_example_workbook.py
```

This overwrites both template workbooks, so do not run it after entering data
unless your edited workbook is backed up.

### One row means one purchasing option

New, used, refurbished, seller-specific, and variant-specific listings must be
separate rows with unique `Part_ID` values:

| Part_ID | Type | Model | Condition | Seller | Price_GBP |
| --- | --- | --- | --- | --- | ---: |
| GPU-001 | GPU | RTX 3090 24GB | Used | eBay seller A | 450 |
| GPU-002 | GPU | RTX 3090 24GB | New | Retailer B | 700 |
| GPU-003 | GPU | RTX 4070 12GB | Used | CeX | 390 |

Do not combine a price range, multiple sellers, or new and used stock in one row.

### Required for every row

| Column | Meaning |
| --- | --- |
| `Part_ID` | Stable, unique identifier such as `CPU-001` |
| `Type` | `CPU`, `GPU`, `Motherboard`, `RAM`, `SSD`, `PSU`, `Case`, or `CPU Cooler` |
| `Brand` | Manufacturer or brand |
| `Model` | Human-readable model name |
| `Condition` | `New`, `Open Box`, `Refurbished`, or `Used` |
| `Price_GBP` | Item price, excluding shipping |
| `Shipping_GBP` | Delivery cost; enter `0` when included |
| `Effective_Price_GBP` | Formula: item price plus shipping |

`Seller`, `URL`, `Date_Found`, `Warranty_Months`, `Variant`, and `Notes` are
strongly recommended because they make listings auditable and affect risk
assessment where applicable.

### Component-specific fields

Blank cells are expected when a field does not apply to a component. Populate
the following fields for each relevant type:

| Type | Required hardware fields |
| --- | --- |
| CPU | `CPU_Socket`, `CPU_Cores`, `CPU_Threads`, `Power_W` |
| GPU | `VRAM_GB`, `GPU_Length_mm`, `Power_W` |
| Motherboard | `Motherboard_Socket`, `Motherboard_RAM_Type`, preferably `Power_W` |
| RAM | `RAM_GB`, `RAM_Type`, preferably `RAM_Speed_MHz` and `Power_W` |
| SSD | `Storage_GB`, `Storage_Type`, preferably `Power_W` |
| PSU | `PSU_W`, preferably `PSU_Efficiency` |
| Case | `Case_Max_GPU_Length_mm`, `Case_Max_Cooler_Height_mm` |
| CPU Cooler | `Cooler_Height_mm`, preferably `Power_W` |

Socket and RAM-type text must match exactly between compatible rows. For
example, use `AM5` on both the CPU and motherboard and `DDR5` on both the RAM and
motherboard. Measurements are in millimetres, capacities are in GB, power is in
watts, and all prices are GBP.

### Score fields

The workbook accepts normalised 0–100 user-defined scores:

- `AI_Score`
- `Animation_Score`
- `Gaming_Score`
- `Performance_Score`
- `Reliability_Score`
- `Value_Score`

These are not raw benchmark columns. Keep source benchmark measurements in a
separate worksheet or external dataset, normalise them consistently, and record
the method and source in `Notes`. Do not mix incomparable measurements or present
the bundled synthetic values as real benchmarks.

Practical scoring guidance:

- use the same 0–100 reference scale for every option;
- compare like with like within each workload;
- document benchmark source, date, and normalisation method;
- avoid giving non-performance infrastructure parts exaggerated workload scores;
- update `Value_Score` when prices change; and
- retain URLs and dates so stale listings can be identified.

### Spreadsheet quality-of-life features

The generated workbook includes an Excel table, filters, frozen headers,
condition/type dropdowns, input-cell highlighting, conditional score formatting,
column widths, instructions, and effective-price formulas. Adding rows inside the
table normally propagates validation and formulas automatically.

## Configuration

Defaults and profiles live in `config/default_config.yaml`:

```yaml
budget_gbp: 1250

weights:
  ai: 0.45
  animation: 0.30
  gaming: 0.20
  value: 0.05

requirements:
  minimum_ram_gb: 32
  minimum_vram_gb: 12
  minimum_storage_gb: 1000

used_parts:
  allowed: true
  maximum_used_parts: null
  risk_penalty_enabled: true

psu:
  headroom_multiplier: 1.25

results:
  top_n: 10
```

Weights must be non-negative and sum to `1.0`. Available profiles are
`balanced`, `ai`, `animation`, `gaming`, and `value`. Add or edit profiles in
YAML rather than changing Python source.

Use another configuration file with the global option placed before the
subcommand:

```bash
python -m pc_optimizer --config config/my_config.yaml optimise --budget 1400
```

Likewise, use another workbook with:

```bash
python -m pc_optimizer --data data/my_parts.xlsx validate
```

## Commands

### Validate the database

```bash
python -m pc_optimizer validate
```

Validation checks duplicate IDs, negative prices, unknown types or conditions,
non-positive capacities, and missing type-specific compatibility data. Errors
identify the affected `Part_ID` or spreadsheet row. Invalid input is not silently
dropped.

### Find the best and Top-N builds

```bash
python -m pc_optimizer optimise
python -m pc_optimizer optimise --budget 1250
python -m pc_optimizer optimise --budget 1250 --profile ai
python -m pc_optimizer optimise --profile gaming --top 20
```

The CP-SAT solver is the default. To use the educational exhaustive-search
baseline:

```bash
python -m pc_optimizer optimise --engine brute_force
```

Brute force is useful for learning and small-dataset correctness comparisons,
but the number of combinations grows multiplicatively with the number of parts.

### Run a budget sweep

```bash
python -m pc_optimizer budget-sweep --min 800 --max 1600 --step 50
python -m pc_optimizer budget-sweep --min 900 --max 1500 --step 100 --profile ai
```

The maximum value is inclusive when it falls on the selected step. The command
exports the best feasible build at each budget, the Pareto frontier, and plots.

### Run tests

```bash
pytest
```

## Compatibility and hard constraints

A returned build contains exactly one CPU, GPU, motherboard, RAM kit, PSU, case,
CPU cooler, and—in the current implementation—one SSD. It must satisfy:

```text
CPU socket == motherboard socket
RAM type == motherboard RAM type
GPU length <= case GPU clearance
cooler height <= case cooler clearance
PSU wattage >= estimated component power × headroom multiplier
RAM >= configured minimum
VRAM >= configured minimum
storage >= configured minimum
effective price <= budget
used-part count <= configured maximum, when set
```

These rules are hard constraints. A high-scoring incompatible build cannot enter
the results.

## Scoring model

AI, animation, gaming, and value build scores are component-relevance weighted
means, not sums. This keeps every metric on the input 0–100 scale and prevents a
build from receiving a higher score merely because it contains more parts.

For example, the GPU contributes 55% of the AI relevance weight, while the CPU
contributes 18%; RAM, storage, and supporting components provide the remainder.
Animation gives more weight to the CPU, and gaming strongly weights both the GPU
and CPU. Exact relevance weights are documented in
`src/pc_optimizer/scoring.py`.

```text
overall = ai_weight × AI
        + animation_weight × animation
        + gaming_weight × gaming
        + value_weight × value
        - used_part_risk_penalty
```

Missing workload scores do not contribute to that metric's weighted mean.

## Used-component risk

New and second-hand options compete directly on price and utility. Non-new parts
receive a small, transparent penalty determined by:

- component type—the default penalty is greater for GPUs and PSUs than RAM;
- condition—open-box and refurbished parts receive smaller factors than used;
- warranty—longer warranty reduces, but does not entirely remove, the penalty.

Risk penalties can be disabled in YAML. Set `allowed: false` to require an
all-new build, or set `maximum_used_parts` to an integer to cap used selections.

## Outputs

### Optimisation workbook

`output/optimised_builds.xlsx` includes selected part IDs and models, total cost,
used-part count, workload scores, risk penalty, and overall score. A normal
optimisation produces best-build and Top-N/profile sheets. A budget sweep writes
budget and Pareto sheets.

Running a new command replaces the existing output workbook. Copy important
results elsewhere before another run.

### Plots

A budget sweep generates these files in `output/plots/`:

- `budget_vs_ai.png`
- `budget_vs_animation.png`
- `budget_vs_gaming.png`
- `budget_vs_overall.png`
- `pareto_frontier.png`

The curves help identify diminishing returns. The Pareto frontier contains
builds for which no alternative is simultaneously no more expensive, at least
as good in AI, animation, and gaming, and strictly better on at least one of
those dimensions.

## Repository structure

```text
pc-build-milp-optimizer/
├── background.md
├── README.md
├── config/
│   └── default_config.yaml
├── data/
│   ├── pc_parts.xlsx
│   └── example_pc_parts.xlsx
├── output/
│   └── plots/
├── scripts/
│   ├── budget_sweep.py
│   ├── create_example_workbook.py
│   └── run_optimizer.py
├── src/pc_optimizer/
│   ├── brute_force.py
│   ├── cli.py
│   ├── compatibility.py
│   ├── config.py
│   ├── data_loader.py
│   ├── models.py
│   ├── optimizer.py
│   ├── pareto.py
│   ├── reporting.py
│   ├── scoring.py
│   └── validation.py
└── tests/
```

The modules deliberately separate data loading, validation, compatibility,
scoring, optimisation, Pareto analysis, and reporting so each rule remains
understandable and testable.

## Troubleshooting

### `No valid build found`

Check whether the budget can cover one of every required component, then review
minimum RAM, VRAM, and storage. Also confirm socket/RAM compatibility, case
clearances, PSU capacity, and used-part limits.

### A valid-looking row fails validation

Ensure the `Type` and `Condition` values match the supported dropdown values,
IDs are unique, numeric cells contain numbers rather than units such as `850W`,
and every relevant compatibility field is populated.

### `No module named pc_optimizer`

Activate the virtual environment and install the project:

```bash
pip install -e ".[dev]"
```

### Excel formulas were not copied

Set `Effective_Price_GBP` to `Price_GBP + Shipping_GBP` for the affected row. If
the table formatting has been damaged, make a backup and regenerate a clean
workbook template with `python scripts/create_example_workbook.py`.

## Current limitations

- Scores are manually supplied and are not automatically derived from benchmarks.
- Exactly one storage device is currently selected.
- Compatibility does not yet cover every form factor, connector, BIOS, cooler
  mount, PCIe lane, or transient-power consideration.
- Prices and listing availability are not scraped or updated automatically.
- Used-market risk is necessarily an approximation.
- Pareto analysis is performed over the builds supplied to it, not every
  imaginable hardware configuration.

Always independently verify current prices, seller legitimacy, physical fit,
firmware support, connectors, and manufacturer power recommendations before
purchasing hardware.

## Future development

The architecture leaves room for raw benchmark ingestion, Blender and gaming
datasets, local-LLM inference measurements, CUDA-aware scoring, multiple storage
devices, automated price collection, price history, electricity-cost modelling,
seller reliability, depreciation, forecasting, and a web interface.
