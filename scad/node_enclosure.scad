// ARMOR-HARDWARE parametric field-node enclosure.
// Copyright (C) 2026 JuanenRac (Electro Hobby 3D). CERN-OHL-S-2.0.
width=180; depth=100; height=70; wall=3; drain_diameter=4;
difference(){ cube([width,depth,height],center=true); translate([0,0,wall]) cube([width-2*wall,depth-2*wall,height],center=true); for(x=[-65,65]) translate([x,-42,-height/2]) cylinder(h=wall+1,d=drain_diameter); }
