package com.metabotsrow.rowapp;

import android.Manifest;
import android.annotation.TargetApi;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.content.pm.PackageManager;
import android.graphics.Color;
import android.graphics.Typeface;
import android.graphics.drawable.ColorDrawable;
import android.net.wifi.ScanResult;
import android.net.wifi.WifiConfiguration;
import android.net.wifi.WifiManager;
import android.os.Build;
import android.os.Bundle;
import android.support.annotation.Nullable;
import android.support.annotation.RequiresApi;
import android.support.v4.app.ActivityCompat;
import android.support.v4.content.ContextCompat;
import android.support.v4.content.res.ResourcesCompat;
import android.support.v7.app.AlertDialog;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;

import java.net.InetAddress;
import java.util.List;

/**
 * Created by Yoshio on 04/10/2018.
 * Updated by Mohamed on 07/11/2018
 */

public class ConnectActivity extends AppCompatActivity implements View.OnClickListener {

    private final String IP = "10.3.141.1";
    private final int PORT = 8808;
    private Object selectedItem;
    private WifiManager wifi;
    private List<ScanResult> results;
    private ArrayAdapter adapter;
    private final int PERMISSION_ACCESS_FINE_LOCATION = 0;

    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {

        // Here, thisActivity is the current activity
        if (ContextCompat.checkSelfPermission(this,
                Manifest.permission.ACCESS_FINE_LOCATION)
                != PackageManager.PERMISSION_GRANTED) {

            ActivityCompat.requestPermissions(this,
                    new String[]{Manifest.permission.ACCESS_FINE_LOCATION}, PERMISSION_ACCESS_FINE_LOCATION);


        }

        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_connect_rover);


        //Set up Wifi
        wifi = (WifiManager) getSystemService(Context.WIFI_SERVICE);

        if (!wifi.isWifiEnabled()) {
            wifi.setWifiEnabled(true);
        }


        getWifiNames();

        // Get reference of widgets from XML layout
        final ListView connectionListView = (ListView) findViewById(R.id.connectionListView);


        // Create an ArrayAdapter from List
        adapter = new ArrayAdapter<String>
                (this, android.R.layout.simple_list_item_1, RoverList.getRoverList().getRoverNames()) {
            @Override
            public View getView(int position, View convertView, ViewGroup parent) {
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
        connectionListView.setAdapter(adapter);

        // Set listener for clicks on items
        connectionListView.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> adapterView, View view, int i, long l) {
                if (selectedItem == null || selectedItem != connectionListView.getItemAtPosition(i)) {
                    connectionListView.setSelector(new ColorDrawable(Color.rgb(189, 189, 189)));
                    selectedItem = connectionListView.getItemAtPosition(i);
                    Controller.getController().setSelectedConnection(RoverList.getRoverList().getRoverFromList(
                            RoverList.getRoverList().getIndexFromName(selectedItem.toString())));
                } else {
                    connectionListView.setSelector(new ColorDrawable(Color.TRANSPARENT));
                    selectedItem = null;
                    Controller.getController().setSelectedConnection(null);

                }
            }
        });

        Button nextBtn = findViewById(R.id.nextBtn);
        nextBtn.setOnClickListener(this);
    }

    private void getWifiNames() {
        if (RoverList.getRoverList().getRovers().size() > 0) {
            RoverList.getRoverList().getRovers().clear();
        }
        registerReceiver(wifiReceiver, new IntentFilter(WifiManager.SCAN_RESULTS_AVAILABLE_ACTION));
        wifi.startScan();
    }

    BroadcastReceiver wifiReceiver = new BroadcastReceiver() {
        @Override
        public void onReceive(Context context, Intent intent) {
            results = wifi.getScanResults();
            unregisterReceiver(this);

            // clear list to avoid old rovers staying.
            RoverList.getRoverList().clearRoverList();

            for (ScanResult result : results) {
                if (result.SSID.contains("Rover")) {
                    RoverList.getRoverList().addRover(result);
                    RoverList.getRoverList().addRoverName(result.SSID);
                    adapter.notifyDataSetChanged();
                }
            }

        }


    };

    @TargetApi(Build.VERSION_CODES.O)
    @RequiresApi(api = Build.VERSION_CODES.O)
    @Override
    public void onClick(View v) {
        Intent intent = new Intent(ConnectActivity.this, RobotBesturen.class);
        startActivity(intent);
        finish();
        if (selectedItem != null) {
            AlertDialog.Builder mBuilder = new AlertDialog.Builder(ConnectActivity.this);
            View mView = getLayoutInflater().inflate(R.layout.dialog_password, null);
            final EditText mPassword = (EditText) mView.findViewById(R.id.insertPw);
            Button connect = (Button) mView.findViewById(R.id.btnConnect);
            Button back = (Button) mView.findViewById(R.id.btnBack);
            mBuilder.setView(mView);
            final AlertDialog dialog = mBuilder.create();
            dialog.show();

            connect.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View view) {
                    if (mPassword.getText().toString().isEmpty()) {
                        Toast.makeText(ConnectActivity.this, "Insert a password!", Toast.LENGTH_SHORT).show();
                    } else {
                        // set selected connection
                        Controller.getController().setSelectedConnection(RoverList.getRoverList().getRoverFromList(RoverList.getRoverList().getIndexFromName(selectedItem.toString())));

                        // get ssid
                        String networkSSID = Controller.getController().getSelectedConnection().SSID;

                        // get password
                        String password = mPassword.getText().toString();

                        WifiConfiguration wifiConfig = new WifiConfiguration();
                        wifiConfig.SSID = String.format("\"%s\"", networkSSID);
                        wifiConfig.preSharedKey = String.format("\"%s\"", password);

                        WifiManager wifiManager = (WifiManager)getSystemService(WIFI_SERVICE);
                        //remember id
                        int netId = wifiManager.addNetwork(wifiConfig);
                        wifiManager.disconnect();
                        wifiManager.enableNetwork(netId, true);
                        wifiManager.reconnect();

                        if(wifiConfig.SSID != null && wifiConfig.SSID.equals("\"" + networkSSID + "\"")) {
                            if (wifi.disconnect() && wifi.enableNetwork(netId, true) && wifi.reconnect()) {
                                Controller.getController().setSelectedRover(
                                        Controller.getController().getSelectedConnection().SSID,
                                        IP,
                                        PORT);
                                Intent intent = new Intent(ConnectActivity.this, RobotBesturen.class);
                                startActivity(intent);
                                finish();
                            } else {
                                Toast.makeText(ConnectActivity.this, "Wrong password inserted.", Toast.LENGTH_SHORT).show();
                            }
                        }
                    }
                }
            });
            back.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View view) {
                    dialog.hide();
                }
            });

        } else {
            Toast.makeText(ConnectActivity.this, "Select a rover first!", Toast.LENGTH_SHORT).show();
        }
    }
}



