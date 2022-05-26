# sbwy.live

A ~proper~ geeky way to check NYC Subway arrival times.

This tool is inspired by [wttr.in](https://wttr.in).

`sbwy.live` is made possible by using APIs from [`transiter`](https://github.com/jamespfennell/transiter).

## Usage
```
curl sbwy.live/<line>        # show stations and their IDs of the line
curl sbwy.live/<zip_code>    # show stations around that zipcode
curl sbwy.live/<station_id>  # show arrival times at a station
```

## Examples

* `curl sbwy.live/R` returns

<img width="642" alt="by_line" src="https://user-images.githubusercontent.com/6183541/170407481-26bfe57f-4b15-42f3-bdb2-ea3fd74aff8b.png">

* `curl sbwy.live/10002` returns

<img width="637" alt="by_zipcode" src="https://user-images.githubusercontent.com/6183541/170407666-62842a4c-333f-418f-99a0-fad4ca6a29fa.png">

* `curl sbwy.live/R21` returns the arrival times

<img width="637" alt="arr_time" src="https://user-images.githubusercontent.com/6183541/170407725-3cb3f2cc-542e-432c-ba54-6ae5ec2d7ed5.png">

