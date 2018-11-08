$(document).ready(function() {
  var socket = io.connect('http://' + document.domain + ':' + location.port);
  var roverInfo = localStorage.getItem("RoverSelection");
  socket.emit('roverConnection', roverInfo);

  window.addEventListener("keydown", controlOnKey, false);

  function controlOnKey(key) {
    if (key.keyCode == "87") {
      socket.emit('roverControl', "forward");
    }
    if (key.keyCode == "65") {
      socket.emit('roverControl', "left");
    }
    if (key.keyCode == "68") {
      socket.emit('roverControl', "right");
    }
    if (key.keyCode == "83") {
      socket.emit('roverControl', "backward");
    }
  }
});
