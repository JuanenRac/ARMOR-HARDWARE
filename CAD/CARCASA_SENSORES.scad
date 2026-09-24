// ==========================================================
// A.R.M.O.R - BASE DE ESQUINA CON RANURAS VINCULADAS DINÁMICAMENTE
// ==========================================================
$fn = 50;

// ==========================================================
// 1. ESTRUCTURA BASE PRINCIPAL (X, Y, Z)
// ==========================================================
longitud_cara_x = 90;     // Extensión total pared posterior X (mm)
longitud_cara_y = 90;     // Extensión total pared posterior Y (mm)
altura_base_z   = 100;    // Altura total base principal Z (mm)
grosor_pared    = 5;      // Grosor de las paredes traseras en L (mm)

// ==========================================================
// 2. PARÁMETROS DE MARCO, ESCALONES Y TAPA
// ==========================================================

// --- 2.1. TECHO Y SUELO (VISERAS Z) ---
techo_z_offset  = 100;    // Posición Z de inicio del techo (mm)
techo_grosor_z  = 4;      // Grosor/Espesor Z del techo (mm)

suelo_z_offset  = -4;     // Posición Z de inicio del suelo (mm)
suelo_grosor_z  = 4;      // Grosor/Espesor Z del suelo (mm)

// --- 2.2. ESCALONES / MARCOS EXTERIORES DE RETENCIÓN (4 LADOS) ---
escalon_suelo_z   = 2.5;  // Pestaña inferior (suelo Z)
escalon_techo_z   = 2.5;  // Pestaña superior (techo Z)
escalon_lateral_x = 0.0;  // Pestaña exterior lateral derecha (solapa X)
escalon_lateral_y = 0.0;  // Pestaña exterior lateral izquierda (solapa Y)

// --- 2.3. TAPA FRONTAL (DIMENSIONES PRINCIPALES) ---
visera_chaflan  = 33;     // Tamaño del chaflán/corte diagonal de esquina (mm)
tapa_grosor     = 2;      // Grosor nominal de la tapa frontal (mm)
tapa_holgura_xy = 0.25;   // Holgura de deslizamiento perimetral en X/Y (mm)
tapa_holgura_z  = 0.25;   // Holgura vertical en Z (mm)

// --- 2.4. CONTROL DE RANURAS VINCULADO AUTOMÁTICAMENTE ---
// Se calculan solos según tapa_grosor + holgura:
ranura_prof_x    = tapa_grosor + tapa_holgura_xy;  
ranura_prof_y    = tapa_grosor + tapa_holgura_xy;  

// Penetración / Mordida dentro de las solapas laterales (mm):
ranura_mordida_x = 2.0;   // Profundidad del carril cortado en solapa lateral X
ranura_mordida_y = 2.0;   // Profundidad del carril cortado en solapa lateral Y

// --- 2.5. SOLAPAS LATERALES (X, Y) ---
solapa_x_grosor  = 4;     // Grosor total de la solapa lateral X (mm)
solapa_x_vuelo_y = 35;    // Saliente/Vuelo exterior cara X (mm)
solapa_x_z_start = -4;    // Inicio vertical Z de la solapa X (mm)
solapa_x_z_alto  = 108;   // Altura Z total de solapa X (mm)

solapa_y_grosor  = 4;     // Grosor total de la solapa lateral Y (mm)
solapa_y_vuelo_x = 35;    // Saliente/Vuelo exterior cara Y (mm)
solapa_y_z_start = -4;    // Inicio vertical Z de la solapa Y (mm)
solapa_y_z_alto  = 108;   // Altura Z total de solapa Y (mm)

distancia_separacion = 150; // Distancia de despiece en vista 0 (mm)

// ==========================================================
// 3. CONFIGURACIÓN DE ELEMENTOS Y TALADROS
// ==========================================================

// --- 3.1. TALADROS DE ANCLAJE A PARED (M8) ---
d_tornillo = 8.5;

t_paredX_1 = [75, -20, 15];
t_paredX_2 = [75, -20, 80];
t_paredY_1 = [-20, 75, 15];
t_paredY_2 = [-20, 75, 80];

// --- 3.2. PASACABLES LATERAL ---
pasacables_d = 15;
pasacables_pos = [-17.5, 88, 88];
pasacables_rot = [90, 0, 0];

