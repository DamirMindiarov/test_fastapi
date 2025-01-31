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
        with c.cd("/home/user"):#
            c.run("docker compose up")
            # c.run("docker pull damirmin/test_fastapi:latest")
            # c.run('docker stop $(docker ps -f name=test_fastapi -qa)')
            # c.run("docker rm $(docker ps -f name=test_fastapi -qa)")
            # c.run("docker run --name test_fastapi -p 80:8000 -d damirmin/test_fastapi:latest")
            #

    os.remove('key')
