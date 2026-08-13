"""Excel and plot reporting."""
from pathlib import Path
import pandas as pd


def flatten_build(build: dict) -> dict:
    row = {k: build.get(k) for k in ("rank", "cost", "ai", "animation", "gaming", "value", "risk_penalty", "overall", "used_parts")}
    for kind, part in build["components"].items():
        items = part if isinstance(part, list) else [part]
        row[kind] = "; ".join(f"{x.get('Brand', '')} {x.get('Model', x.get('Part_ID', ''))} [{x.get('Part_ID')}]".strip() for x in items)
    return row


def export_results(path: str | Path, sheets: dict[str, list[dict]], validation_errors: list[str] | None = None) -> Path:
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        for name, builds in sheets.items():
            pd.DataFrame([flatten_build(x) for x in builds]).to_excel(writer, sheet_name=name[:31], index=False)
        pd.DataFrame({"Validation message": validation_errors or ["No validation errors"]}).to_excel(writer, sheet_name="Validation Report", index=False)
        for ws in writer.book.worksheets:
            ws.freeze_panes = "A2"; ws.auto_filter.ref = ws.dimensions
            for column in ws.columns:
                ws.column_dimensions[column[0].column_letter].width = min(55, max(12, max(len(str(c.value or "")) for c in column) + 2))
    return path


def plot_budget_sweep(rows: list[dict], output_dir: str | Path) -> list[Path]:
    import matplotlib.pyplot as plt
    output = Path(output_dir); output.mkdir(parents=True, exist_ok=True); paths = []
    if not rows: return paths
    for metric in ("ai", "animation", "gaming", "overall"):
        fig, ax = plt.subplots(figsize=(7, 4)); ax.plot([x["budget"] for x in rows], [x[metric] for x in rows], marker="o")
        ax.set(xlabel="Budget (£)", ylabel=f"{metric.title()} score", title=f"Budget vs {metric.title()} performance"); ax.grid(alpha=.25); fig.tight_layout()
        path = output / f"budget_vs_{metric}.png"; fig.savefig(path, dpi=150); plt.close(fig); paths.append(path)
    return paths


def plot_pareto(rows: list[dict], output_dir: str | Path) -> Path | None:
    if not rows: return None
    import matplotlib.pyplot as plt
    output = Path(output_dir); output.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(7, 4)); points = ax.scatter([x["cost"] for x in rows], [x["ai"] for x in rows], c=[x["gaming"] for x in rows], cmap="viridis")
    ax.set(xlabel="Cost (£)", ylabel="AI score", title="Pareto frontier (colour: gaming score)"); fig.colorbar(points, ax=ax, label="Gaming score"); fig.tight_layout()
    path = output / "pareto_frontier.png"; fig.savefig(path, dpi=150); plt.close(fig); return path
