# Event Capacity and Attendance Planning Agent

A deterministic local-first agent that validates event-planning inputs, estimates attendance from a supplied rate, checks the estimate against stated venue capacity, and generates an evidence-based JSON report.

## Run (Python 3.10+, no third-party dependencies)
```bash
python3 verification/readiness_audit.py
python3 -m unittest discover -s tests -v
python3 -m core.cli examples/event_plan.json --output event_report.json
```

See `examples/event_plan.json` for the input schema. The expected attendance estimate is `ceil(registrations * expected_attendance_rate)`.

## Safety and limitations
Estimates depend on supplied assumptions and do not guarantee turnout. The agent does not certify legal occupancy or safety, contact attendees, book venues, or modify event systems. A responsible organizer must verify occupancy limits, emergency exits, accessibility, staffing, and venue rules.
