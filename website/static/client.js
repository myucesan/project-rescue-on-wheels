$(document).ready(function () {
    var socket = io.connect('http://' + document.domain + ':' + location.port);    
    var pc = new RTCPeerConnection();
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
    socket.emit('t', "INSHAALLAAAH");
    socket.on('lala', function(data) {
       console.log(data);
 	});

    $('#Get').on('click', function () {
        socket.emit('t', "YEE");
    });

    pc.addEventListener('icegatheringstatechange', function() {
        console.log("Works?");
    }, false);

    // connect audio / video

    pc.addEventListener('track', function (stream) {
        document.getElementById('audio').srcObject = stream.streams[0];
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
    
    
    $('#microphone').on('click', function () {
        
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

        
    });

