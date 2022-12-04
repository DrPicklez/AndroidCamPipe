package com.example.cameragrabber;

import android.os.AsyncTask;
import android.util.Log;

public class ConnectTask extends AsyncTask<String, String, NetworkMan> {

    @Override
    protected NetworkMan doInBackground(String... message) {

        //we create a TCPClient object
        NetworkMan mNetworkMan = new NetworkMan(new NetworkMan.OnMessageReceived() {
            @Override
            //here the messageReceived method is implemented
            public void messageReceived(String message) {
                //this method calls the onProgressUpdate
                publishProgress(message);
            }
        });
        mNetworkMan.run();

        return null;
    }

    @Override
    protected void onProgressUpdate(String... values) {
        super.onProgressUpdate(values);
        //response received from server
        Log.d("test", "response " + values[0]);
        //process server response here....

    }
}
