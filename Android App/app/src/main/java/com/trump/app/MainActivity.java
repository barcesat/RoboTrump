package com.trump.app;

import android.graphics.Color;
import android.support.v7.app.ActionBarActivity;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.os.Handler;
import android.os.Message;
import android.os.Bundle;
import android.util.Log;
import android.view.MotionEvent;
import android.view.View;
import android.widget.ImageView;
import android.widget.Toast;
import android.speech.RecognizerIntent;

import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStream;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.net.InetAddress;
import java.net.Socket;
import java.net.UnknownHostException;
import java.util.ArrayList;
import java.util.Set;
import java.util.UUID;

// *****************************************
// ************** Warning *****************
// ****************************************
// This is not good code. Please don't use this
// for anything important. It was written at 4am.


public class MainActivity extends ActionBarActivity {

    // All the imageViews (buttons)
    ImageView trump, trumpBorder, button1, button2, uparrow, downarrow, leftarrow, rightarrow;

    // Constants to send to the RPi
    protected static final String GREET_VOTERS = "greet";
    protected static final String STOP_GREETING = "stop greet";
    protected static final String SPEECH = "speech";
    protected static final String STOP_SPEECH = "stop speech";
    protected static final String FORWARD = "forward";
    protected static final String BACKWARDS = "backwards";
    protected static final String LEFT = "left";
    protected static final String RIGHT = "right";
    protected static final String STOP = "stop";
//    protected static final String CHECK_TASK = "check";

    protected static final int SUCCESS_CONNECT = 1;
    protected static final int FAIL_CONNECT = 2;
    protected static final int MESSAGE_READ = 3;
    protected static final int MESSAGE_WRITE = 4;
    protected static final int TIMER_UP = 5;

    private static final String ADDRESS = "192.168.0.100";
    private static final int PORT = 8888;

    private boolean move = false;

    IntentFilter filter;
    BroadcastReceiver receiver;
    String tag = "MainDebugging";
    // Connection status
    private boolean status = false;

    private boolean button1Clicked = false;
    private boolean button2Clicked = false;

    private Socket socket;

