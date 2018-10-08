package com.metabotsrow.rowapp;
/**
 * Created by Mohamed.
 */
import org.json.JSONException;
import org.json.JSONObject;

import java.io.*;
import java.net.*;


public class Client implements Serializable {

    private DatagramSocket socket;
    private JSONObject insertedValues;
    private InetAddress host;
    private int port;
    private byte[] data;
    private DatagramPacket packet;


    public Client(InetAddress host, int port) {
        this.host = host;
        this.port = port;

        try {
            socket = new DatagramSocket();

        }  catch (IOException e) {
            e.printStackTrace();
        }

        insertedValues = new JSONObject();

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

    public void insertValues(String state, int speed) {
        try {
            insertedValues.put("state", state);
            insertedValues.put("speed", speed);
        } catch (JSONException e) {
            e.printStackTrace();
        }
    }

    public byte[] getData() {
        return data;
    }

    public void setData(byte[] data) {
        this.data = data;
    }

    public void sendData() {
        try {
            data = insertedValues.toString().getBytes();
            packet = new DatagramPacket(data, data.length, host, port);
            socket.send(packet);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public void close() {
        socket.close();
    }

}
