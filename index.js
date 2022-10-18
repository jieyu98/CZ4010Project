$(document).ready(function () {

    let length = 0;

    var h_direction = null;
    var v_direction = null;
    var cur_h_direction = null;
    var cur_v_direction = null;
    var x = null;
    var y = null;

    var v_direction;

    $("#mouse-area").mousemove(function (e) {
        if (length >= 2048) {
            return;
        }

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

            return;
        }

        // Check if direction is null 
        if (h_direction == null && v_direction == null) {
            // Assign direction by comparing cur_x, cur_y with previous x, y
            if (cur_x > x) {
                h_direction = "right";
            }
            else {
                h_direction = "left";
            }

            if (cur_y > y) {
                v_direction = "down";
            }
            else {
                v_direction = "up";
            }

            return;
        }

        // Now x, y and direction should no longer be null

        // Check if moving left or right
        if (cur_x > x) {
            cur_h_direction = "right";
        }

        if (cur_x < x) {
            cur_h_direction = "left";
        }

        // Check if moving up or down
        if (cur_y > y) {
            cur_v_direction = "down";
        }

        if (cur_y < y) {
            cur_v_direction = "up";
        }

        //Compare current direction with old direction, only update if different
        if (h_direction != cur_h_direction || v_direction != cur_v_direction) {
            const output_area = document.getElementById('output-area');

            // Truncate msg if neccessary
            if (length + msg.length > 2048) {
                var temp = 2048 - length;
                msg = truncateString(msg, temp);
            }

            output_area.value += msg;
            length += msg.length;
        }

        // Update x, y, and h_direction
        x = cur_x;
        y = cur_y;
        h_direction = cur_h_direction;
        v_direction = cur_v_direction;

        // Update length
        $('#mouse-bits').text(length);

        return;
    });

    function dec2bin(dec) {
        return (dec >>> 0).toString(2);
    }

    function truncateString(str, num) {
        if (num > str.length) {
            return str;
        } else {
            str = str.substring(0, num);
            return str;
        }

    }

})


