# cli.py

import argparse
import subprocess
from src.ml.training.train_all import train_all_models
from src.ml.training.candle_regression import train_candle_regression


def main():
    parser = argparse.ArgumentParser(description="Market ML CLI")

    sub = parser.add_subparsers(dest="command")

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

    if args.command == "train":
        raw_path = f"data/raw/btc_{args.tf}_raw.csv"
        train_candle_regression(raw_path, model_name=f"model_{args.tf}")
        print(f"Model trained for timeframe {args.tf}")

    elif args.command == "train-all":
        train_all_models()

    elif args.command == "ui":
        subprocess.run(["streamlit", "run", "streamlit_app/app.py"])

    elif args.command == "scheduler" and args.action == "start":
        from src.data.scheduler import start_scheduler
        start_scheduler()
        print("Scheduler started")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
