package com.company;

import java.io.*;
import java.net.*;


public class Client extends Thread {

    private DatagramSocket socket;
    private String key;
    private InetAddress host;
    private int port;
    private byte[] data;
    private DatagramPacket packet;


    public Client(InetAddress host, int port) {
        this.host = host;
        this.port = port;

        try {
            socket = new DatagramSocket();
            socket.connect(host, port);

        }  catch (IOException e) {
            e.printStackTrace();
        }

    }

    public String getHost() {
        return host.toString();
    }

    public void setHost(InetAddress host) {
        this.host = host;
    }

    public int getPort() {
        return port;
    }

    public void getPort(int port) {
        this.port = port;
    }

    public DatagramSocket getSocket() {
        return socket;
    }

    public void setKey(String string) {
        key = string;
    }

    public String getKey() {
        return key;
    }

    public byte[] getData() {
        return data;
    }

    public void setData(byte[] data) {
        this.data = data;
    }

    public void sendData(String message) {
        try {
            data = message.getBytes();
            packet = new DatagramPacket(data, data.length, host, port);
            socket.send(packet);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

}