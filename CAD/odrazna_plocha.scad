
translate([-30/2, 8, 0]) cube([30,20, 2]);
translate([-15/2, 0, 0]) cube([15,20, 2]);
difference(){
translate([-15/2, 0, 0]) cube([15,2, 20]);
    
translate([0, 0, 13]) rotate([90, 0, 0])cylinder(d=6.3, h=10, center=true);
}