package com.example.kdel.testfinalproject;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;

import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.HttpUrl;
import okhttp3.MediaType;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;

import org.json.JSONArray;
import org.json.JSONObject;
import org.json.JSONException;

import java.util.HashMap;
import java.util.Map;
import java.util.List;
import java.util.ArrayList;

import android.util.Log;
import android.widget.SimpleAdapter;
import android.widget.TextView;

import java.io.IOException;

public class MainActivity extends AppCompatActivity {
    OkHttpClient mOkHttpClient;
    TextView responseVar;
    String TeamName = "Blackhawks";
    String TeamCity = "Chicago";
    String ArenaName = "Broadhouse Bully";
    public static final MediaType JSON = MediaType.parse("application/json; charset=utf-8");
    public static final MediaType STR = MediaType.parse("application/text; charset=utf-8");


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        responseVar = (TextView) findViewById(R.id.textview);
        mOkHttpClient = new OkHttpClient();
        HttpUrl requrl = HttpUrl.parse("https://osucs496finalproject.appspot.com/teams");
        String bodyString = "{\"teamName\": \"" + TeamName + "\" , \"teamCity\": \"" + TeamCity + "\", \"arenaName\": \"" + ArenaName + "\"}";
        try{
            //JSONObject obj = new JSONObject(bodyString);

            RequestBody body = RequestBody.create(JSON, bodyString);
            Request request = new Request.Builder()
                    .url(requrl)
                    .post(body)
                    .build();

            mOkHttpClient.newCall(request).enqueue(new Callback() {
                @Override
                public void onFailure(Call call, IOException e) {
                    e.printStackTrace();
                }

                @Override
                public void onResponse(Call call, Response response) throws IOException {
                    String r = response.body().string();
                }
            });
        }catch (Throwable tx){
            Log.e("My app", "Could not JSON" + bodyString);
        }
    }
}
