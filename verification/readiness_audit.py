from pathlib import Path
import re, sys
ROOT = Path(__file__).resolve().parents[1]
REQUIRED = ["agent.yaml","README.md","EXPLAINABILITY.md","LICENSE","core/__init__.py","core/engine.py","core/cli.py","examples/event_plan.json","tools/validate_event_plan.yaml","tools/estimate_attendance.yaml","tools/generate_capacity_report.yaml","skills/capacity-planning/SKILL.md","skills/attendance-forecasting/SKILL.md","skills/event-safety-review/SKILL.md","tests/test_engine.py","verification/readiness_audit.py"]
def main():
    missing = [p for p in REQUIRED if not (ROOT/p).is_file()]
    text = (ROOT/"agent.yaml").read_text(encoding="utf-8")
    m = re.search(r"^name:\s*([a-z][a-z0-9-]*)\s*$", text, re.M)
    name_ok = bool(m and m.group(1) == "event-capacity-attendance-planning-agent")
    exp = (ROOT/"EXPLAINABILITY.md").read_text(encoding="utf-8")
    headings = ["## Purpose","## Inputs","## Decision","## Severity and Prioritization","## Outputs and Evidence","## Tool: validate-event-plan","## Tool: estimate-attendance","## Tool: generate-capacity-report","## Human Review and Safety","## Auditability","## Global Limits"]
    explain_ok = all(h in exp for h in headings)
    print(f"Required files: {len(REQUIRED)-len(missing)}/{len(REQUIRED)}")
    print(f"Agent name valid: {'PASS' if name_ok else 'FAIL'}")
    print(f"Explainability sections: {'PASS' if explain_ok else 'FAIL'}")
    if missing: print("Missing files:", ", ".join(missing))
    if not name_ok: print("Expected agent name: event-capacity-attendance-planning-agent")
    if not explain_ok: print("Missing headings:", ", ".join(h for h in headings if h not in exp))
    return 1 if missing or not name_ok or not explain_ok else 0
if __name__ == "__main__": sys.exit(main())
