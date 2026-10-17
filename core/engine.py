from math import ceil

REQUIRED_FIELDS = ("event_id", "event_name", "venue_capacity", "registrations", "expected_attendance_rate")

def validate_event_plan(data):
    issues = []
    if not isinstance(data, dict):
        return ["Input must be a JSON object."]
    for field in REQUIRED_FIELDS:
        if field not in data:
            issues.append(f"Missing required field: {field}.")
    for field in ("event_id", "event_name"):
        if field in data and (not isinstance(data[field], str) or not data[field].strip()):
            issues.append(f"{field} must be a non-empty string.")
    if "venue_capacity" in data:
        v = data["venue_capacity"]
        if isinstance(v, bool) or not isinstance(v, int) or v <= 0:
            issues.append("venue_capacity must be a positive integer.")
    if "registrations" in data:
        v = data["registrations"]
        if isinstance(v, bool) or not isinstance(v, int) or v < 0:
            issues.append("registrations must be a non-negative integer.")
    if "expected_attendance_rate" in data:
        v = data["expected_attendance_rate"]
        if isinstance(v, bool) or not isinstance(v, (int, float)) or not 0 <= v <= 1:
            issues.append("expected_attendance_rate must be a number between 0 and 1 inclusive.")
    if "minimum_staff_ratio" in data:
        v = data["minimum_staff_ratio"]
        if isinstance(v, bool) or not isinstance(v, (int, float)) or v <= 0:
            issues.append("minimum_staff_ratio, when supplied, must be a positive number.")
    return issues

def estimate_attendance(registrations, expected_attendance_rate):
    return ceil(registrations * expected_attendance_rate)

def build_report(data):
    issues = validate_event_plan(data)
    if issues:
        return {"status": "review_required",
                "event": {"event_id": data.get("event_id"), "event_name": data.get("event_name")} if isinstance(data, dict) else {},
                "validation_issues": issues, "estimate": None, "findings": [],
                "recommended_actions": ["Correct validation issues and rerun the report."],
                "limitations": ["Uses only supplied data.", "No estimate is produced for invalid input.", "Not a safety or legal-compliance certification."]}
    capacity, registrations, rate = data["venue_capacity"], data["registrations"], data["expected_attendance_rate"]
    estimate = estimate_attendance(registrations, rate)
    utilization = estimate / capacity
    if estimate > capacity:
        status, priority = "capacity_exceeded", "high"
        finding = "Estimated attendance exceeds the supplied venue capacity."
        actions = ["Do not treat this plan as approved.", "Confirm permitted occupancy with venue personnel.", "Consider a larger approved venue, registration limit, or additional session.", "Obtain human review before proceeding."]
    elif utilization >= 0.90:
        status, priority = "within_capacity_review_recommended", "medium"
        finding = "Estimated attendance is within stated capacity but at least 90% of it."
        actions = ["Confirm capacity and attendance-rate assumptions.", "Review exits, accessible routes, staffing, and crowd-management arrangements with venue personnel."]
    else:
        status, priority = "within_capacity", "low"
        finding = "Estimated attendance is below 90% of the supplied venue capacity."
        actions = ["Confirm assumptions and venue occupancy rules.", "Review accessibility, emergency routes, and staffing before final approval."]
    return {"status": status, "event": {"event_id": data["event_id"], "event_name": data["event_name"]},
            "assumptions": {"registrations": registrations, "expected_attendance_rate": rate, "venue_capacity": capacity, "formula": "ceil(registrations * expected_attendance_rate)"},
            "estimate": {"expected_attendance": estimate, "venue_capacity": capacity, "capacity_utilization": round(utilization, 4), "priority": priority},
            "validation_issues": [], "findings": [{"message": finding, "priority": priority, "evidence": {"registrations": registrations, "expected_attendance_rate": rate, "expected_attendance": estimate, "venue_capacity": capacity}}],
            "recommended_actions": actions,
            "limitations": ["Actual attendance may differ.", "Attendance rate is supplied and not independently verified.", "Legal occupancy, fire safety, accessibility, and venue rules are not verified.", "Human review is required before the event."]}
