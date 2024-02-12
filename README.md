# aws-lambda-msk-ops

Lambda function that performs various actions against MSK cluster.

## RESET_CONSUMER_GROUP_OFFSETS_BY_DATETIME_ALL_TOPICS

Resets the consumer group offset with the provided datetime.

### Input Payload

```
{
  "RequestType": "RESET_CONSUMER_GROUP_OFFSETS_BY_DATETIME_ALL_TOPICS",
  "ConsumerGroup": "test-topic",
  "DateTime": "2023-04-17T00:00:00.000"
}
```

If `DateTime` is not supplied then it uses the current date timestamp for offset reset.

```
{
  "RequestType": "RESET_CONSUMER_GROUP_OFFSETS_BY_DATETIME_ALL_TOPICS",
  "ConsumerGroup": "test-topic"
}
```
