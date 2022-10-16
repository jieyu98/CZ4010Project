$(document).ready(function () {

    let length = 0;

    var h_direction = null;
    var v_direction = null;
    var cur_direction = null;
    var x = null;
    var y = null;

    var v_direction;

    $("#mouse-area").mousemove(function (e) {
        var offset = $(this).parent().offset();
        var cur_x = e.pageX - offset.left;
        var cur_y = e.pageY - offset.top;

        var x_bin = dec2bin(cur_x);
        var y_bin = dec2bin(cur_y);

        var msg = x_bin + y_bin;

        // Check if x and y are null (First loop)
        if (x == null && y == null) {
            x = cur_x;
            y = cur_y;

            console.log("first x"+x);
            return;
        }

        // Check if direction is null 
        if (h_direction == null) {
            // Assign direction by comparing cur_x, cur_y with previous x, y
            if (cur_x > x) {
                h_direction = "right";
            }
            else {
                h_direction = "left";
            }

            return;
        }

        // Now x, y and direction should no longer be null

        // Check if moving left or right
        if (cur_x > x) {
            cur_direction = "right";
        } 
        
        if (cur_x < x) {
            cur_direction = "left";
        }

        // Compare direction with h_direction, only update if different
        if (h_direction != cur_direction) {
            const output_area = document.getElementById('output-area');
            output_area.value += msg;
        }

        // Update x, y, and h_direction
        x = cur_x;
        y = cur_y;
        h_direction = cur_direction;

        return;
    });

    function dec2bin(dec) {
        return (dec >>> 0).toString(2);
    }

})


