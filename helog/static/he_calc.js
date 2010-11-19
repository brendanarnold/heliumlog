// Returns true if a string is a simple integer
function isInteger(s) {
    return /^\s*\d+\s*$/.exec(s);
}
// Calculate the boil off and the amount taken from the transport dewar
function calc_transfers() {
    // First to boil off
    var meter_before = $("#meter_before").val();
    var meter_after = $("#meter_after").val();
    meter_before = meter_before.replace('\.', '');
    meter_after = meter_after.replace('\.', '');
    var boiled_off = 0.0;
    if (isInteger(meter_before) && isInteger(meter_after)) {
        meter_before = parseInt(meter_before);
        meter_after = parseInt(meter_after);
        boiled_off = (meter_after - meter_before)  / 7.57;
        $('#he_boiled_off').html(Math.round(boiled_off));
    } else {
        $('#he_boiled_off').html('N/A');
    }
    // Now the litres taken
    var transport_dewar_before = $('#transport_dewar_before').val();
    var transport_dewar_after = $('#transport_dewar_after').val();
    var taken = 0.0;
    if (isInteger(transport_dewar_before) && 
      isInteger(transport_dewar_after)) {
        transport_dewar_before = parseInt(transport_dewar_before);
        transport_dewar_after = parseInt(transport_dewar_after);
        taken = transport_dewar_before - transport_dewar_after;
        $('#he_taken').html(Math.round(taken));
    } else {
        $('#he_taken').html('N/A');
    } 
    // Finally try calculating the amount extra in the cryostat
    var in_cryostat = 0.0;
    if (isInteger(transport_dewar_before) && 
      isInteger(transport_dewar_after) &&
      isInteger(meter_before) && 
      isInteger(meter_after)
    ) {
        transport_dewar_before = parseInt(transport_dewar_before);
        transport_dewar_after = parseInt(transport_dewar_after);
        meter_before = parseInt(meter_before);
        meter_after = parseInt(meter_after);
        var taken = transport_dewar_before - transport_dewar_after;
        var boiled_off = (meter_after - meter_before)  / 7.57;
        in_cryostat = taken - boiled_off;
        $('#he_in_cryostat').html(Math.round(in_cryostat));
    } else {
        $('#he_in_cryostat').html('N/A');
    } 
}

// Counts down the undo timeframe before changing the style
function undo_countdown() {
    var counter = $('#undo_counter');
    var undo_text = $('#undo_text');
    var undo_flash = $('.undo');
    var time_left = parseInt(counter.html());
    var timer_id = setInterval(function() {
        if (time_left > 0) {
            counter.html(time_left);
        } else {
            clearInterval(timer_id);
            undo_text.remove();
            undo_flash.addClass('ok');
            undo_flash.removeClass('undo');
        }
        time_left = time_left - 1;
    }, 1000);
}

// Setup stuff that happens on load
$(document).ready(function() {
    calc_transfers();
    $("#log_transfer input").change(function(event) {
        calc_transfers();
    });
    // Now see if 'undo' is present - do some neat javascript stuff
    if ($('.undo').length > 0) {
        undo_countdown();
    }
});
