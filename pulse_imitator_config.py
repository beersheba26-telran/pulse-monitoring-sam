"""Configuration for the simple pulse values imitator."""

SNS_TOPIC_ARN = "arn:aws:sns:us-east-1:246814138873:pulse-events.fifo"
DEVICE_COUNT = 5
DURATION_SECONDS = 5 * 60
INTERVAL_SECONDS = 1.0
# See Readme.md for details on pulse value generation 
DEVICES = {
    "dev_001": {"group": "1", "current_pulse": 0},
    "dev_002": {"group": "2", "current_pulse": 0},
    "dev_003": {"group": "3", "current_pulse": 0},
    "dev_004": {"group": "1", "current_pulse": 0},
    "dev_005": {"group": "2", "current_pulse": 0},
    "dev_006": {"group": "3", "current_pulse": 0},
    "dev_007": {"group": "1", "current_pulse": 0},
    "dev_008": {"group": "2", "current_pulse": 0},
    "dev_009": {"group": "3", "current_pulse": 0},
    "dev_010": {"group": "1", "current_pulse": 0},
    "dev_011": {"group": "2", "current_pulse": 0},
    "dev_012": {"group": "3", "current_pulse": 0},
    "dev_013": {"group": "1", "current_pulse": 0},
    "dev_014": {"group": "2", "current_pulse": 0},
    "dev_015": {"group": "3", "current_pulse": 0},
    "dev_016": {"group": "1", "current_pulse": 0},
    "dev_017": {"group": "2", "current_pulse": 0},
    "dev_018": {"group": "3", "current_pulse": 0},
    "dev_019": {"group": "1", "current_pulse": 0},
    "dev_020": {"group": "2", "current_pulse": 0},
    "dev_021": {"group": "3", "current_pulse": 0},
    "dev_022": {"group": "1", "current_pulse": 0},
    "dev_023": {"group": "2", "current_pulse": 0},
    "dev_024": {"group": "3", "current_pulse": 0},
    "dev_025": {"group": "1", "current_pulse": 0},
    "dev_026": {"group": "2", "current_pulse": 0},
    "dev_027": {"group": "3", "current_pulse": 0},
    "dev_028": {"group": "1", "current_pulse": 0},
    "dev_029": {"group": "2", "current_pulse": 0},
    "dev_030": {"group": "3", "current_pulse": 0},
    "dev_031": {"group": "1", "current_pulse": 0},
    "dev_032": {"group": "2", "current_pulse": 0},
    "dev_033": {"group": "3", "current_pulse": 0},
    "dev_034": {"group": "1", "current_pulse": 0},
    "dev_035": {"group": "2", "current_pulse": 0},
    "dev_036": {"group": "3", "current_pulse": 0},
    "dev_037": {"group": "1", "current_pulse": 0},
    "dev_038": {"group": "2", "current_pulse": 0},
    "dev_039": {"group": "3", "current_pulse": 0},
    "dev_040": {"group": "1", "current_pulse": 0},
    "dev_041": {"group": "2", "current_pulse": 0},
    "dev_042": {"group": "3", "current_pulse": 0},
    "dev_043": {"group": "1", "current_pulse": 0},
    "dev_044": {"group": "2", "current_pulse": 0},
    "dev_045": {"group": "3", "current_pulse": 0},
    "dev_046": {"group": "1", "current_pulse": 0},
    "dev_047": {"group": "2", "current_pulse": 0},
    "dev_048": {"group": "3", "current_pulse": 0},
    "dev_049": {"group": "1", "current_pulse": 0},
    "dev_050": {"group": "2", "current_pulse": 0}
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

