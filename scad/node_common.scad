// ==========================================================
// A.R.M.O.R - WHAT THE ENCLOSURES OF THE NODES SHARE
// Included by node_box.scad (solar, electrical and alarm nodes) and by node_enclosure_radar.scad, so that a number two enclosures need to agree on is written once.
//
// The cable glands are the ones a shop sells, not a diameter chosen to look right: the hole is the thread of the gland plus a small play, and the sizes below are the major
// diameters of the common plastic glands (PG7 12.5 mm, M12x1.5 12 mm, PG9 15.2 mm, M16x1.5 16 mm). Check the thread of the gland you buy against these numbers before cutting.
// STATUS: a starting point; nothing here has been printed or measured.
// ==========================================================

// ---- shell of the box of the nodes that are not the radar (mm)
wall   = 3;        // wall thickness
lid_t  = 3;        // lid thickness
clear  = 0.3;      // play between the lid and the box

// ---- cable glands: the thread (major diameter) of each size, and the play of the hole around it
gland_pg7   = 12.5;
gland_m12   = 12;
gland_pg9   = 15.2;
gland_m16   = 16;
gland_play  = 0.4;   // the hole is this much wider than the thread
function gland_hole(thread) = thread + gland_play;
