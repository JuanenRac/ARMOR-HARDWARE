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
| Supply | 5 V, source able to give more than 200 mA; 120 mA average, so three modules draw about 0.6 W |
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
* The CAD front cover is `tapa_grosor = 2` mm. For a permittivity near 2.5 that is close to a *quarter* of a
  wavelength in the material, which is neither of the two recommended cases and, for a plain slab, where
  reflection is greatest. This is arithmetic from the manual's formula, not a measurement, and the real
  permittivity of the printed ASA or PETG is unknown: measure it (see [BENCH_ACCEPTANCE](BENCH_ACCEPTANCE.md))
  before printing the final cover, and consider about 1 mm or about 3.9 mm.
* Check the antenna-to-cover distance in the CAD against 12.4 mm or 18.6 mm; it has not been checked.
