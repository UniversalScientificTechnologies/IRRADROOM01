diry_x = 200;
diry_y = 65;

ramecek_x = 238;
ramecek_y = 145;
ramecek_d = 25;

M3_screw_diameter = 3.3;
M3_nut_diameter = 5.8;
M3_head_height = 2.8;

lcd_x = 178;
lcd_y = 113;

term_x = 199;
term_y = 140;
term_d = ramecek_d-3;
$fn=40;

difference(){
        
    minkowski(){
        translate([0, 0, (ramecek_d-2)/2]) cube([ramecek_x-4, ramecek_y-4, ramecek_d-2], center=true);
        union(){
            cylinder(d1=4, d2=1, h=2, $fn=50);
        }
    }
    
    for(x=[-0.5, 0.5]*diry_x, y=[-0.5, 0.5]*diry_y)
        translate([x, y, 0])
            union(){
                translate([0, 0, -0.1])
                    cylinder(d=M3_screw_diameter, h=ramecek_d-M3_head_height+0.1+0.15);
                translate([0, 0, ramecek_d-M3_head_height+0.3])
                    cylinder(d=M3_nut_diameter, h=10);
                translate([0, 0, ramecek_d-1+0.31])
                    cylinder(d1=M3_nut_diameter, d2=M3_nut_diameter+1, h=0.7);
            }
     cube([lcd_x, lcd_y, 50], center=true);
     translate([0, 0, ramecek_d+4.5])
        minkowski(){
            cube([lcd_x, lcd_y, ramecek_d/2-2], center=true);
            cylinder(d1=0, d2=2, h=1);
        }
     
     translate([0, 0, term_d/2]) cube([term_x, term_y, term_d], center=true);
     
     
     translate([0, 0, (ramecek_d-10)/2-0.1]) cube([ramecek_x-7, ramecek_y-7, ramecek_d-10], center=true);
     translate([0, 0, (ramecek_d-4)/2]) cube([ramecek_x-7, ramecek_y/3, ramecek_d-4], center=true);
     translate([0, 55, (ramecek_d-4)/2]) cube([ramecek_x-7, ramecek_y/5, ramecek_d-4], center=true);
     translate([0, -55, (ramecek_d-4)/2]) cube([ramecek_x-7, ramecek_y/5, ramecek_d-4], center=true);
}