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
