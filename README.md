# car-computer-raspberry

This project is about developing an "Intelligent" Car Computer based on Raspberry Pi Zero .

- connection to the car through obd2 connector 
- connection from Raspberry to Elm 327 obd2 with Bluetooth connection
- Raspberry gather continuosly data from the car, such as speed, engine rpm, oil temperature, ambient temperature , ecc...
- Raspberry has a camera ( Picamera v2 )


The aim of this project is to automatically detect objects on the road, and give feedbacks and warnings , for example:

- traffic sign detection - speed limit : Compare the car speed to the limit speed and give audio feedback through the car speakers

- car and pedestrian detection ( along with other objects ): warning about the proximity of other objects 

- lane detection : warnings to keep the car within the lanes

