# la-fabrica
Microservices that run my smarthome

### Alert system MQTT

This microservice wait for data coming through MQTT in order to analyze it. It raises and triggers either visible or audible alarms if one evaluate condition happens.

### Alert system rquest

This microservice request data to different sources and triggers either visible or audible alarms if one evaluated condition happend.

### Data panel front

This microservice is a web frontend that shows data in form of dashboards in different screens around the house. The data comes from different sources, including Homeware.

### Data panel API

This microservice is an REST API for the data dashboards. It request data to different sources and cache for the right amount time.

### Data panel autoload

This microservice forces the loading of the dashboard in a chromecast when not playing anything on it.

### Logic pool MQTT

This microservice is in charge of making logic relationships between devices and scenes. It interacts with Homeware MQTT API for detecting trigger events and making changes in devices.

### Logic pool time

This microservice makes changes in Homeware devices using time as trigger.

### MQTT 2 BigQuery

This microservice sends Homeware's data to Google Cloud BigQuery. It uses the Homeware MQTT API for detecting changes in the monitored data.