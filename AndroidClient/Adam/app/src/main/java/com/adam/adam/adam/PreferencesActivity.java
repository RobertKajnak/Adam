package com.adam.adam.adam;

import android.content.Intent;
import android.os.AsyncTask;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.CheckBox;
import android.widget.DatePicker;
import android.widget.LinearLayout;
import android.widget.RadioButton;
import android.widget.ScrollView;
import android.widget.TextView;
import android.widget.Toast;

import com.facebook.AccessToken;

import org.json.JSONObject;
import org.w3c.dom.Text;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.net.Socket;
import java.net.SocketException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;

public class PreferencesActivity extends AppCompatActivity {

    final String SERVERIP="10.0.2.2";
    final int SERVERPORT = 23260;

    ScrollView mScrollViewMain;
    TextView mGreetingText;
    DatePicker mDatePicker;
    Button mButtonConfirm;
    DatePicker mDate;
    TextView mLastMessage; // for debugging mainly
    ArrayList<CheckBox> mCheckboxes = new ArrayList<>();
    LinearLayout mLinearLayoutCheckboxes;
    RadioButton mRadioGuide;
    LinearLayout weekdayLayout;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_preferences);


        //Intent intentThatStartedThisActivity = getIntent();

        mGreetingText = (TextView) findViewById(R.id.text_greeting);
        mDatePicker = (DatePicker) findViewById(R.id.datePicker);
        mButtonConfirm = (Button) findViewById(R.id.button_confirm);
        mLinearLayoutCheckboxes = (LinearLayout) findViewById(R.id.listview_checkboxes);
        mScrollViewMain = (ScrollView) findViewById(R.id.scrollViewMain);
        mLastMessage = (TextView) findViewById(R.id.lastMessageTextView);
        mRadioGuide = (RadioButton) findViewById(R.id.radioGuide);


        final AccessToken accessToken = AccessToken.getCurrentAccessToken();
        if(accessToken==null || accessToken.isExpired()){
            mGreetingText.setText("Log in not functioning properly. PLease restart the app");
        }
        else{
            //mGreetingText.setText(
             //       "User ID: "+ accessToken.getUserId());
            mGreetingText.setText("Greetings, John!\nFill in your preferences and we'll find you the perfect match");
        }

        mButtonConfirm.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                PreferencePacket prefs = new PreferencePacket();
                prefs.token = accessToken.getToken();
                prefs.usertype = mRadioGuide.isChecked()?1:0;
                if (prefs.usertype == 0){
                    Date date1= (Date) new Date
                        (mDatePicker.getYear()-1900, mDatePicker.getMonth(), mDatePicker.getDayOfMonth());
                    SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd");
                    String dateString = sdf.format(date1);
                    prefs.date = dateString;
                }
                else{
                    ///guide section
                }
                //prefs.likes.add();

                for ( int i=0; i < mLinearLayoutCheckboxes.getChildCount(); i++) {
                    CheckBox cb = (CheckBox) mLinearLayoutCheckboxes.getChildAt(i);
                    if (cb.isChecked()){
                        prefs.addDay(i);
                    }
                }

                new ServerComm().execute(prefs.getJSON());
                Intent startChatApplicationIntent = new Intent(PreferencesActivity.this,ChatActivity.class);

                startActivity(startChatApplicationIntent);
            }
        });
        mCheckboxes.add((CheckBox)findViewById(R.id.checkbox_cafe));
        mCheckboxes.add((CheckBox)findViewById(R.id.checkbox_mus));
        mCheckboxes.add((CheckBox)findViewById(R.id.checkbox_old));
        mCheckboxes.add((CheckBox)findViewById(R.id.checkbox_uniq));
        mCheckboxes.add((CheckBox)findViewById(R.id.checkbox_park));
    }

    public  void onCheckboxTicked(View view){
        boolean isAtleastOne = false;
        for (CheckBox cb: mCheckboxes ) {
            if (cb.isChecked()){
                isAtleastOne = true;
                break;
            }
        }
        if (isAtleastOne){
            mButtonConfirm.setVisibility(View.VISIBLE);
            mScrollViewMain.fullScroll(View.FOCUS_DOWN);
            mScrollViewMain.invalidate();
        }
        else{
            mButtonConfirm.setVisibility(View.GONE);
        }
    }

    public void onRadioButtonClicked(View view) {
        // Is the button now checked?
        boolean checked = ((RadioButton) view).isChecked();
        if (checked){
            //mButtonConfirm.setVisibility(View.VISIBLE);
            mLinearLayoutCheckboxes.setVisibility(View.VISIBLE);
            mDatePicker.setVisibility(View.VISIBLE);
        }

        // Check which radio button was clicked
        /// Impement this if different options are needed for guide and tourist
        switch(view.getId()) {
            case R.id.radioGuide:
                if (checked)
                    //Toast.makeText(this, "Guide Selected. Will be implemented", Toast.LENGTH_SHORT).show();

                    //mDatePicker.setVisibility(View.GONE);
                    break;
            case R.id.radioTourist:
                if (checked)

                    break;
        }
    }

    public class ServerComm extends AsyncTask<String,String,String> {

        @Override
        protected void onPostExecute(String result) {
            if (result == null || result.isEmpty()) {
                Toast.makeText(PreferencesActivity.this, "Failed to connect", Toast.LENGTH_LONG).show();
                //mLastMessage.setText("Failed to connect");
            }
            else {
                //mLastMessage.setText(result);
            }
        }

        @Override
        protected void onProgressUpdate(String... values) {
            if (values!=null ) {
                //mLastMessage.setText(values[0]);
                //Toast.makeText(PreferencesActivity.this, values[0], Toast.LENGTH_SHORT).show();
                super.onProgressUpdate(values);
            }
        }

        @Override
        protected String doInBackground(String... params) {
            String msg = "";
            Socket socket = null;
            publishProgress("Attempting to establish conenction");

            try {
                try {
                    //socket = new Socket("176.63.17.182", 12034);
                    socket = new Socket(SERVERIP,SERVERPORT);
                    //socket = new Socket();
                }catch (Exception e){
                    return "Connection Failed: " + e.getMessage();
                }
                //publishProgress("Socket created \n");



                BufferedReader in = new BufferedReader(new InputStreamReader(
                        socket.getInputStream()));
                PrintWriter out = new PrintWriter(new BufferedWriter(
                        new OutputStreamWriter(socket.getOutputStream())), true);

                //publishProgress("IO ready for transmission \n");

                out.println(params[0]);

               // publishProgress("Message sent, waiting for response");

                msg= in.readLine();
                /*while (!msg.equals("END")){
                    studentList.add(Student.deserialize(msg));
                    msg= in.readLine();
                }*/


                in.close();
                out.close();
                socket.close();
                //publishProgress("Connection closed.");
                return msg;

            } catch (Exception e) {
                e.printStackTrace();
            }
            return null;
        }

    }

}
