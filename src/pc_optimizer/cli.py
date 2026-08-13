"""Friendly command-line entry point."""
import argparse
from pathlib import Path
from .config import load_config, with_profile
from .data_loader import group_parts, load_parts
from .optimizer import optimise_pc
from .pareto import pareto_front
from .reporting import export_results, plot_budget_sweep, plot_pareto
from .validation import validate_parts

ROOT = Path.cwd()


def _parser():
    parser = argparse.ArgumentParser(prog="pc-optimizer", description="Optimise compatible PC builds from Excel")
    parser.add_argument("--config", default="config/default_config.yaml"); parser.add_argument("--data", default="data/pc_parts.xlsx")
    sub = parser.add_subparsers(dest="command", required=True)
    opt = sub.add_parser("optimise"); opt.add_argument("--budget", type=float); opt.add_argument("--profile", default="balanced"); opt.add_argument("--top", type=int); opt.add_argument("--engine", choices=("solver", "brute_force"), default="solver")
    sweep = sub.add_parser("budget-sweep"); sweep.add_argument("--min", dest="minimum", type=int, default=800); sweep.add_argument("--max", dest="maximum", type=int, default=1600); sweep.add_argument("--step", type=int, default=50); sweep.add_argument("--profile", default="balanced"); sweep.add_argument("--engine", choices=("solver", "brute_force"), default="solver")
    sub.add_parser("validate")
    return parser


def _kwargs(config):
    used = config.get("used_parts", {}); maximum = 0 if not used.get("allowed", True) else used.get("maximum_used_parts")
    return {"headroom_multiplier": config.get("psu", {}).get("headroom_multiplier", 1.25), "maximum_used_parts": maximum, "risk_penalty_enabled": used.get("risk_penalty_enabled", True)}


def main(argv=None):
    args = _parser().parse_args(argv); frame = load_parts(args.data); errors = validate_parts(frame)
    if args.command == "validate":
        if errors: print("Validation failed:\n- " + "\n- ".join(errors)); return 1
        print(f"Validation passed: {len(frame)} purchasing options"); return 0
    if errors: print("Validation failed:\n- " + "\n- ".join(errors)); return 1
    config = with_profile(load_config(args.config), args.profile); parts = group_parts(frame); common = _kwargs(config)
    if args.command == "optimise":
        budget = args.budget or config["budget_gbp"]; top = args.top or config["results"]["top_n"]
        builds = optimise_pc(parts, budget, config["weights"], config["requirements"], engine=args.engine, top_n=top, **common)
        if not builds: print(f"No valid build found under £{budget:,.2f}. Try a larger budget or relaxed requirements."); return 2
        export_results("output/optimised_builds.xlsx", {"Best Build": builds[:1], f"Top {top} Builds": builds, args.profile.title(): builds})
        print(f"Best build: £{builds[0]['cost']:,.2f}, overall {builds[0]['overall']:.2f}. Wrote output/optimised_builds.xlsx"); return 0
    rows = []
    for budget in range(args.minimum, args.maximum + 1, args.step):
        found = optimise_pc(parts, budget, config["weights"], config["requirements"], engine=args.engine, top_n=1, **common)
        if found: rows.append({"budget": budget, **found[0]})
    frontier = pareto_front(rows); export_results("output/optimised_builds.xlsx", {"Budget Sweep": rows, "Pareto Frontier": frontier})
    plot_budget_sweep(rows, "output/plots"); plot_pareto(frontier, "output/plots"); print(f"Wrote {len(rows)} budget results, workbook and plots"); return 0
