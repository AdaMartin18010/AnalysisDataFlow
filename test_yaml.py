import yaml

code = """
version: '3.8'

services:
  jobmanager:
    image: flink:1.18-scala_2.12
    command: jobmanager
    environment:
      - JOB_MANAGER_RPC_ADDRESS=jobmanager
      - FLINK_PROPERTIES=
          jobmanager.memory.process.size: 2048m
          state.backend: rocksdb
          state.checkpoints.dir: s3://checkpoints
    ports:
      - "8081:8081"
"""

try:
    yaml.safe_load(code)
    print('OK')
except Exception as e:
    print(e)
