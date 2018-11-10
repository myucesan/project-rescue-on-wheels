var selection;
var roverInfo = {
    name: ["Rover 08", "Rover 09", "Rover 10", "Rover 13"],
    ip: ["192.168.192.52", "1", "2", "3"],
    port: [8025, 1, 1, 1]
  };
var selectedRover = {
  name: null,
  ip: null,
  port: null
}


$(document).ready(function(){
  $('#rover1').text(roverInfo.name[0]);
  $('#rover2').text(roverInfo.name[1]);
  $('#rover3').text(roverInfo.name[2]);
  $('#rover4').text(roverInfo.name[3]);
$('#rover1').on('click', function(){
    selection = $(this).text();
    $(this).css("background-color", "#ccc");
    $('#rover2').css("background-color", "#eee");
    $('#rover3').css("background-color", "#eee");
    $('#rover4').css("background-color", "#eee");
    console.log(selection);
});
$('#rover2').on('click', function(){
    selection = $(this).text();
    $(this).css("background-color", "#ccc");
    $('#rover1').css("background-color", "#eee");
    $('#rover3').css("background-color", "#eee");
    $('#rover4').css("background-color", "#eee");
    console.log(selection);
});
$('#rover3').on('click', function(){
    selection = $(this).text();
    $(this).css("background-color", "#ccc");
    $('#rover1').css("background-color", "#eee");
    $('#rover2').css("background-color", "#eee");
    $('#rover4').css("background-color", "#eee");
    console.log(selection);
});
$('#rover4').on('click', function(){
    selection = $(this).text();
    $(this).css("background-color", "#ccc");
    $('#rover1').css("background-color", "#eee");
    $('#rover2').css("background-color", "#eee");
    $('#rover3').css("background-color", "#eee");
    log.console(selection === sendRoverInfo.name[0]);
});
$('#connect').on('click', function(){

    if (selection === roverInfo.name[0]) {
      selectedRover.name = roverInfo.name[0];
      selectedRover.ip = roverInfo.ip[0];
      selectedRover.port = roverInfo.port[0];
    }
    if (selection === roverInfo.name[1]) {
      selectedRover.name = roverInfo.name[1];
      selectedRover.ip = roverInfo.ip[1];
      selectedRover.port = roverInfo.port[1];
    }
    if (selection === roverInfo.name[2]) {
      selectedRover.name = roverInfo.name[2];
      selectedRover.ip = roverInfo.ip[2];
      selectedRover.port = roverInfo.port[2];
    }
    if (selection === roverInfo.name[3]) {
      selectedRover.name = roverInfo.name[3];
      selectedRover.ip = roverInfo.ip[3];
      selectedRover.port = roverInfo.port[3];
    }
    localStorage.setItem("RoverSelection", JSON.stringify(selectedRover));
});
});