    Handler mHandler = new Handler() {
        @Override
        public void handleMessage(Message msg) {
            Log.i(tag, "in handler");
            super.handleMessage(msg);
            switch (msg.what) {
                case SUCCESS_CONNECT:
                    Toast.makeText(getApplicationContext(), "All is very well and good sir", Toast.LENGTH_SHORT).show();
                    Log.i(tag, "connected");
                    status = true;
                    trumpBorder.setVisibility(View.VISIBLE);
                    break;
                case FAIL_CONNECT:
                    // This app really doesn't do a good job of verifying the
                    // connection or receiving messages.
                    Toast.makeText(getApplicationContext(), "Could not connect to candidate", Toast.LENGTH_LONG).show();
                    Log.i(tag, "failed to connect");
                    status = false;
                    trumpBorder.setVisibility(View.INVISIBLE);
                    break;
                case MESSAGE_READ:
                    // No reading at the moment
                    break;
                case MESSAGE_WRITE:
                    if (status) {
                        String str = (String) msg.obj;
                        write(str);
                        Toast.makeText(getApplicationContext(), str, Toast.LENGTH_SHORT).show();
                    }
                    break;
                case TIMER_UP:
                    //
                    break;
            }
        }
    };

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        Log.i(tag, "Creating Screen");
        //initialize the variables
        init();

    }

    // This handles all the button presses (image clicks, technically)
    public void imageClick(View v) {

        Log.i(tag, "button pressed");

        switch (v.getId()) {
            case R.id.trump:
                Log.i(tag, "status is " + status);
                if (!status) {
                    connectToRaspberry();
                } else {
//                    startVoiceRecognitionActivity();
                    closeConnection();
                }
                break;
            case R.id.button1:
                startTask(1);
                break;
            case R.id.button2:
                startTask(2);
                break;
//            case R.id.uparrow:
//                mHandler.obtainMessage(MESSAGE_WRITE, FORWARD).sendToTarget();
//                break;
//            case R.id.downarrow:
//                mHandler.obtainMessage(MESSAGE_WRITE, BACKWARDS).sendToTarget();
//                break;
//            case R.id.leftarrow:
//                mHandler.obtainMessage(MESSAGE_WRITE, LEFT).sendToTarget();
//                break;
//            case R.id.rightarrow:
//                mHandler.obtainMessage(MESSAGE_WRITE, RIGHT).sendToTarget();
//                break;
        }


    }


    private void init() {

        trump = (ImageView) findViewById(R.id.trump);
        trumpBorder = (ImageView) findViewById(R.id.trumpBorder);

        button1 = (ImageView) findViewById(R.id.button1);
        button2 = (ImageView) findViewById(R.id.button2);

        // The arrows are meant to control Robo-Trump's directional
        // movements. At GeekCon we didn't quite get this synced up
        // in time and ended up doing it a different way, but this
        // app code works if you're inclined to use it.

        uparrow = (ImageView) findViewById(R.id.uparrow);
        uparrow.setOnTouchListener(new View.OnTouchListener() {
            @Override
            public boolean onTouch(View v, MotionEvent event) {
                if (event.getAction() == MotionEvent.ACTION_DOWN && !move) {
                    mHandler.obtainMessage(MESSAGE_WRITE, FORWARD).sendToTarget();
                    move = true;
                } else if (event.getAction() == MotionEvent.ACTION_UP && move) {
                    mHandler.obtainMessage(MESSAGE_WRITE, STOP).sendToTarget();
                    move = false;
                }
                return true;
            }
        });
        downarrow = (ImageView) findViewById(R.id.downarrow);
        downarrow.setOnTouchListener(new View.OnTouchListener() {
            @Override
            public boolean onTouch(View v, MotionEvent event) {
                if (event.getAction() == MotionEvent.ACTION_DOWN && !move) {
                    mHandler.obtainMessage(MESSAGE_WRITE, BACKWARDS).sendToTarget();
                    move = true;
                } else if (event.getAction() == MotionEvent.ACTION_UP && move) {
                    mHandler.obtainMessage(MESSAGE_WRITE, STOP).sendToTarget();
                    move = false;
                }
                return true;
            }
        });
        leftarrow = (ImageView) findViewById(R.id.leftarrow);
        leftarrow.setOnTouchListener(new View.OnTouchListener() {
            @Override
            public boolean onTouch(View v, MotionEvent event) {
                if (event.getAction() == MotionEvent.ACTION_DOWN && !move) {
                    mHandler.obtainMessage(MESSAGE_WRITE, LEFT).sendToTarget();
                    move = true;
                } else if (event.getAction() == MotionEvent.ACTION_UP && move) {
                    mHandler.obtainMessage(MESSAGE_WRITE, STOP).sendToTarget();
                    move = false;
                }
                return true;
            }
        });
        rightarrow = (ImageView) findViewById(R.id.rightarrow);
        rightarrow.setOnTouchListener(new View.OnTouchListener() {
            @Override
            public boolean onTouch(View v, MotionEvent event) {
                if (event.getAction() == MotionEvent.ACTION_DOWN && !move) {
                    mHandler.obtainMessage(MESSAGE_WRITE, RIGHT).sendToTarget();
                    move = true;
                } else if (event.getAction() == MotionEvent.ACTION_UP && move) {
                    mHandler.obtainMessage(MESSAGE_WRITE, STOP).sendToTarget();
                    move = false;
                }
                return true;
            }
        });

    }

    // A button has been pressed
    private void startTask(int i) {
        if (status) {
            switch (i) {
                case 1:
                    if (status) {
                        if (!button1Clicked) {
                            write(GREET_VOTERS);
                            button1.setBackgroundColor(Color.parseColor("#4E0909"));
                            button1Clicked = true;
                        } else {
                            write(STOP_GREETING);
                            button1.setBackgroundColor(Color.parseColor("#9C1213"));
                            button1Clicked = false;
                        }
                    }
                    break;
                case 2:
                    if (status) {
                        if (!button2Clicked) {
                            write(SPEECH);
                            button2.setBackgroundColor(Color.parseColor("#4E0909"));
                            button2Clicked = true;
                        } else {
                            write(STOP_SPEECH);
                            button2.setBackgroundColor(Color.parseColor("#9C1213"));
                            button2Clicked = false;
                        }
                    }
                    break;
            }

        } else {
            showDisconnected();
        }
    }

    //switch to Pi
    private void connectToRaspberry() {
        new Thread(new ClientThread()).start();
    }

    class ClientThread implements Runnable {

        @Override
        public void run() {
            // Where the socket connection magic happens
            try {
                InetAddress serverAddr = InetAddress.getByName(ADDRESS);
                socket = new Socket(serverAddr, PORT);
                Log.i(tag, "socket created");
                status = true;
                mHandler.obtainMessage(SUCCESS_CONNECT).sendToTarget();
            } catch (UnknownHostException e) {
                e.printStackTrace();
                mHandler.obtainMessage(FAIL_CONNECT).sendToTarget();
            } catch (IOException e) {
                e.printStackTrace();
                mHandler.obtainMessage(FAIL_CONNECT).sendToTarget();
            }
        }


    }

    public void write(String message) {
        try {
            PrintWriter out = new PrintWriter(new BufferedWriter(new OutputStreamWriter(socket.getOutputStream())), true);
            out.println(message);
            Log.i(tag, "message sent");
            Toast.makeText(this, "Message Sent", Toast.LENGTH_SHORT);
        } catch (IOException e) {
            e.printStackTrace();
            Log.i(tag, "message failed");
            Toast.makeText(this, "Message Failed", Toast.LENGTH_SHORT);
            showDisconnected();
        }
    }

    // This will be called if the app realizes the connection is no longer working,
    // for instance if you walk out of range and then try to use it
    private void showDisconnected() {
        trumpBorder.setVisibility(View.INVISIBLE);
        button1.setBackgroundColor(Color.parseColor("#9C1213"));
        button2.setBackgroundColor(Color.parseColor("#9C1213"));
    }

    private void closeConnection() {
        if (socket.isConnected()) {
            try {
                socket.close();
                status = false;
                showDisconnected();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }


    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.main, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();
        if (id == R.id.action_settings) {
            return true;
        }
        return super.onOptionsItemSelected(item);
    }

    @Override
    protected void onPause() {
        super.onPause();
    }


    @Override
    protected void onResume() {
        super.onResume();

    }

    protected void onStop() {
        super.onStop();
        if (status) {
            try {
                socket.close();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
        status = false;
        showDisconnected();
    }
}
