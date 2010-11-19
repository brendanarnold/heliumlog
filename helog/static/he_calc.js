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
        boiled_off = (meter_after - meter_before)  / 0.757;
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
        var boiled_off = (meter_after - meter_before)  / 0.757;
        in_cryostat = taken - boiled_off;
        $('#he_in_cryostat').html(Math.round(in_cryostat));
    } else {
        $('#he_in_cryostat').html('N/A');
    } 
}

// Counts down the undo timeframe before changing the style
function undo_countdown() {
    // Have to hack this since flash doesn't allow HTML it seems
    var undo_flash = $('.undo');
    var url = undo_flash.html().split('|')[1];
    var stem = undo_flash.html().split('|')[0];
    var time_left = 30;
    undo_flash.html(stem + ' - <span id="timer">' + time_left + '</span> seconds left to <a href="' + url + '">Undo</a>');
    var timer_id = setInterval(function() {
        if (time_left > 0) {
            $('#timer').html(time_left);
        } else {
            clearInterval(timer_id);
            undo_flash.html(stem);
            undo_flash.addClass('ok');
            undo_flash.removeClass('undo');
        }
        time_left = time_left - 1;
    }, 1000);
}
$(document).ready(function() {
    calc_transfers();
    $("#log_transfer input").change(function(event) {
        calc_transfers();
    });
    // Now see if 'undo' is present
    if ($('.undo').length > 0) {
        undo_countdown();
    }
});
