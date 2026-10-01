// ==========================================================
// A.R.M.O.R - CORNER BASE WITH DYNAMICALLY LINKED SLOTS
// ==========================================================
$fn = 50;

// ==========================================================
// 1. MAIN BASE STRUCTURE (X, Y, Z)
// ==========================================================
face_length_x = 90;       // Total extension of back wall X (mm)
face_length_y = 90;       // Total extension of back wall Y (mm)
base_height_z  = 100;     // Total height of main base Z (mm)
wall_thickness  = 5;      // Thickness of L-shaped back walls (mm)

// ==========================================================
// 2. FRAME, STEPS, AND COVER PARAMETERS
// ==========================================================

// --- 2.1. CEILING AND FLOOR (Z VISORS) ---
ceiling_z_offset  = 100;  // Z start position of the ceiling (mm)
ceiling_thickness_z  = 4; // Z thickness/depth of the ceiling (mm)

floor_z_offset  = -4;     // Z start position of the floor (mm)
floor_thickness_z  = 4;   // Z thickness/depth of the floor (mm)

// --- 2.2. STEPS / OUTER RETAINING FRAMES (4 SIDES) ---
floor_step_z   = 2.5;     // Bottom tab (floor Z)
ceiling_step_z   = 2.5;   // Top tab (ceiling Z)
lateral_step_x = 0.0;     // Right lateral outer tab (overlap X)
lateral_step_y = 0.0;     // Left lateral outer tab (overlap Y)

// --- 2.3. FRONT COVER (MAIN DIMENSIONS) ---
visor_chamfer  = 33;      // Corner diagonal cut/chamfer size (mm)
cover_thickness     = 2;  // Nominal thickness of the front cover (mm)
cover_clearance_xy = 0.25;// Perimeter sliding clearance in X/Y (mm)
cover_clearance_z  = 0.25;// Vertical clearance in Z (mm)

// --- 2.4. AUTOMATICALLY LINKED SLOT CONTROL ---
// Automatically calculated based on cover_thickness + clearance:
slot_depth_x    = cover_thickness + cover_clearance_xy;  
slot_depth_y    = cover_thickness + cover_clearance_xy;  

// Penetration / Bite inside lateral flaps (mm):
slot_bite_x = 2.0;        // Cut rail depth in lateral flap X
slot_bite_y = 2.0;        // Cut rail depth in lateral flap Y

// --- 2.5. LATERAL FLAPS (X, Y) ---
flap_x_thickness  = 4;    // Total thickness of lateral flap X (mm)
flap_x_overhang_y = 35;   // Outer projection/overhang face X (mm)
flap_x_z_start = -4;      // Vertical Z start of flap X (mm)
flap_x_z_height  = 108;   // Total Z height of flap X (mm)

flap_y_thickness  = 4;    // Total thickness of lateral flap Y (mm)
flap_y_overhang_x = 35;   // Outer projection/overhang face Y (mm)
flap_y_z_start = -4;      // Vertical Z start of flap Y (mm)
flap_y_z_height  = 108;   // Total Z height of flap Y (mm)

separation_distance = 150;// Disassembly distance in view mode 0 (mm)

// ==========================================================
// 3. ELEMENT CONFIGURATION AND DRILL HOLES
// ==========================================================

// --- 3.1. WALL ANCHOR DRILL HOLES (M8) ---
screw_d = 8.5;

wallX_hole_1 = [75, -20, 15];
wallX_hole_2 = [75, -20, 80];
wallY_hole_1 = [-20, 75, 15];
wallY_hole_2 = [-20, 75, 80];

// --- 3.2. LATERAL CABLE GLAND / PASSTHROUGH ---
cable_gland_d = 15;
cable_gland_pos = [-17.5, 88, 88];
cable_gland_rot = [90, 0, 0];

// --- 3.3. TOP LEFT SOLID RECTANGLE ---
rect_length = 73;
rect_width = 21;
rect_thickness = 4;
rect_pos = [-17.5, 35, 100];
rect_rot = [0, 0, 0];

