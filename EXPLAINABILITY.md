# Explainability and Decision Record

## 1. Purpose and Scope

The Event Capacity and Attendance Planning Agent validates a supplied event plan, estimates attendance using an explicitly supplied attendance-rate assumption, compares the estimate with stated venue capacity, and generates an evidence-based report for human review.

The agent uses deterministic rules. It does not fetch external information, independently verify venue occupancy, guarantee attendance, or make final safety decisions.

## 2. Inputs and Data Provenance

The event plan supplies the following fields:

- `event_id`: identifier for the event.
- `event_name`: event name.
- `venue_capacity`: stated venue capacity.
- `registrations`: supplied registration count.
- `expected_attendance_rate`: supplied attendance-rate assumption.
- `event_date`: optional event date.
- `notes`: optional event notes.
- `minimum_staff_ratio`: optional staffing assumption.

The required fields and accepted types must agree with the implementation's validation rules. The expected attendance rate must be between zero and one inclusive. Capacity must be a positive integer, and registrations must be a non-negative integer.

All calculations use supplied values. The agent does not silently substitute missing values, estimate a rate from historical data, or treat assumptions as verified facts.

## 3. Decision Flow

The decision process follows this order:

1. Read the supplied event plan.
2. Validate the input structure and required fields.
3. Check capacity, registration count, and attendance-rate constraints.
4. If validation fails, report the issues and do not treat an attendance estimate as valid.
5. If validation succeeds, calculate estimated attendance as the ceiling of registrations multiplied by the supplied attendance rate.
6. Compare estimated attendance with the supplied venue capacity.
7. Assign the corresponding capacity status and priority.
8. Record the input values, assumptions, calculation, findings, limitations, and recommended human-review actions in the report.

The result must remain traceable to the supplied plan and the documented calculation.

## 4. Calculation and Boundary Cases

The estimate is:

`estimated_attendance = ceil(registrations * expected_attendance_rate)`

Capacity utilization is calculated from estimated attendance and venue capacity when the inputs are valid.

- If estimated attendance exceeds capacity, classify the result as `capacity_exceeded`.
- If estimated attendance is at least 90% of capacity but does not exceed capacity, flag it for review.
- If estimated attendance is below 90% of capacity, classify it as `within_capacity`.
- If required input validation fails, do not issue a valid capacity conclusion.

Boundary cases must be handled consistently:

- Zero registrations produce an estimate of zero when the supplied rate is valid.
- A rate of zero produces an estimate of zero.
- A rate of one produces an estimate equal to registrations.
- An estimate equal to venue capacity is not an exceedance, but it requires careful review.
- An estimate greater than venue capacity must be flagged.
- Missing, malformed, or out-of-range values must not be silently converted into valid inputs.

## 5. Severity and Prioritization

Priority communicates the need for attention; it is not a certification of event safety.

- `high`: invalid required input or estimated attendance exceeds stated capacity.
- `medium`: estimated attendance is within capacity but reaches at least 90% of capacity.
- `low`: estimated attendance is below 90% of capacity.
- `review`: assumptions, conflicting details, or other unresolved information require human confirmation.

When validation fails, invalid input takes precedence over a capacity conclusion because the estimate cannot be trusted. Recommendations must identify the evidence that caused the flag.

## 6. Outputs and Evidence

The report should preserve, where produced by the implementation:

- Event identifier and relevant supplied input values.
- Validation issues and their associated fields.
- Estimated attendance and the calculation assumption.
- Stated venue capacity and capacity comparison.
- Capacity utilization, when validly calculable.
- Status or priority assigned by the rules.
- Findings, recommended actions, and limitations.
- A clear indication when human review is required.

Evidence must distinguish supplied facts from calculated values and assumptions. A recommendation must be explainable from the recorded finding rather than an unsupported claim.

## 7. Tool: validate-event-plan

### Inputs and Data Sources

Reads the supplied event plan. It does not query external sources or independently verify registration records or venue capacity.

### Decision and Reasoning

Checks the input structure, required fields, capacity, registrations, and attendance-rate constraints according to the implementation.

