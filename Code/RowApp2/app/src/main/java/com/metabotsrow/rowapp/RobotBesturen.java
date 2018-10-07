package com.metabotsrow.rowapp;

import android.content.Context;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.Display;
import android.view.MotionEvent;
import android.view.View;
import android.view.WindowManager;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.TextView;

import com.erz.joysticklibrary.JoyStick;

import java.io.Serializable;
import java.net.InetAddress;
import java.net.UnknownHostException;

// Het streamt niet echt een mp4 bestand ofzo. We doen de streampagina gewoon in de WebView.
// https://code.tutsplus.com/tutorials/streaming-video-in-android-apps--cms-19888
public class RobotBesturen extends AppCompatActivity implements Serializable, JoyStick.JoyStickListener {
    private static final String DEBUG_TAG = "DEBUG";
    private Client client;
    private Rover rover = Controller.getController().getSelectedRover();
    private boolean prevStop;
    private boolean prevRight;
    private boolean prevForward;
    private boolean prevLeft;
    private boolean prevBackward;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_robot_besturen);

        // Setup camera
        String videoPath = String.format("http://%s:%d/?action=stream", rover.getIP(), rover.getPort());
        WebView webView = findViewById(R.id.webView);
        webView.getSettings().setLoadWithOverviewMode(true);
        webView.getSettings().setUseWideViewPort(true);
        webView.loadUrl(videoPath);
        webView.setVerticalScrollBarEnabled(false);
        webView.setHorizontalScrollBarEnabled(false);

        // Disable scrolling in WebView
        webView.setOnTouchListener(new View.OnTouchListener() {
            @Override
            public boolean onTouch(View v, MotionEvent event) {
                return (event.getAction() == MotionEvent.ACTION_MOVE);
            }
        });

        // Get socket from previous activity.
        try {
            client = new Client(InetAddress.getByName(rover.getIP()), rover.getPort());
        } catch (Exception e) {
            e.printStackTrace();
        }

        Log.d("DEBUG_TAG", client.getHost());

        // Create joystick
        JoyStick joyStick = findViewById(R.id.joyStick);
        joyStick.setListener(this);

        // Show data in UI
        TextView ipTextView = findViewById(R.id.ip);
        ipTextView.setText(String.format("IP: %s", rover.getIP()));
        TextView portTextView = findViewById(R.id.port);
        portTextView.setText(String.format("PORT: %d", rover.getPort()));
        TextView roverTextView = findViewById(R.id.rover);
        roverTextView.setText(rover.getName());
    }

    @Override
    public void onMove(JoyStick joyStick, double angle, double power, int direction) {
        // -1 = STOP, 0 = LEFT, 2 = FORWARD, 4 = RIGHT, 6 = BACKWARD
        switch(direction){
            case -1:
                // To avoid unnecessary traffic, we avoid sending the same direction multiple times.
                if(!prevStop){
                    client.sendData("stop");
                    prevStop = true; prevRight = false; prevForward = false; prevLeft = false; prevBackward = false;
                    Log.d(DEBUG_TAG, "stop");
                }
                break;
            case 0:
                if(!prevLeft){
                    client.sendData("left");
                    prevStop = false; prevRight = false; prevForward = false; prevLeft = true; prevBackward = false;
                    Log.d(DEBUG_TAG, "left");
                }
                break;
            case 2:
                if(!prevForward){
                    client.sendData("forward");
                    prevStop = false; prevRight = false; prevForward = true; prevLeft = false; prevBackward = false;
                    Log.d(DEBUG_TAG, "forward");
                }
                break;
            case 4:
                if(!prevRight){
                    client.sendData("right");
                    prevStop = false; prevRight = true; prevForward = false; prevLeft = false; prevBackward = false;
                    Log.d(DEBUG_TAG, "right");
                }
                break;
            case 6:
                if(!prevBackward){
                    client.sendData("backward");
                    prevStop = false; prevRight = false; prevForward = false; prevLeft = false; prevBackward = true;
                    Log.d(DEBUG_TAG, "backward");
                }
                break;
        }
    }

    @Override
    public void onTap() {

    }

    @Override
    public void onDoubleTap() {

    }
}
