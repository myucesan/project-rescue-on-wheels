package com.metabotsrow.rowapp;

import android.os.AsyncTask;
import android.view.LayoutInflater;
import android.widget.TextView;

public class OnReceive extends AsyncTask<Void, String, Void> {


    @Override
    protected Void doInBackground(Void... voids) {
        while (true) {
            Client.getClient().receiveData();
        }
    }


}
