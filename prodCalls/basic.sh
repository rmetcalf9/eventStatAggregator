curl -X POST \
  https://api.metcarob.com/eventstataggregator/v0/private/api/main/statsB/challengeappstage/statname/statsubname \
  -H 'cache-control: no-cache' \
  -H 'content-type: application/json' \
  -H 'postman-token: 9c21eeb7-a9d1-65cf-38cc-d8688882f28c' \
  -d '{
  "start": "2021-01-01T15:50-04:00",
  "end": "2021-03-01T15:50-04:00"
}'

