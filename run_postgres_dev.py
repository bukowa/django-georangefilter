import docker

client = docker.from_env()

container_name = "georangefilter"
port = 5432

envs = {"POSTGRES_PASSWORD": "", "POSTGRES_DB": container_name}


try:
    client.containers.get(container_name).remove(force=True)
except Exception as err:
    print(err)
    pass

client.containers.run(
    "postgres",
    name=container_name,
    environment=envs,
    ports={5432: port},
    restart_policy={"Name": "always"},
    detach=True,
)
