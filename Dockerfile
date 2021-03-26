FROM python:3
WORKDIR /usr/src/app
COPY . .
RUN pip install discord[voice] PyNaCl requests datetime asyncio apscheduler psutil
CMD ["launcher.py"]
ENTRYPOINT ["python3"]
