package com.adam.adam.adam;

import android.util.Log;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.Arrays;

/**
 * Created by Hesiris on 20/12/2017.
 */

public class PreferencePacket {
    public String token;
    //type: 0 for tourist 1 for guide
    public int usertype;
    String date;
    String likes;

    public PreferencePacket() {
        likes = "00000";
    }
    public PreferencePacket(String token, int usertype, String date,String goodDays, ArrayList<String> likes) {
        this.token = token;
        this.usertype = usertype;
        this.date = date;
        this.likes = goodDays;
    }

    public void addDay(int day){
        //this.likes |= day;
        char[] ca = this.likes.toCharArray();
        ca[day] = '1';
        this.likes = Arrays.toString(ca);
    }
    public void removeDay(int day){
        //if ( (this.likes & day) == 0)
        //this.likes ^= day;
        char[] ca = this.likes.toCharArray();
        ca[day] = '0';
        this.likes = Arrays.toString(ca);
    }

    public String getJSON(){
        JSONObject prefJSON =new  JSONObject();
        try {
            prefJSON.put("token",token);
            prefJSON.put("usertype",usertype);
            prefJSON.put("date",date);
            prefJSON.put("likes", likes);
        } catch (JSONException e) {
            Log.e("JSON","Failed to parse",e);
        }

        return prefJSON.toString();
    }
}
