package com.metabotsrow.rowapp;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.MotionEvent;
import android.view.View;
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
    private static final String IP = "10.3.141.1";
    private static final int PORT = 8712;
    private Client client;
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
        String videoPath = String.format("http://%s:%d/?action=stream", IP, PORT);
        WebView webView = findViewById(R.id.webView);
        webView.loadUrl(videoPath);

        // Create socket
        try {
            client = new Client(InetAddress.getByName(IP), PORT);
        } catch (UnknownHostException e) {
            e.printStackTrace();
        }

        // Create joystick
        JoyStick joyStick = findViewById(R.id.joyStick);
        joyStick.setListener(this);

        // Show data in UI
        TextView ipTextView = findViewById(R.id.ip);
        ipTextView.setText(String.format("IP: %s", IP));
        TextView portTextView = findViewById(R.id.port);
        portTextView.setText(String.format("PORT: %d", PORT));
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