// --- 3.4. CONDENSATION DRAINAGE ---
drain_d = 4;
drain_points = [
    [20, -15, 0],
    [50, -15, 0],
    [75, -15, 0],
    [-15, 20, 0],
    [-15, 50, 0],
    [-15, 75, 0],
    [-12, -12, 0]
];

// --- 3.5. LATERAL SENSOR RECESSES ---
s1_recess_left_height = 15;  s1_recess_left_width = 10;  s1_recess_left_depth = 5;  s1_recess_left_dist = 20;
s1_recess_right_height = 15; s1_recess_right_width = 10; s1_recess_right_depth = 5; s1_recess_right_dist = 20;

s2_recess_left_height = 15;  s2_recess_left_width = 10;  s2_recess_left_depth = 5;  s2_recess_left_dist = 20;
s2_recess_right_height = 15; s2_recess_right_width = 10; s2_recess_right_depth = 5; s2_recess_right_dist = 20;

s3_recess_left_height = 15;  s3_recess_left_width = 10;  s3_recess_left_depth = 5;  s3_recess_left_dist = 20;
s3_recess_right_height = 15; s3_recess_right_width = 10; s3_recess_right_depth = 5; s3_recess_right_dist = 20;

// ==========================================================
// 4. SENSOR DIMENSIONS AND POSITIONS
// ==========================================================
sensor_width = 40;        
sensor_height = 15;         

s1_x = 45;  s1_y = -5;  s1_z = 50;  s1_azimuth = 30;   s1_tilt = 20;
s2_x = -5;  s2_y = 45;  s2_z = 50;  s2_azimuth = -120; s2_tilt = 20;
s3_x = 0;   s3_y = 0;   s3_z = 50;  s3_azimuth = -45;  s3_tilt = 20;  s3_depth = 28;

// ==========================================================
// CONSTRUCTION MODULES AND 2D/3D PROFILES
// ==========================================================

module solid_block(tilt) {
    hull() {
        translate([0, 4, 0]) 
            cube([sensor_width + 12, 8, sensor_height + 20], center=true);
        translate([0, -12, 0]) 
            rotate([tilt, 0, 0]) 
            cube([sensor_width + 8, 2, sensor_height + 12], center=true);
    }
}

module central_solid_block(tilt, depth) {
    hull() {
        translate([0, depth/2, 0]) 
            cube([sensor_width + 12, depth, sensor_height + 20], center=true);
        translate([0, -12, 0]) 
            rotate([tilt, 0, 0]) 
            cube([sensor_width + 8, 2, sensor_height + 12], center=true);
    }
}

module single_recess(width, depth, height, dist_x, tilt) {
    translate([0, -12, 0])
        rotate([tilt, 0, 0])
            translate([dist_x, -1 + depth/2, 0])
                cube([width, depth + 2, height], center=true);
}

// 2D OUTER CEILING/FLOOR PROFILE
module outer_frame_profile_2d() {
    dimension_x = -flap_x_overhang_y - lateral_step_x;
    dimension_y = -flap_y_overhang_x - lateral_step_y;
    
    polygon(points=[
        [wall_thickness, wall_thickness],
        [face_length_x, wall_thickness],
        [face_length_x, dimension_x],
        [dimension_y + visor_chamfer, dimension_x],
        [dimension_y, dimension_x + visor_chamfer],
        [dimension_y, face_length_y],
        [wall_thickness, face_length_y]
    ]);
}

// 2D COVER HOUSING CHANNEL (HOLLOW LAYER BASED ON COVER THICKNESS + CLEARANCE)
module cover_cut_profile_2d() {
    k_off_x = slot_depth_x * (sqrt(2) - 1);
    k_off_y = slot_depth_y * (sqrt(2) - 1);

