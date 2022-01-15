FROM anirudhvs/chrome:v1

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /xss_bot

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD python3 xss_bot.py