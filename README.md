# Propane Scale
## What is the problem this code is trying to solve?
[Pumping Station: One](www.pumpingstationone.org) has a forge that is fed by a 100lbs propane cylinder. The gas is fed to the forge via a simple regulator that does not have a gauge to indicate how much gas remains, leading to folks running out while using the forge which can be very frustrating. 

So in keeping with it being a hackerspace, I built a scale using loadcells and the cylinder sits on that, reporting the weight constantly via MQTT for other services to make use of the info (currently a Slack bot that you can query to find the percentage remaining).

## Hardware
The load cells are plugged into an [OpenScale board](https://www.sparkfun.com/products/13261). The board is basically a custom Arduino which is fine for getting the load cells to work, but I soldered the wires to a Raspberry Pi 0 so I would have a Wifi-based Linux computer to use so the box with the electronics could be tucked away near the scale without worrying about running an ethernet cable.

## Software
The program itself is pretty straightforward. The one thing to note in the `weigh()` function is that it reads the samples at one-minute increments and then returns the floor'ed mean of the samples, as there can be some fluctuation from sample to sample (and the OpenScale board is sending the sample every second). 

After the weight is returned, the value along with the current timestamp is sent to the MQTT server running on `glue`; which is a Linux VM running at PS1. From there, a Slack bot (written in Go) makes the value available to anyone who queries it in the `#HotMetalShop` and `#forging` channels.
