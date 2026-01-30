# Auto Login Bookmedi.vn Admin

Dùng **Selenium** + Chrome. Cần cài [Chrome](https://www.google.com/chrome/) trước.

## Cài đặt lần đầu

```bash
cd "AUTO_CLICK"
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Chạy

**Cách 1 – Terminal:**
```bash
source venv/bin/activate
python run_login.py
```

**Cách 2 – Double-click (macOS):**  
Mở file `Chạy đăng nhập.command` (chuột phải → Mở nếu macOS chặn). Lần đầu sẽ tự tạo venv và cài thư viện.

---

Luồng: truy cập trang đăng nhập → điền email → điền mật khẩu → nhấn Đăng nhập → chờ vào Bảng điều khiển.  
Chrome sẽ mở, khi xong nhấn Enter trong terminal để đóng.
# auto_click
