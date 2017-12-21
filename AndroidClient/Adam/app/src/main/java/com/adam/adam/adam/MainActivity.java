package com.adam.adam.adam;

import android.app.Activity;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.content.Intent;
import android.widget.Toast;

import com.facebook.CallbackManager;
import com.facebook.FacebookCallback;
import com.facebook.FacebookException;
import com.facebook.FacebookSdk;
import com.facebook.appevents.AppEventsLogger;
import com.facebook.login.LoginResult;
import com.facebook.login.widget.LoginButton;

import java.util.Arrays;

public class MainActivity extends Activity {

    CallbackManager callbackManager;
    LoginButton loginButton;
    Button instaLoginButton;
    TextView login_result;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        FacebookSdk.sdkInitialize(getApplicationContext());
        AppEventsLogger.activateApp(this);

        callbackManager = CallbackManager.Factory.create();
        loginButton = (LoginButton) findViewById(R.id.login_button);
       // loginButton.setReadPermissions("email");
        loginButton.setReadPermissions(Arrays.asList("user_posts","user_status","email","user_likes","user_birthday","user_videos"));

        //authButton.setReadPermissions(Arrays.asList("user_status"));
        instaLoginButton = (Button) findViewById(R.id.instaLogin);

        login_result = (TextView) findViewById(R.id.login_result);


        loginButton.registerCallback(callbackManager, new FacebookCallback<LoginResult>() {
            @Override
            public void onSuccess(LoginResult loginResult) {
                Log.d("LoginToken",
                        "User ID: "
                                + loginResult.getAccessToken().getUserId()
                                + "\n" +
                                "Auth Token: "
                                + loginResult.getAccessToken().getToken()
                );
                Intent startPreferencesActivityIntent = new Intent(MainActivity.this, PreferencesActivity.class);

                startActivity(startPreferencesActivityIntent);
            }

            @Override
            public void onCancel() {
                //Toast.makeText( this,"Login Cancelled", Toast.LENGTH_SHORT).show();
                login_result.setText("Login Cancelled");
            }

            @Override
            public void onError(FacebookException exception) {
                login_result.setText("Login failed. Reason: " + exception.getMessage());
            }
        });

        instaLoginButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent startPreferencesActivityIntent = new Intent(MainActivity.this, PreferencesActivity.class);

                startActivity(startPreferencesActivityIntent);
            }
        });
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        callbackManager.onActivityResult(requestCode, resultCode, data);
        super.onActivityResult(requestCode, resultCode, data);
    }

}