    p1_out = [face_length_x - flap_x_thickness + slot_bite_x, -flap_x_overhang_y];
    p2_out = [-flap_y_overhang_x + visor_chamfer, -flap_x_overhang_y];
    p3_out = [-flap_y_overhang_x, -flap_x_overhang_y + visor_chamfer];
    p4_out = [-flap_y_overhang_x, face_length_y - flap_y_thickness + slot_bite_y];

    p4_in  = [-flap_y_overhang_x + slot_depth_y, face_length_y - flap_y_thickness + slot_bite_y];
    p3_in  = [-flap_y_overhang_x + slot_depth_y, -flap_x_overhang_y + visor_chamfer + k_off_y];
    p2_in  = [-flap_y_overhang_x + visor_chamfer + k_off_x, -flap_x_overhang_y + slot_depth_x];
    p1_in  = [face_length_x - flap_x_thickness + slot_bite_x, -flap_x_overhang_y + slot_depth_x];

    polygon(points=[p1_out, p2_out, p3_out, p4_out, p4_in, p3_in, p2_in, p1_in]);
}

// 2D FRONT COVER PROFILE (DYNAMICALLY SUPPORTS ANY THICKNESS)
module cover_profile_2d() {
    k_offset = cover_thickness * (sqrt(2) - 1);
    
    p1_out = [face_length_x - flap_x_thickness, -flap_x_overhang_y];
    p2_out = [-flap_y_overhang_x + visor_chamfer, -flap_x_overhang_y];
    p3_out = [-flap_y_overhang_x, -flap_x_overhang_y + visor_chamfer];
    p4_out = [-flap_y_overhang_x, face_length_y - flap_y_thickness];
    
    p4_in  = [-flap_y_overhang_x + cover_thickness, face_length_y - flap_y_thickness];
    p3_in  = [-flap_y_overhang_x + cover_thickness, -flap_x_overhang_y + visor_chamfer + k_offset];
    p2_in  = [-flap_y_overhang_x + visor_chamfer + k_offset, -flap_x_overhang_y + cover_thickness];
    p1_in  = [face_length_x - flap_x_thickness, -flap_x_overhang_y + cover_thickness];
    
    polygon(points=[p1_out, p2_out, p3_out, p4_out, p4_in, p3_in, p2_in, p1_in]);
}

// ==========================================================
// MAIN BASE PIECE
// ==========================================================

module outer_support() {
    dimension_x = -flap_x_overhang_y - lateral_step_x;
    dimension_y = -flap_y_overhang_x - lateral_step_y;

    cut_start_z = floor_z_offset + floor_step_z; 
    cut_end_z    = ceiling_z_offset + ceiling_thickness_z - ceiling_step_z;
    total_cut_h  = cut_end_z - cut_start_z;

