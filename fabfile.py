import os

from fabric import Connection, task


@task
def deploy(ctx):

    with open('key', 'w') as f:
        f.write(os.environ["P_SSH_KEY"])
    # with open('key', 'w') as f:
    #     f.write(a)

    with Connection(
            "85.209.9.55",
            user="user",
            connect_kwargs={"key_filename": 'key'},
    ) as c:
        with c.cd("/home/user/test_fastapi"):#
            c.run("docker compose down")
            c.run("git pull")
            c.run("docker compose up -d")

    os.remove('key')
