FROM python:3.11.10

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

RUN pip install waitress

EXPOSE 8080

ENTRYPOINT ["waitress-serve", "--call"]

CMD ["outlier_detection:create_app"]