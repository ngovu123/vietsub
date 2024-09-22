{
    "version": 2,
    "builds": [
      {
        "src": "main.py",  // Đổi tên tệp nếu cần
        "use": "@vercel/python"
      }
    ],
    "routes": [
      {
        "src": "/(.*)",
        "dest": "main.py"  // Đổi tên tệp nếu cần
      }
    ]
  }
  