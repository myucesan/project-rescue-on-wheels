package com.metabotsrow.rowapp;

import android.net.wifi.ScanResult;

/**
 * Created by Mohamed.
 */
public class Controller {

    private static Controller instance;
    private ScanResult selectedConnection;
    private Rover selectedRover;

    static {
        instance = new Controller();
    }

    private Controller() {
    }

    public ScanResult getSelectedConnection() {
        return selectedConnection;
    }

    public void setSelectedConnection(ScanResult connection) {
        selectedConnection = connection;
    }

    public static Controller getController() {
        return instance;
    }

    public Rover getSelectedRover() {
        return selectedRover;
    }

    public void setSelectedRover(String name, String ip, int port) {
        selectedRover = new Rover(name, ip, port);
    }


}

