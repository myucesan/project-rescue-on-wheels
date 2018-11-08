package com.metabotsrow.rowapp;

import android.Manifest;
import android.annotation.TargetApi;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.content.pm.PackageManager;
import android.graphics.Typeface;
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
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.ListView;
import android.widget.TextView;

import java.math.BigInteger;
import java.net.InetAddress;
import java.net.UnknownHostException;
import java.nio.ByteOrder;
import java.time.Duration;
import java.util.List;
import java.util.concurrent.Callable;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;
import java.util.concurrent.TimeUnit;

/**
 * Created by Yoshio on 04/10/2018.
 * Updated by Mohamed on 07/11/2018
 */

public class ConnectActivity extends AppCompatActivity implements View.OnClickListener {

    private Object selectedItem;
    private WifiManager wifi;
    private List<ScanResult> results;
    private ArrayAdapter adapter;
    private final int PERMISSION_ACCESS_FINE_LOCATION = 0;
    private InetAddress myAddr;

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

//        // Simple check if rovers are already initialized
//        if(RoverList.getRoverList().getRovers().size() == 0){
//            // Initializing rovers only if they aren't already
//            RoverList.getRoverList().addRover(new Rover("DUMMY ROVER 2", "192.168.192.52", 8802));
//            RoverList.getRoverList().addRover(new Rover("ROVER 8", "10.3.141.1", 8812));
//            RoverList.getRoverList().addRover(new Rover("DUMMY ROVER 11", "10.3.141.1", 8810));
//            RoverList.getRoverList().addRover(new Rover("DUMMY ROVER 21", "10.3.141.1", 8821));
//        }

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
                    selectedItem = connectionListView.getItemAtPosition(i);
                    Controller.getController().setSelectedConnection(RoverList.getRoverList().getRoverFromList(
                            RoverList.getRoverList().getIndexFromName(selectedItem.toString())));
                    String s = selectedItem.toString();
                    Log.d("DEBUG_TAG", s);
                }
            });

            Button connectBtn = findViewById(R.id.connectBtn);
            connectBtn.setOnClickListener(this);
        }

        private void getWifiNames () {
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

                for (ScanResult result : results) {
                    if (result.SSID.contains("UPC")) {
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
        public void onClick (View v){
            // Check if any item is selected.
            if (selectedItem.toString().contains("UPC")) {
                Controller.getController().setSelectedConnection(RoverList.getRoverList().getRoverFromList(
                        RoverList.getRoverList().getIndexFromName(selectedItem.toString())));

                String networkSSID = Controller.getController().getSelectedConnection().SSID;
                String networkPass = "gsEcYi8iw4wi";

                WifiConfiguration conf = new WifiConfiguration();
                conf.SSID = "\"" + networkSSID + "\"";

                if (Controller.getController().getSelectedConnection().capabilities.contains("WPA")) {
                    conf.preSharedKey = "\"" + networkPass + "\"";
                } else if (Controller.getController().getSelectedConnection().capabilities.contains("WEP")) {
                    conf.wepKeys[0] = "\"" + networkPass + "\"";
                    conf.wepTxKeyIndex = 0;
                    conf.allowedKeyManagement.set(WifiConfiguration.KeyMgmt.NONE);
                    conf.allowedGroupCiphers.set(WifiConfiguration.GroupCipher.WEP40);
                } else {
                    conf.allowedKeyManagement.set(WifiConfiguration.KeyMgmt.NONE);
                }

                wifi.addNetwork(conf);

                List<WifiConfiguration> list = wifi.getConfiguredNetworks();
                for( WifiConfiguration b : list ) {
                    if(b.SSID != null && b.SSID.equals("\"" + networkSSID + "\"")) {
                        wifi.disconnect();
                        wifi.enableNetwork(b.networkId, true);
                        wifi.reconnect();
                        if (wifi.enableNetwork(b.networkId, true) && wifi.reconnect()) {

                          try {
                                Thread.sleep(4000);
                            } catch (InterruptedException e) {
                                e.printStackTrace();
                            }

                            int ip = wifi.getConnectionInfo().getIpAddress();
                            ip = (ByteOrder.nativeOrder().equals(ByteOrder.LITTLE_ENDIAN)) ?
                                    Integer.reverseBytes(ip) : ip;

                            byte[] ipAddress = BigInteger.valueOf(ip).toByteArray();

                            try {
                                myAddr = InetAddress.getByAddress(ipAddress);
                            } catch (UnknownHostException e) {
                                e.printStackTrace();
                            }

                            Controller.getController().setSelectedRover(
                                    myAddr.getHostAddress(),
                                    Integer.toString(wifi.getConnectionInfo().getIpAddress()),
                                    8802
                            );
                            break;
                        }
                    }
                }


                Intent intent = new Intent(this, RobotBesturen.class);
                startActivity(intent);
                finish();
            }
        }

    }
