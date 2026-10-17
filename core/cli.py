import argparse, json, sys
from pathlib import Path
from core.engine import build_report

def main(argv=None):
    parser = argparse.ArgumentParser(description="Validate an event plan and generate a capacity report.")
    parser.add_argument("input", help="Input event-plan JSON file")
    parser.add_argument("--output", default="event_report.json", help="Output JSON report path")
    args = parser.parse_args(argv)
    try:
        data = json.loads(Path(args.input).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"Input error: {exc}", file=sys.stderr)
        return 2
    report = build_report(data)
    try:
        Path(args.output).write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    except OSError as exc:
        print(f"Output error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(report, indent=2))
    return 0 if not report["validation_issues"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