### Outputs and Evidence

Returns validation issues associated with the fields or conditions that failed. A successful validation means the supplied values passed these checks; it does not mean the values are factually verified.

### Limits and Constraints

Cannot confirm legal occupancy, data accuracy, venue suitability, or real-world attendance.

### Failure Handling

Malformed JSON, a non-object input, missing fields, or invalid values must be reported rather than silently repaired. Downstream calculations must not be represented as valid when required validation fails.

### Human Review

Correct invalid values and verify their source before relying on the estimate.

## 8. Tool: estimate-attendance

### Inputs and Data Sources

Uses the supplied registration count and expected attendance rate after the required validation checks.

### Decision and Reasoning

Calculates the ceiling of registrations multiplied by the expected attendance rate. Rounding upward avoids reporting a fractional person.

### Outputs and Evidence

Returns the attendance estimate and the assumptions used, as supported by the implementation. The estimate must be distinguishable from an observed attendance count.

### Limits and Constraints

Does not learn from historical attendance, verify registrations, or guarantee turnout. Actual attendance may differ from the estimate.

### Failure Handling

Do not produce or present a valid estimate when required validation fails. Preserve the relevant validation issues for the report.

### Human Review

Confirm that the supplied attendance-rate assumption is appropriate for the event.

## 9. Tool: generate-capacity-report

### Inputs and Data Sources

Uses the event plan, calculation results, and validation findings supplied by the workflow.

### Decision and Reasoning

Compares a valid estimate with stated capacity, assigns the appropriate status or priority, and records recommendations based on the findings.

### Outputs and Evidence

Produces a JSON report containing findings, evidence, recommendations, and limitations as supported by the implementation. Validation failures must remain visible in the report.

### Limits and Constraints

Does not contact attendees, change bookings, reserve a venue, certify regulatory compliance, or guarantee safe event operation.

### Failure Handling

When validation issues exist, retain them and indicate that review is required. Do not describe an invalid or incomplete calculation as a confirmed capacity result.

### Human Review

The organizer must verify venue limits, accessibility, emergency exits, staffing, emergency planning, and venue-specific requirements before approving the event.

## 10. Recommendation-to-Evidence Traceability

Recommendations must be connected to their triggering evidence:

- Invalid required field: identify the field and request correction or verification.
- Estimated attendance above capacity: identify the estimate and stated capacity; request a revised plan or an appropriate venue decision.
- Estimated attendance at least 90% of capacity: identify the estimate and utilization; request a capacity and operational review.
- Unverified attendance-rate assumption: label it as an assumption and request confirmation.
- Incomplete or conflicting information: identify the unresolved issue and request human review.

These are decision guidelines. The exact report wording and available fields depend on the implementation. The agent must not claim that an action has been completed unless the system actually performed it.

## 11. Human Review and Safety

A numeric estimate is not a safety guarantee. A person must verify actual occupancy limits, accessible routes, emergency exits, staffing, emergency procedures, and venue-specific rules.

The agent provides decision support only. Final event approval remains with the responsible organizer and relevant venue personnel.

## 12. Auditability and Reproducibility

For identical valid inputs and the same implementation, the deterministic calculation should produce the same estimate and rule-based capacity classification.

An auditor should be able to trace:

1. The supplied inputs.
2. Validation results.
3. The attendance formula and supplied rate.
4. The calculated estimate.
5. The comparison with stated capacity.
6. The resulting status or priority.
7. The evidence and recommended human-review action.

Do not describe unrecorded reasoning, external verification, or actions as if they occurred.

## 13. Global Limits

No external services are queried. No attendee data is inferred. No venue is booked and no event is modified. Supplied information may be incomplete or inaccurate, and actual attendance may differ from the estimate.


## Additional Audit Coverage
## Purpose
## Inputs
## Decision
## Severity and Prioritization
## Outputs and Evidence
## Tool: validate-event-plan
## Tool: estimate-attendance
## Tool: generate-capacity-report
## Human Review and Safety
## Auditability
## Global Limits
