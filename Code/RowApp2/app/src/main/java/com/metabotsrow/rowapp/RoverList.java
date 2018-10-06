package com.metabotsrow.rowapp;
/**
 * Created by Mohamed.
 */
import java.util.ArrayList;
import java.util.List;

public final class RoverList {

    private List<Rover> rovers;
    private List<String> roverNames;

    private static RoverList instance;

    static {
        instance = new RoverList();
    }

    private RoverList() {
        rovers = new ArrayList<>();
        roverNames = new ArrayList<>();
    }

    public Rover getRoverFromList(int index) {
        return rovers.get(index);
    }

    public int getIndexFromName(String name) {
        return roverNames.indexOf(name);
    }

    public void addRover(Rover rover) {
        rovers.add(rover);
        roverNames.add(rover.getName());
    }

    public void removeRover(int i) {
        rovers.remove(i);
    }

    public static RoverList getRoverList() {
        return instance;
    }

    public List<Rover> getRovers() {
        return rovers;
    }

    public List<String> getRoverNames() {
        return roverNames;
    }

}
