import aiohttp_jinja2 
import jinja2 
import asyncio 
import json 
import sys 
import os

import cv2
from aiohttp import web
from av import VideoFrame

from aiortc import RTCPeerConnection, RTCSessionDescription, VideoStreamTrack
from aiortc.contrib.media import MediaBlackhole, MediaPlayer, MediaRecorder

import socketio

from routes import setup_routes

ROOT = '/home/pi/RescueOnTheWheelsProject/WebApp/website'

socket = socketio.AsyncServer(async_mode='aiohttp')
app = web.Application()
socket.attach(app)
aiohttp_jinja2.setup(
    app, loader=jinja2.FileSystemLoader('./templates'))
#main = Main()

#async def compass():
 #   while True:
  #      socket.emit('compass', main._compass.degrees(main._compass.heading())

#async def distance():
 #   while True:
  #      socket.emit('temperature', "{:.1f}".format(main._temperature.convert())

#async def temperature():
 #   while True;:
  #      socket.emit('distance', "{:.1f}".format(main._distance.get_distance())


@socket.on('outputString')
async def output_string(sid, text):
    main._lcd.output_string(text)

@socket.on('direction')
async def drive_into_direction(sid, direction):
    if not main.is_disabled():
        main._motor_control.drive(direction)

@socket.on('backtrack')
async def track_back(sid):
    main.disable()
    main._motor_control.reverse_drive()
    main.enable()



async def offer(request):
    params = await request.json()
    offer = RTCSessionDescription(
        sdp=params['sdp'],
        type=params['type'])

    pc = RTCPeerConnection()
    pcs.add(pc)

    # prepare local media

    player = MediaPlayer('hw:1', format='alsa', options={'channels': '1'})
    recorder = MediaRecorder('plughw:0,0', format='alsa')

    @pc.on('iceconnectionstatechange')
    async def on_iceconnectionstatechange():
        print('ICE connection state is %s' % pc.iceConnectionState)
        if pc.iceConnectionState == 'failed':
            await pc.close()
            pcs.discard(pc)

    @pc.on('track')
    def on_track(track):
        print('Track %s received' % track.kind)

        
        pc.addTrack(player.audio)
        recorder.addTrack(track)

        @track.on('ended')
        async def on_ended():
            print('Track %s ended' % track.kind)
            await recorder.stop()

    # handle offer
    await pc.setRemoteDescription(offer)
    await recorder.start()

    # send answer
    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)

    return web.Response(
        content_type='application/json',
        text=json.dumps({
            'sdp': pc.localDescription.sdp,
            'type': pc.localDescription.type
        }))


pcs = set()


async def on_shutdown(app):
    # close peer connections
    coros = [pc.close() for pc in pcs]
    await asyncio.gather(*coros)
    pcs.clear()


if __name__ == '__main__':
    app.on_shutdown.append(on_shutdown)
    app.router.add_post('/offer', offer)
    setup_routes(app)
    web.run_app(app, host='192.168.137.241', port=sys.argv[1:][0])
