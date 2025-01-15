# QCiEnMED
Ensuring data quality, citizen engagement and energy efficiency in IoT flash flood monitoring systems


Flooding is an inevitable phenomenon that might cause massive loss of people's lives and destruction of infrastructure. One of the effects of climate change in Mediterranean areas is the increase in the frequency and severity of environmental emergency episodes. Among other phenomena, severe Mediterranean meteorological events are precursors of the generation of rapidly evolving and very localized floods, which are therefore difficult to detect and predict with current remote sensing and modelization tools.

Given the increasing virulence and frequency of the flood effects, the need to develop knowledge and platforms that contribute to improve the protection of the population is evident. Automatic monitoring through sensor networks, the development of reliable digital technologies and the understanding of the data obtained during these episodes are fundamental actions required by practitioners, city authorities, Infrastruture engineers, and first responders, for placing emergency tasks in real-time. In this context, the sensor data is at the center of forecasting outputs, so it is important to assess the quality of the data from which decisions are made. Poor understanding of the quality of the data can lead to poor decisions.

The overall objective of the QFloodMED project is the development of disruptive and resilient AI-IoT technologies and tools using hardware and software approaches that guarantee data quality and the development of energy efficient open hardware solutions that can support sustainable environmental policies considering European and Spanish ecological transition objectives. This project addresses the challenge of improving high quality automatic flood early warning systems through the application of AI strategies and the development of new energy efficiency CPU designs based on open hardware. As a result, both coordinated projects aim to mitigate the negative consequences of the current climate and adverse weather. The broad and multidisciplinary knowledge of each research team will be used to achieve substantial improvements in the quality of sensor data and in the performance of field equipment to ensure accurate data collection at competitive energy costs.

The specific objectives of the QCiEnMED project are twofold: the first one is to design energy efficient software and hardware technologies based on the machine learning strategies for the implementation of a framework that guarantees the quality of the data provided by the measurement stations and allows an accurate short-term prediction of flash flood events. The second goal is to integrate first responders in emergency situations as data sources and real-time quality checkers for sensor values. It also aims to incorporate citizens as short-term forecast receivers, resulting in a quick preventive response of the society trying to reduce the negative effects of flash floods.It also aims to incorporate citizens as short-term forecast receivers, resulting in a quick preventive response of the society trying to reduce the negative effects of flash floods. The stakeholders integration in digital systems have been enforced due to the alignment with Sustainable Development Goals, specifically 16.7, contributing to making public decision-making related to flood events more inclusive, participatory and responsive.

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