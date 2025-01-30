import os

from fabric import Connection, task


@task
def deploy(ctx):
    a = os.environ["P_SSH_KEY"]

    with open('key', 'w') as f:
        f.write(a)

    with Connection(
            "85.209.9.55",
            user="user",
            connect_kwargs={"key_filename": 'key', 'password': 'akacuki21'},
    ) as c:
        with c.cd("/home/user"):
            c.run("docker pull damirmin/test_fastapi:3.0.0")
            c.run("docker run -p 80:8000 -d damirmin/test_fastapi:3.0.0")

    os.remove('key')
