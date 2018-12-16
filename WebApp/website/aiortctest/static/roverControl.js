$(document).ready(function () {
    var socket = io.connect('http://' + document.domain + ':' + location.port);
    var pc = new RTCPeerConnection();
    var roverInfo = localStorage.getItem("RoverSelection");
    var c = document.getElementById("canvastest");
    var micCheck = false;
    var ctx = c.getContext("2d");
    ctx.beginPath();
    ctx.moveTo(200, 100);
    ctx.lineWidth = 4;
    var x_b = 200;
    var y_b = 100;
    var hoek = Math.PI / 2;
    var v = 4;

    pc.addEventListener('icegatheringstatechange', function() {
        console.log("Works?");
    }, false);

    // connect audio / video

    pc.addEventListener('track', function (stream) {
        document.getElementById('audio').srcObject = stream;
    });


    function negotiate() {
        return pc.createOffer().then(function (offer) {
            return pc.setLocalDescription(offer);
        }).then(function () {
            // wait for ICE gathering to complete
            return new Promise(function (resolve) {
                if (pc.iceGatheringState === 'complete') {
                    resolve();
                } else {
                    function checkState() {
                        if (pc.iceGatheringState === 'complete') {
                            pc.removeEventListener('icegatheringstatechange', checkState);
                            resolve();
                        }
                    }

                    pc.addEventListener('icegatheringstatechange', checkState);
                }
            });
        }).then(function () {
            var offer = pc.localDescription;

            return fetch('/offer', {
                body: JSON.stringify({
                    sdp: offer.sdp,
                    type: offer.type,
                }),
                headers: {
                    'Content-Type': 'application/json'
                },
                method: 'POST'
            });
        }).then(function (response) {
            return response.json();
        }).then(function (answer) {
            return pc.setRemoteDescription(answer);
        }).catch(function (e) {
            alert(e);
        });
    }


    // this is a callback that triggers when the my response event is emitted by the server.
    socket.on('temperature', function (msg) {
        $('#temperatureId').text(msg + " DEGC");
    });
    socket.on('compass', function (msg) {
        $('#compassId').text(msg + " DEG");
    });
    socket.on('distance', function (msg) {
        $('#distId').text(msg + " CM");
    });

    socket.emit('roverConnection', roverInfo);
    $('#ip').text("IP:" + JSON.parse(roverInfo).ip);
    $('#port').text("Port:" + JSON.parse(roverInfo).port);
    $('#roverNo').text(JSON.parse(roverInfo).name);

    $('#Get').on('click', function () {
        socket.emit('outputString', $('#textbox').val());
    });
    $('#driveback').on('click', function () {
        socket.emit('backtrack');
    });


    $('#microphone').on('click', function () {
        socket.emit('microphone', "lalal");
        if (micCheck == false) {
            micCheck = true;

            navigator.mediaDevices.getUserMedia({audio: true}).then(function (stream) {
                stream.getTracks().forEach(function (track) {
                    pc.addTrack(track, stream);
                });
                return negotiate();
            });
        }
        else
            {
                micCheck = false;
                // close transceivers
                if (pc.getTransceivers) {
                    pc.getTransceivers().forEach(function (transceiver) {
                        transceiver.stop();
                    });
                }

                // close local audio / video
                pc.getSenders().forEach(function (sender) {
                    sender.track.stop();
                });

                // close peer connection
                setTimeout(function () {
                    pc.close();
                }, 500);
            }
        }
    );

        window.addEventListener("keydown", controlOnKey, false);
        window.addEventListener("keyup", stop, false);

        function stop(key) {
            socket.emit('direction', "stop");
        }

        function controlOnKey(key) {
            var t = 1000;
            if (key.keyCode == "87") {
                x_b += v * Math.cos(hoek)
                y_b -= v * Math.sin(hoek);
                ctx.lineTo(x_b, y_b);
                ctx.strokeStyle = "white";
                ctx.stroke();
                console.log("Going forward");
                socket.emit('direction', "forward");
            }
            if (key.keyCode == "65") {
                hoek += t * (Math.PI / 1800)
                console.log("Going left");
                socket.emit('direction', "left");
            }
            if (key.keyCode == "68") {
                hoek += t * (-Math.PI / 2600);
                console.log("Going right");
                socket.emit('direction', "right");
            }
            if (key.keyCode == "83") {
                x_b -= v * Math.cos(hoek);
                y_b -= v * Math.sin(hoek);
                ctx.fillRect(x_b, y_b, 2, 2);
                ctx.stroke();
                console.log("Going backward");
                socket.emit('direction', "backward");
            }
        }

        socket.on('lineDrawer', function (lineCalculation) {
            var test = JSON.parse(lineCalculation);
            var t = test["time"] * 1000;
            var direction = test["state"];
            console.log(direction);
            console.log(t);
            switch (direction) {
                case "left":
                    hoek += t * (Math.PI / 1800);
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
                    hoek += t * (-Math.PI / 2600);
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
