package com.example.chatbot;

public class Message {
    private String text;
    private boolean isSender;

    public Message(String text, boolean isSender) {
        this.text = text;
        this.isSender = isSender;
    }

    public String getText() {
        return text;
    }

    public boolean isSender() {
        return isSender;
    }
}