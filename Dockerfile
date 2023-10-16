FROM archlinux:latest
RUN pacman -S python-dotenv curl python-pip
RUN pip install -r requirements.txt
EXPOSE 80

WORKDIR /app

CMD ["python","webhook.py"]