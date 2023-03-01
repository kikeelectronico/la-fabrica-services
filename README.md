# la-fabrica
Microservices that run my smarthome

![My home architecture](https://assets.enriquegomez.me/Arquitectura-La-fabrica.jpg)

### Alert system rquest

This microservice requests data to different sources and triggers either visible or audible alarms if one evaluated condition happend.

### Data panel API

This microservice is a REST API for the data dashboards. It request data to different sources and cache for the right amount time.

### Data panel autoload

This microservice forces the loading of the dashboard in a chromecast when not playing anything on it. Not in use at the moment.

### Data panel front

This microservice is a web frontend that shows data in form of dashboards in different screens around the house. The data comes from different sources, including Homeware.

### DNS Updater

This microservice get the public IP of the router and update the value in the DNS if needed.

### Heartbeat monitor

This microservice monitors the heartbeats sent by the rest of microservices and send an alert if needed.

### Heartbeat request

This microservice requests heartbeats to the passive microservices. A microservice is passive when it doesn't send the heartbeats by itself, it needs an external request.

### Hue 2 mqtt

This microservice gets data from the Philips Hue Bridge and push it to Homeware via MQTT

### Logic pool Hue

This microservice is in charge of making logic relationships between Philips Hue switches and other devices and scenes. It interacts with Hue bridge API for detecting trigger events in the switches and making changes in devices.

### Logic pool MQTT

This microservice is in charge of making logic relationships between devices and scenes. It interacts with Homeware MQTT API for detecting trigger events and making changes in devices.

### Logic pool time

This microservice makes changes in Homeware devices using time as trigger.

### Message alert

This microservice is in charge of sending telegram messages.

### MQTT 2 BigQuery

This microservice sends Homeware's data to Google Cloud BigQuery. It uses the Homeware MQTT API for detecting changes in the monitored data.

### MQTT 2 Hue

This microservice connects Homeware with a Philips Hue Bridge.

### Presence detection

An experiment in which I am trying to evaluate if it makes sense to decide if the house is empty using the IPs of critical devices.

### Telegram bot

A way to interact with the system via Telegram. It is not currently in use, but probably I will update it soon.

### Voice alert

This microservice generates voice alerts using text to speech and the smart speakers at home.