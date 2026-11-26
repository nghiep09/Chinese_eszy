# Bản v0.3.3 – Sửa 4 ô Chủ đề học

Trang chủ theo mẫu đỏ/kem. **Chủ đề học** gồm 4 ô 2 hàng × 2 cột theo đúng thứ tự:

1. **Từ vựng** (词): chạm để vào thẳng màn hình học Từ vựng hiện có của v0.3.0 (bao gồm trắc nghiệm, ghép từ, chọn file và các thao tác cũ).
2. **Phát âm** (音): thẻ hiển thị “Sắp ra mắt”; chạm sẽ hiện thông báo. Nút loa trong bài Từ vựng/Ngữ pháp vẫn được giữ nhưng chưa xác nhận sửa lỗi crash Android.
3. **Ngữ pháp** (语): chạm mở trang cấp độ ngữ pháp đã xây dựng.
4. **Luyện nghe** (听): thẻ hiển thị “Sắp ra mắt”; chạm sẽ hiện thông báo.

## Đã sửa
- Bỏ nút phủ `FloatLayout` của 4 thẻ cũ; dùng `FeatureCard(ButtonBehavior, BoxLayout)` để phần chữ không bị che và có thể nhấn trên cả thẻ.
- Dùng ký tự tiếng Trung thay cho emoji/font biểu tượng thiếu glyph, tránh biểu tượng hình ô vuông trên Android. Áp dụng cả thống kê và thanh điều hướng.
- Giữ nguyên `show_vocabulary()` và `vocab_root` từ v0.3.0.
- Điều chỉnh lưới thành hai hàng đều nhau; hiển thị tiêu đề và phụ đề ở từng thẻ.
- Hạ lượng log Actions và thêm bước kiểm tra APK ZIP trước khi upload, giúp phát hiện APK hỏng.

## Kiểm tra
- 18/18 bài kiểm tra chức năng của dự án đạt.
- Cú pháp Python đã kiểm tra.
- Chưa thể chạy Kivy giao diện hoặc cài APK trên Android trong môi trường hiện tại.
- Nếu nút loa còn đóng ứng dụng, lấy `adb logcat` để chẩn đoán; thay đổi này không sửa TTS.
