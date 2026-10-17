# Hardware validation boundary

The enclosure model is a printable mechanical starting point, not an IP, RF or
thermal rating. Validate 24 GHz attenuation, condensation drainage, cable glands,
PoE isolation and PTC surface temperature on a real prototype before deployment.

## The thickness of the front cover and the 24 GHz radar

The front cover is 2 mm thick (`cover_thickness` in `scad/node_enclosure_radar.scad`). For a 24 GHz radar behind a plastic window, the thickness matters: the wave in a printed plastic (relative permittivity about 2.5 to 2.7: ASA, ABS and PETG are near 2.5, PLA near 2.7) is about 7.6 to 7.9 mm long, so a window reflects the most at a quarter of it (about 1.9 to 2 mm) and the least at half of it (about 3.8 to 3.9 mm) or when it is very thin (1 mm or less). A 2 mm cover is therefore close to the worst case **by this calculation**; it is a calculation, not a measurement, and the printed material, its infill and the air gap to the antenna change it. Before relying on the range of a printed node, measure the same radar with and without the cover and, if it loses range or shows echoes, try 1 mm or 3.8 mm, with the cover parallel to the antenna. The model has not been changed for this: the cover is also a structural part (the slots of the box are cut from its thickness) and the change needs a printed trial.

## What is versioned here

The STL, 3MF and AMF files of the enclosure are generated from the OpenSCAD source and kept in the repository so that the model can be printed without installing OpenSCAD; the source is the truth and a file that disagrees with it is stale. Regenerating them from the source is part of changing the model.
