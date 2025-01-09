# Outlier detection server
This code contains a server for an outlier detection system, using the batched version of the code developed in [this repository](https://github.com/BarkSanson/kalman-mk-iforest). 
It is simply a Flask server that receives a block of data, processes it to detect outliers and sends the results to another server.

## Data process and format
The data is expected to come from an station, with an string ID, and following the next process:
1. The station must be first initialized, sending a JSON with the station ID and the data variables that will be sent to /initialize endpoint. The format is:
```json
{
    "id_estacio": "station_1",
    "variables": {
      "var_1": 32,
      "var_2": 128,
      "var_3": 256
    }
}
```
Each number assigned to each variable represents the maximum window length that will be used for that concrete variable.

2. After the initialization, a block of data can be sent to the server to the /detection endpoint, using the following format:
```json
{
    "id_estacio": "station_1",
    "numero_mostres": 2,
    "mostres": [
        {
            "timestamp": "2021-01-01 00:00:00",
            "values": {
                "var_1": 0.5,
                "var_2": 4,
                "var_3": 2 
            }
        },
        {
            "timestamp": "2021-01-01 00:01:00",
            "values": {
              "var_1": 0.6,
              "var_2": 5,
              "var_3": 1
            }
        }
    ]
}
```
3. Once the server received the data, it will process it and send the results to the server specified as DATA_SERVER_ENDPOINT env variable. The format
of the results is:
```json
[
    {
        "id_estacio": "station_1",
        "variable": "var_1",
        "dates": [
            "2021-01-01 00:00:00",
            "2021-01-01 00:01:00"
        ]
    },
    {
        "id_estacio": "station_1",
        "variable": "var_2",
        "dates": [
            "2021-01-01 00:00:00",
            "2021-01-01 00:01:00"
        ]
    }
]
```

# How to run

There is a Dockerfile that can be used to run the server. The server needs the DATA_SERVER_ENDPOINT env variable, and makes use of
two volumes: /logs and /models. The first one is used to store the logs of the server, and the second one to store the models that are used
to detect the outliers. The server can be run with the following command:
```bash
docker run -d -p 8080:8080 -e DATA_SERVER_ENDPOINT=<endpoint> -v /path/to/logs:/logs -v /path/to/models:/models barksanson/outlier-detection
```
This image uses Waitress as the server, and the server is exposed in the 8080 port.