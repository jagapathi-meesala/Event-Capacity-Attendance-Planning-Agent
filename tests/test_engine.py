import unittest
from core.engine import validate_event_plan, estimate_attendance, build_report
VALID = {"event_id":"EVT-1","event_name":"Sample Event","venue_capacity":100,"registrations":80,"expected_attendance_rate":0.75}
class EventPlanningTests(unittest.TestCase):
    def test_valid_plan(self): self.assertEqual(validate_event_plan(VALID), [])
    def test_estimate_rounds_up(self): self.assertEqual(estimate_attendance(11, 0.5), 6)
    def test_within_capacity(self): self.assertEqual(build_report(VALID)["status"], "within_capacity")
    def test_capacity_exceeded(self): self.assertEqual(build_report({**VALID,"registrations":200,"expected_attendance_rate":1.0})["status"], "capacity_exceeded")
    def test_near_capacity(self): self.assertEqual(build_report({**VALID,"registrations":100,"expected_attendance_rate":0.95})["estimate"]["priority"], "medium")
    def test_invalid_capacity(self): self.assertTrue(any("venue_capacity" in x for x in validate_event_plan({**VALID,"venue_capacity":0})))
    def test_invalid_rate(self): self.assertTrue(any("expected_attendance_rate" in x for x in validate_event_plan({**VALID,"expected_attendance_rate":1.2})))
    def test_missing_fields(self): self.assertGreater(len(validate_event_plan({"event_id":"x"})), 0)
    def test_invalid_root(self): self.assertTrue(validate_event_plan([]))
    def test_human_review_and_limitations(self): self.assertTrue(build_report(VALID)["recommended_actions"] and build_report(VALID)["limitations"])
if __name__ == "__main__": unittest.main()
