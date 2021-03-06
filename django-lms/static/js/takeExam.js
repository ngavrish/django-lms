$(document).ready(function() {		

	function lockExam() {	
		var input = prompt("Enter exam password:");
		if (input == password) {
			return $(".hidden").removeClass("hidden");
		}
		history.go(-1);
	}

	function rebuildTime(time) {
		var hr = Math.floor(time / 3600);
		var min = Math.floor(time / 60);
		var sec = time - min * 60;	
		var rem = (hr > 9 ? hr : "0" + hr) + ":" + (min > 9 ? min : "0" + min) + ":" + (sec > 9 ? sec : "0" + sec);
		if (time <= 60) {
			$("#remaining").css('color', 'red');
		}
		$("#remaining").text("Remaining time: " + rem);
	}

	if (password) {	
		lockExam();
	} else {
		$(".hidden").removeClass("hidden");
	}

	var limit = raw_limit.split(":");
	var seconds = limit[0] * 3600 + limit[1] * 60;
	var counter = setInterval(timer, 1000);
	rebuildTime(seconds);

	function timer() {
		seconds -= 1;
		if (seconds == 0) {
			clearInterval(counter);
	    	$("#submit").click();
	 	}
	 	rebuildTime(seconds);
	}

	window.onbeforeunload = function() {
		return "Exam in progress. Choosing to continue will submit your current answers.";
	}

	window.onunload = function() {
        $.ajax({
        	async: false,
            type: $("form").attr('method'),
            url: $("form").attr('action'),
            data: $("form").serialize(),
            success: function() {
            	history.go(-1);
            }
        });
    }

	$("a").click(function(e) {
		if (confirm("Exam in progress. Choosing to continue will submit your current answers.")) {		
			$("#submit").click();
		}
		return false;
	});

	$("#submit").click(function() {
		window.onbeforeunload = null;
		window.onunload = null;
	});
});