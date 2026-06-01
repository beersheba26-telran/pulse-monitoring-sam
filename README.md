# Pulse values reducer
## Saving all pulse values for each device into DynamoDB
- device-id as Partition Key
- list of pulse values as data related to the partition key
- started_at as timestamp of creating partition for the device
- each probe data are used for adding new value into the appropriate list
## At the configured time period (for example Production 1 hour, test 1 minute )
### Creating reduced probe containing
- device_id
- min pulse value
- median pulse value
- max pulse value 
- timestamp
### deleting the record with the list of pulse values
### publishing the created probe inside SNS topic "reduced-pulse-values"
# Reduced values processor placeholder
- lambda function as a subscriber of SNS topic with reduced value
- Prints out reduced values
# Simple imitator pulse values
- 5 devices
- each device sends random probe (device_id, random pulse value [60-200])
- duration is 5 minutes
- each second - one generated probe