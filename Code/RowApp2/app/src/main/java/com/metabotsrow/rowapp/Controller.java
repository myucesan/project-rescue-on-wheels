package com.metabotsrow.rowapp;
/**
 * Created by Mohamed.
 */
public class Controller {

    private static Controller instance;
    private Rover selectedRover;

    static {
        instance = new Controller();
    }

    private Controller() {
    }

    public static Controller getController() {
        return instance;
    }

    public Rover getSelectedRover() {
        return selectedRover;
    }

    public void setSelectedRover(Rover rover) {
        selectedRover = rover;
    }


}

