"""Configuration for the simple pulse values imitator."""

SNS_TOPIC_ARN = "arn:aws:sns:us-east-1:246814138873:pulse-events.fifo"
DEVICE_COUNT = 5
DURATION_SECONDS = 5 * 60
INTERVAL_SECONDS = 1.0
# See Readme.md for details on pulse value generation 
DEVICES = {
    "dev-001": {"group": "1", "current_pulse": 0},
    "dev-002": {"group": "2", "current_pulse": 0},
    "dev-003": {"group": "3", "current_pulse": 0},
    "dev-004": {"group": "1", "current_pulse": 0},
    "dev-005": {"group": "2", "current_pulse": 0},
    "dev-006": {"group": "3", "current_pulse": 0},
    "dev-007": {"group": "1", "current_pulse": 0},
    "dev-008": {"group": "2", "current_pulse": 0},
    "dev-009": {"group": "3", "current_pulse": 0},
    "dev-010": {"group": "1", "current_pulse": 0},
    "dev-011": {"group": "2", "current_pulse": 0},
    "dev-012": {"group": "3", "current_pulse": 0},
    "dev-013": {"group": "1", "current_pulse": 0},
    "dev-014": {"group": "2", "current_pulse": 0},
    "dev-015": {"group": "3", "current_pulse": 0},
    "dev-016": {"group": "1", "current_pulse": 0},
    "dev-017": {"group": "2", "current_pulse": 0},
    "dev-018": {"group": "3", "current_pulse": 0},
    "dev-019": {"group": "1", "current_pulse": 0},
    "dev-020": {"group": "2", "current_pulse": 0},
    "dev-021": {"group": "3", "current_pulse": 0},
    "dev-022": {"group": "1", "current_pulse": 0},
    "dev-023": {"group": "2", "current_pulse": 0},
    "dev-024": {"group": "3", "current_pulse": 0},
    "dev-025": {"group": "1", "current_pulse": 0},
    "dev-026": {"group": "2", "current_pulse": 0},
    "dev-027": {"group": "3", "current_pulse": 0},
    "dev-028": {"group": "1", "current_pulse": 0},
    "dev-029": {"group": "2", "current_pulse": 0},
    "dev-030": {"group": "3", "current_pulse": 0},
    "dev-031": {"group": "1", "current_pulse": 0},
    "dev-032": {"group": "2", "current_pulse": 0},
    "dev-033": {"group": "3", "current_pulse": 0},
    "dev-034": {"group": "1", "current_pulse": 0},
    "dev-035": {"group": "2", "current_pulse": 0},
    "dev-036": {"group": "3", "current_pulse": 0},
    "dev-037": {"group": "1", "current_pulse": 0},
    "dev-038": {"group": "2", "current_pulse": 0},
    "dev-039": {"group": "3", "current_pulse": 0},
    "dev-040": {"group": "1", "current_pulse": 0},
    "dev-041": {"group": "2", "current_pulse": 0},
    "dev-042": {"group": "3", "current_pulse": 0},
    "dev-043": {"group": "1", "current_pulse": 0},
    "dev-044": {"group": "2", "current_pulse": 0},
    "dev-045": {"group": "3", "current_pulse": 0},
    "dev-046": {"group": "1", "current_pulse": 0},
    "dev-047": {"group": "2", "current_pulse": 0},
    "dev-048": {"group": "3", "current_pulse": 0},
    "dev-049": {"group": "1", "current_pulse": 0},
    "dev-050": {"group": "2", "current_pulse": 0}
}
DELTA_PERCENT_RANGES =[(2, 6), (7, 15), (16, 50),  (51, 100)]  
# [20, 50, 70, 100] means 20% - first range (2, 6), 30% - second range (7, 15), 20% - third range (16, 50), 30% - fourth range (51, 100) 
# [40, 50, 60, 100] means 40% - first range (2, 6), 10% - second range (7, 15), 10% - third range (16, 50), 40% - fourth range (51, 100) 
# [50, 80, 90, 100] means 50% - first range (2, 6), 30% - second range (7, 15), 10% - third range (16, 50), 10% - fourth range (51, 100) 
   
GROUPS = {
    "1": {"pulse_min": 40, "pulse_max": 150, "prob_change":10, "percent_ranges_thresholds": (20, 50, 70, 100),\
        "prob_incr": 70, "first_pulse_range": (50, 90)},
    "2": {"pulse_min": 52, "pulse_max": 200, "prob_change":20, "percent_ranges_thresholds": (40, 50, 60, 100),\
        "prob_incr": 50,"first_pulse_range": (70, 120)},
    "3": {"pulse_min": 55, "pulse_max": 220, "prob_change":40, "percent_ranges_thresholds": (50, 80, 90, 100),\
        "prob_incr": 5,"first_pulse_range": (60, 180)}
}

