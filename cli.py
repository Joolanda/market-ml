# cli.py

import argparse
import subprocess


def main():
    parser = argparse.ArgumentParser(description="Market ML CLI")

    sub = parser.add_subparsers(dest="command")

    # FX Weekly
    fetch_cmd = sub.add_parser("fetch-data", help="Download daily prices and interest rates into data/raw/")
    fetch_cmd.add_argument("--strict", action="store_true", help="Exit with an error if any download fails")
    weekly_cmd = sub.add_parser("fx-weekly", help="Build the FX Weekly report (reports/fx_weekly/)")
    weekly_cmd.add_argument("--assets", nargs="*", help="Asset keys, e.g. eurusd eurpln (default: all)")
    eval_cmd = sub.add_parser("fx-eval", help="Print the walk-forward track record per market")
    eval_cmd.add_argument("--assets", nargs="*", help="Asset keys (default: all)")

    # Train single model
    train_cmd = sub.add_parser("train")
    train_cmd.add_argument("--tf", required=True, help="Timeframe to train (e.g. 15m)")

    # Train all models
    sub.add_parser("train-all")

    # Run Streamlit UI
    sub.add_parser("ui")

    # Start scheduler
    sched_cmd = sub.add_parser("scheduler")
    sched_cmd.add_argument("action", choices=["start"])

    args = parser.parse_args()

    if args.command == "fetch-data":
        from src.data.sources import update_all
        results = update_all()
        for name, status in results.items():
            print(f"{name:8s} {status}")
        if args.strict and any(s.startswith("FAILED") for s in results.values()):
            raise SystemExit("One or more downloads failed (--strict)")

    elif args.command == "fx-weekly":
        from src.fx.report import build_all, write_report
        outlooks = build_all(args.assets)
        path = write_report(outlooks)
        print(f"FX Weekly written to {path}")
        for o in outlooks:
            print(f"  {o.asset.name:8s} [{o.source}] P(up) {o.p_up:.0%}  "
                  f"80% {o.fmt(o.low_80)}–{o.fmt(o.high_80)}  vol {o.vol_regime}")

    elif args.command == "fx-eval":
        from src.fx.report import build_all, track_record_table
        print(track_record_table(build_all(args.assets)))

    elif args.command == "train":
        from src.ml.training.candle_regression import train_candle_regression
        raw_path = f"data/raw/btc_{args.tf}_raw.csv"
        train_candle_regression(raw_path, model_name=f"model_{args.tf}")
        print(f"Model trained for timeframe {args.tf}")

    elif args.command == "train-all":
        from src.ml.training.train_all import train_all_models
        train_all_models()

    elif args.command == "ui":
        subprocess.run(["streamlit", "run", "app.py"])

    elif args.command == "scheduler" and args.action == "start":
        from src.data.scheduler import start_scheduler
        start_scheduler()
        print("Scheduler started")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
