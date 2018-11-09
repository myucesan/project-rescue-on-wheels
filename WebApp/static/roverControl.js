$(document).ready(function() {
  var socket = io.connect('http://' + document.domain + ':' + location.port);
  var roverInfo = localStorage.getItem("RoverSelection");
  var control = {
		"device": "Webapp",
		"state": null,
                "speed": 220
	};
  socket.emit('roverConnection', roverInfo);

  window.addEventListener("keydown", controlOnKey, false);
  window.addEventListener("keyup", stop, false);

  function stop(key) {
      control.direction = "stop";
      socket.emit('roverControl', JSON.stringify(control));
   }

  function controlOnKey(key) {
    if (key.keyCode == "87") {
      control.direction = "forward";
      socket.emit('roverControl', JSON.stringify(control));
    }
    if (key.keyCode == "65") {
      control.direction = "left";
      socket.emit('roverControl', JSON.stringify(control));
    }
    if (key.keyCode == "68") {
      control.direction = "right";
      socket.emit('roverControl', JSON.stringify(control));
    }
    if (key.keyCode == "83") {
      control.direction = "backward";
      socket.emit('roverControl', JSON.stringify(control));
    }
    if (key.keyCode == "32") {
      control.direction = "socket";
      socket.emit('roverControl', JSON.stringify(control));
    }
  }
});
