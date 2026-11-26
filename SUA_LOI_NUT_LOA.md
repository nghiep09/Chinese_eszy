# Bản v0.3.1 – sửa lỗi thoát ứng dụng khi nhấn loa

## Thay đổi
- Thay PythonJavaClass TTS OnInitListener bằng Java SpeechBridge độc lập.
- Mọi tác vụ tạo engine, phát âm, dừng và shutdown chạy qua Android UI thread.
- Không gọi callback TTS trực tiếp vào Python; nếu Android không có giọng tiếng Trung, thông báo Toast thay vì làm gián đoạn app.
- Bắt lỗi Python khi bấm nút loa để hiển thị thông báo.
- Giữ nguyên tính năng từ vựng, ngữ pháp, JSON, Excel và giao diện v0.3.

## Cách cập nhật
1. Giải nén ZIP này và thay toàn bộ source trên GitHub.
2. Build lại APK bằng GitHub Actions. **Cần build APK mới**, thay file `.py` mà không build sẽ không thêm được lớp Java mới.
3. Cài bản mới (v0.3.1) và thử phát âm cả trong từ vựng và ngữ pháp.
4. Nếu điện thoại chưa có giọng Mandarin, vào **Cài đặt > Chuyển văn bản thành giọng nói (Text-to-speech)**, cài giọng **Tiếng Trung (Trung Quốc)** rồi thử lại.

## Nếu vẫn bị đóng app
Kết nối điện thoại với máy tính, bật USB debugging và lấy log:
`adb logcat -c` rồi bấm loa, sau đó `adb logcat -d -v time > crash.txt`.
Gửi crash.txt để xác định lỗi thực tế (tìm FATAL EXCEPTION, AndroidRuntime, python, ChineseSpeech).

**Lưu ý:** Đây là bản sửa dựa trên việc đọc mã nguồn, chưa được xác nhận bằng chạy APK trên điện thoại thực tế.
