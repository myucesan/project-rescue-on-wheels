$(document).ready(function() {
  var socket = io.connect('http://' + document.domain + ':' + location.port);
  var roverInfo = localStorage.getItem("RoverSelection");
  var c = document.getElementById("canvastest");
  var ctx = c.getContext("2d");
  ctx.beginPath();
  ctx.moveTo(200, 100);
  ctx.lineWidth = 4;
  var x_b = 200;
  var y_b = 100;
  var hoek = Math.PI/2;
  var v = 4;
  var control = {
		"device": "Webapp",
		"state": null,
                "speed": 220,
		"backtrack": 0
	};
  socket.emit('roverConnection', roverInfo);
  $('#ip').text("IP:" + JSON.parse(roverInfo).ip);
  $('#port').text("Port:" + JSON.parse(roverInfo).port);
  $('#roverNo').text(JSON.parse(roverInfo).name);
  
  $('#Get').on('click', function(){
    socket.emit('outputString', $('#textbox').val());
	});

  $('#driveback').on('click', function(){
    control.backtrack = 1;
    socket.emit('roverControl', JSON.stringify(control));
});

  window.addEventListener("keydown", controlOnKey, false);
  window.addEventListener("keyup", stop, false);

  function stop(key) {
      control.state = "stop";
      control.backtrack = 0;
      socket.emit('roverControl', JSON.stringify(control));
   }

  function controlOnKey(key) {
    if (key.keyCode == "87") {
      control.state = "forward";
      control.backtrack = 0;
      socket.emit('roverControl', JSON.stringify(control));
    }
    if (key.keyCode == "65") {
      control.state = "left";
      control.backtrack = 0;
      socket.emit('roverControl', JSON.stringify(control));
    }
    if (key.keyCode == "68") {
      control.state = "right";
      control.backtrack = 0;
      socket.emit('roverControl', JSON.stringify(control));
    }
    if (key.keyCode == "83") {
      control.state = "backward";
      control.backtrack = 0;
      socket.emit('roverControl', JSON.stringify(control));
    }
    if (key.keyCode == "32") {
      control.state = "socket";
      socket.emit('roverControl', JSON.stringify(control));
    }
  }

  socket.on('lineDrawer', function(lineCalculation) {
	var test = JSON.parse(lineCalculation);
	var t = test["time"]*1000;
	var direction = test["state"];
	console.log(direction);
	console.log(t);
	switch (direction) {
        	case "left":
            		hoek += t*(Math.PI/1800);
            		console.log("Hoek (links): " + hoek);
            		break;
        	case "forward":
            		x_b += v * Math.cos(hoek);
            		y_b -= v * Math.sin(hoek);
            		ctx.lineTo(x_b, y_b);
			ctx.strokeStyle = "white";
            		ctx.stroke();
            		console.log("Rechtdoor (x, y): " + x_b + ", " + y_b);
            		break;
        	case "right":
	        	hoek += t*(-Math.PI/2600);
            		console.log("Hoek (rechts): " + hoek);
            		break;
        	case "backward":
           		x_b += v * Math.cos(hoek);
            		y_b += v * Math.sin(hoek);
            		ctx.lineTo(x_b, y_b);
			ctx.strokeStyle = "white";
            		ctx.stroke();
            		console.log("Achteruit (x, y): " + x_b + ", " + y_b);
            		break;
    	}
	
  }); 
});