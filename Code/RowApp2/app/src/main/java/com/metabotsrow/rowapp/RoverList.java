package com.metabotsrow.rowapp;
/**
 * Created by Mohamed.
 */
import android.net.wifi.ScanResult;

import java.util.ArrayList;
import java.util.List;

public final class RoverList {

    private List<String> roverNames;

    private List<ScanResult> rovers;

    private static RoverList instance;

    static {
        instance = new RoverList();
    }

    private RoverList() {
        rovers = new ArrayList<>();
        roverNames = new ArrayList<>();
    }

    public ScanResult getRoverFromList(int index) {
        return rovers.get(index);
    }

    public int getIndexFromName(String name) {
        return roverNames.indexOf(name);
    }

    public void addRover(ScanResult rover) {
        rovers.add(rover);
    }

    public void addRoverName(String name) {
        roverNames.add(name);
    }

    public void removeRoverName(int i) {
        roverNames.remove(i);
    }

    public void removeRover(int i) {
        rovers.remove(i);
    }


    public List<String> getRoverNames() {
        return roverNames;
    }



    public static RoverList getRoverList() {
        return instance;
    }

    public List<ScanResult> getRovers() {
        return rovers;
    }

}
