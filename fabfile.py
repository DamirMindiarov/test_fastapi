import os

from fabric import Connection, task

print(os.environ["P_SSH_KEY"])

@task
def deploy(ctx):
    with Connection(
        "85.209.9.55",
        user="user",
        connect_kwargs={"key_filename": os.environ["P_SSH_KEY"]},
    ) as c:
        with c.cd("/home/user"):
            c.run("docker pull damirmin/test_fastapi:3.0.0")
            c.run("docker run -p 80:8000 -d damirmin/test_fastapi:3.0.0")
