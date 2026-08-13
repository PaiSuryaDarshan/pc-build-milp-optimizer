# PC Build MILP Optimizer

> **An Excel-driven PC configuration optimiser that treats building a PC as what it really is: a constrained optimisation problem.**

A Python optimisation engine for finding high-utility, fully compatible PC builds under a fixed budget, using **Google OR-Tools**, integer decision variables, hardware constraints, workload-specific performance weighting, new/used pricing, budget sweeps, and Pareto analysis.

---

## 📰 Why does this exist?

PC hardware pricing has become weird.

And, more importantly, different components don't necessarily become expensive at the same time.

The GPU market provides a particularly good example.

### 2023 — The GPU market "normalises"... sort of

By the end of 2023, the extraordinary cryptocurrency-era GPU shortage had largely disappeared. TechSpot's year-end analysis described the broader GPU market as having returned to relatively normal pricing behaviour, with most RTX 40-series cards at or below MSRP.

There was one rather large exception: the RTX 4090.

Its lowest observed US retail price moved from roughly **$1,700 in October to $2,000 in November and December**, approximately **25% above its $1,600 MSRP**.

[TechSpot — GPU Pricing Update: 2023 Year in Review](https://www.techspot.com/article/2784-gpu-pricing-update/?utm_source=chatgpt.com)

The market was no longer experiencing the absurd shortages of the cryptocurrency boom, but "normal" didn't necessarily mean cheap.

---

### 2024 — AI changes the economics

The AI boom introduced another source of demand for high-performance silicon.

One European market analysis found that the average wholesale selling price of its 100 most-clicked graphics cards increased from approximately **€812 in Q1 2023 to €1,913 in Q1 2024**. The analysis connected the change partly to Nvidia's increasing focus on the much more profitable AI accelerator market.

At the consumer level, the picture was more nuanced. TechSpot's 2024 tracking found many mainstream GPU prices relatively flat rather than universally skyrocketing; the RTX 4070, for example, remained around $550 for an extended period.

[ITscope — Graphics cards and the AI boom, Q1 2024](https://blog.itscope.com/en/itscope-market-barometer-q1-2024?utm_source=chatgpt.com)

[TechSpot — 2024 GPU Pricing Update](https://www.techspot.com/article/2855-gpu-pricing-update/?utm_source=chatgpt.com)

So the important observation wasn't simply:

> **"Everything became more expensive."**

It was that different parts of the hardware market were beginning to move differently.

---

### 2025–2026 — It gets weird again

The next major disruption came from AI-driven demand for memory and compute.

Between **November 2025 and February 2026**, global GPU prices reportedly increased by around **15% on average**, with some high-end products moving considerably more.

Then memory became an even bigger problem.

By 2026, analyses of the memory market were describing extraordinary increases in RAM pricing as AI infrastructure consumed enormous quantities of memory and manufacturers prioritised high-value products such as HBM. One analysis suggested inflation-adjusted RAM cost per gigabyte had effectively returned to levels associated with the late 2000s.

And in August 2026, another GPU price survey found some RTX 50-series median retail prices rising dramatically in only two months:

| GPU              | June 2026 | August 2026 | Change |
| ---------------- | --------: | ----------: | -----: |
| RTX 5060         |   $369.99 |     $469.99 |   +27% |
| RTX 5060 Ti 16GB |   $569.99 |     $804.99 |   +39% |
| RTX 5070         |   $659.99 |     $899.99 |   +36% |
| RTX 5090         | $4,299.99 |   $4,699.99 |    +9% |

[Tom's Hardware — RTX 50-series prices spike in August 2026](https://www.tomshardware.com/pc-components/gpus/geforce-rtx-50-series-gpu-prices-spike-as-much-as-39-percent-as-blackwell-price-hikes-hit-the-us-rtx-5070-gets-a-36-percent-hike-rtx-5060-up-27-percent-at-the-median-of-newegg-listings?utm_source=chatgpt.com)

The DIY PC market therefore isn't experiencing one simple uniform inflation rate.

It is experiencing **component-specific disequilibrium**.

---

# The interesting bit: one expensive component can make another cheaper

This was the part that made me interested in the problem.

Suppose RAM suddenly becomes extremely expensive.

A rational consumer might decide:

> *I'll wait before building my PC.*

That doesn't just affect RAM demand.

That consumer also doesn't buy:

* a motherboard,
* a CPU,
* a PSU,
* a case,
* a cooler,
* or potentially a GPU.

Demand for complementary components can therefore weaken.

Retailers and manufacturers may subsequently discount slower-moving inventory.

The exact causal relationship is obviously more complicated than *"RAM goes up → motherboard goes down"* — supply contracts, inventories, product launches, regional pricing and manufacturer strategy all matter.

But the underlying idea is important:

**PC component markets don't necessarily move together.**

A terrible time to buy one component can simultaneously create an unusually attractive price for another.

Recent reports have even documented retailers bundling extremely scarce GPUs with multiple motherboards and other components, apparently as a mechanism for moving slower-selling inventory.

And that creates an interesting optimisation problem.

---

# 💡 The idea

Instead of asking:

> **"What is the best PC?"**

I wanted to ask:

> **"Given everything actually available to me right now — new and second-hand — what combination of components produces the highest utility without exceeding my budget?"**

That's subtly different.

A £450 used GPU might dominate a £600 new GPU.

A 24 GB GPU might be considerably more useful for local AI workloads than a faster gaming GPU with 12 GB.

A discounted motherboard might justify moving from one CPU platform to another.

Spending £70 more on the GPU might be worthwhile if £70 can simultaneously be recovered by choosing a motherboard currently trading unusually cheaply.

And the "best" build changes depending on whether I care about:

**AI development, animation/rendering, gaming, price/performance, reliability, new-vs-used risk, or some weighted combination of all of them.**

At that point, manually comparing builds becomes increasingly stupid.

So I turned it into an optimisation problem.

---

# 🧮 What this repository actually does

The basic pipeline is:

```text
PC_Parts.xlsx
      │
      ▼
Data validation
      │
      ▼
Compatibility engine
      │
      ▼
Performance / utility scoring
      │
      ▼
Integer optimisation
      │
      ▼
Top-N compatible builds
      │
      ├── Budget sweep
      ├── Workload profiles
      └── Pareto analysis
      │
      ▼
Optimised_Builds.xlsx
```

Excel deliberately remains the human-facing database.

I manually enter real components that I can actually purchase:

```text
Component
Model
Condition
Seller
Price
Shipping
Warranty
VRAM
RAM
Socket
Power
Dimensions
Performance data
...
```

Python handles the part humans are bad at:

**systematically evaluating combinations.**

---

# ⚙️ Optimisation model

The problem is fundamentally a **0–1 integer optimisation problem**.

For every purchasable component (i), define:

[
x_i \in {0,1}
]

where:

```text
xᵢ = 1  → buy the component
xᵢ = 0  → don't buy the component
```

A simplified objective is:

[
\max \sum_i U_i x_i
]

where (U_i) represents the contribution of a component to the overall utility of the build.

The optimiser operates subject to constraints.

For example:

[
\text{Total Cost} \leq \text{Budget}
]

and:

[
\sum_{\text{CPU}}x_i = 1
]

[
\sum_{\text{GPU}}x_i = 1
]

[
\sum_{\text{Motherboard}}x_i = 1
]

along with compatibility and hardware requirements.

---

## Solver

The production optimisation engine uses **Google OR-Tools CP-SAT**.

Technically, CP-SAT is a constraint-programming/SAT-based integer solver rather than a traditional LP-relaxation MILP solver.

The model itself, however, naturally resembles a **binary mixed/integer optimisation formulation**, with component-selection variables and linear/logical constraints.

That makes CP-SAT particularly useful here because PC configuration contains a large number of discrete decisions:

```text
Select / don't select
Compatible / incompatible
New / used
AM5 / LGA1700
DDR4 / DDR5
Fits / doesn't fit
Enough power / insufficient power
```

[Google OR-Tools Optimization Documentation](https://developers.google.com/optimization?utm_source=chatgpt.com)

A simple brute-force implementation is also retained as a transparent baseline and correctness check.

---

# 🎯 Multi-objective utility

There isn't one universal definition of a "good PC."

The repository therefore supports configurable priorities.

For example:

```yaml
weights:
  ai: 0.50
  animation: 0.30
  gaming: 0.20
```

A different user could instead choose:

```yaml
weights:
  ai: 0.10
  animation: 0.10
  gaming: 0.80
```

Same market.

Same components.

Same budget.

Potentially a completely different optimal machine.

---

# 🤖 AI-first optimisation

One motivation for building this was that traditional gaming-oriented price/performance comparisons don't necessarily represent my workload.

For local AI development, factors such as:

* GPU architecture
* VRAM capacity
* CUDA/software support
* memory bandwidth
* system RAM
* CPU capability
* storage

can matter differently from average gaming FPS.

A second-hand 24 GB GPU may therefore remain extremely attractive for certain workloads even when a newer GPU provides superior gaming efficiency.

The scoring system keeps workload-specific performance separate so those trade-offs remain visible rather than being collapsed prematurely into one generic "performance" number.

---

# ♻️ New vs used

Second-hand hardware is treated as another optimisation dimension rather than automatically being considered better or worse.

The database can contain:

```text
RTX XXXX | New  | £600
RTX XXXX | Used | £430
```

as two separate purchasing options.

The optimiser can account for:

* effective purchase price,
* warranty,
* condition,
* seller type,
* component-specific risk,
* and configurable used-hardware penalties.

This means a used component only wins when its additional utility per pound compensates for the risk assigned to it.

---

# 🔌 Compatibility constraints

A £1,200 collection of individually excellent components is useless if they don't form a computer.

The optimisation therefore enforces constraints such as:

```text
CPU socket = motherboard socket

RAM generation = motherboard RAM generation

GPU length <= case GPU clearance

Cooler height <= case cooler clearance

PSU capacity >= estimated system load × safety factor

RAM >= configured minimum

VRAM >= configured minimum

Storage >= configured minimum

Total effective price <= budget
```

Invalid builds never enter the final ranking.

---

# 💷 Budget sweeps

One optimal build isn't necessarily the most interesting result.

The repository can repeatedly optimise across a range of budgets:

```text
£800
£850
£900
£950
...
£1,500
£1,550
```

This produces a performance-versus-budget curve.

The useful question then becomes:

> **Where does spending another £50 stop producing a meaningful improvement?**

That helps identify the **price/performance knee** rather than blindly spending the maximum available budget.

---

# 📈 Pareto frontier

Sometimes there is no single best machine.

Imagine:

```text
Build A
£1,180
AI: 98
Gaming: 82

Build B
£1,210
AI: 91
Gaming: 95

Build C
£1,245
AI: 95
Gaming: 91
```

None universally dominates the others.

The repository therefore identifies **Pareto-optimal configurations**: builds where improving one objective requires sacrificing another.

This lets the final decision remain a human one.

The optimiser removes bad choices.

It doesn't pretend subjective preferences don't exist.

---

# 🧠 And, admittedly, I wanted an excuse to practise optimisation

There is another reason this repository exists.

I wanted to properly practise **integer optimisation, constraint modelling and solver-based programming** on a problem I actually cared about.

Not just:

```python
model.solve()
```

followed by pretending I understood what happened.

The project is deliberately intended to involve:

* defining decision variables,
* constructing objective functions,
* translating physical requirements into constraints,
* thinking about discrete optimisation,
* validating solutions,
* comparing brute force against solver output,
* exploring multi-objective optimisation,
* performing Pareto analysis,
* and understanding why the optimiser selected what it selected.

And I wanted the implementation to be **hard-coded, not vibe-coded**.

AI can help me debug, review ideas and explain things, but the point of this repository is for me to understand and deliberately write the important optimisation logic myself.

If I can't explain a constraint mathematically, I probably shouldn't be hiding it behind an optimisation library.

---

# 🏗️ Architecture

```text
pc-build-milp-optimizer/
│
├── data/
│   └── pc_parts.xlsx
│
├── config/
│   └── default_config.yaml
│
├── src/
│   └── pc_optimizer/
│       ├── data_loader.py
│       ├── validation.py
│       ├── compatibility.py
│       ├── scoring.py
│       ├── brute_force.py
│       ├── optimizer.py
│       ├── pareto.py
│       ├── reporting.py
│       └── cli.py
│
├── tests/
│
├── output/
│   ├── optimised_builds.xlsx
│   └── plots/
│
├── README.md
├── requirements.txt
└── pyproject.toml
```

The modules deliberately separate:

**data → validation → compatibility → scoring → optimisation → reporting**

so that the optimisation model remains understandable and testable.

---

# 🚀 Example

```bash
python -m pc_optimizer optimise --budget 1250 --profile ai
```

Example conceptual output:

```text
OPTIMAL BUILD
Budget: £1,250

CPU          Ryzen 9 7900              Used     £235
GPU          RTX 3090 24GB             Used     £445
Motherboard  B650 Gaming X AX          New      £125
RAM          32GB DDR5-6000            New       £75
SSD          2TB NVMe                  New       £90
PSU          850W Gold                 New       £90
Case         Fractal Pop Air           New       £70
Cooler       Phantom Spirit            New       £38

TOTAL                                  £1,168

AI Score          94.2
Animation Score   91.8
Gaming Score      86.4
Overall Utility   92.7
```

The numbers above are illustrative only.

Real optimisation is only as meaningful as the benchmark and market data supplied to the model.

---

# ⚠️ What this project does **not** claim

This repository does not magically know the objective value of a GPU.

Garbage in still means garbage out.

Performance scores must ultimately be supported by appropriate benchmark data, and second-hand risk cannot be represented perfectly by a scalar penalty.

The optimiser answers:

> **"Given these data, assumptions, constraints and preferences, what is mathematically optimal?"**

It does **not** answer:

> **"What is objectively the world's best PC?"**

That distinction matters.

---

# 🔮 Future work

Potential extensions include automated price collection, historical price tracking, Blender benchmark ingestion, gaming benchmark ingestion, local-LLM inference benchmarks, CUDA-specific scoring, electricity-cost modelling, component depreciation, seller-risk modelling, price forecasting and eventually a lightweight web interface.

But those come later.

The first objective is much simpler:

> **Build a transparent optimisation model, understand every important constraint, feed it real market data, and find out whether mathematics can build me a better PC than I can manually.**
