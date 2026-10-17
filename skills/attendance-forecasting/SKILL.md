---
name: attendance-forecasting
description: Estimate expected event attendance using supplied registration counts and attendance-rate assumptions.
---

# Attendance Forecasting

## Purpose
Estimate expected attendance for an event using the supplied registration count and expected attendance rate.

## Inputs
- Registration count
- Expected attendance rate

## Method
Calculate expected attendance as the ceiling of registration count multiplied by the attendance rate.

## Rules
- Use only supplied values.
- Validate that registration count is non-negative and attendance rate is between 0 and 1.
- State the formula and assumptions.
- Do not present estimated attendance as actual attendance.
- Flag missing or invalid inputs for human review.
