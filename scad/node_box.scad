// ==========================================================
// A.R.M.O.R - PARAMETRIC BOX FOR THE NODES THAT ARE NOT THE RADAR
// A screw-down box with a lid for the solar, electrical and alarm nodes (and a frame for the HMI): the walls, the posts for the board, the holes for the cables, a vent, a
// pocket for a tamper micro-switch under the lid and, for the alarm panel, a bay for the backup battery.
//
// STATUS: a starting point. All four presets render as valid solids, but none has been printed, and the sizes of the boards are the ones from their data sheets, not
// measured: check every number against the real board and print a first copy in draft quality before anything is mounted in it. It is not IP rated.
// Use:  openscad -D 'part="box"' -D 'preset="alarm"' -o node_box_alarm.stl node_box.scad      (part: "box", "lid" or "both"; preset: "solar", "electrical", "alarm", "hmi")
// ==========================================================
$fn = 48;
part   = "both";
preset = "solar";

// ---- what each preset is: [inside width, inside depth, inside height, board width, board depth, hole pitch x, hole pitch y, battery bay (0 = none), cable glands]
// The board sizes: Waveshare ESP32-S3-ETH about 66 x 53 mm; the base board of the electrical and alarm nodes is larger (to be measured). Glands are listed as [x from the left wall, diameter].
function inside(p)      = p == "solar" ? [110, 80, 45] : p == "electrical" ? [140, 100, 50] : p == "alarm" ? [150, 110, 60] : [190, 120, 28];
function board(p)       = p == "solar" ? [66, 53] : p == "electrical" ? [120, 80] : p == "alarm" ? [120, 80] : [170, 100];
function battery(p)     = p == "alarm" ? [70, 48, 100] : [0, 0, 0];      // a 12 V 7 Ah lead battery is about 151 x 65 x 94: change it to the one that is used
function glands(p)      = p == "solar" ? [[20, 12], [45, 12], [70, 12], [95, 12]] : p == "electrical" ? [[20, 14], [50, 14], [80, 14], [110, 14]] : p == "alarm" ? [[25, 14], [60, 14], [95, 14], [130, 14]] : [[30, 10]];

wall    = 3;        // wall thickness (mm)
lid_t   = 3;        // lid thickness (mm)
post_d  = 7;        // the posts for the board: diameter and height
post_h  = 6;
screw_d = 3.2;      // the screws of the lid and of the board (M3 self-tapping into the posts)
clear   = 0.3;      // play between the lid and the box
vent    = true;     // a row of slots in the lid so the heat can leave (the ESP32 and the relays warm the inside)

cav = inside(preset);
bd  = board(preset);
bat = battery(preset);

module rounded(w, d, h, r = 3) {
    hull() for (x = [r, w - r], y = [r, d - r]) translate([x, y, 0]) cylinder(r = r, h = h);
}

module box() {
    ow = cav[0] + 2 * wall;  od = cav[1] + 2 * wall;  oh = cav[2] + wall;
    difference() {
        rounded(ow, od, oh);
        translate([wall, wall, wall]) rounded(cav[0], cav[1], cav[2] + 1, 1.5);
        // the holes for the cables, on the front wall, at mid height
        for (g = glands(preset)) translate([wall + g[0], -1, wall + cav[2] / 2]) rotate([-90, 0, 0]) cylinder(d = g[1], h = wall + 2);
        // the four corner holes for the lid screws are pilot holes in the corner posts
        for (x = [wall + 4, ow - wall - 4], y = [wall + 4, od - wall - 4]) translate([x, y, oh - 12]) cylinder(d = screw_d - 0.4, h = 13);
        // a notch for the label (the serial number and the set-up code of the board)
        translate([ow - 40, od - 0.6, oh / 2 - 8]) cube([34, 1, 16]);
    }
    // the posts of the lid screws, in the four corners
    for (x = [wall + 4, ow - wall - 4], y = [wall + 4, od - wall - 4]) difference() {
        translate([x, y, wall]) cylinder(d = 9, h = oh - wall);   // 9 mm, so the post overlaps the walls by 0.5 mm instead of only touching them
        translate([x, y, oh - 12]) cylinder(d = screw_d - 0.4, h = 13);
    }
    // the posts of the board, on a grid that fits a board of the size of the preset (replace the holes with the real ones)
    bx = wall + (cav[0] - bd[0]) / 2;  by = wall + (cav[1] - bd[1]) / 2;
    for (x = [4, bd[0] - 4], y = [4, bd[1] - 4]) difference() {
        translate([bx + x, by + y, wall]) cylinder(d = post_d, h = post_h);
        translate([bx + x, by + y, wall + 1]) cylinder(d = screw_d - 0.4, h = post_h);
    }
    // the bay of the backup battery of the alarm panel: two walls that keep it from sliding
    if (bat[0] > 0) {
        translate([wall + 3, wall + 3, wall]) cube([2, bat[1], 26]);
        translate([wall + 3 + bat[0], wall + 3, wall]) cube([2, bat[1], 26]);
    }
}

module lid() {
    ow = cav[0] + 2 * wall;  od = cav[1] + 2 * wall;
    difference() {
        union() {
            rounded(ow, od, lid_t);
            // a lip that goes inside the box and keeps the lid from sliding
            translate([wall + clear, wall + clear, lid_t]) rounded(cav[0] - 2 * clear, cav[1] - 2 * clear, 2, 1.5);
        }
        for (x = [wall + 4, ow - wall - 4], y = [wall + 4, od - wall - 4]) translate([x, y, -1]) cylinder(d = screw_d, h = lid_t + 4);
        if (vent) for (i = [0 : 7]) translate([ow / 2 - 30 + i * 8, od / 2 - 15, -1]) cube([3, 30, lid_t + 4]);
    }
    // a pocket under the lid for a micro-switch that opens when the lid is taken off (the tamper input of the node): 20 x 10 x 6 mm, near the front edge
    translate([ow / 2 - 10, wall + 1, lid_t]) cube([20, 3, 6]);
}

if (part == "box" || part == "both") box();
if (part == "lid" || part == "both") translate([0, cav[1] + 2 * wall + 15, 0]) lid();
