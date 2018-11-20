package com.metabotsrow.rowapp;
/**
 * Created by Mohamed.
 */
public class Rover {

    private static int startid = 1;
    private int id;
    private String name;
    private String ip;
    private int port;

    public Rover(String name, String ip, int port) {
        id = startid++;
        this.name = name;
        this.port = port;
        this.ip = ip;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getIP() {
        return ip;
    }

    public int getID() {
        return id;
    }

    public void setIP(String ip) {
        this.ip = ip;
    }

    public int getPort() {
        return port;
    }

    public void setPort(int port) {
        this.port = port;
    }

}
