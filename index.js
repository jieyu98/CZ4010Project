$(document).ready(function () {

    let length = 0;

    var h_direction = "right";
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

        // console.log(cur_x);

        if (x == null)
            x = cur_x;
        if (y == null)
            y = cur_y;
    
        if (h_direction == "right" && cur_x < x) {
            console.log(cur_x);
            // Display in textarea
            const output_area = document.getElementById('output-area');
            output_area.value += msg;

            length += msg.length;

            x = cur_x;
            y = cur_y;

            h_direction = "left";
            // console.log(length)
        }
        else if (h_direction == "left" && cur_x > x) {
            console.log(cur_x);
            // Display in textarea
            const output_area = document.getElementById('output-area');
            output_area.value += msg;

            length += msg.length;

            x = cur_x;
            y = cur_y;

            h_direction = "right";
            // console.log(length)
        }

        console.log(h_direction);

    });

    function dec2bin(dec) {
        return (dec >>> 0).toString(2);
    }

})


