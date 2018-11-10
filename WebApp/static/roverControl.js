$(document).ready(function() {
  var socket = io.connect('http://' + document.domain + ':' + location.port);
  var roverInfo = localStorage.getItem("RoverSelection");
  var control = {
		"device": "Webapp",
		"state": null,
                "speed": 220,
		"backtrack" : 0
	};
  socket.emit('roverConnection', roverInfo);

  window.addEventListener("keydown", controlOnKey, false);
  window.addEventListener("keyup", stop, false);

  $('#driveback').on('click', function(){
    console.log("TEST")
    control.backtrack = 1
    socket.emit('roverControl', JSON.stringify(control));
});

  function stop(key) {
      control.state = "stop";
      socket.emit('roverControl', JSON.stringify(control));
   }

  function controlOnKey(key) {
    if (key.keyCode == "87") {
      control.state = "forward";
      socket.emit('roverControl', JSON.stringify(control));
    }
    if (key.keyCode == "65") {
      control.state = "left";
      socket.emit('roverControl', JSON.stringify(control));
    }
    if (key.keyCode == "68") {
      control.state = "right";
      socket.emit('roverControl', JSON.stringify(control));
    }
    if (key.keyCode == "83") {
      control.state = "backward";
      socket.emit('roverControl', JSON.stringify(control));
    }
    if (key.keyCode == "32") {
      control.state = "socket";
      socket.emit('roverControl', JSON.stringify(control));
    }
  }
  socket.on('lineDrawer', function(lineCalculation) {
	console.log(lineCalculation)
  }); 
});
