# Event Stat Aggregator

My first choice of implementing this functionality was to use elasticSearch but it turned out this was not compatible with my infrastructure so I have instead make this simple stat aggregator. In future I may migrate to elastic search.

## Config

The app splits events into the day they occur
timestamps must be in a single timezone that is specified by:
APIAPP_TIMEZONE="America/St_Johns"   #default "Europe/London"

## Events

Events are read from a queue. The body must be JSON and must have the following elements:

id - ID of event (passed in)
name - Name of event (Such as "ChallengeCompleted")
subname - Subname of event (Such as an id of a particular challenge)
timestamp - timestamp of event
  

