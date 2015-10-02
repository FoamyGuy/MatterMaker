module box(length, width, thickness){
    difference(){
        cube([length, width, thickness]);
        translate([1, 1, 1]){
            cube([length - 2, width - 2, thickness]);
        }
    }
}

module lid(length, width, thickness){
    difference(){
    box(length, width, thickness);
        translate([12,3,-.01]){
            mirror([1,0,0]){
                rotate([0,0,90]){
                    linear_extrude(height=.4){
                        text("S S S", size=15);
                    }
                }
            }
        }
    }
}

box(30, 30, 30);

translate([2.5,0,10]){
    rotate([90,0,0]){
        linear_extrude(height=.6){
            text("");
        }
    }
}

//lid(37.9, 58, 5);
//lid(36.4, 56.4, 5);