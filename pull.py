import sys
import os
import docker
from configparser import ConfigParser

config_file = '/root/.aws/ecr'
config = ConfigParser()

with open(config_file) as f:
    config.read_file(f)
    f.close()

link = config.get('repository', 'link')

if len(sys.argv) < 2:
    repo_name = input("Repository name (<alias>:<tag>):")

else:
    repo_name = sys.argv[1]

print("Repository: {0}".format(repo_name))

if ':' in repo_name:
    repo_name, tag = repo_name.split(':')
else:
    tag = 'latest'

print("Preparing pull from '{0}/{1}:{2}'".format(link, repo_name, tag))

client = docker.from_env()

for image in client.images.list():
    if repo_name in image.attrs.get('RepoTags'):
        print("Repository já existe")
        exit(1)

os.system('docker pull {0}/{1}:{2}'.format(link, repo_name, tag))