// --- 3.3. RECTÁNGULO MACIZO SUPERIOR IZQUIERDO ---
rec_largo = 73;
rec_ancho = 21;
rec_grosor = 4;
rec_pos = [-17.5, 35, 100];
rec_rot = [0, 0, 0];

// --- 3.4. DRENAJES DE CONDENSACIÓN ---
d_drenaje = 4;
puntos_drenaje = [
    [20, -15, 0],
    [50, -15, 0],
    [75, -15, 0],
    [-15, 20, 0],
    [-15, 50, 0],
    [-15, 75, 0],
    [-12, -12, 0]
];

// --- 3.5. REBAJES LATERALES DE SENSORES ---
s1_reb_izq_alto = 15;  s1_reb_izq_ancho = 10;  s1_reb_izq_prof = 5;  s1_reb_izq_dist = 20;
s1_reb_der_alto = 15;  s1_reb_der_ancho = 10;  s1_reb_der_prof = 5;  s1_reb_der_dist = 20;

s2_reb_izq_alto = 15;  s2_reb_izq_ancho = 10;  s2_reb_izq_prof = 5;  s2_reb_izq_dist = 20;
s2_reb_der_alto = 15;  s2_reb_der_ancho = 10;  s2_reb_der_prof = 5;  s2_reb_der_dist = 20;

s3_reb_izq_alto = 15;  s3_reb_izq_ancho = 10;  s3_reb_izq_prof = 5;  s3_reb_izq_dist = 20;
s3_reb_der_alto = 15;  s3_reb_der_ancho = 10;  s3_reb_der_prof = 5;  s3_reb_der_dist = 20;

// ==========================================================
// 4. DIMENSIONES Y POSICIONES DE LOS SENSORES
// ==========================================================
sensor_ancho = 40;        
sensor_alto = 15;         

s1_x = 45;  s1_y = -5;  s1_z = 50;  s1_azimut = 30;   s1_inclinacion = 20;
s2_x = -5;  s2_y = 45;  s2_z = 50;  s2_azimut = -120; s2_inclinacion = 20;
s3_x = 0;   s3_y = 0;   s3_z = 50;  s3_azimut = -45;  s3_inclinacion = 20;  s3_profundidad = 28;

// ==========================================================
// MÓDULOS DE CONSTRUCCIÓN Y PERFILES 2D/3D
// ==========================================================

module taco_macizo(inc) {
    hull() {
        translate([0, 4, 0]) 
            cube([sensor_ancho + 12, 8, sensor_alto + 20], center=true);
        translate([0, -12, 0]) 
            rotate([inc, 0, 0]) 
            cube([sensor_ancho + 8, 2, sensor_alto + 12], center=true);
    }
}

module taco_macizo_central(inc, prof) {
    hull() {
        translate([0, prof/2, 0]) 
            cube([sensor_ancho + 12, prof, sensor_alto + 20], center=true);
        translate([0, -12, 0]) 
            rotate([inc, 0, 0]) 
            cube([sensor_ancho + 8, 2, sensor_alto + 12], center=true);
    }
}

module rebaje_unico(ancho, prof, alto, dist_x, inc) {
    translate([0, -12, 0])
        rotate([inc, 0, 0])
            translate([dist_x, -1 + prof/2, 0])
                cube([ancho, prof + 2, alto], center=true);
}

// PERFIL EXTERIOR TECHO/SUELO 2D
module perfil_marco_ext_2d() {
    cota_x = -solapa_x_vuelo_y - escalon_lateral_x;
    cota_y = -solapa_y_vuelo_x - escalon_lateral_y;
    
    polygon(points=[
        [grosor_pared, grosor_pared],
        [longitud_cara_x, grosor_pared],
        [longitud_cara_x, cota_x],
        [cota_y + visera_chaflan, cota_x],
        [cota_y, cota_x + visera_chaflan],
        [cota_y, longitud_cara_y],
        [grosor_pared, longitud_cara_y]
    ]);
}

// CANAL DE ALOJAMIENTO DE TAPA 2D (VACÍA SEGÚN GROSOR DE TAPA + HOLGURA)
module perfil_tapa_corte_2d() {
    k_off_x = ranura_prof_x * (sqrt(2) - 1);
    k_off_y = ranura_prof_y * (sqrt(2) - 1);

