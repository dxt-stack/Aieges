#!/usr/bin/env python3
"""
AEGIS Command-Line Autonomous Automation Interface
Allows headless execution, cron scheduling, and developer orchestration of the AEGIS Organism.
"""

import sys
import os
import argparse
import json
from aegis.orchestrator import AegisOrchestrator
from aegis.core.models import RevenuePriorityEnum


def format_table(rows, headers):
    col_widths = [len(h) for h in headers]
    for row in rows:
        for i, val in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(val)))
    
    header_str = " | ".join(h.ljust(col_widths[i]) for i, h in enumerate(headers))
    sep_str = "-+-".join("-" * col_widths[i] for i in range(len(headers)))
    
    lines = [header_str, sep_str]
    for row in rows:
        lines.append(" | ".join(str(val).ljust(col_widths[i]) for i, val in enumerate(row)))
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="AEGIS Autonomous Economic Growth & Intelligent Survival CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # Command: status
    subparsers.add_parser("status", help="Inspect AEGIS organism status, treasury, and survival state")

    # Command: loop
    loop_parser = subparsers.add_parser("loop", help="Execute Value Creation Loop cycles")
    loop_parser.add_argument("--cycles", type=int, default=1, help="Number of loop cycles to execute")

    # Command: venture
    venture_parser = subparsers.add_parser("venture", help="Venture management")
    venture_sub = venture_parser.add_subparsers(dest="subcommand")
    
    v_new = venture_sub.add_parser("new", help="Scaffold new venture with canonical 16-doc suite")
    v_new.add_argument("--name", type=str, required=True, help="Venture name")
    v_new.add_argument("--category", type=str, default="SaaS", help="Revenue category")
    v_new.add_argument("--tagline", type=str, default="Autonomous Value Stream", help="Tagline / value proposition")
    v_new.add_argument("--mrr", type=float, default=15000.0, help="Target MRR ($)")
    v_new.add_argument("--budget", type=float, default=2000.0, help="Initial budget ($)")

    v_list = venture_sub.add_parser("list", help="List all ventures")

    # Command: division
    div_parser = subparsers.add_parser("division", help="Dispatch task directly to an autonomous division")
    div_parser.add_argument("--name", type=str, required=True, choices=["RESEARCH", "PRODUCT", "ENGINEERING", "MARKETING", "OPERATIONS", "FINANCE"], help="Division name")
    div_parser.add_argument("--task", type=str, required=True, help="Task / Directive name")

    # Command: treasury
    treasury_parser = subparsers.add_parser("treasury", help="Update treasury parameters")
    treasury_parser.add_argument("--reserves", type=float, help="Cash reserves ($)")
    treasury_parser.add_argument("--burn", type=float, help="Monthly burn ($)")
    treasury_parser.add_argument("--revenue", type=float, help="Monthly revenue ($)")

    args = parser.parse_args()
    orchestrator = AegisOrchestrator(workspace_root=os.getenv("AEGIS_WORKSPACE"))

    if args.command == "status" or not args.command:
        state = orchestrator.state_mgr.state
        t = state.treasury
        print("=" * 65)
        print("🛡️  AEGIS AUTONOMOUS ECONOMIC SYSTEM STATUS")
        print("=" * 65)
        print(f" Organism Identity   : {state.name} (v{state.version})")
        print(f" Survival Posture    : [{state.survival_state.value}]")
        print(f" Cash Reserves       : ${t.cash_reserves:,.2f}")
        print(f" Monthly Burn Rate   : ${t.monthly_burn:,.2f}")
        print(f" Monthly MRR Revenue : ${t.monthly_revenue:,.2f}")
        print(f" Net Burn Rate       : ${t.net_burn:,.2f}/mo")
        print(f" Runway Days         : {t.runway_days:.1f} Days")
        print(f" Fortress Target     : ${t.target_reserves:,.2f}")
        print(f" Active Ventures     : {len(orchestrator.state_mgr.ventures)}")
        print(f" Evaluated Opps      : {len(orchestrator.state_mgr.opportunities)}")
        print(f" Pending Governance  : {len(orchestrator.governance.get_pending())}")
        print(f" Knowledge Entries   : {len(orchestrator.knowledge_base.entries)}")
        print("=" * 65)

    elif args.command == "loop":
        for i in range(args.cycles):
            print(f"\n⚡ [AEGIS LOOP] Executing cycle {i+1}/{args.cycles}...")
            res = orchestrator.execute_single_loop_cycle()
            print(f"   Cycle #{res['cycle_number']} | Posture: {res['survival_state']} | Duration: {res['duration_seconds']}s")
            print(f"   Top Opportunity : {res.get('top_opportunity')}")
            print(f"   Action Executed : {res.get('action_taken')}")

    elif args.command == "venture":
        if args.subcommand == "new":
            print(f"🚀 Initializing venture '{args.name}' ({args.category})...")
            v = orchestrator.create_venture_and_docs(
                venture_name=args.name,
                category=args.category,
                tagline=args.tagline,
                target_mrr=args.mrr,
                budget=args.budget
            )
            v_dir = os.path.join(orchestrator.workspace_root, "ventures", v.slug)
            print(f"✅ Created venture: {v.name}")
            print(f"📁 Generated 16 canonical documents in: {v_dir}")
        elif args.subcommand == "list" or not args.subcommand:
            ventures = list(orchestrator.state_mgr.ventures.values())
            rows = [
                [
                    v.name,
                    v.category.value if hasattr(v.category, 'value') else str(v.category),
                    f"${v.target_mrr:,.0f}",
                    f"${v.current_mrr:,.0f}",
                    v.status
                ]
                for v in ventures
            ]
            print(format_table(rows, ["Venture Name", "Category", "Target MRR", "Current MRR", "Status"]))

    elif args.command == "division":
        div_map = {
            "RESEARCH": orchestrator.research_div,
            "PRODUCT": orchestrator.product_div,
            "ENGINEERING": orchestrator.engineering_div,
            "MARKETING": orchestrator.marketing_div,
            "OPERATIONS": orchestrator.operations_div,
            "FINANCE": orchestrator.finance_div,
        }
        div = div_map[args.name]
        print(f"🏢 Executing [{args.name}] directive: {args.task}...")
        res = div.execute_directive(args.task, {}, orchestrator.current_state)
        print(json.dumps(res, indent=2))

    elif args.command == "treasury":
        t = orchestrator.state_mgr.update_treasury(
            cash_reserves=args.reserves,
            monthly_burn=args.burn,
            monthly_revenue=args.revenue
        )
        print(f"✅ Treasury updated: Reserves=${t.cash_reserves:,.2f}, Burn=${t.monthly_burn:,.2f}, Revenue=${t.monthly_revenue:,.2f}")
        print(f"   New Posture: [{orchestrator.current_state.value}] (Runway: {t.runway_days:.1f} days)")


if __name__ == "__main__":
    main()
