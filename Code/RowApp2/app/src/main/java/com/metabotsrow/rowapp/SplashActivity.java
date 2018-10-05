package com.metabotsrow.rowapp;

import android.content.Intent;
import android.os.Bundle;
import android.os.SystemClock;
import android.support.annotation.Nullable;
import android.support.v7.app.AppCompatActivity;

/**
 * Created by Yoshio on 04/10/2018.
 */
public class SplashActivity extends AppCompatActivity {

    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        SystemClock.sleep(3000);
        Intent intent = new Intent(this, RobotBesturen.class);
        startActivity(intent);
        finish();
    }
}