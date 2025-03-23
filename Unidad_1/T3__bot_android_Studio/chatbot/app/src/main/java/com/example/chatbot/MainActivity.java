package com.example.chatbot;

import android.content.Intent;
import android.content.pm.PackageManager;
import android.graphics.Bitmap;
import android.net.Uri;
import android.os.Bundle;
import android.provider.MediaStore;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.Toast;

import androidx.activity.result.ActivityResultLauncher;
import androidx.activity.result.contract.ActivityResultContracts;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;

import com.google.android.material.button.MaterialButton;
import com.google.android.material.textfield.TextInputEditText;

public class MainActivity extends AppCompatActivity {

    private static final int PERMISSION_REQUEST_CODE = 100;
    private TextInputEditText nameEditText, ageEditText;
    private MaterialButton submitButton, changeBackgroundButton;
    private ImageView backgroundImageView;

    // ActivityResultLauncher para seleccionar imagen
    private final ActivityResultLauncher<Intent> pickImageLauncher = registerForActivityResult(
            new ActivityResultContracts.StartActivityForResult(),
            result -> {
                if (result.getResultCode() == RESULT_OK && result.getData() != null) {
                    Uri imageUri = result.getData().getData();
                    try {
                        Bitmap bitmap = MediaStore.Images.Media.getBitmap(getContentResolver(), imageUri);
                        backgroundImageView.setImageBitmap(bitmap);
                        backgroundImageView.setVisibility(ImageView.VISIBLE);
                    } catch (Exception e) {
                        e.printStackTrace();
                        Toast.makeText(this, "Error al cargar la imagen", Toast.LENGTH_SHORT).show();
                    }
                }
            });

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // Inicializar vistas
        nameEditText = findViewById(R.id.nameEditText);
        ageEditText = findViewById(R.id.ageEditText);
        submitButton = findViewById(R.id.submitButton);
        changeBackgroundButton = findViewById(R.id.changeBackgroundButton);
        backgroundImageView = findViewById(R.id.backgroundImageView);

        // Solicitar permisos en tiempo de ejecución
        checkAndRequestPermissions();

        // Configurar el listener del botón "Enviar"
        submitButton.setOnClickListener(v -> {
            String name = nameEditText.getText().toString().trim();
            String age = ageEditText.getText().toString().trim();

            if (name.isEmpty() || age.isEmpty()) {
                Toast.makeText(this, "Por favor, completa todos los campos", Toast.LENGTH_SHORT).show();
            } else {
                // Redirigir a ChatbotActivity
                Intent intent = new Intent(MainActivity.this, ChatbotActivity.class);
                intent.putExtra("name", name); // Pasar el nombre a la siguiente actividad
                intent.putExtra("age", age);  // Pasar la edad a la siguiente actividad
                startActivity(intent);
            }
        });

        // Configurar el listener del botón "Cambiar fondo"
        changeBackgroundButton.setOnClickListener(v -> {
            Intent intent = new Intent();
            intent.setType("image/*");
            intent.setAction(Intent.ACTION_GET_CONTENT);
            pickImageLauncher.launch(Intent.createChooser(intent, "Seleccionar imagen de fondo"));
        });
    }

    // Método para verificar y solicitar permisos
    private void checkAndRequestPermissions() {
        String[] permissions = {
                android.Manifest.permission.INTERNET,
                android.Manifest.permission.CAMERA,
                android.Manifest.permission.RECORD_AUDIO,
                android.Manifest.permission.WRITE_EXTERNAL_STORAGE,
                android.Manifest.permission.READ_EXTERNAL_STORAGE
        };

        boolean allPermissionsGranted = true;
        for (String permission : permissions) {
            if (ContextCompat.checkSelfPermission(this, permission) != PackageManager.PERMISSION_GRANTED) {
                allPermissionsGranted = false;
                break;
            }
        }

        if (!allPermissionsGranted) {
            ActivityCompat.requestPermissions(this, permissions, PERMISSION_REQUEST_CODE);
        }
    }

    // Método para manejar la respuesta de la solicitud de permisos
    @Override
    public void onRequestPermissionsResult(int requestCode, String[] permissions, int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        if (requestCode == PERMISSION_REQUEST_CODE) {
            for (int i = 0; i < grantResults.length; i++) {
                if (grantResults[i] != PackageManager.PERMISSION_GRANTED) {
                    Toast.makeText(this, "Permiso denegado: " + permissions[i], Toast.LENGTH_SHORT).show();
                }
            }
        }
    }
}