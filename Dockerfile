# ---------- ① 基础镜像：自带三大浏览器 ----------
FROM mcr.microsoft.com/playwright/python:v1.44.0-jammy

# ---------- ② 复制项目 ----------
WORKDIR /app
COPY . /app

# ---------- ③ 让根目录在 PYTHONPATH 内 ----------
ENV PYTHONPATH=/app

# ---------- ④ 安装 Python 依赖 ----------
# 如需加速，可在 pip.conf 里改成清华/科大源；此处用官方默认源
RUN pip install --no-cache-dir -r requirements.txt

# ---------- ⑤ 入口（根据你的需求二选一） ----------
# A. 运行前端
ENTRYPOINT ["python", "-m", "frontend.app"]
# B. 若只想跑爬虫 CLI，请改成：
# ENTRYPOINT ["python", "-m", "crawler.main", "--seed", "https://example.com"]
