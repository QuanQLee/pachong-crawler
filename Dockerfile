# ---------- �� ���������Դ���������� ----------
FROM mcr.microsoft.com/playwright/python:v1.44.0-jammy

# ---------- �� ������Ŀ ----------
WORKDIR /app
COPY . /app

# ---------- �� �ø�Ŀ¼�� PYTHONPATH �� ----------
ENV PYTHONPATH=/app

# ---------- �� ��װ Python ���� ----------
# ������٣����� pip.conf ��ĳ��廪/�ƴ�Դ���˴��ùٷ�Ĭ��Դ
RUN pip install --no-cache-dir -r requirements.txt

# ---------- �� ��ڣ�������������ѡһ�� ----------
# A. ����ǰ��
ENTRYPOINT ["python", "-m", "frontend.app"]
# B. ��ֻ�������� CLI����ĳɣ�
# ENTRYPOINT ["python", "-m", "crawler.main", "--seed", "https://example.com"]
