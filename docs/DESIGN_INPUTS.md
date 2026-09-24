# Design inputs and open decisions

The outdoor node design must reserve independent volumes for three radar modules,
the ESP32-S3-ETH-PoE controller, sensor window, cable gland, PoE magnetics and
PTC heater. Do not place a metallic, conductive or carbon-loaded material in
front of a 24 GHz radar aperture without measured attenuation data.

Before fabrication, record exact board outlines, connectors, screw locations,
antenna keep-outs, thermal path and ingress target. The current CAD remains a
mechanical concept, not manufacturing evidence.
