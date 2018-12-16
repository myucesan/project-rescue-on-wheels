package com.metabotsrow.rowapp;

import android.os.Bundle;
import android.os.SystemClock;
import android.support.v7.app.AlertDialog;
import android.support.v7.app.AppCompatActivity;
import android.view.MotionEvent;
import android.view.View;
import android.webkit.WebView;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import com.erz.joysticklibrary.JoyStick;
import com.github.nkzawa.socketio.client.IO;
import com.github.nkzawa.socketio.client.Socket;
import com.github.nkzawa.emitter.Emitter;

import java.io.Serializable;
import java.net.URISyntaxException;

// Het streamt niet echt een mp4 bestand ofzo. We doen de 1streampagina gewoon in de WebView.
// https://code.tutsplus.com/tutorials/streaming-video-in-android-apps--cms-19888
public class RobotBesturen extends AppCompatActivity implements Serializable, JoyStick.JoyStickListener {
    private static final String DEBUG_TAG = "DEBUG";
    //private Client client;
    private Rover rover = Controller.getController().getSelectedRover();
    private int speed = 230;
    private boolean prevStop;
    private boolean prevRight;
    private boolean prevForward;
    private boolean prevLeft;
    private boolean prevBackward;
    private Socket mSocket;
    {
        try {
            mSocket = IO.socket("http://" + rover.getIP() + ":" + rover.getPort());
        } catch (URISyntaxException e) {}
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        mSocket.on("temperature", onTemperature);
        mSocket.on("compass", onCompass);
        mSocket.on("distance", onDistance);
        mSocket.connect();


        setContentView(R.layout.activity_robot_besturen);
        // Setup camera
//        String videoPath = String.format("http://%s:%d/cam.mjpg", rover.getIP(), (rover.getPort()+1));
        String videoPath = String.format("http://10.3.141.1:9908/?action=stream");
        WebView webView = findViewById(R.id.webView);
        webView.getSettings().setLoadWithOverviewMode(true);
        webView.getSettings().setUseWideViewPort(true);
        SystemClock.sleep(6000);
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
        Button sendText = findViewById(R.id.lcdButton);
        sendText.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                AlertDialog.Builder mBuilder = new AlertDialog.Builder(RobotBesturen.this);
                View mView = getLayoutInflater().inflate(R.layout.dialog_sendtext, null);
                final EditText textToSend = (EditText) mView.findViewById(R.id.insertText);
                Button send = (Button) mView.findViewById(R.id.btnSend);
                Button back = (Button) mView.findViewById(R.id.btnBack);
                mBuilder.setView(mView);
                final AlertDialog dialog = mBuilder.create();
                dialog.show();
                send.setOnClickListener(new View.OnClickListener() {
                    @Override
                    public void onClick(View view) {
                        if (textToSend.getText().length() <= 32) {
                            mSocket.emit("outputString", textToSend.getText().toString());
                        } else {
                            Toast.makeText(RobotBesturen.this, "Text must contain less than 33 characters!", Toast.LENGTH_SHORT).show();
                        }
                    }
                });
                back.setOnClickListener(new View.OnClickListener() {
                    @Override
                    public void onClick(View view) {
                        dialog.hide();
                    }
                });
            }
        });
    }

    private Emitter.Listener onTemperature = new Emitter.Listener() {
        @Override
        public void call(final Object... args) {
            runOnUiThread(new Runnable() {
                @Override
                public void run() {
                    TextView tempValue = findViewById(R.id.tvTemperature);
                    tempValue.setText(args[0].toString());
                }
            });
        }
    };

    private Emitter.Listener onCompass = new Emitter.Listener() {
        @Override
        public void call(final Object... args) {
            runOnUiThread(new Runnable() {
                @Override
                public void run() {
                    TextView tvCompass = findViewById(R.id.tvCompass);
                    tvCompass.setText(args[0].toString());
                }
            });
        }
    };

    private Emitter.Listener onDistance = new Emitter.Listener() {
        @Override
        public void call(final Object... args) {
            runOnUiThread(new Runnable() {
                @Override
                public void run() {
                    TextView tvCompass = findViewById(R.id.tvDistance);
                    tvCompass.setText(args[0].toString());
                }
            });
        }
    };

    @Override
    public void onMove(JoyStick joyStick, double angle, double power, int direction) {
        // -1 = STOP, 0 = LEFT, 2 = FORWARD, 4 = RIGHT, 6 = BACKWARD
        switch(direction){
            case -1:
                // To avoid unnecessary traffic, we avoid sending the same direction multiple times.
                if(!prevStop){
                    mSocket.emit("direction", "stop");
                    prevStop = true; prevRight = false; prevForward = false; prevLeft = false; prevBackward = false;
                    //Log.d(DEBUG_TAG, "stop");
                }
                break;
            case 0:
                if(!prevLeft){
                    mSocket.emit("direction", "left");
                    prevStop = false; prevRight = false; prevForward = false; prevLeft = true; prevBackward = false;
                    //Log.d(DEBUG_TAG, "left");
                }
                break;
            case 2:
                if(!prevForward){
                    mSocket.emit("direction", "forward");
                    prevStop = false; prevRight = false; prevForward = true; prevLeft = false; prevBackward = false;
                    //Log.d(DEBUG_TAG, "forward");
                }
                break;
            case 4:
                if(!prevRight){
                    mSocket.emit("direction", "right");
                    prevStop = false; prevRight = true; prevForward = false; prevLeft = false; prevBackward = false;
                    //Log.d(DEBUG_TAG, "right");
                }
                break;
            case 6:
                if(!prevBackward){
                    mSocket.emit("direction", "backward");
                    prevStop = false; prevRight = false; prevForward = false; prevLeft = false; prevBackward = true;
                    //Log.d(DEBUG_TAG, "backward");
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