    p1_out = [longitud_cara_x - solapa_x_grosor + ranura_mordida_x, -solapa_x_vuelo_y];
    p2_out = [-solapa_y_vuelo_x + visera_chaflan, -solapa_x_vuelo_y];
    p3_out = [-solapa_y_vuelo_x, -solapa_x_vuelo_y + visera_chaflan];
    p4_out = [-solapa_y_vuelo_x, longitud_cara_y - solapa_y_grosor + ranura_mordida_y];

    p4_in  = [-solapa_y_vuelo_x + ranura_prof_y, longitud_cara_y - solapa_y_grosor + ranura_mordida_y];
    p3_in  = [-solapa_y_vuelo_x + ranura_prof_y, -solapa_x_vuelo_y + visera_chaflan + k_off_y];
    p2_in  = [-solapa_y_vuelo_x + visera_chaflan + k_off_x, -solapa_x_vuelo_y + ranura_prof_x];
    p1_in  = [longitud_cara_x - solapa_x_grosor + ranura_mordida_x, -solapa_x_vuelo_y + ranura_prof_x];

    polygon(points=[p1_out, p2_out, p3_out, p4_out, p4_in, p3_in, p2_in, p1_in]);
}

// PERFIL DE LA TAPA FRONTAL 2D (SOPORTA CUALQUIER GROSOR DINÁMICAMENTE)
module perfil_tapa_2d() {
    k_offset = tapa_grosor * (sqrt(2) - 1);
    
    p1_out = [longitud_cara_x - solapa_x_grosor, -solapa_x_vuelo_y];
    p2_out = [-solapa_y_vuelo_x + visera_chaflan, -solapa_x_vuelo_y];
    p3_out = [-solapa_y_vuelo_x, -solapa_x_vuelo_y + visera_chaflan];
    p4_out = [-solapa_y_vuelo_x, longitud_cara_y - solapa_y_grosor];
    
    p4_in  = [-solapa_y_vuelo_x + tapa_grosor, longitud_cara_y - solapa_y_grosor];
    p3_in  = [-solapa_y_vuelo_x + tapa_grosor, -solapa_x_vuelo_y + visera_chaflan + k_offset];
    p2_in  = [-solapa_y_vuelo_x + visera_chaflan + k_offset, -solapa_x_vuelo_y + tapa_grosor];
    p1_in  = [longitud_cara_x - solapa_x_grosor, -solapa_x_vuelo_y + tapa_grosor];
    
    polygon(points=[p1_out, p2_out, p3_out, p4_out, p4_in, p3_in, p2_in, p1_in]);
}

// ==========================================================
// PIEZA BASE PRINCIPAL
// ==========================================================

module soporte_exterior() {
    cota_x = -solapa_x_vuelo_y - escalon_lateral_x;
    cota_y = -solapa_y_vuelo_x - escalon_lateral_y;

    z_corte_inicio = suelo_z_offset + escalon_suelo_z; 
    z_corte_fin    = techo_z_offset + techo_grosor_z - escalon_techo_z;
    h_corte_total  = z_corte_fin - z_corte_inicio;

