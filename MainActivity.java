package com.damithri.cutewordfinderapp;

import android.os.Bundle;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;

import androidx.activity.OnBackPressedCallback;
import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity {

    private WebView myWebView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        myWebView = findViewById(R.id.webView);

        // Enable JavaScript & DOM storage
        WebSettings webSettings = myWebView.getSettings();
        webSettings.setJavaScriptEnabled(true);
        webSettings.setDomStorageEnabled(true);   // ✅ Fix for localStorage
        webSettings.setDatabaseEnabled(true);     // ✅ Allow IndexedDB
        webSettings.setSupportZoom(false);        // Optional (disable zoom)

        // Keep browsing inside the app
        myWebView.setWebViewClient(new WebViewClient());

        // 🌸 Load your deployed Streamlit app
        myWebView.loadUrl("https://dictionary-web-app-guovdglxgjtq2p9ugzxprf.streamlit.app");

        // ✅ Handle back gesture with dispatcher (modern way)
        getOnBackPressedDispatcher().addCallback(this, new OnBackPressedCallback(true) {
            @Override
            public void handleOnBackPressed() {
                if (myWebView.canGoBack()) {
                    myWebView.goBack();
                } else {
                    finish();
                }
            }
        });
    }
}
