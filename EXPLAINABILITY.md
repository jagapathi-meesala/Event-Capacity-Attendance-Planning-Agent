# Explainability and Decision Record

## Purpose
Validate event-plan inputs, estimate attendance using an explicitly supplied rate, compare the estimate with the stated venue capacity, and record evidence for human review.

## Inputs
Required: `event_id`, `event_name`, `venue_capacity`, `registrations`, `expected_attendance_rate`. Optional: `event_date`, `notes`, `minimum_staff_ratio`. No outside data is fetched.

## Decision
Estimate = ceiling of registrations multiplied by expected attendance rate. An estimate above capacity is `capacity_exceeded`; an estimate at least 90% of capacity is flagged for review; a lower estimate is `within_capacity`. Invalid inputs prevent a valid estimate.

## Severity and Prioritization
- `high`: invalid required input or estimated attendance exceeds capacity.
- `medium`: estimate is within capacity but reaches at least 90% of it.
- `low`: estimate is below 90% of capacity.
- `review`: assumptions or details require human confirmation.

## Outputs and Evidence
The JSON report records validation issues, assumptions, estimated attendance, capacity utilization, priority, recommended actions, and limitations.

## Tool: validate-event-plan
### Inputs and Data Sources
Reads the supplied event plan object only.
### Decision and Reasoning
Checks required fields, positive integer capacity, non-negative integer registrations, and attendance rate between zero and one inclusive.
### Outputs and Evidence
Returns validation issues by field.
### Limits and Constraints
Does not verify actual legal occupancy or registration data.
### Failure Handling
Invalid JSON or non-object input is reported by the CLI.
### Human Review
Correct invalid fields and verify their sources.

## Tool: estimate-attendance
### Inputs and Data Sources
Uses registrations and the supplied expected attendance rate.
### Decision and Reasoning
Computes `ceil(registrations * expected_attendance_rate)`.
### Outputs and Evidence
Returns the estimate and assumptions.
### Limits and Constraints
Does not learn a rate from historical data or guarantee turnout.
### Failure Handling
No estimate is produced when validation fails.
### Human Review
Confirm the attendance-rate assumption.

## Tool: generate-capacity-report
### Inputs and Data Sources
Uses the validated plan and deterministic calculation.
### Decision and Reasoning
Compares the estimate with supplied venue capacity and assigns a priority band.
### Outputs and Evidence
Produces JSON with findings, evidence, recommendations, and limitations.
### Limits and Constraints
Does not contact attendees, change bookings, or certify safety compliance.
### Failure Handling
Validation issues are retained and status becomes `review_required`.
### Human Review
The organizer remains responsible for venue, accessibility, emergency planning, and approval.

## Human Review and Safety
A numeric estimate is not a safety guarantee. A person must confirm occupancy limits, accessible routes, emergency exits, staffing, and venue-specific rules.

## Auditability
Outputs are deterministic from the supplied input and documented formula.

## Global Limits
No external services are queried, no attendee data is inferred, and no event is booked or modified. Actual attendance may differ from estimates.
