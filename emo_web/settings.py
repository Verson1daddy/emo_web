# 移除 CSRF_TRUSTED_ORIGINS 配置

TEMPLATES = [
    {
        # ...existing code...
        'DIRS': [BASE_DIR / 'templates'],  # 确保包含模板目录
        'APP_DIRS': True,  # 确保启用应用模板目录
        # ...existing code...
    },
]
