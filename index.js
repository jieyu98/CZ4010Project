$(document).ready(function () {

    let length = 0;

    var h_direction = null;
    var v_direction = null;
    var cur_h_direction = null;
    var cur_v_direction = null;
    var x = null;
    var y = null;

    var v_direction;

    var mouse_bits = "";
    var padded_cloud_str = "";

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
            const output_area = document.getElementById('mouse-output');

            // Truncate msg if neccessary
            if (length + msg.length > 2048) {
                var temp = 2048 - length;
                msg = truncateString(msg, temp);
            }

            mouse_bits += msg;
            output_area.value = mouse_bits;
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

    // Call Weather API
    $('#weather-btn').click(function () {
        $('#spinner-div').show(); //Load button clicked show spinner
        const output_area = document.getElementById('weather-output');
        output_area.value = "";

        //Send the AJAX call to the server
        $.ajax({
            'url': 'https://weather-csprng.jieyu98.repl.co/api/csprng',
            'type': 'GET',
            'success': function (data) {
                padded_cloud_str = data[1]; // Store padded
                output_area.value = data[0]; // Display unpadded
            },
            complete: function () {
                $('#spinner-div').hide();//Request is complete so hide spinner
            }
        });
    });

    $('#shuffle-btn').click(function () {
        if (document.getElementById("mouse-output").value.length != "2048") {
            alert("Please finish generating the mouse bits.");
            return;
        } else if (document.getElementById("weather-output").value == "") {
            alert("Please retrieve the weather bits.");
            return;
        }

        $('#spinner-div-2').show(); //Load button clicked show spinner
        const output_area = document.getElementById('shuffle-output');
        const prime_p_area = document.getElementById('prime-p-output');
        const prime_q_area = document.getElementById('prime-q-output');
        output_area.value = "";

        //Send the AJAX call to the server
        $.ajax({
            'url': 'https://weather-csprng.jieyu98.repl.co/api/csprng',
            'type': 'POST',
            'data': {
                'mouse_bits': mouse_bits, // Send mouse bits
                'padded_cloud_str': padded_cloud_str // Send padded
            },
            'success': function (data) {
                output_area.value = data[0];
                prime_p_area.value = data[1];
                prime_q_area.value = data[2];
            },
            complete: function () {
                $('#spinner-div-2').hide();//Request is complete so hide spinner
            }
        });
    });

    $('#get-prime-btn').click(function () {
        const prime_area = document.getElementById('prime-area');
        if (prime_area.style.display == 'block')
            prime_area.style.display = 'none';
        else
            prime_area.style.display = 'block';

    });

    $('#copy-p-btn').click(function () {        
        // Get the text field
        var p_text = document.getElementById("prime-p-output");

        // Select the text field
        p_text.select();
        navigator.clipboard.writeText(p_text.value);
    });

    $('#copy-q-btn').click(function () {        
        // Get the text field
        var q_text = document.getElementById("prime-q-output");

        // Select the text field
        q_text.select();
        navigator.clipboard.writeText(q_text.value);
    });
})


