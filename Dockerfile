FROM python:3
WORKDIR /usr/src/app
COPY . .
RUN pip install discord.py[voice] requests datetime asyncio apscheduler psutil discord-py-slash-command
CMD ["launcher.py"]
ENTRYPOINT ["python3"]
