# Datastructures I am using

## Events Table

```
id - unique GUID assigned on insert
creation_date - date the event hit the database
tenant - each queue puts messages into a sintle tenant
event_name - Name of event (Such as "ChallengeCompleted")
event_subname - Subname of event (Such as an id of a particular challenge)
event_id - ID of event (passed in)
dom - day of month of event - 1-31
month - event month number - 1-12
year - event year (4 digit number)
event_date - date of event in SQL Alchemy format
```

### Rejected fields
 - event_dest - destination event was sent to is NOT a field so system can work when migrating from queues to topics

