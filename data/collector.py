import time, datetime, pathlib

out = pathlib.Path("/data/heartbeat.log")
out.parent.mkdir(exist_ok=True)

while True:
    line = f"{datetime.datetime.now(datetime.UTC).isoformat()} alive\n"
    with out.open("a") as f:
        f.write(line)
    print(line, end="", flush=True)
    time.sleep(5)