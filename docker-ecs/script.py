import json
import os

data = json.load(open('terraform_state_file.json', 'r'))

APP_SERVICE_HOST = data["load_balancers"]["value"][0]["dns_name"]
LOADBALANCER = data["load_balancers"]["value"][0]["name"]
SG_LOADBALANCER = data["load_balancers"]["value"][0]["security_groups"][0]
PRIVATE_SUBNET = data["subnets_private"]["value"]
VPC = data["vpc_id"]["value"]

ECS_CONTEXT = "dev"
PROJECT_NAME = "aline-jd"

print("Setting cluster environment variables...")
with open('./.env', 'w') as f:
    f.write("VPC=%s\n" % VPC)
    f.write("LOAD_BALANCER=%s\n" % LOADBALANCER)
    f.write("SUBNET=%s\n" % PRIVATE_SUBNET)
    f.write("SG_LOADBALANCER=%s\n" % SG_LOADBALANCER)


os.system("cat static.env >> .env")

print("Launching cluster...")
os.system("sudo docker context use %s && sudo docker compose --env-file .env -p %s up" % (ECS_CONTEXT,PROJECT_NAME))
