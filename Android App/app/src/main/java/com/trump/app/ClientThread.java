package com.trump.app;

import java.io.BufferedWriter;
import java.io.IOException;
import java.io.OptionalDataException;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.io.BufferedWriter;
import java.io.BufferedReader;
import java.io.InputStreamReader;

import java.io.StreamCorruptedException;
import java.net.InetAddress;
import java.net.Socket;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.net.UnknownHostException;

import android.content.Context;
import android.util.Log;


/**
 * Created by jeffreymoskowitz on 9/16/16.
 */
public class ClientThread implements Runnable {

    // Change these to your specifications
    private static final String ADDRESS = "172.24.1.1";
    private static final int PORT = 8888;

    private static final int BUFFER_SIZE = 1024;

    private Socket socket;

    static Context clientcontext;

    String tag = "MainDebugging";

    private boolean run = false;

    @Override
    public void run() {

        run = true;

        try {
            InetAddress serverAddr = InetAddress.getByName(ADDRESS);
            socket = new Socket(serverAddr, PORT);
            Log.i(tag, "socket created");
        } catch (UnknownHostException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }

    }

    public void write(Context context, String message) {
        clientcontext = context;
        try {
            PrintWriter out = new PrintWriter(new BufferedWriter(new OutputStreamWriter(socket.getOutputStream())), true);
            out.println(message);
            Log.i(tag, "message sent");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public void closeConnection(Context context) {
        clientcontext = context;
        try {
            socket.close();
            Log.i(tag, "Connection closed");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
