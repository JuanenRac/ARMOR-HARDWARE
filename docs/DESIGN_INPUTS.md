# Design inputs and open decisions

The outdoor node design must reserve independent volumes for three radar modules,
the ESP32-S3-ETH-PoE controller, sensor window, cable gland, PoE magnetics and
PTC heater. Do not place a metallic, conductive or carbon-loaded material in
front of a 24 GHz radar aperture without measured attenuation data.

Before fabrication, record exact board outlines, connectors, screw locations,
antenna keep-outs, thermal path and ingress target. The current CAD remains a
mechanical concept, not manufacturing evidence.

## The HLK-LD2450, from its manual

Facts taken from the Hi-Link *HLK-LD2450 Instruction manual* V1.00 (2023-05-10); they are the
manufacturer's statements, not measurements of this project.

| Item | Manual |
|---|---|
| Size | 15 mm x 44 mm, pin or socket interface (UART, 5 V, GND) |
| Supply | 5 V, source able to give more than 200 mA; 120 mA average, so each module draws about 0.6 W and three draw about 1.8 W |
| Logic | 3.3 V I/O, UART 256000 baud, 8N1 |
| Range and angle | 6 m maximum, azimuth plus or minus 60 degrees, pitch plus or minus 35 degrees, three targets, 10 Hz |
| Band | 24 GHz to 24.25 GHz, FMCW |
| Ambient temperature | -40 to 85 degrees C |
| Mounting | Wall mounting, height 1.5 m to 2 m recommended; antenna facing the area, open and unobstructed; fixed firmly (shaking degrades detection) |
| Back of the module | The antenna's back lobe can see movement behind the module; a metal shield or back plate reduces it |
| Several 24 GHz radars | Do not point them at each other; keep them as far apart as possible |
| Cover | No metal or conductive material or coating; smooth, flat and of uniform thickness, parallel to the antenna |

### Cover guidance in the manual, applied to this enclosure

* Distance from the antenna to the inner face of the cover: 1 or 1.5 wavelengths, that is **12.4 mm or 18.6 mm** at
  24.125 GHz, tolerance plus or minus 1.2 mm.
* Thickness: about half a wavelength **in the material** (plus or minus 20 %); for an ABS-like plastic
  (relative permittivity about 2.5) that is about **3.9 mm**. If that is not possible, use a low-permittivity
  material at **one eighth of a wavelength or thinner**, about 1 mm for that same plastic.
* The CAD front cover is `cover_thickness = 2` mm. For a permittivity near 2.5 that is close to a *quarter* of a
  wavelength in the material, which is neither of the two recommended cases and, for a plain slab, where
  reflection is greatest. This is arithmetic from the manual's formula, not a measurement, and the real
  permittivity of the printed ASA or PETG is unknown: measure it (see [BENCH_ACCEPTANCE](BENCH_ACCEPTANCE.md))
  before printing the final cover, and consider about 1 mm or about 3.9 mm.
* The antenna-to-cover distance in the CAD, worked out by hand from the parameters (OpenSCAD was not available to measure it), taking the front face of each radar holder as the antenna plane:
  the diagonal radar (`s3`) sits about 12.2 mm from the inner face of the cover, inside the tolerance of 12.4 mm, but it is tilted 20 degrees to it; the two side radars (`s1`, `s2`) are
  about 17.6 mm from it measured square to the cover (20.3 mm along the beam), with 30 degrees of yaw and 20 degrees of tilt. **Neither recommended distance is met on the two side radars and the cover
  is not parallel to any of the three antennas.** The model has not been changed (it needs a printed trial and the real position of the antenna on the LD2450 module): a faceted cover with one flat window square to each radar,
  or holders turned to be parallel to their stretch of cover, is the way to fix it. The bench rows *Cover thickness and distance* and *Sensor separation* are where it gets measured.

## The electrical node and mains voltage

The electrical node's base board measures mains voltage (see ARMOR-NODE-ELECTRICAL). `scad/node_box.scad` is a printed SELV box: it has no barrier between a mains zone and a low-voltage zone, no creepage and clearance distances and no flame-retardant (V-0) material, so it is **not** an enclosure for mains wiring.
Put the mains side in a certified enclosure or on a DIN rail, and use the printed box only for the low-voltage part, or separate the zones physically and print in a V-0 rated material.

## The solar node and Pylontech batteries: inputs for a next base board

What the makers' manuals say about the connectors of a Pylontech battery, written down for the next revision of the solar base board. It is taken from the manuals, not measured on our board; check every pin against the battery in hand before wiring.

* **Console port (RJ45, RS232 levels):** pin 3 is the battery's transmit (to the node's receive), pin 6 its receive (from the node's transmit), pin 8 is ground. The console of recent batteries runs at 115200 baud; an old unit may say another speed (19200) in its `info`. Some batteries (the US2000B) use an RJ11 for it, and an RJ11 cable may carry only two wires.
* **Waking a sleeping battery:** pins 4 and 5 of the console port take +5 to 12 V (5 to 15 mA) for at least half a second, with ground on pin 5; the US2000C, US3000C, US5000 and UP5000 support it. A future revision can add an **output for it**: a small load switch or a transistor from a protected 5 V rail, current-limited, that the firmware pulses only when a battery has stopped answering. Nothing is driven today.
* **Dry contacts (the *Contact* RJ45 port):** output 1 means *stop charge*, output 2 *stop discharge* and output 3 a *BMS error*; they are passive signals of at most 25 V. A future revision can read them with **opto-isolated inputs** (an opto-coupler with a series resistor sized for 25 V and a pull-up on the node's side), so the protection state is known independently of the console. They are inputs only: input 1 of the battery (*switch the battery off*) is never driven.
* **RS485 and CAN:** the RS485 pins are 7 and 8 (A and B) and the CAN pins 4, 5 and 6 (H, L and ground) of their own ports; the RS485 speed is set by the battery's DIP switch 1 (on: 9600, off: 115200; restart the battery after changing it) and CAN runs at 500 kbit/s.
* **Level converter:** a MAX3232 powered from 3.3 V needs its five 0.1 uF capacitors; the base board already has one per pair of sockets.
