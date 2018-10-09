package com.metabotsrow.rowapp;
/**
 * Created by Mohamed.
 */
import android.util.Log;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.*;
import java.net.*;


public class Client implements Serializable {

    private DatagramSocket socket;
    private JSONObject insertedValues;
    private JSONObject obtainedValues;
    private InetAddress host;
    private int port;
    private byte[] dataToReceive;
    private byte[] dataToSend;
    private DatagramPacket sentPacket;
    private DatagramPacket receivedPacket;
    private static Client client;

    static {
        client = new Client();
    }


    private Client() {

        try {
            socket = new DatagramSocket();

        }  catch (IOException e) {
            e.printStackTrace();
        }

        insertedValues = new JSONObject();
        obtainedValues = new JSONObject();

        dataToReceive = new byte[2048];

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

    public void setPort(int port) {
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

    public byte[] getDataToSend() {
        return dataToSend;
    }

    public void setData(byte[] dataToSend) {
        this.dataToSend = dataToSend;
    }

    public void sendData() {
        try {
            dataToSend = insertedValues.toString().getBytes();
            sentPacket = new DatagramPacket(dataToSend, dataToSend.length, host, port);
            socket.send(sentPacket);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public String receiveData() {
        receivedPacket = new DatagramPacket(dataToReceive, dataToReceive.length);
        try {
            socket.receive(receivedPacket);
        } catch (IOException e) {
            e.printStackTrace();
        }
        String receivedString = new String(dataToReceive, 0, receivedPacket.getLength());
        Log.d("DEBUG_TAG", receivedString);
        return receivedString;

    }

    public static Client getClient() {
        return client;
    }

    public void close() {
        socket.close();
    }

}
