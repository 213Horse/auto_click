#!/bin/bash
cd "$(dirname "$0")"
echo "=== Auto Login Bookmedi.vn ==="

# Dùng venv nếu có
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "Đang tạo môi trường ảo..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
fi

python3 run_login.py
echo ""
read -p "Nhấn Enter để thoát..."
