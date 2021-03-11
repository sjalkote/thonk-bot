FROM python:3
WORKDIR /usr/src/app
COPY . .
RUN pip install discord
RUN pip install PyNaCl
RUN pip install requests
RUN pip install asyncio
RUN pip install apscheduler
CMD ["launcher.py"]
ENTRYPOINT ["python3"]
