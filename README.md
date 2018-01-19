# cartographer


## Description
This python library implements a simple network client to resolve the latitude, and longitude coordinates for a given address by using third party geocoding services.

## Requirements
⋅⋅* Python 2.7 or later.
⋅⋅* A Google Maps API key. (Found [here](https://developers.google.com/maps/documentation/geocoding/get-api-key))
⋅⋅* A HERE app_id and app_code. (Found [here](https://developer.here.com/documentation/geocoder/common/credentials.html))

## Usage
In order to use this library, a script `geo_client_service` is provided which queries the google API, the here API or a custom url defined by the url. The script uses an argument parser to recognize which of the three options to use. For a list of options, type `./geo_client_service` on the terminal, to get a help message.
```
sidd@sidd-pc:~/cartographer$ ./geo_client_service 
usage: geo_client_service [-h] [--google_query] [--here_query]
                          [--custom_query]

Geocoding Proxy Service.

optional arguments:
  -h, --help          show this help message and exit
  --google_query, -g  Make a request to the Google Geo Coding API, no args
  --here_query, -r    Make a request to the HERE Geo Coding API, no args
  --custom_query, -c  Make a request to a custom Geo Coding API, no args

```

## Feaatures
