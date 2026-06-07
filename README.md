# Separated branch from "main" branch
## create branch "pulse-jumps-branch
- it should contain only stuff related to jump pulse values
- template.yaml file should be updated appropriately
# Introduce common layer for logger_config exactly as we've done in the branch redeuced_values_branch
# Add lambda function for population jumps pulse values into MongoDB collection
## format of a document
- device_id
- previous pulse value
- current pulse values
- date/time in ISO UTC format with no TZ