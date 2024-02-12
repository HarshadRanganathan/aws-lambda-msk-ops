import logging
import os
import subprocess
import time
from datetime import datetime

# Logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def reset_consumer_group_offsets_by_datetime_all_topics(consumer_group, datetime):
    command = f"""kafka-consumer-groups.sh --bootstrap-server {os.environ['BOOTSTRAP_SERVERS']} --command-config kafka.properties --group {consumer_group} --reset-offsets --all-topics --to-datetime {datetime} --execute"""

    output = subprocess.run(
        f'{command}',
        encoding='utf-8',
        capture_output=True,
        shell=True,
        check=False
    )
    
    logger.info(output)
    logger.info(output.stdout)


def generate_date_time():
    current_date_time = datetime.now()
    return current_date_time.strftime("%Y-%m-%dT00:00:00.000")

def check_consumer_group_lag(consumer_group, timeout_in_min):

    command = f"""kafka-consumer-groups.sh --bootstrap-server {os.environ['BOOTSTRAP_SERVERS']} --command-config kafka.properties --describe -group {consumer_group} | awk '{{sum += $6}} END {{print sum}}'"""

    if timeout_in_min > 15:
        logger.error('TimeoutInMinutes cannot be greater than 15')
        exit(1)
      
    # wait until current_lag is 0 upto a timeout of timeout_in_min from current time
    timeout = time.time() + 60 * timeout_in_min
  
    # initialize current_lag with a random initial value
    current_lag = 100
  
    while current_lag != 0:
        output = subprocess.run(
            f'{command}',
            encoding='utf-8',
            capture_output=True,
            shell=True,
            check=False
        )
        try:
            current_lag = int(output.stdout)
        except ValueError:
            logger.error(output.stderr)
            exit(1)
        logger.info("Current lag is %s", current_lag)
      
        if time.time() > timeout:
            logger.info("Timeout! Lag is not 0. Exiting...")
            break
        elif current_lag != 0:
            # wait for 30 seconds before checking the lag again
            time.sleep(30)
    return {  
        'current_lag': current_lag 
    } 

def lambda_handler(event, context):
    
    logger.info(f"Event {event}")

    os.environ['PATH'] = 'kafka_2.12-'+ os.environ['KAFKA_VERSION']+'/bin:' + os.environ['PATH']

    try: 
        if event['RequestType'] == 'RESET_CONSUMER_GROUP_OFFSETS_BY_DATETIME_ALL_TOPICS':
            if not 'DateTime' in event:
                reset_consumer_group_offsets_by_datetime_all_topics(event['ConsumerGroup'], generate_date_time())
            else:
                reset_consumer_group_offsets_by_datetime_all_topics(event['ConsumerGroup'], event['DateTime'])
        elif event['RequestType'] == 'CHECK_CONSUMER_GROUP_LAG':
            # if event doesn't contain TimeoutInMinutes, default it to 0
            if not 'TimeoutInMinutes' in event:
                event['TimeoutInMinutes'] = 0
            return check_consumer_group_lag(event['ConsumerGroup'], int(event['TimeoutInMinutes']))
    except RuntimeError:
        logger.error('Signaling failure')
        sys.exit(1)
    else:
        logger.info('exit 0 block')
