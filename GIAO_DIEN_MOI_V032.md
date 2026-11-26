# Giao diện mới v0.3.2

Thiết kế trang chủ dựa trên hình ảnh người dùng cung cấp: nền kem, màu đỏ chủ đạo, thẻ bài học hôm nay nổi bật, các ô danh mục 2 cột, từ vựng mới và thanh điều hướng phía dưới.

## Cấu trúc
- `home_redesign.py`: giao diện trang chủ mới viết bằng Kivy (không dùng CSS HTML).
- `grammar_ui.py`: sử dụng giao diện mới và thêm trang Hồ sơ học tập.
- `main.py`: giữ chức năng từ vựng cũ, ngữ pháp, và TextToSpeech của v0.3.1.
- `buildozer.spec`: cập nhật version 0.3.2.

## Hành vi
- Chạm **Từ vựng** để trở lại toàn bộ chức năng từ vựng cũ.
- Chạm **Ngữ pháp** hoặc **Bài học** để xem cấp độ.
- Chạm **Phát âm** để vào chế độ từ vựng có loa.
- Chạm **Ôn tập** để học lại những câu sai.
- Chạm **Hồ sơ** để xem số liệu học tập thực tế.
- Chạm **Tiếp tục học** để mở bài ngữ pháp chưa hoàn thành.
- Các con số là dữ liệu thực, không dùng thống kê minh họa như ngày streak hoặc xếp hạng.

## Kiểm tra
`python -m unittest discover -s tests -v` — 18/18 pass.
Đã kiểm tra cú pháp Python. Chưa thử trực tiếp Kivy/Android vì môi trường không có Kivy và Android SDK.
**Lưu ý:** Lỗi loa trên thiết bị Android chưa được xác nhận đã khắc phục; nếu app còn thoát, cần lấy `adb logcat` để chẩn đoán lỗi Java/Android.
