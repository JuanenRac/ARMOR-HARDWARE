# The pins of the nodes

One table for the box and the wiring, made by `tools/pinout.py` from the tables the firmware is built with (`firmware_base/core/board_s3.hpp` and `base_board.hpp` of ARMOR-COMMON);
the test `tests/test_pinout.py` fails when this file is not what those tables give, so it cannot drift. Every pin is a setting in the panel of the node: these are where a node that
was never configured looks first. Nothing here has been checked on a board; the sizes and positions of the connectors are in `DESIGN_INPUTS.md`.

The two boards are the Waveshare ESP32-S3-ETH (`s3-eth`: Ethernet on a W5500, a microSD socket and a camera connector) and an ESP32-S3-WROOM-1 N16R8 development board
(`s3-wifi`: Wi-Fi only). `free` is a pin a port may use, `care` a pin that works but has a second role, `never` a pin the firmware does not offer.

## The pins of the module

| GPIO | s3-eth | s3-wifi |
| --- | --- | --- |
| 0 | care: BOOT button, read at reset | care: BOOT button, read at reset |
| 1-2 | free | free |
| 3 | care: strapping pin, read at reset | care: strapping pin, read at reset |
| 4-7 | care: microSD socket (free when no card is used) | free |
| 8 | never: camera connector (not on the header) | free |
| 9-14 | never: W5500 Ethernet controller (not on the header) | free |
| 15-18 | free | free |
| 19-20 | never: native USB | never: native USB |
| 21 | free | free |
| 22-25 | never: does not exist (not on the header) | never: does not exist (not on the header) |
| 26-32 | never: external flash (not on the header) | never: external flash (not on the header) |
| 33-34 | never: octal PSRAM (not on the header) | never: octal PSRAM (not on the header) |
| 35-37 | never: octal PSRAM (not on the header) | never: octal PSRAM |
| 38-42 | free | free |
| 43-44 | care: UART0: the boot ROM prints at every reset | care: UART0 to the USB-serial socket |
| 45-46 | care: strapping pin, read at reset | care: strapping pin, read at reset |
| 47 | free | free |
| 48 | free | care: on-board RGB LED |

## The ten serial ports (rx / tx / direction)

A direction pin of `-` means the port has none (a plain UART, or a transceiver that switches by itself).

| Port | s3-eth | s3-wifi |
| --- | --- | --- |
| 1 | 16 / 15 / 7 | 16 / 15 / 7 |
| 2 | 18 / 17 / 6 | 18 / 17 / 8 |
| 3 | 4 / 5 / - | 4 / 5 / 6 |
| 4 | 1 / 2 / - | 9 / 10 / - |
| 5 | 21 / 47 / - | 11 / 12 / - |
| 6 | 38 / 39 / - | 13 / 14 / - |
| 7 | 40 / 41 / - | 21 / 47 / - |
| 8 | 42 / 48 / - | 38 / 39 / - |
| 9 | 43 / 44 / - | 40 / 41 / - |
| 10 | 3 / 46 / - | 42 / 1 / - |

## The base board (electrical and alarm nodes)

`-` is no pin until one is chosen in the panel.

| Item | s3-eth | s3-wifi |
| --- | --- | --- |
| Zigbee radio: rx, tx, reset, bootloader | 18, 17, 43, 44 | 18, 17, 21, 47 |
| Relay 1 | 38 | 38 |
| Relay 2 | 39 | 39 |
| Relay 3 | 40 | 40 |
| Relay 4 | 41 | 41 |
| Relay 5 | 42 | 42 |
| Relay 6 | 47 | 11 |
| Relay 7 | 48 | 12 |
| Relay 8 | 21 | 13 |
| Analog input 1 (ADC1) | 1 | 1 |
| Analog input 2 (ADC1) | 2 | 2 |
| Analog input 3 (ADC1) | 4 | 4 |
| Analog input 4 (ADC1) | 5 | 5 |
| Analog input 5 (ADC1) | 6 | 6 |
| Analog input 6 (ADC1) | 7 | 7 |
| Analog input 7 (ADC1) | - | 8 |
| Analog input 8 (ADC1) | - | 9 |
