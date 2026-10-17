---
name: capacity-planning
description: Compare estimated event attendance against supplied venue capacity and identify capacity risks.
---

# Capacity Planning

## Purpose
Evaluate whether expected attendance fits within the supplied venue capacity.

## Inputs
- Expected attendance
- Venue capacity

## Method
Compare expected attendance with venue capacity and calculate capacity utilization as expected attendance divided by venue capacity when capacity is valid and positive.

## Rules
- Use only supplied values.
- Reject missing, invalid, or non-positive venue capacity.
- Flag estimates that exceed venue capacity.
- Explain the comparison and supporting values.
- Do not claim legal occupancy or venue safety has been verified.
- Require human review of final capacity decisions.
