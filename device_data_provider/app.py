stub_configuration = {
    "device_1": {
        "min_value": 50,  
        "max_value": 210, 
        "deviation_percent_threshold": 50
    },
    "device_2": {
        "min_value": 50,  
        "max_value": 210, 
        "deviation_percent_threshold": 50
    },
    "device_3": {
        "min_value": 40,  
        "max_value": 220, 
        "deviation_percent_threshold": 40
    },
    "device_4": {
        "min_value": 60,  
        "max_value": 180, 
        "deviation_percent_threshold": 60
    },
    "device_5": {
        "min_value": 40,  
        "max_value": 220, 
        "deviation_percent_threshold": 40
    },
    "unknown_device": {
        "min_value": 50,  
        "max_value": 210, 
        "deviation_percent_threshold": 50
    }
    
    
}
def lambda_handler(event, context):
    """even of direct invocation with device_id value
    it returns payload
    {
        min_value: int,
        max_value: int,
        deviation_percent_threshold: int
    }
    the given code is only stub (real implementation will work with SQL)
    
    """
    device_id = event["device_id"]
    return stub_configuration.get(device_id, stub_configuration["unknown_device"])