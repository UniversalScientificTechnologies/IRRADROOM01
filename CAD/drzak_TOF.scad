intersection(){
    translate([-59/2, 0, 0]) difference(){
        cylinder(d=55+4, h=10);
        cylinder(d=55, h=11);
    }
    cube(30, center=true);
}

difference(){
for(y = [-10, 10])
    translate([-3, y-5/2, 0])
        cube([13, 5, 2]);
for(y = [-10, 10])
    translate([15/2, y, -1])
        cylinder(d=3.2, h=10, $fn=20);
}