# ml-ball-demo

## Overview:
This repo is has all the files needed to run a new interactive musical instrument.

## Description:
- An arduino nano ble sense, fitted inside of a stress ball, send IMU data via bluetooth.
- A computer receives the IMU data via a python, and redirects it locally via OSC.
- OSC data is fed into Wekinator, which processes into the desired outputs (currently 3, can be modified)
- Max/MSP patch receives the Wekinator outputs and drives the music.

## Big thanks to:
- [Kris Winer for the IMU code](https://github.com/kriswiner/LSM9DS1)
- [Rebecca Fiebrink's Wekinator](http://www.wekinator.org/)
- [Python BLE comm tutorial](https://ladvien.com/python-serial-terminal-with-arduino-and-bleak/)



