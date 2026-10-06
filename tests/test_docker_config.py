from pathlib import Path
import yaml

def test_docker_compose_syntax():
    compose_path = Path("docker/docker-compose.yml")
    assert compose_path.exists(), "docker-compose.yml does not exist"
    with open(compose_path, "r") as f:
        config = yaml.safe_load(f)
    services = config.get("services", {})
    assert "namenode" in services
    assert "datanode" in services
    assert "hive-server" in services