    difference() {
        union() {
            // Paredes L traseras principales
            cube([longitud_cara_x, grosor_pared, altura_base_z]);
            cube([grosor_pared, longitud_cara_y, altura_base_z]);
            
            // Soportes de sensores
            translate([s1_x, s1_y, s1_z]) rotate([0, 0, s1_azimut]) taco_macizo(s1_inclinacion);
            translate([s2_x, s2_y, s2_z]) rotate([0, 0, s2_azimut]) taco_macizo(s2_inclinacion);
            translate([s3_x, s3_y, s3_z]) rotate([0, 0, s3_azimut]) taco_macizo_central(s3_inclinacion, s3_profundidad);

            // Techo macizo (Z)
            translate([0, 0, techo_z_offset]) 
                linear_extrude(height = techo_grosor_z) 
                perfil_marco_ext_2d();

            // Suelo macizo (Z)
            translate([0, 0, suelo_z_offset]) 
                linear_extrude(height = suelo_grosor_z) 
                perfil_marco_ext_2d();

            // Solapa vertical lateral X
            translate([longitud_cara_x - solapa_x_grosor, cota_x, solapa_x_z_start])
                cube([solapa_x_grosor, solapa_x_vuelo_y + grosor_pared + escalon_lateral_x, solapa_x_z_alto]);

            // Solapa vertical lateral Y
            translate([cota_y, longitud_cara_y - solapa_y_grosor, solapa_y_z_start])
                cube([solapa_y_vuelo_x + grosor_pared + escalon_lateral_y, solapa_y_grosor, solapa_y_z_alto]);

            // Rectángulo macizo superior izquierdo
            translate(rec_pos)
                rotate(rec_rot)
                cube([rec_ancho, rec_largo, rec_grosor], center=true);
        }

        // --- SUBTRACCIONES Y VACÍADOS ---

        // Vaciado interior central
        translate([grosor_pared, grosor_pared, -20])
            cube([longitud_cara_x + 50, longitud_cara_y + 50, altura_base_z + 100]);

        // ALOJAMIENTO PERIMETRAL DE LA TAPA
        translate([0, 0, z_corte_inicio])
            linear_extrude(height = h_corte_total)
                perfil_tapa_corte_2d();

        // Taladros M8 de pared
        translate(t_paredX_1) rotate([-90, 0, 0]) cylinder(h=40, d=d_tornillo);
        translate(t_paredX_2) rotate([-90, 0, 0]) cylinder(h=40, d=d_tornillo);
        translate(t_paredY_1) rotate([0, 90, 0]) cylinder(h=40, d=d_tornillo);
        translate(t_paredY_2) rotate([0, 90, 0]) cylinder(h=40, d=d_tornillo);

        // Pasacables lateral
        translate(pasacables_pos)
            rotate(pasacables_rot)
            cylinder(h=40, d=pasacables_d, center=true);

        // Drenajes de suelo
        for (pt = puntos_drenaje) {
            translate([pt[0], pt[1], suelo_z_offset - 1 + pt[2]])
                cylinder(h = suelo_grosor_z + 2, d = d_drenaje);
        }

        // Rebajes de sensores
        translate([s1_x, s1_y, s1_z]) rotate([0, 0, s1_azimut]) {
            rebaje_unico(s1_reb_izq_ancho, s1_reb_izq_prof, s1_reb_izq_alto, -s1_reb_izq_dist, s1_inclinacion);
            rebaje_unico(s1_reb_der_ancho, s1_reb_der_prof, s1_reb_der_alto,  s1_reb_der_dist, s1_inclinacion);
        }

        translate([s2_x, s2_y, s2_z]) rotate([0, 0, s2_azimut]) {
            rebaje_unico(s2_reb_izq_ancho, s2_reb_izq_prof, s2_reb_izq_alto, -s2_reb_izq_dist, s2_inclinacion);
            rebaje_unico(s2_reb_der_ancho, s2_reb_der_prof, s2_reb_der_alto,  s2_reb_der_dist, s2_inclinacion);
        }

        translate([s3_x, s3_y, s3_z]) rotate([0, 0, s3_azimut]) {
            rebaje_unico(s3_reb_izq_ancho, s3_reb_izq_prof, s3_reb_izq_alto, -s3_reb_izq_dist, s3_inclinacion);
            rebaje_unico(s3_reb_der_ancho, s3_reb_der_prof, s3_reb_der_alto,  s3_reb_der_dist, s3_inclinacion);
        }
    }
}

// ==========================================================
// MÓDULO DE LA TAPA FRONTAL
// ==========================================================

module tapa_frontal() {
    z_inicio_tapa = suelo_z_offset + escalon_suelo_z + tapa_holgura_z;
    h_efectiva = (techo_z_offset + techo_grosor_z - escalon_techo_z) - z_inicio_tapa - tapa_holgura_z;
    
    translate([0, 0, z_inicio_tapa]) {
        linear_extrude(height = h_efectiva)
            perfil_tapa_2d();
    }
}

// ==========================================================
// SELECCIÓN DE VISTA / MODO DE EXPORTACIÓN
// ==========================================================
// 0 = Despiece (Tapa desplazada)
// 1 = Vista Ensamblada Completa
// 2 = Solo Pieza Base Principal
// 3 = Solo Tapa Frontal (para STL)

modo_vista = 0; 

if (modo_vista == 0) {
    soporte_exterior();
    translate([-distancia_separacion, -distancia_separacion, 0])
        color("Crimson", 0.85) tapa_frontal();

} else if (modo_vista == 1) {
    soporte_exterior();
    color("Crimson", 0.85) tapa_frontal();

} else if (modo_vista == 2) {
    soporte_exterior();

} else if (modo_vista == 3) {
    tapa_frontal();
}