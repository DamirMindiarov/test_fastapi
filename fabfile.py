import os

from fabric import Connection, task


@task
def deploy(ctx):

    with open('key', 'w') as f:
        f.write(os.environ["P_SSH_KEY"])

    with Connection(
            "85.209.9.55",
            user="user",
            connect_kwargs={"key_filename": 'key'},
    ) as c:
        with c.cd("/home/user"):#
            c.run("docker pull damirmin/test_fastapi:latest")
            c.run('docker ps --filter "name=test_fastapi" | docker stop test_fastapi')
            c.run("docker rm $(docker ps -f name=test_fastapi -qa)")
            c.run("docker run --name test_fastapi -p 80:8000 -d damirmin/test_fastapi:latest")

    os.remove('key')
