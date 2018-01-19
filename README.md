# cartographer


## Description
This python library implements a simple network client to resolve the latitude, and longitude coordinates for a given address by using third party geocoding services.

## Requirements
* Python 2.7.9 or later.
* A Google Maps API key. (Found [here](https://developers.google.com/maps/documentation/geocoding/get-api-key))
* A HERE app_id and app_code. (Found [here](https://developer.here.com/documentation/geocoder/common/credentials.html))

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

The program prompts the user for the api credentials, and once entered, it asks the user to enter the address for which the lat and lng are to be resolved. The address entered is a space separated string. -
```
Please enter the address separated by spaces:
3451 Walnut Street Philadelphia
```

For which the output displayed on the terminal will look like - 
```
[INFO] Address: Franklin Building, 3451 Walnut St, Philadelphia, PA 19104, USA
[INFO] Latitude: 39.9533837
[INFO] Longitude: -75.1938205
```

### Using the json parser
The library also has the functionality to traverse jason data and retreive a particular value embedded within the tree. If the json data returned by the google api is 
```
{
   "results" : [
      {
         "address_components" : [
            {
               "long_name" : "3618",
               "short_name" : "3618",
               "types" : [ "street_number" ]
            },
            .......
         ],
         "formatted_address" : "3618 Garrott St, Houston, TX 77006, USA",
         "geometry" : {
            "location" : {
               "lat" : 29.7400054,
               "lng" : -95.38579500000002
            },
            "location_type" : "ROOFTOP",
            "viewport" : {
               "northeast" : {
                  "lat" : 29.7413543802915,
                  "lng" : -95.38444601970852
               },
               "southwest" : {
                  "lat" : 29.7386564197085,
                  "lng" : -95.38714398029153
               }
            }
         },
         "partial_match" : true,
         "place_id" : "ChIJSZmHA2W_QIYREyCmQWVayNs",
         "types" : [ "street_address" ]
      }
   ],
   "status" : "OK"
}
```
If we want to access the `lat` and `lng` fields, under location under geometry, the parameter path would be `"results/geometry/location/lat"` and `"results/geometry/location/lng"`. This path can be fed to `tools.get_config` method to retrieve the corresponding value.

## Features
* Implemented in Python
* Supports multiple geocoding services (Google and HERE)
* Fallback to a backup geocoding service, in case the primary service fails
* RESTful HTTP Interface
* Uses JSON for data serialization
* Json parser to get a particular parameter from the given jason data
* Uses a [PIMPL architecture](http://en.cppreference.com/w/cpp/language/pimpl), to essentially hide the implementation details, and use a stable api to access member functions of the library.
* Provides an option to query a custom url
* [Gitflow](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow) workflow design
* Uses python


## Future work
* Geo Point class can be extended to use lat and lng from different view points, different geometries
* SSL certificates not verified needs to be fixed
* Add more geo coding services
* Provide interface for adding a new geo coding interface in real time

## References
* Geocoding Service by [HERE](https://developer.here.com/documentation/geocoder/topics/quick-start.html)
* Geocoding Service by [Google](https://developers.google.com/maps/documentation/geocoding/start)
* [RESTful HTTP Interface](https://en.wikipedia.org/wiki/Representational_state_transfer)
* [JSON](https://en.wikipedia.org/wiki/JSON)
* [Python](https://www.python.org/)
* [git](https://git-scm.com/)
* [Python Client for Google Maps Services](https://github.com/googlemaps/google-maps-services-python)