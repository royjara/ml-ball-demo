# ml-ball-demo

## Overview:
This repo has all the files needed to run a new interactive musical instrument.
Currently it doesn't sound very melodic but with some more work it could be a nifty instrument.

## Description:
- An arduino nano ble sense, fitted inside of a stress ball, send IMU data via bluetooth.
- A computer receives the IMU data via a python, and redirects it locally via OSC.
- OSC data is fed into Wekinator, which processes into the desired outputs (currently 3, can be modified)
- Max/MSP patch receives the Wekinator outputs and drives the music.

### Notice that to power the board using a battery you have to solder the 5V pad.
![2021-11-01 20 47 50](https://user-images.githubusercontent.com/32803636/147714506-2f3845c6-6b26-403c-84f5-d962fd3147a9.jpg)


### Rough soft case - could be replace by a 3D printed enclosure. 
![2021-11-01 20 48 24](https://user-images.githubusercontent.com/32803636/147714508-1c62f53d-811e-4da6-9d55-e3a701fb1880.jpg)
![2021-11-01 20 49 00](https://user-images.githubusercontent.com/32803636/147714510-702e52e9-a368-4b3c-bd77-e173e8e5a786.jpg)



## Big thanks to:
- [Kris Winer for the IMU code](https://github.com/kriswiner/LSM9DS1)
- [Rebecca Fiebrink's Wekinator](http://www.wekinator.org/)
- [Python BLE comm tutorial](https://ladvien.com/python-serial-terminal-with-arduino-and-bleak/)



