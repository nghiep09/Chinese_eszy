package vn.hoctiengtrung;

import android.app.Activity;
import android.content.Context;
import android.os.Bundle;
import android.speech.tts.TextToSpeech;
import android.widget.Toast;
import java.util.Locale;

/**
 * Runs Android TextToSpeech independently of Python callbacks.
 * All engine operations are marshalled onto Android's UI thread.
 */
public final class SpeechBridge {
    private static TextToSpeech engine;
    private static boolean ready = false;
    private static boolean initializing = false;
    private static String pending;
    private static Activity activity;
    private static int generation = 0;

    private SpeechBridge() {}

    private static void toast(final String message) {
        if (activity != null) {
            Toast.makeText(activity.getApplicationContext(), message, Toast.LENGTH_LONG).show();
        }
    }

    public static void play(final Activity caller, final String text) {
        if (caller == null || text == null || text.trim().isEmpty()) return;
        caller.runOnUiThread(new Runnable() {
            @Override public void run() {
                try {
                    activity = caller;
                    pending = text;
                    if (ready && engine != null) {
                        speakPending();
                    } else if (!initializing) {
                        initialize();
                    }
                } catch (Throwable error) {
                    android.util.Log.e("ChineseSpeech", "TTS play failed", error);
                    toast("Không thể phát âm. Hãy kiểm tra dịch vụ chuyển văn bản thành giọng nói.");
                    reset();
                }
            }
        });
    }

    private static void initialize() {
        initializing = true;
        final int current = ++generation;
        final Activity owner = activity;
        engine = new TextToSpeech(owner.getApplicationContext(), new TextToSpeech.OnInitListener() {
            @Override public void onInit(final int status) {
                owner.runOnUiThread(new Runnable() {
                    @Override public void run() {
                        if (current != generation) return;
                        initializing = false;
                        try {
                            if (status != TextToSpeech.SUCCESS || engine == null) {
                                toast("Không khởi tạo được giọng đọc. Hãy kiểm tra cài đặt TTS trên Android.");
                                reset();
                                return;
                            }
                            int result = engine.setLanguage(Locale.SIMPLIFIED_CHINESE);
                            if (result == TextToSpeech.LANG_MISSING_DATA || result == TextToSpeech.LANG_NOT_SUPPORTED) {
                                toast("Cần cài đặt giọng tiếng Trung trong mục Chuyển văn bản thành giọng nói.");
                                reset();
                                return;
                            }
                            ready = true;
                            speakPending();
                        } catch (Throwable error) {
                            android.util.Log.e("ChineseSpeech", "TTS initialization failed", error);
                            toast("Chưa thể phát âm tiếng Trung trên thiết bị này.");
                            reset();
                        }
                    }
                });
            }
        });
    }

    private static void speakPending() {
        final String text = pending;
        pending = null;
        if (text == null || engine == null || !ready) return;
        int result = engine.speak(text, TextToSpeech.QUEUE_FLUSH, new Bundle(), "chinese-lesson");
        if (result == TextToSpeech.ERROR) {
            toast("Không đọc được câu này. Hãy thử bật giọng tiếng Trung trong cài đặt Android.");
        }
    }

    public static void stop(final Activity caller) {
        if (caller == null) return;
        caller.runOnUiThread(new Runnable() {
            @Override public void run() {
                pending = null;
                try { if (engine != null) engine.stop(); }
                catch (Throwable error) { android.util.Log.w("ChineseSpeech", "TTS stop failed", error); }
            }
        });
    }

    public static void shutdown(final Activity caller) {
        if (caller == null) return;
        caller.runOnUiThread(new Runnable() {
            @Override public void run() { reset(); }
        });
    }

    private static void reset() {
        generation++;
        pending = null;
        ready = false;
        initializing = false;
        if (engine != null) {
            try { engine.shutdown(); }
            catch (Throwable error) { android.util.Log.w("ChineseSpeech", "TTS shutdown failed", error); }
            engine = null;
        }
    }
}
