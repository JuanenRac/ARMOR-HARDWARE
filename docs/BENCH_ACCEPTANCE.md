# Bench acceptance matrix

Nothing here has been measured yet. Every row starts as **not tested**. The requirements come
from the project specification; the pass criteria marked *proposed* are engineering suggestions
to be confirmed or changed by the owner before a prototype is built, and they are not results.

A row turns to **passed** only with a dated measurement record (instrument, method, value,
photo or log) stored with the prototype. A criterion that cannot be measured is rewritten until it can.

## Radio and sensing

| Item | Requirement | How to verify | Pass criterion | Status |
|---|---|---|---|---|
| 24 GHz transparency of the 1 mm radar cover (printed ASA/PETG) | The cover must not hide a person from the LD2450 | Same target at the same distances with and without the cover; compare reported range and track continuity | *Proposed:* detection range loss under 10 % and no track drops on a walking person at 3 m and 6 m | not tested |
| Cover thickness and distance | The front cover is 2 mm in the CAD, close to a quarter wavelength in an ABS-like plastic; the manual recommends about 3.9 mm or 1 mm or thinner, and 12.4 mm or 18.6 mm from the antenna to the cover | Measure the detection range and position error with covers of about 1 mm, 2 mm and 3.9 mm, and with the antenna at about 12 mm and 18 mm from the cover | *Proposed:* the chosen thickness loses the least range; record the material's real permittivity | not tested |
| Cover material | No metallic, conductive or carbon-loaded material in front of a radar aperture | Material data sheet; repeat the row above for each print material and colour | Attenuation measured for every material actually used | not tested |
| Three-sensor coverage | Three LD2450/LD2461 cover the 90° corner without a blind wedge | Walk a marked arc at 2, 4 and 6 m; record which sensor reports | Every angle covered by at least one sensor; hand-over between sensors keeps one track | not tested |
| Mounting height and back lobe | The manual recommends 1.5 m to 2 m and a metal shield behind the module | Walk behind the enclosure with and without a metal back plate | No phantom tracks from movement behind the node | not tested |
| Sensor separation | Radars do not disturb each other | Run all three, then one at a time; compare tracks | No change in a reference target's reported position beyond sensor noise | not tested |
| Ambient light window | The VEML7700 reads correctly through the translucent window | Compare against a reference lux meter from dark to full sun | *Proposed:* within 20 % across the range; day/night threshold flips at the configured lux | not tested |

## Environment

| Item | Requirement | How to verify | Pass criterion | Status |
|---|---|---|---|---|
| Ingress | Watertight corner enclosure with a peak visor | Spray test to the chosen IP target; cable gland torque per data sheet | *Target to be chosen:* no water inside after the test | not tested |
| Condensation drainage | Drainage holes let condensation out | Cycle temperature and humidity in a chamber or overnight outdoors | No standing water; window stays clear with the heater working | not tested |
| PTC surface temperature | The anti-fog heater must not damage the print or the electronics | Thermocouple on the PTC surface and on the nearest printed wall at full heater duty in a warm enclosure | *Proposed:* printed wall under 60 °C and no deformation after 8 h; well below the material's glass transition | not tested |
| Dew-point control | The heater keeps the window above the dew point | Cold-humid soak; log window temperature and dew point | Window stays more than 3 °C above the dew point while heating; heater off when dry | not tested |
| Print material | ASA or PETG survives the site | Sun and heat soak on a sample | No warp that opens a seam or shifts a sensor | not tested |

## Power and network

| Item | Requirement | How to verify | Pass criterion | Status |
|---|---|---|---|---|
| PoE budget | Node 3.8 to 5.5 W with the heater on; camera about 8 to 12 W; a 30 W PoE+ input leaves about 12.5 W margin | Inline power meter on the 48 V feed at idle, radars on, heater on, camera IR and motor active | Measured peak stays under the 30 W port limit with margin | not tested |
| PoE isolation | The PoE magnetics are isolated | Board and switch data sheets; continuity and hi-pot per the design | Isolation confirmed for the exact board used | not tested |
| Network segmentation | Field devices sit in the sensor VLAN with no internet | From a node and a camera: reach the broker, fail to reach the internet and other VLANs | Only the allowed broker, RTSP and API paths work | not tested |
| Broker identity | One identity and ACL per node | Try to read or write another node's topics with a node's credentials | Refused | not tested |
| Power loss | Central power redundancy | Pull the switch or server power with a UPS in place | Nodes report offline through the last will; the server restarts cleanly | not tested |

## Cameras

| Item | Requirement | How to verify | Pass criterion | Status |
|---|---|---|---|---|
| Stream | RTSP main and sub streams work | Discover paths from the server; view live for an hour | Stable video, no relay restarts | not tested |
| PTZ | Bounded movement over the camera's real protocol (Hi3510, PSIA or ONVIF) | Each direction, zoom and stop from Studio and the phone | Moves and stops; a fixed camera reports a real failure | not tested |
| Digest authentication | The camera accepts the server's authentication scheme | Test each camera model and firmware | Recorded per model in the compatibility table | not tested |

## Compatibility table (fill in per camera)

| Camera model and firmware | RTSP path | Auth | PTZ protocol | Night IR | Result |
|---|---|---|---|---|---|
| | | | | | not tested |
