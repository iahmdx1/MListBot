#!/bin/bash

# التأكد من وجود متغير البيئة BOT_TOKEN
if [ -z "$BOT_TOKEN" ]; then
  echo "Error: BOT_TOKEN environment variable not set."
  exit 1
fi

# تثبيت المكتبات المطلوبة من requirements.txt
pip install -r requirements.txt

# تشغيل البوت
python main.py
