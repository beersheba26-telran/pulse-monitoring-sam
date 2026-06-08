from logger_config import logger
import psycopg
"""
receives events from SNS topic jumps-topic
creates notification data according to the percentge of 
jump in current value relative to the previous value
defines severirty of notification 40-50% - Minor,
51-70% - Major, more 70% - Critical
and stores the notification data into table notifications
see notifications.png for schema
"""
