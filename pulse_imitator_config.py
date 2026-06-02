"""Configuration for the simple pulse values imitator."""

SNS_TOPIC_ARN = "arn:aws:sns:us-east-1:246814138873:pulse-events.fifo"
DEVICE_COUNT = 5
DURATION_SECONDS = 5 * 60
INTERVAL_SECONDS = 1.0
# See Readme.md for details on pulse value generation 
DEVICES = {
    "device-1": {"group": "group-1", "current_pulse": 0},
    "device-2": {"group": "group-1", "current_pulse": 0},
    "device-3": {"group": "group-2", "current_pulse": 0},
    "device-4": {"group": "group-3", "current_pulse": 0},
    "device-5": {"group": "group-2", "current_pulse": 0}
}
DELTA_PERCENT_RANGES =[(2, 6), (7, 15), (16, 50),  (51, 100)]  
# [20, 50, 70, 100] means 20% - first range (2, 6), 30% - second range (7, 15), 20% - third range (16, 50), 30% - fourth range (51, 100) 
# [40, 50, 60, 100] means 40% - first range (2, 6), 10% - second range (7, 15), 10% - third range (16, 50), 40% - fourth range (51, 100) 
# [50, 80, 90, 100] means 50% - first range (2, 6), 30% - second range (7, 15), 10% - third range (16, 50), 10% - fourth range (51, 100) 
   
GROUPS = {
    "group-1": {"pulse_min": 50, "pulse_max": 210, "prob_change":10, "percent_ranges_thresholds": (20, 50, 70, 100),\
        "prob_incr": 70},
    "group-2": {"pulse_min": 40, "pulse_max": 220, "prob_change":20, "percent_ranges_thresholds": (40, 50, 60, 100),\
        "prob_incr": 50},
    "group-3": {"pulse_min": 60, "pulse_max": 180, "prob_change":40, "percent_ranges_thresholds": (50, 80, 90, 100),\
        "prob_incr": 50}
}

