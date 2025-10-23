# 🌌 FateVerse – User Stories & Acceptance Criteria (v2)

---

## 🔢 1. Numerology – Thần Số Học
**User Story:**  
As a user, I want to calculate my numerology number based on my date of birth and name so that I can understand my personality and life path.

**Acceptance Criteria:**  
- [ ] User nhập **họ tên** và **ngày/tháng/năm sinh**.  
- [ ] Hệ thống tính các chỉ số chính:
  - **Life Path Number** (đường đời)  
  - **Expression Number** (biểu đạt)  
  - **Soul Urge Number** (linh hồn)  
  - **Personality Number** (tính cách)  
- [ ] Hiển thị kết quả:  
  - Các chỉ số kèm mô tả chi tiết ý nghĩa  
  - Tính cách, điểm mạnh, điểm yếu  
  - Gợi ý hướng nghề nghiệp hoặc tình duyên phù hợp  
- [ ] UI có animation “vũ trụ đang tính toán 🔮” trước khi hiển thị.  
- [ ] Nếu input thiếu → hiển thị cảnh báo “Nhập đủ tên và ngày sinh để xem số mệnh nha!”.  
- [ ] Cho phép user **lưu và chia sẻ** kết quả (tạo image card có số chủ đạo + quote).

---

## 🌙 2. Horoscope & Zodiac (Bói theo ngày sinh)
**User Story:**  
As a user, I want to enter my birth date to see my zodiac sign, element, and lucky traits so that I can learn about my destiny and compatibility.

**Acceptance Criteria:**  
- [ ] User nhập **ngày/tháng/năm sinh**.  
- [ ] App tự động xác định **cung hoàng đạo**.  
- [ ] Hiển thị:  
  - Tên cung  
  - Ngũ hành / Element (Fire, Earth, Water, Air)  
  - Lucky color / Lucky number  
  - Mô tả tính cách tổng quát  
  - Các cung hợp và khắc  
- [ ] Có animation chòm sao chuyển động nhẹ.  
- [ ] Có nút “Chia sẻ lá số” → sinh hình ảnh đẹp.  

---

## 💘 3. Love Compatibility (Bói tình duyên)
**User Story:**  
As a user, I want to check compatibility between me and another person so that I can understand how well we match emotionally and spiritually.

**Acceptance Criteria:**  
- [ ] User nhập **tên và ngày sinh** của 2 người.  
- [ ] Hệ thống tính:  
  - Điểm tương hợp (%)  
  - Phân tích cung hoàng đạo & thần số học 2 bên  
  - Nhận xét vui nhộn “Tình duyên có duyên hay nghiệp”  
- [ ] Hiển thị kết quả với animation trái tim đập.  
- [ ] Có phần **“AI Recommendation”**: lời khuyên duy trì mối quan hệ.  
- [ ] Có nút **“Share result”** → xuất hình ảnh (VD: “Tụi mình hợp 87% 💘”).  
- [ ] Nếu thiếu input → cảnh báo vui nhộn “Thiếu người yêu để bói nè 😅”.  

---

## 🔮 4. Tarot Reading (Bói Tarot)
**User Story:**  
As a user, I want to draw tarot cards online so that I can receive insights into my past, present, and future.

**Acceptance Criteria:**  
- [ ] User chọn **chủ đề bói**: tình yêu / công việc / sức khỏe.  
- [ ] Deck có sẵn các lá bài Tarot (Major Arcana).  
- [ ] Khi user chọn 3 lá → animation lật bài 3D.  
- [ ] Mỗi lá hiển thị:  
  - Tên + Ảnh  
  - Ý nghĩa ngắn  
  - Phân tích chi tiết theo vị trí (quá khứ / hiện tại / tương lai)  
- [ ] Kết quả tổng hợp có **“Lời khuyên hôm nay”**.  
- [ ] Có thể “rút lại” hoặc “lưu kết quả”.  

---

## 🌈 5. Daily Fortune (Lá số hôm nay)
**User Story:**  
As a returning user, I want to receive a daily fortune message so that I can start my day with motivation and positivity.

**Acceptance Criteria:**  
- [ ] Khi mở app, nếu chưa xem hôm nay → hiển thị fortune.  
- [ ] Nội dung fortune gồm:  
  - Lời khuyên trong ngày  
  - Màu may mắn  
  - Emoji hoặc quote ngắn  
- [ ] Kết quả random hoặc dựa theo ngày sinh.  
- [ ] Khi đã xem → hiển thị “Bạn đã xem fortune hôm nay 🌞”.  
- [ ] Có nút **“Share fortune”** → xuất ảnh hoặc link chia sẻ.  

---

## 🧾 6. User History & Sharing
**User Story:**  
As a registered user, I want to view my saved fortune results so that I can reflect on my past predictions.

**Acceptance Criteria:**  
- [ ] Mỗi kết quả (Tarot, Tình duyên, Thần số học, Chiêm tinh, Fortune) được lưu kèm ngày.  
- [ ] Trang “Lịch sử xem bói” hiển thị danh sách + loại bói.  
- [ ] User có thể xoá riêng từng entry hoặc toàn bộ.  
- [ ] Khi share, app tạo card ảnh có quote + icon.  

---

## 🧘 7. UI/UX Experience
**User Story:**  
As a user, I want the app to feel magical and interactive so that I enjoy the fortune-telling experience.

**Acceptance Criteria:**  
- [ ] Giao diện gradient tím – xanh thiên hà – vàng ánh sáng.  
- [ ] Animation particle và glow khi chờ kết quả.  
- [ ] Hiệu ứng âm thanh nhỏ khi rút bài hoặc xem số mệnh.  
- [ ] Hỗ trợ mobile và desktop.  
- [ ] Có dark/light mode.  

---

## 🔐 8. Account & Preferences
**User Story:**  
As a user, I want to log in and customize my preferences so that I can personalize my spiritual experience.

**Acceptance Criteria:**  
- [ ] Đăng nhập bằng Google / Email.  
- [ ] Lưu ngày sinh, tên, theme, và kết quả.  
- [ ] Có thể chọn theme (Tím thiên hà / Xanh vũ trụ / Vàng ánh sáng).  
- [ ] Dữ liệu đồng bộ trên mọi thiết bị.
