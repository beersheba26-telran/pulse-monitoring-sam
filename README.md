
# Jumps-Analyzer Microservice
- Subscriber of ingest stream SNS-FIFO (existing) , SQS-FIFO being created in the SAM template
- DynamoDB for keeping the last pulse value of the device
- Analyzing by comparing current and previous last values. If the refresh is more than a configured value (Default 40%) then it creates probe being sent to the topic “pulse-jumps”. That probe has the following structure <br>
{<br>
	“Device_id”: < string > <br>
	“Previous_pulse_value”: < number > <br>
	“Current_pulse_value”:< number > <br>
    "timestamp":<number>
} <br>
DynamoDB table and “pulse-jumps” topic should be created / deleted in SAM template
# Jumps-processor
- only placeholder functionality for testing Jumps-Analyzer microservice
- subscriber "pulse-jumps" SNS topic
- printing out the fields of "jump" probe being published from Jumps-Analyzer
