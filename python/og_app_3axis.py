# https://tutorialedge.net/python/concurrency/asyncio-event-loops-tutorial/
import os
import sys
import asyncio
import platform
from datetime import datetime
from typing import Callable, Any

from aioconsole import ainput
from bleak import BleakClient, discover

from pythonosc import udp_client
import struct

selected_device = []


class DataToOsc:

    def __init__(self, ip, port, osc_path):
        '''
        ip (str) : ip address to post osc
        port (int) : port number to post osc data
        osc_path (str) : path to publish osc data
        '''
        self.ip = ip
        self.port = port
        self.osc_path = osc_path
        self.client = udp_client.SimpleUDPClient(self.ip, self.port)

    def write_to_osc(self, data_values: Any):
        self.client.send_message(
            self.osc_path, [struct.unpack('f', data_values[0])[0],
                            struct.unpack('f', data_values[1])[0],
                            struct.unpack('f', data_values[2])[0]
                            ])
        # print(
        #     f"{self.osc_path} {struct.unpack('f', data_values[0])[0]} {struct.unpack('f', data_values[1])[0]} {struct.unpack('f', data_values[2])[0]}")
        # print(f"{self.osc_path} { data_values}")


class Connection:

    client: BleakClient = None

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop,
        readq0_characteristic: str,
        data_dump_handler0: Callable[[str, Any], None],
        data_dump_size: int = 3,
    ):
        self.loop = loop
        self.readq0_characteristic = readq0_characteristic

        self.data_dump_handler0 = data_dump_handler0

        self.last_packet_time = datetime.now()
        self.dump_size = data_dump_size
        self.connected = False
        self.connected_device = None

        self.rx_data = []
        self.rx_timestamps = []
        self.rx_delays = []

    def on_disconnect(self, client: BleakClient):
        self.connected = False
        # Put code here to handle what happens on disconnet.
        print(f"Disconnected from {self.connected_device.name}!")

    async def cleanup(self):
        if self.client:
            await self.client.stop_notify(self.readq0_characteristic)
            await self.client.disconnect()

    async def manager(self):
        print("Starting connection manager.")
        while True:
            if self.client:
                await self.connect()
            else:
                await self.select_device()
                await asyncio.sleep(15.0)

    async def connect(self):
        if self.connected:
            return
        try:
            await self.client.connect()
            self.connected = await self.client.is_connected()
            if self.connected:
                print(F"Connected to {self.connected_device.name}")
                self.client.set_disconnected_callback(self.on_disconnect)
                await self.client.start_notify(
                    self.readq0_characteristic, self.notification_handler0,
                )
                while True:
                    if not self.connected:
                        break
                    await asyncio.sleep(0.1)
            else:
                print(f"Failed to connect to {self.connected_device.name}")
        except Exception as e:
            print(e)

    async def select_device(self):
        print("Bluetooh LE hardware warming up...")
        await asyncio.sleep(2.0)  # Wait for BLE to initialize.
        devices = await discover()

        print("Please select device: ")
        for i, device in enumerate(devices):
            print(f"{i}: {device.name}")

        response = -1
        while True:
            response = await ainput("Select device: ")
            try:
                response = int(response.strip())
            except:
                print("Please make valid selection.")

            if response > -1 and response < len(devices):
                break
            else:
                print("Please make valid selection.")

        print(f"Connecting to {devices[response].address}")
        self.connected_device = devices[response]
        self.client = BleakClient(devices[response].address)

    def notification_handler0(self, sender: int, data: Any):
        self.rx_data.append(data)
        if len(self.rx_data) >= self.dump_size:
            self.data_dump_handler0(self.rx_data)
            self.rx_data = []

#############
# Loops
#############


async def main():
    while True:
        # YOUR APP CODE WOULD GO HERE.
        await asyncio.sleep(0.01)


#############
# App Main
#############
q0_characteristic = "0000181a-0000-1000-8000-00805f9b34fb"
q1_characteristic = "00002A3D-0000-1000-8000-00805f9b34fb"
q2_characteristic = "00002A58-0000-1000-8000-00805f9b34fb"

if __name__ == "__main__":

    # Create the event loop.
    loop = asyncio.get_event_loop()

    data_to_osc0 = DataToOsc("127.0.0.1", 10000, "/wek/inputs")
    connection = Connection(
        loop, q0_characteristic, data_to_osc0.write_to_osc,
    )
    try:
        asyncio.ensure_future(connection.manager())
        asyncio.ensure_future(main())
        print("entering run_forever loop :^)")
        loop.run_forever()
    except KeyboardInterrupt:
        print()
        print("User stopped program.")
    finally:
        print("Disconnecting...")
        loop.run_until_complete(connection.cleanup())
