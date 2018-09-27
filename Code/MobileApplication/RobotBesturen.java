package com.metabotsrow.rowapp;

import android.app.AlertDialog;
import android.app.ProgressDialog;
import android.graphics.PixelFormat;
import android.media.MediaPlayer;
import android.net.Uri;
import android.os.AsyncTask;
import android.provider.MediaStore;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.MotionEvent;
import android.view.View;
import android.webkit.WebView;
import android.widget.Button;
import android.widget.MediaController;
import android.widget.VideoView;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.io.Serializable;
import java.net.InetAddress;
import java.net.ServerSocket;
import java.net.Socket;
import java.net.UnknownHostException;


// Het streamt niet echt een mp4 bestand ofzo. We doen de streampagina gewoon in de WebView.
// https://code.tutsplus.com/tutorials/streaming-video-in-android-apps--cms-19888
public class RobotBesturen extends AppCompatActivity implements Serializable {
    private String videoPath ="http://10.3.141.1:8090/?action=stream";
    private Client client;
    private View.OnTouchListener handleForward = new View.OnTouchListener() {
        @Override
        public boolean onTouch(View v, MotionEvent event) {
            switch (event.getAction()) {
                case MotionEvent.ACTION_DOWN:
                    client.sendData("forward");
                    break;
                case MotionEvent.ACTION_UP:
                    client.sendData("stop");

            }

            return false;

        }
    };
    private View.OnTouchListener handleBackward = new View.OnTouchListener() {
        @Override
        public boolean onTouch(View v, MotionEvent event) {
            switch (event.getAction()) {
                case MotionEvent.ACTION_DOWN:
                    client.sendData("backward");
                    break;
                case MotionEvent.ACTION_UP:
                    client.sendData("stop");

            }

            return false;

        }
    };
    private View.OnTouchListener handleLeft = new View.OnTouchListener() {
        @Override
        public boolean onTouch(View v, MotionEvent event) {
            switch (event.getAction()) {
                case MotionEvent.ACTION_DOWN:
                    client.sendData("left");
                    break;
                case MotionEvent.ACTION_UP:
                    client.sendData("stop");

            }

            return false;

        }
    };
    private View.OnTouchListener handleRight = new View.OnTouchListener() {
        @Override
        public boolean onTouch(View v, MotionEvent event) {
            switch (event.getAction()) {
                case MotionEvent.ACTION_DOWN:
                    client.sendData("right");
                    break;
                case MotionEvent.ACTION_UP:
                    client.sendData("stop");

            }

            return false;

        }
    };

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_robot_besturen);
        WebView webView = findViewById((R.id.webView));
        webView.loadUrl(videoPath);

        try {
            client = new Client(InetAddress.getByName("192.168.192.52"), 8762);
        } catch (UnknownHostException e) {
            e.printStackTrace();
        }

        Button forward = (Button) findViewById(R.id.forwardBtn);
        Button backward = (Button) findViewById(R.id.backwardBtn);
        Button left = (Button) findViewById(R.id.leftBtn);
        Button right = (Button) findViewById(R.id.rightBtn);

        forward.setOnTouchListener(handleForward);
        backward.setOnTouchListener(handleBackward);
        left.setOnTouchListener(handleLeft);
        right.setOnTouchListener(handleRight);

    }



}
