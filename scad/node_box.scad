// ==========================================================
// A.R.M.O.R - PARAMETRIC BOX FOR THE NODES THAT ARE NOT THE RADAR
// A screw-down box with a lid for the solar, electrical and alarm nodes: the walls, the posts for the board, the holes for the cables, a vent and a pocket for a tamper
// micro-switch under the lid. The lid has a ring-shaped lip that goes inside the walls and leaves the four corner posts free, so it rests on the rim of the box and on the posts.
//
// There is no preset for the touch panel: the Waveshare ESP32-S3-Touch-LCD-7C-BOX comes in its own enclosure, and a window for the 7-inch screen has to be cut from its
// official drawing. There is no battery bay either: the alarm node is powered over PoE from a switch behind a UPS, and the siren has its own battery (see ARMOR-NODE-ALARM).
//
// STATUS: a starting point. The three presets are checked by the asserts below (the board fits, the cable holes fit, the lid clears the posts), but none has been printed, and
// the sizes of the boards are the ones from their data sheets, not measured: check every number against the real board and print a first copy in draft quality before anything
// is mounted in it. It is not IP rated, and it is not a mains enclosure: the electrical node must not be put in it with mains voltage inputs wired (see docs/DESIGN_INPUTS.md).
// Use:  openscad -D 'part="box"' -D 'preset="alarm"' -o node_box_alarm.stl node_box.scad      (part: "box", "lid" or "both"; preset: "solar", "electrical", "alarm")
// ==========================================================
$fn = 48;
part   = "both";
preset = "solar";

// ---- what each preset is: the inside size, the board size and the cable glands
// The board sizes: Waveshare ESP32-S3-ETH about 66 x 53 mm; the base board of the electrical and alarm nodes is larger (to be measured). Glands are listed as [x from the left wall, diameter].
function inside(p)      = p == "solar" ? [110, 80, 45] : p == "electrical" ? [140, 100, 50] : [150, 110, 60];
function board(p)       = p == "solar" ? [66, 53] : [120, 80];
function glands(p)      = p == "solar" ? [[20, 12], [45, 12], [70, 12], [95, 12]] : p == "electrical" ? [[20, 14], [50, 14], [80, 14], [110, 14]] : [[25, 14], [60, 14], [95, 14], [130, 14]];

wall    = 3;        // wall thickness (mm)
lid_t   = 3;        // lid thickness (mm)
post_d  = 7;        // the posts for the board: diameter and height
post_h  = 6;
screw_d = 3.2;      // the screws of the lid and of the board (M3 self-tapping into the posts)
clear   = 0.3;      // play between the lid and the box
lip_w   = 1.6;      // the width of the ring-shaped lip of the lid
post_cap = 9;       // the diameter of the posts of the lid screws
vent    = true;     // a row of slots in the lid so the heat can leave (the ESP32 and the relays warm the inside)

cav = inside(preset);
bd  = board(preset);

// What would make a print useless is caught when the file is rendered, not on the printer.
assert(preset == "solar" || preset == "electrical" || preset == "alarm", "preset must be solar, electrical or alarm");
assert(part == "box" || part == "lid" || part == "both", "part must be box, lid or both");
assert(bd[0] + 2 * 4 + 2 * post_d / 2 <= cav[0] && bd[1] + 2 * 4 + 2 * post_d / 2 <= cav[1], "the board and its posts do not fit inside the box");
assert(lip_w >= 1.2 && lip_w <= 3, "the lip of the lid must be a ring between 1.2 and 3 mm wide");
assert(len([for (g = glands(preset)) if (g[0] - g[1] / 2 < 9 || g[0] + g[1] / 2 > cav[0] - 9) 1]) == 0, "a cable hole is cut by a wall or a corner post");
assert(len([for (g = glands(preset)) if (g[1] > cav[2] - 2) 1]) == 0, "a cable hole is taller than the inside of the box");

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
    // the posts of the lid screws, in the four corners; they reach the rim of the walls, and the lid rests on both (its lip is a ring with a gap for each post)
    for (x = [wall + 4, ow - wall - 4], y = [wall + 4, od - wall - 4]) difference() {
        translate([x, y, wall]) cylinder(d = post_cap, h = oh - wall);   // 9 mm, so the post overlaps the walls by 0.5 mm instead of only touching them
        translate([x, y, oh - 12]) cylinder(d = screw_d - 0.4, h = 13);
    }
    // the posts of the board, on a grid that fits a board of the size of the preset (replace the holes with the real ones)
    bx = wall + (cav[0] - bd[0]) / 2;  by = wall + (cav[1] - bd[1]) / 2;
    for (x = [4, bd[0] - 4], y = [4, bd[1] - 4]) difference() {
        translate([bx + x, by + y, wall]) cylinder(d = post_d, h = post_h);
        translate([bx + x, by + y, wall + 1]) cylinder(d = screw_d - 0.4, h = post_h);
    }
}

module lid() {
    ow = cav[0] + 2 * wall;  od = cav[1] + 2 * wall;
    difference() {
        union() {
            rounded(ow, od, lid_t);
            // a ring-shaped lip that goes inside the box and keeps the lid from sliding; the four posts of the lid screws have their own gap in it
            difference() {
                translate([wall + clear, wall + clear, lid_t]) rounded(cav[0] - 2 * clear, cav[1] - 2 * clear, 2, 1.5);
                translate([wall + clear + lip_w, wall + clear + lip_w, lid_t - 1]) rounded(cav[0] - 2 * clear - 2 * lip_w, cav[1] - 2 * clear - 2 * lip_w, 4, 1);
                for (x = [wall + 4, ow - wall - 4], y = [wall + 4, od - wall - 4]) translate([x, y, lid_t - 1]) cylinder(d = post_cap + 2 * clear, h = 4);
            }
        }
        for (x = [wall + 4, ow - wall - 4], y = [wall + 4, od - wall - 4]) translate([x, y, -1]) cylinder(d = screw_d, h = lid_t + 4);
        if (vent) for (i = [0 : 7]) translate([ow / 2 - 30 + i * 8, od / 2 - 15, -1]) cube([3, 30, lid_t + 4]);
    }
    // a pocket under the lid for a micro-switch that opens when the lid is taken off (the tamper input of the node): two walls that hold a switch of 20 x 10 x 6 mm
    // (measure the real one), just inside the front lip
    for (dy = [0, 1.5 + 10.4]) translate([ow / 2 - 10, wall + clear + lip_w + 0.6 + dy, lid_t]) cube([20, 1.5, 6]);
}

if (part == "box" || part == "both") box();
if (part == "lid" || part == "both") translate([0, cav[1] + 2 * wall + 15, 0]) lid();