    difference() {
        union() {
            // Main back L-shaped walls
            cube([face_length_x, wall_thickness, base_height_z]);
            cube([wall_thickness, face_length_y, base_height_z]);
            
            // Sensor supports
            translate([s1_x, s1_y, s1_z]) rotate([0, 0, s1_azimuth]) solid_block(s1_tilt);
            translate([s2_x, s2_y, s2_z]) rotate([0, 0, s2_azimuth]) solid_block(s2_tilt);
            translate([s3_x, s3_y, s3_z]) rotate([0, 0, s3_azimuth]) central_solid_block(s3_tilt, s3_depth);

            // Solid ceiling (Z)
            translate([0, 0, ceiling_z_offset]) 
                linear_extrude(height = ceiling_thickness_z) 
                outer_frame_profile_2d();

            // Solid floor (Z)
            translate([0, 0, floor_z_offset]) 
                linear_extrude(height = floor_thickness_z) 
                outer_frame_profile_2d();

            // Vertical lateral flap X
            translate([face_length_x - flap_x_thickness, dimension_x, flap_x_z_start])
                cube([flap_x_thickness, flap_x_overhang_y + wall_thickness + lateral_step_x, flap_x_z_height]);

            // Vertical lateral flap Y
            translate([dimension_y, face_length_y - flap_y_thickness, flap_y_z_start])
                cube([flap_y_overhang_x + wall_thickness + lateral_step_y, flap_y_thickness, flap_y_z_height]);

            // Top left solid rectangle
            translate(rect_pos)
                rotate(rect_rot)
                cube([rect_width, rect_length, rect_thickness], center=true);
        }

        // --- SUBTRACTIONS AND HOLLOWING ---

        // Central inner hollowing
        translate([wall_thickness, wall_thickness, -20])
            cube([face_length_x + 50, face_length_y + 50, base_height_z + 100]);

        // COVER PERIMETER HOUSING
        translate([0, 0, cut_start_z])
            linear_extrude(height = total_cut_h)
                cover_cut_profile_2d();

        // Wall M8 drill holes
        translate(wallX_hole_1) rotate([-90, 0, 0]) cylinder(h=40, d=screw_d);
        translate(wallX_hole_2) rotate([-90, 0, 0]) cylinder(h=40, d=screw_d);
        translate(wallY_hole_1) rotate([0, 90, 0]) cylinder(h=40, d=screw_d);
        translate(wallY_hole_2) rotate([0, 90, 0]) cylinder(h=40, d=screw_d);

        // Lateral cable gland / passthrough
        translate(cable_gland_pos)
            rotate(cable_gland_rot)
            cylinder(h=40, d=cable_gland_d, center=true);

        // Floor drains
        for (pt = drain_points) {
            translate([pt[0], pt[1], floor_z_offset - 1 + pt[2]])
                cylinder(h = floor_thickness_z + 2, d = drain_d);
        }

        // Sensor recesses
        translate([s1_x, s1_y, s1_z]) rotate([0, 0, s1_azimuth]) {
            single_recess(s1_recess_left_width, s1_recess_left_depth, s1_recess_left_height, -s1_recess_left_dist, s1_tilt);
            single_recess(s1_recess_right_width, s1_recess_right_depth, s1_recess_right_height,  s1_recess_right_dist, s1_tilt);
        }

        translate([s2_x, s2_y, s2_z]) rotate([0, 0, s2_azimuth]) {
            single_recess(s2_recess_left_width, s2_recess_left_depth, s2_recess_left_height, -s2_recess_left_dist, s2_tilt);
            single_recess(s2_recess_right_width, s2_recess_right_depth, s2_recess_right_height,  s2_recess_right_dist, s2_tilt);
        }

        translate([s3_x, s3_y, s3_z]) rotate([0, 0, s3_azimuth]) {
            single_recess(s3_recess_left_width, s3_recess_left_depth, s3_recess_left_height, -s3_recess_left_dist, s3_tilt);
            single_recess(s3_recess_right_width, s3_recess_right_depth, s3_recess_right_height,  s3_recess_right_dist, s3_tilt);
        }
    }
}

// ==========================================================
// FRONT COVER MODULE
// ==========================================================

module front_cover() {
    cover_start_z = floor_z_offset + floor_step_z + cover_clearance_z;
    effective_h = (ceiling_z_offset + ceiling_thickness_z - ceiling_step_z) - cover_start_z - cover_clearance_z;
    
    translate([0, 0, cover_start_z]) {
        linear_extrude(height = effective_h)
            cover_profile_2d();
    }
}

// ==========================================================
// VIEW SELECTION / EXPORT MODE
// ==========================================================
// 0 = Exploded view (Cover displaced)
// 1 = Full Assembled View
// 2 = Main Base Piece Only
// 3 = Front Cover Only (for STL)

view_mode = 0; 

if (view_mode == 0) {
    outer_support();
    translate([-separation_distance, -separation_distance, 0])
        color("Crimson", 0.85) front_cover();

} else if (view_mode == 1) {
    outer_support();
    color("Crimson", 0.85) front_cover();

} else if (view_mode == 2) {
    outer_support();

} else if (view_mode == 3) {
    front_cover();
}