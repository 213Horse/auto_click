#!/usr/bin/env python3
"""
Auto login Bookmedi.vn Admin
Chạy: python run_login.py
"""

import time
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Trang đích (chưa đăng nhập sẽ chuyển sang form đăng nhập)
LOGIN_URL = "https://bookmedi.vn/admin/index.php?route=marketing/coupon"
EMAIL = "sach@sach123.vn"
PASSWORD = "2V;&2KCH@WU3ky~7"

# Thời gian nghỉ giữa các thao tác (giây) - tránh bị chặn do thao tác quá nhanh
# Tăng lên 2–2.5 nếu vẫn bị chặn
DELAY = 1.5

# Đường dẫn file mã voucher (cùng thư mục với script)
VOUCHERS_FILE = Path(__file__).parent / "vouchers.txt"


def get_next_voucher() -> str:
    """Lấy mã đầu tiên từ vouchers.txt và xóa nó khỏi file."""
    if not VOUCHERS_FILE.exists():
        raise FileNotFoundError(f"Không tìm thấy file {VOUCHERS_FILE}")
    with open(VOUCHERS_FILE, "r", encoding="utf-8") as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]
    if not lines:
        raise ValueError("File vouchers.txt đã hết mã!")
    code = lines[0]
    remaining = lines[1:]
    with open(VOUCHERS_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(remaining))
        if remaining:
            f.write("\n")
    return code


def main():
    options = Options()
    # Bỏ headless để thấy trình duyệt chạy
    # options.add_argument("--headless")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        print("1. Đang truy cập trang phiếu giảm giá...")
        driver.get(LOGIN_URL)
        time.sleep(DELAY)

        wait = WebDriverWait(driver, 15)

        print("2. Đang điền email...")
        email_input = wait.until(EC.presence_of_element_located((By.ID, "input-email")))
        email_input.clear()
        time.sleep(0.5)
        email_input.send_keys(EMAIL)
        time.sleep(DELAY)

        print("3. Đang điền mật khẩu...")
        pass_input = driver.find_element(By.ID, "input-password")
        pass_input.clear()
        time.sleep(0.5)
        pass_input.send_keys(PASSWORD)
        time.sleep(DELAY)

        print("4. Đang nhấn nút Đăng nhập...")
        driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

        # Chờ đăng nhập xong (URL có token = đã đăng nhập)
        wait.until(lambda d: "token=" in d.current_url)
        print("5. Đăng nhập thành công! Đã vào trang Phiếu giảm giá.")
        time.sleep(DELAY)

        print("6. Đang nhấn nút Thêm mới...")
        add_btn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.pull-right a.btn.btn-success[href*="coupon/add"]'))
        )
        time.sleep(0.5)
        add_btn.click()
        print("7. Đã mở trang Thêm phiếu giảm giá mới.")
        time.sleep(DELAY)

        # Chờ form load
        wait.until(EC.presence_of_element_located((By.ID, "input-name")))

        # Lấy mã voucher từ file (mỗi lần chạy lấy 1 mã từ trên xuống)
        voucher_code = get_next_voucher()
        print(f"   Dùng mã: {voucher_code}")

        print("8. Đang điền tên phiếu giảm giá...")
        name_input = driver.find_element(By.ID, "input-name")
        name_input.clear()
        time.sleep(0.5)
        name_input.send_keys("Voucher_Skyline")
        time.sleep(DELAY)

        print("9. Đang điền mã phiếu...")
        code_input = driver.find_element(By.ID, "input-code")
        code_input.clear()
        time.sleep(0.5)
        code_input.send_keys(voucher_code)
        time.sleep(DELAY)

        print("10. Đang chọn loại Giảm tiền cố định...")
        # Option "Giảm tiền cố định" có value="F" - set trực tiếp qua JS (tránh Select2 dropdown)
        driver.execute_script("""
            var sel = document.getElementById('input-type');
            sel.value = 'F';
            if (typeof jQuery !== 'undefined') {
                jQuery(sel).trigger('change');
            } else {
                sel.dispatchEvent(new Event('change', { bubbles: true }));
            }
        """)
        time.sleep(DELAY)

        print("11. Đang điền số tiền giảm...")
        discount_input = driver.find_element(By.ID, "input-discount")
        discount_input.clear()
        time.sleep(0.5)
        discount_input.send_keys("100000")
        print("12. Đã điền xong form thêm phiếu giảm giá.")

        input("Nhấn Enter để đóng trình duyệt...")

    except Exception as e:
        print(f"Lỗi: {e}")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
