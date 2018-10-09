package com.metabotsrow.rowapp;

import android.content.Intent;
import android.graphics.Typeface;
import android.os.Bundle;
import android.os.SystemClock;
import android.support.annotation.Nullable;
import android.support.v4.content.res.ResourcesCompat;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.RecyclerView;
import android.util.Log;
import android.view.View;
import android.view.ViewGroup;
import android.webkit.WebView;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.ListView;
import android.widget.ScrollView;
import android.widget.TextView;

import com.erz.joysticklibrary.JoyStick;

import java.net.InetAddress;
import java.net.UnknownHostException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

/**
 * Created by Yoshio on 04/10/2018.
 */
public class ConnectActivity extends AppCompatActivity implements View.OnClickListener {
    private Object selectedItem;

    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_connect_rover);

        // Get reference of widgets from XML layout
        final ListView connectionListView = (ListView) findViewById(R.id.connectionListView);

        // Simple check if rovers are already initialized
        if(RoverList.getRoverList().getRovers().size() == 0){
            // Initializing rovers only if they aren't already
            RoverList.getRoverList().addRover(new Rover("DUMMY ROVER 2", "10.3.141.1", 8802));
            RoverList.getRoverList().addRover(new Rover("ROVER 8", "10.3.141.1", 8762));
            RoverList.getRoverList().addRover(new Rover("DUMMY ROVER 11", "10.3.141.1", 8811));
            RoverList.getRoverList().addRover(new Rover("DUMMY ROVER 21", "10.3.141.1", 8821));
        }

        // Create an ArrayAdapter from List
        ArrayAdapter<String> arrayAdapter = new ArrayAdapter<String>
                (this, android.R.layout.simple_list_item_1, RoverList.getRoverList().getRoverNames()){
            @Override
            public View getView(int position, View convertView, ViewGroup parent){
                // Get the Item from ListView
                View view = super.getView(position, convertView, parent);

                // Initialize a TextView for ListView each Item
                TextView tv = (TextView) view.findViewById(android.R.id.text1);

                // Set the text color of TextView (ListView Item)
                tv.setTextColor(getResources().getColor(R.color.colorDark));

                tv.setTextSize(25);

                // Set font of TextView
                Typeface face = ResourcesCompat.getFont(getContext(), R.font.agency_fb);
                tv.setTypeface(face);

                // Generate ListView Item using TextView
                return view;
            }
        };

        // DataBind ListView with items from ArrayAdapter
        connectionListView.setAdapter(arrayAdapter);

        // Set listener for clicks on items
        connectionListView.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> adapterView, View view, int i, long l) {
                selectedItem = connectionListView.getItemAtPosition(i);
                String s = selectedItem.toString();
                Log.d("DEBUG_TAG", s);
            }
        });

        Button connectBtn = findViewById(R.id.connectBtn);
        connectBtn.setOnClickListener(this);
    }

    @Override
    public void onClick(View v) {
        // Check if any item is selected.
        if(selectedItem.toString().contains("ROVER")){
            Controller.getController().setSelectedRover(RoverList.getRoverList().getRoverFromList(
                    RoverList.getRoverList().getIndexFromName(selectedItem.toString())
            ));
            Intent intent = new Intent(this, RobotBesturen.class);
            startActivity(intent);
            finish();
        }
    }
}