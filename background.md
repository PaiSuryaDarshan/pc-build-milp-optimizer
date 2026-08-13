# Background and Motivation

This document contains the economic context and motivation behind the PC Build
Optimizer. For installation and usage instructions, see [README.md](README.md).

## 📰 Why does this exist?

PC hardware pricing has become weird.

More importantly, the different parts required to build a PC do not move neatly
up and down together.

A GPU can be becoming cheaper while RAM is becoming more expensive. Memory can
collapse in price while GPU supply remains constrained. A particular GPU tier
can fall towards MSRP while the flagship moves in the opposite direction.

For someone buying an entire system rather than one isolated component, that
creates an interesting problem:

> The cheapest time to buy each individual component is not necessarily the same
> moment, and the best overall build depends on the prices of all of them at
> once.

The GPU and memory markets between 2023 and 2026 provide a particularly useful
example.

---

## 2023: GPUs begin to normalise while memory collapses

The beginning of 2023 looked relatively encouraging for consumer GPU buyers.

By March, TechSpot described GPU price inflation as being largely behind the
market. The RTX 4090, for example, had fallen from approximately **$1,800 in
February to $1,650 in March**, placing it only slightly above its $1,600 launch
MSRP. Availability of current-generation cards had also improved substantially.

[TechSpot — GPU Pricing Update, March 2023: Back to MSRP](https://www.techspot.com/article/2647-gpu-pricing-update/)

At almost exactly the same time, however, the memory market was experiencing a
very different problem: **oversupply**.

TrendForce estimated that average PC DRAM selling prices would decline by
approximately **15–20% quarter-on-quarter in Q2 2023**, citing large inventories
and weak demand. DDR4 was particularly exposed to the oversupply.

[TrendForce — DRAM and NAND Flash Prices Expected to Fall Further in Q2 2023](https://www.trendforce.com/presscenter/news/20230509-11667.html)

So already the market was not moving as one unit.

```text
Early 2023

GPU market      → availability improving / pricing normalising
PC DRAM         → significant price decline
Consumer demand → comparatively weak
```

For a complete system builder, cheap memory could therefore partially compensate
for a GPU that was still expensive in absolute terms.

---

## Late 2023: the direction begins to reverse

The memory decline did not continue indefinitely.

By October 2023, TrendForce was forecasting **3–8% quarter-on-quarter increases
in PC DRAM contract prices for Q4**, following production cuts and attempts by
memory manufacturers to restore profitability.

DDR5 had already begun rising during Q3, while DDR4 manufacturers were becoming
increasingly unwilling to continue reducing prices.

[TrendForce — Q4 DRAM Contract Prices Set to Rise](https://www.trendforce.com/presscenter/news/20231013-11880.html)

The GPU market was simultaneously producing one of the clearest examples of why
a single statement such as "GPU prices were falling" can be misleading.

Much of the market was behaving relatively normally, but the RTX 4090 diverged.

TechSpot recorded the RTX 4090 at around **$1,700 in November 2023**, and by its
December review the card was selling for roughly **$2,000**, substantially above
its $1,600 MSRP.

[TechSpot — Black Friday GPU Buying Guide, November 2023](https://www.techspot.com/article/2771-gpu-pricing-update/)

[TechSpot — GPU Pricing Update: 2023 Year in Review](https://www.techspot.com/article/2784-gpu-pricing-update/)

The result was a market in which:

```text
PC DRAM        ↓ dramatically earlier in 2023
PC DRAM        ↑ begins reversing in late 2023

Mainstream GPU pricing → relatively normal
RTX 4090 pricing       → sharply elevated
```

That distinction matters.

There was no single "PC hardware inflation rate."

---

## 2024: RAM goes up, while mainstream GPU pricing mostly goes sideways

The DRAM recovery became much more obvious in 2024.

In January, TrendForce forecast **10–15% increases in PC DRAM contract prices in
Q1 2024**, with DDR5 expected to lead the increase.

[TrendForce — DRAM Contract Prices Projected to Increase 13–18% in Q1 2024](https://www.trendforce.com/presscenter/news/20240108-11988.html)

After the April 2024 Taiwan earthquake affected semiconductor production,
TrendForce subsequently raised its estimate for overall Q2 DRAM contract-price
growth to approximately **13–18%**.

[TrendForce — DRAM Contract Prices for Q2 Adjusted to a 13–18% Increase](https://www.trendforce.com/presscenter/news/20240507-12128.html)

Consumer GPU pricing, however, did not exhibit an equivalent broad increase.

TechSpot's June 2024 analysis described the current-generation GPU market as
having experienced **little to no price movement across 2024**. The RTX 4070,
for example, had remained around **$550 since September 2023**.

[TechSpot — GPU Pricing Update, June 2024](https://www.techspot.com/article/2855-gpu-pricing-update/)

That gives a particularly useful example of the disequilibrium this project is
interested in:

```text
2024

PC DRAM       ↑ meaningful price increases
Mainstream GPU prices → broadly flat
```

Buying decisions therefore depended increasingly on the **combination** of
components rather than on whether "PC hardware" in general was cheap or
expensive.

---

## Late 2024 into early 2025: memory weakens again

The memory cycle then moved in the opposite direction once more.

At the end of 2024, TrendForce forecast that PC DRAM contract prices would fall
approximately **8–13% in Q1 2025**.

The cited causes included weak end-market demand, inventory reduction by PC
manufacturers, increased DDR4 supply, and cautious purchasing.

[TrendForce — PC DRAM Prices Expected to Drop 8–13% in Q1 2025](https://www.trendforce.com/presscenter/news/20241230-12424.html)

So in only about two years the simplified DRAM cycle had already looked like:

```text
Q2 2023       ↓ 15–20%
Late 2023     ↑ reversal begins
Q1 2024       ↑ roughly 10–15%
Q2 2024       ↑ further increases
Q1 2025       ↓ roughly 8–13%
```

That is exactly the kind of market where a static "best PC build" list ages
quickly.

---

## 2025: next-generation GPUs launch expensive, then actually come down

The RTX 50-series introduced another useful price cycle.

Launch-period supply was constrained and real retail pricing for some Blackwell
GPUs substantially exceeded Nvidia's advertised pricing.

But that did **not** simply continue upward throughout the year.

By May 2025, European RTX 50-series prices had begun moving downward.

TechSpot reported that the least-expensive RTX 5080 had fallen from about
**€1,169 at the end of March to €1,119**, approximately the local MSRP.

More strikingly, the RTX 5070 Ti fell from around **€869 to €799**, putting
available models below the local suggested price.

[TechSpot — RTX 50-Series GPU Prices Drop Below MSRP in Europe](https://www.techspot.com/news/107753-nvidia-rtx-50-series-gpu-prices-drop-below.html)

By September 2025, the same phenomenon was visible in the US market.

Tom's Hardware reported RTX 50-series cards finally reaching or falling below
MSRP, including RTX 5070 models available below the card's **$549 launch
price**.

[Tom's Hardware — RTX 50-Series GPUs Finally Selling at and Below MSRP](https://www.tomshardware.com/pc-components/gpus/geforce-rtx-50-series-gpus-are-finally-selling-at-and-below-msrp-rtx-5070-dips-below-usd549)

By late November, TechSpot was finding the RTX 5070 around **$500**, with some
Black Friday offers reaching roughly **$480**.

[TechSpot — Cost Per Frame: Best Value Graphics Cards, December 2025](https://www.techspot.com/article/3061-cost-per-frame-gpu/)

This is an important part of the story because it prevents the history from
being reduced to:

> GPUs kept getting more expensive because of AI.

They didn't.

At least some important consumer GPU segments **came down materially during
2025**.

---

## Late 2025: RAM suddenly becomes the problem

While GPU pricing was improving, the memory market began moving violently in the
other direction.

By November 2025, TrendForce reported extraordinary retail increases in DDR5
memory.

Citing retail data, it reported 64 GB DDR5 kits exceeding **$500**, with some
market tracking showing average 64 GB kit prices above **$600**, compared with
around **$200 earlier in the year**.

Reported increases for some newer DDR5 products were in the region of
**120–200%**.

[TrendForce — 64GB DDR5 RAM Reportedly Now Pricier Than a PlayStation 5](https://www.trendforce.com/news/2025/11/27/news-64gb-ddr5-ram-reportedly-now-pricier-than-a-playstation-5-amid-soaring-memory-costs/)

The important point here is the timing.

During parts of 2025:

```text
RTX 50-series GPUs       ↓ moving toward / below MSRP
DDR5 RAM                 ↑ rapidly becoming more expensive
```

The bottleneck in the cost of a new system had shifted.

That is almost the perfect example of why optimising the **whole PC** matters
more than optimising components independently.

---

## 2026: the memory shock becomes extreme

The situation intensified dramatically at the start of 2026.

In February, TrendForce revised its forecast for conventional DRAM contract
prices in Q1 2026 to an extraordinary **90–95% quarter-on-quarter increase**.

For **PC DRAM specifically**, TrendForce expected contract prices to increase by
**more than 100% quarter-on-quarter**.

The company attributed the imbalance primarily to strong AI and data-centre
demand consuming supply and strengthening memory manufacturers' pricing power.

[TrendForce — Memory Price Outlook for Q1 2026 Sharply Upgraded](https://www.trendforce.com/presscenter/news/20260202-12911.html)

That meant RAM was no longer a relatively small line item that could safely be
treated as an afterthought in a build.

For high-memory AI and workstation systems in particular, RAM could materially
change the optimal allocation of the entire budget.

---

## And expensive RAM began affecting everything around it

This is where the economics become particularly relevant to this project.

A person building a PC does not demand RAM independently.

RAM, CPUs, motherboards, GPUs, cases, cooling, storage, and PSUs are
**complementary goods** within a complete system.

If one essential component becomes prohibitively expensive, some buyers delay
the entire build.

By June 2026, reports citing industry sources suggested motherboard sales had
already fallen by **more than 25%**, with high RAM and SSD prices causing
enthusiasts to postpone new systems.

[Tom's Hardware — Rising RAM Prices Hit Motherboard Sales](https://www.tomshardware.com/pc-components/ram/lexar-regional-manager-says-that-ram-prices-are-expected-to-double-by-the-end-of-the-year-discounts-and-stabilized-prices-result-from-distributors-getting-rid-of-old-stock-or-sourcing-products-from-other-regions)

Separate reporting on the motherboard industry projected a roughly **28%
year-on-year contraction** across the four largest motherboard manufacturers in
2026.

[Tom's Hardware — Motherboard Sales Collapse by More Than 25%](https://www.tomshardware.com/pc-components/motherboards/motherboard-sales-collapse-by-more-than-25-percent-as-chipmakers-strangle-enthusiast-pc-market-to-build-more-ai-chips-asus-projected-to-sell-5-million-fewer-boards-in-2025-gigabyte-msi-and-asrock-also-expected-to-see-reduced-sales-numbers)

This supports the basic intuition behind this repository:

> Making one essential PC component extremely expensive can reduce demand for
> other components required to complete the same machine.

However, there is an important qualification.

It would be too simplistic to claim:

> RAM becomes expensive → motherboard prices automatically fall.

The evidence supports **falling motherboard demand and shipments**, not a
universal fall in motherboard prices.

Motherboard manufacturers were simultaneously exposed to their own component
and PCB cost pressures, and reports in August 2026 warned that those costs could
push some motherboard prices upward.

The more defensible conclusion is:

> Weak demand can create unusual discounts, bundles, and inventory-clearing
> opportunities in some complementary components even while their underlying
> production costs are moving in the opposite direction.

That distinction is important.

---

## 2026: GPU prices turn upward again

The relatively favourable GPU pricing seen during parts of 2025 did not last.

A global analysis comparing **November 2025 with February 2026** found average
pricing across a selection of Nvidia, AMD, and Intel GPUs had increased by
approximately **15%**.

Nvidia's higher-end products moved considerably more. In the US sample, the RTX
5070 Ti was reported around **37% more expensive**, while the RTX 5080 was
roughly **43% more expensive** than in November.

[Tom's Hardware — $1,000 Bought an RTX 5080 in November; Now It Buys an RTX 5070 Ti](https://www.tomshardware.com/pc-components/gpus/usd1-000-bought-an-rtx-5080-in-november-2025-now-it-only-buys-an-rtx-5070-ti-report-shows-15-percent-average-global-price-hike-across-nvidia-amd-and-intel-gpus)

There was still some temporary relief.

TechSpot's April 2026 global survey found the RTX 5080 had fallen approximately
**4% compared with February**, although it remained around **23% above MSRP on
average** across the surveyed regions.

[TechSpot — GPU Pricing Remains Broken, Even if It Has Stopped Getting Worse](https://www.techspot.com/article/3115-gpu-pricing-q2-2026/)

That again demonstrates the volatility:

```text
Early 2025        GPU prices elevated
Mid/late 2025     ↓ substantial easing on several RTX 50 models
Late 2025–Feb 26  ↑ sharp reversal
Feb–Apr 2026      ↓ small correction on some models
```

And then prices moved upward again.

---

## August 2026: GPUs get ugly again

By August 2026, US retail tracking showed another sharp increase across several
RTX 50-series models.

Median Newegg pricing reportedly changed as follows between June and August:

| GPU              | June 2026 | August 2026 | Change |
| ---------------- | --------: | ----------: | -----: |
| RTX 5050         |   $299.99 |     $314.99 |    +5% |
| RTX 5060         |   $369.99 |     $469.99 |   +27% |
| RTX 5060 Ti 8GB  |   $469.99 |     $529.99 |   +13% |
| RTX 5060 Ti 16GB |   $569.99 |     $804.99 |   +39% |
| RTX 5070         |   $659.99 |     $899.99 |   +36% |
| RTX 5070 Ti      | $1,099.99 |   $1,099.99 |   Flat |
| RTX 5080         | $1,461.99 |   $1,499.99 |    +3% |
| RTX 5090         | $4,299.99 |   $4,699.99 |    +9% |

[Tom's Hardware — RTX 50-Series Prices Spike as Much as 39% in August 2026](https://www.tomshardware.com/pc-components/gpus/geforce-rtx-50-series-gpu-prices-spike-as-much-as-39-percent-as-blackwell-price-hikes-hit-the-us-rtx-5070-gets-a-36-percent-hike-rtx-5060-up-27-percent-at-the-median-of-newegg-listings)

Not every card moved equally.

The RTX 5070 Ti was flat in that comparison, the RTX 5080 increased only
slightly, while the RTX 5060 Ti 16 GB and RTX 5070 moved dramatically.

AMD's contemporary pricing was also reported as moving far less aggressively
than those particular Nvidia products.

Once again:

> "GPU prices increased" is technically true, but not sufficiently descriptive
> to make a purchasing decision.

**Which GPU? Which manufacturer? Which memory configuration? Which country?
Which month?**

Those questions matter.

---

# The whole landscape

The simplified history now looks something like this:

| Period        | PC RAM / DRAM        | Consumer GPU market        | What mattered                          |
| ------------- | -------------------- | -------------------------- | -------------------------------------- |
| Early 2023    | ↓ sharply            | ↓ / normalising            | Memory oversupply                      |
| Late 2023     | ↑ begins             | Mostly stable, 4090 ↑      | Different GPU tiers diverge            |
| 2024          | ↑ significantly      | Mostly flat                | RAM becomes relatively less attractive |
| Early 2025    | ↓                    | RTX 50 initially expensive | Memory eases                           |
| Mid–late 2025 | Turning sharply ↑    | ↓ toward/below MSRP        | Brief GPU buying opportunity           |
| Late 2025     | ↑↑                   | Some GPUs still attractive | RAM becomes major build cost           |
| Q1 2026       | ↑↑↑                  | ↑ sharply                  | Memory crisis spreads into GPUs        |
| Spring 2026   | Still extremely high | Some GPU prices ↓ slightly | Temporary correction                   |
| Summer 2026   | Still high           | Mixed → then ↑ sharply     | Component-specific volatility          |

The exact percentages depend on whether one examines contract DRAM, retail RAM
kits, MSRP, lowest retail GPU prices, median listings, country, or model.

The useful point is not that every line moves perfectly in opposition.

It very obviously does not.

The useful point is:

> **The relative attractiveness of different PC components changes independently
> enough that the optimal allocation of a fixed budget can change surprisingly
> quickly.**

---

# The interesting bit: one expensive component affects the rest of the build

This was the part that made me interested in the problem.

Suppose RAM suddenly becomes extremely expensive.

A sensible consumer might decide:

> I'll wait before building my PC.

That does not only remove one RAM purchase.

The delayed build may also mean:

* no motherboard purchase;
* no CPU purchase;
* no case;
* no cooler;
* no PSU;
* no SSD; and
* potentially no GPU.

The 2026 motherboard-sales data provides a real example of this complementary
demand effect.

The result is not necessarily that all of those products instantly become
cheaper.

Instead, manufacturers and retailers can be left with **different amounts of
inventory pressure in different product categories**.

That can create discounts or strange bundles.

In August 2026, for example, Taiwanese retail listings were reported offering
scarce RTX 5090 GPUs in packages containing large numbers of motherboards and
other components, including one particularly absurd bundle involving **eight
motherboards**.

[Tom's Hardware — RTX 5090 Ships in Bizarre Eight-Motherboard Bundle](https://www.tomshardware.com/pc-components/gpus/nvidia-rtx-5090-ships-in-bizarre-8-motherboard-bundle-retailers-hold-gpus-hostage-similar-to-the-crypto-boom)

It is difficult to think of a more literal demonstration of mismatched
component scarcity.

Apparently the market's solution to:

> "I would like one GPU."

was occasionally:

> "Excellent. Would you also like eight motherboards?"

---

# 💡 The idea

Instead of asking:

> What is the best PC?

I wanted to ask:

> Given everything actually available to me right now—new and second-hand—what
> compatible combination produces the highest utility without exceeding my
> budget?

That is subtly different.

A £450 used GPU might dominate a £600 new GPU.

A 24 GB GPU may be substantially more useful for local AI workloads than a
faster gaming GPU limited to 12 GB.

A motherboard currently being discounted may make one CPU platform unexpectedly
more attractive than another.

A relatively expensive GPU might still belong in the optimal build if unusually
cheap RAM, storage, or motherboard pricing frees enough budget elsewhere.

Likewise, an apparently excellent GPU deal can become irrelevant if the memory
required for the intended workload suddenly consumes hundreds of pounds more
than expected.

The optimisation therefore needs to operate at the **system level**.

The "best component" and the "component belonging to the best build" are not
necessarily the same thing.

---

## Why AI-focused builds need separate treatment

Gaming-oriented price/performance comparisons do not necessarily represent an
AI development workload.

Local AI work may place different importance on:

* GPU compute architecture;
* supported software ecosystems;
* VRAM capacity;
* memory bandwidth;
* CUDA compatibility;
* system RAM;
* CPU performance;
* storage capacity; and
* storage throughput.

A second-hand 24 GB GPU can therefore remain extremely attractive for certain
workloads even when a newer GPU provides better gaming efficiency.

That distinction becomes even more important when memory prices are volatile:
VRAM and system RAM are not merely specification-sheet numbers; they can alter
which workloads are practical in the first place.

The optimizer therefore keeps workload-specific scores separate so those
trade-offs remain visible.

---

## New and second-hand hardware

Used hardware is treated as another decision dimension rather than as
automatically better or worse.

New and used examples of the same model are separate purchasing options.

For example:

```text
RTX XXXX 24 GB | New  | £700
RTX XXXX 24 GB | Used | £450
```

Their prices compete directly, while configurable penalties can account for:

* condition;
* remaining warranty;
* seller type;
* component type; and
* estimated second-hand risk.

This means a used component wins only when the utility gained from its lower
price outweighs the assigned risk.

In a volatile market, the second-hand market also gives the optimiser another
source of potential disequilibrium to exploit.

---

## Why this is an optimisation problem

Once enough candidate components exist, manually comparing builds becomes
increasingly silly.

The problem contains:

* discrete choices;
* a fixed budget;
* mutually exclusive selections;
* minimum performance requirements;
* physical compatibility requirements;
* power constraints;
* workload-specific objectives; and
* trade-offs between price, performance, reliability, and risk.

For each component (i), the model can define a binary decision variable:

[
x_i \in {0,1}
]

where:

```text
x_i = 1  → select the component
x_i = 0  → do not select the component
```

The optimiser then searches for the combination with the highest utility while
respecting constraints such as:

```text
Total cost <= budget

Exactly one CPU
Exactly one GPU
Exactly one motherboard
Exactly one RAM configuration
Exactly one PSU

CPU socket = motherboard socket
RAM generation = motherboard support
GPU length <= case clearance
Cooler height <= case clearance
PSU capacity >= required system power

RAM >= configured minimum
VRAM >= configured minimum
Storage >= configured minimum
```

The project uses Google OR-Tools for the production optimisation model while
retaining a brute-force implementation as a transparent baseline.

---

## The educational motivation

The repository is also an excuse to practise integer optimisation, constraint
modelling, and solver-based programming using a problem with tangible
consequences.

It is intended to make the important ideas inspectable:

* defining binary decision variables;
* constructing objective functions;
* translating physical requirements into mathematical constraints;
* modelling compatibility;
* comparing exhaustive search with a solver;
* validating solutions;
* exploring multi-objective optimisation;
* generating budget sweeps; and
* understanding Pareto trade-offs.

The guiding principle is simple:

> If an important constraint cannot be explained clearly, it should not be
> hidden behind an optimisation library.

I also wanted the important optimisation logic to be deliberately written and
understood rather than generated as an opaque pile of code.

In other words:

**hard-coded, not vibe-coded.**

Although I would be lying if I claimed this was motivated entirely by
intellectual curiosity and not by the increasingly urgent fact that I actually
need a PC. :eyes:

---

## What the optimizer can and cannot claim

The optimizer answers:

> Given these data, assumptions, constraints, and preferences, what is optimal?

It does not automatically determine the objective value of every component.

It does not predict the future price of a GPU.

It does not know whether an eBay RTX 3090 has spent the previous three years
living a peaceful life inside a workstation or mining cryptocurrency in a
warehouse at 3 a.m.

And it does not identify the universally best PC.

Its output is only as meaningful as the:

* pricing data;
* benchmark data;
* compatibility information;
* optimisation weights;
* risk assumptions; and
* constraints

provided to it.

Used-market risk in particular cannot be represented perfectly by one scalar.

The purpose is therefore not to outsource the purchasing decision completely.

It is to eliminate incompatible and demonstrably inferior configurations,
identify high-utility alternatives, expose the relevant trade-offs, and make it
much easier for a human to decide where their money should go.

In a stable market, that is useful.

In a market where RAM can collapse, recover, collapse again, then more than
double while GPUs fall below MSRP and subsequently surge again...

it becomes a little more interesting.
