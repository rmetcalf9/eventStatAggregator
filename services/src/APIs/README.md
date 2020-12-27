# API Plan

## Stats endpoints

POST /api/public/main/statsA/%tenant%/%name%
POST /api/public/main/statsB/%tenant%/%name%/%subname%

For both post the following json to give the inclusive start and end:
```
{
    "start": startTimestamp (only date part used),
    "end": endTimestamp (only date part used)
}
```

Response looks like:
```
{
    daily: [
        {daynum: 1, date: '20200915', count: 123},
        {daynum: 2, date: '20200916', count: 123},
        {daynum: 3, date: '20200917', count: 123}
    ]
}
```
daynum is a sequence number that the results can be orderd by.
