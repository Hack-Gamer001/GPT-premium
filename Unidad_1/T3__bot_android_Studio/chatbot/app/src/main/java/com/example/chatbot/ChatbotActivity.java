package com.example.chatbot;

import android.content.Intent;
import android.os.Bundle;
import android.speech.RecognizerIntent;
import android.speech.tts.TextToSpeech;
import android.widget.TextView;
import android.widget.Toast;
import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.widget.Toolbar;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import com.google.android.material.button.MaterialButton;
import com.google.android.material.floatingactionbutton.FloatingActionButton;
import com.google.android.material.textfield.TextInputEditText;

import java.util.ArrayList;
import java.util.List;
import java.util.Locale;
import okhttp3.*;
import org.json.JSONException;
import org.json.JSONObject;
import java.io.IOException;

public class ChatbotActivity extends AppCompatActivity {

    private RecyclerView chatRecyclerView;
    private TextInputEditText messageEditText;
    private FloatingActionButton sendButton;
    private MaterialButton audioButton;
    private TextView welcomeTextView;
    private ChatAdapter chatAdapter;
    private List<Message> messageList;
    private OkHttpClient httpClient;
    private TextToSpeech textToSpeech;
    private static final int REQUEST_CODE_SPEECH_INPUT = 1000;
    private static final String API_URL = "https://1579-2001-1388-5e21-c7bc-5535-6bac-b0af-6dca.ngrok-free.app/chat"; // URL de la API

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_chatbot);

        // Configurar la toolbar
        Toolbar toolbar = findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);
        if (getSupportActionBar() != null) {
            getSupportActionBar().setDisplayShowTitleEnabled(false);
        }

        // Obtener los datos enviados desde MainActivity
        String name = getIntent().getStringExtra("name");
        String age = getIntent().getStringExtra("age");

        // Inicializar vistas
        welcomeTextView = findViewById(R.id.welcomeTextView);
        chatRecyclerView = findViewById(R.id.chatRecyclerView);
        messageEditText = findViewById(R.id.messageEditText);
        sendButton = findViewById(R.id.sendButton);
        audioButton = findViewById(R.id.audioButton);

        // Personalizar mensaje de bienvenida
        if (name != null && age != null) {
            welcomeTextView.setText("¡Hola " + name + "! Soy tu Profe Robot. ¿En qué puedo ayudarte hoy?");
        }

        // Configurar RecyclerView
        messageList = new ArrayList<>();
        chatAdapter = new ChatAdapter(messageList);
        chatRecyclerView.setLayoutManager(new LinearLayoutManager(this));
        chatRecyclerView.setAdapter(chatAdapter);

        // Inicializar OkHttpClient
        httpClient = new OkHttpClient();

        // Inicializar TextToSpeech
        textToSpeech = new TextToSpeech(this, status -> {
            if (status != TextToSpeech.ERROR) {
                textToSpeech.setLanguage(new Locale("es", "ES"));
            }
        });

        // Manejar el clic del botón "Enviar"
        sendButton.setOnClickListener(v -> {
            String messageText = messageEditText.getText().toString().trim();
            if (!messageText.isEmpty()) {
                sendMessage(messageText);
            }
        });

        // Manejar el clic del botón "Hablar por audio"
        audioButton.setOnClickListener(v -> {
            startVoiceInput();
        });

        // Añadir mensaje de bienvenida inicial al chat
        if (messageList.isEmpty()) {
            messageList.add(new Message("¡Hola! Soy tu Profe Robot. ¿En qué puedo ayudarte hoy?", false));
            chatAdapter.notifyItemInserted(0);
        }
    }

    private void sendMessage(String messageText) {
        // Agregar mensaje del usuario
        messageList.add(new Message(messageText, true)); // true = emisor
        chatAdapter.notifyItemInserted(messageList.size() - 1);

        // Limpiar el EditText
        messageEditText.setText("");

        // Desplazar el RecyclerView al final
        chatRecyclerView.scrollToPosition(messageList.size() - 1);

        // Enviar mensaje a la API de Llama
        sendMessageToLlamaAPI(messageText);
    }

    private void sendMessageToLlamaAPI(String userMessage) {
        // Crear el cuerpo de la solicitud en formato JSON
        JSONObject jsonBody = new JSONObject();
        try {
            jsonBody.put("pregunta", userMessage);
        } catch (JSONException e) {
            e.printStackTrace();
        }

        // Crear la solicitud HTTP POST
        RequestBody requestBody = RequestBody.create(MediaType.parse("application/json"), jsonBody.toString());
        Request request = new Request.Builder()
                .url(API_URL)
                .post(requestBody)
                .build();

        // Enviar la solicitud de manera asíncrona
        httpClient.newCall(request).enqueue(new Callback() {
            @Override
            public void onFailure(Call call, IOException e) {
                e.printStackTrace();
                runOnUiThread(() -> {
                    // Mostrar un mensaje de error
                    messageList.add(new Message("Error al conectar con el asistente.", false));
                    chatAdapter.notifyItemInserted(messageList.size() - 1);
                    chatRecyclerView.scrollToPosition(messageList.size() - 1);
                });
            }

            @Override
            public void onResponse(Call call, Response response) throws IOException {
                if (response.isSuccessful()) {
                    try {
                        // Obtener la respuesta de la API
                        String responseBody = response.body().string();
                        JSONObject jsonResponse = new JSONObject(responseBody);
                        String assistantMessage = jsonResponse.getString("respuesta");

                        // Agregar la respuesta del asistente
                        runOnUiThread(() -> {
                            messageList.add(new Message(assistantMessage, false)); // false = receptor
                            chatAdapter.notifyItemInserted(messageList.size() - 1);
                            chatRecyclerView.scrollToPosition(messageList.size() - 1);

                            // Hablar la respuesta
                            textToSpeech.speak(assistantMessage, TextToSpeech.QUEUE_FLUSH, null, null);
                        });
                    } catch (JSONException e) {
                        e.printStackTrace();
                        runOnUiThread(() -> {
                            messageList.add(new Message("Error al procesar la respuesta del asistente.", false));
                            chatAdapter.notifyItemInserted(messageList.size() - 1);
                            chatRecyclerView.scrollToPosition(messageList.size() - 1);
                        });
                    }
                } else {
                    runOnUiThread(() -> {
                        // Mostrar un mensaje de error
                        messageList.add(new Message("Error en la respuesta del asistente.", false));
                        chatAdapter.notifyItemInserted(messageList.size() - 1);
                        chatRecyclerView.scrollToPosition(messageList.size() - 1);
                    });
                }
            }
        });
    }

    private void startVoiceInput() {
        Intent intent = new Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH);
        intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL, RecognizerIntent.LANGUAGE_MODEL_FREE_FORM);
        intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE, new Locale("es", "ES"));
        intent.putExtra(RecognizerIntent.EXTRA_PROMPT, "¿En qué puedo ayudarte?");
        try {
            startActivityForResult(intent, REQUEST_CODE_SPEECH_INPUT);
        } catch (Exception e) {
            Toast.makeText(getApplicationContext(), "Lo siento, tu dispositivo no soporta entrada de voz", Toast.LENGTH_SHORT).show();
        }
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (requestCode == REQUEST_CODE_SPEECH_INPUT && resultCode == RESULT_OK && data != null) {
            ArrayList<String> result = data.getStringArrayListExtra(RecognizerIntent.EXTRA_RESULTS);
            if (result != null && !result.isEmpty()) {
                String spokenText = result.get(0);
                messageEditText.setText(spokenText);
                sendMessage(spokenText);
            }
        }
    }

    @Override
    protected void onDestroy() {
        if (textToSpeech != null) {
            textToSpeech.stop();
            textToSpeech.shutdown();
        }
        super.onDestroy();
    }
}