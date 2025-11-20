import argparse
import sys
import yaml
from jinja2 import Environment, FileSystemLoader
from typing import Dict, List, Optional

def parse_envs(envs_str: Optional[str]) -> Optional[List[Dict[str, str]]]:
    if not envs_str:
        return None
    envs = []
    for item in envs_str.split(','):
        if '=' not in item:
            continue
        k, v = item.split('=', 1)
        envs.append({'name': k.strip(), 'value': v.strip()})
    return envs if envs else None

def render_deployment(name: str, labels: Optional[str], replicas: int, envs: Optional[List[Dict[str, str]]]) -> str:
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('deployment.yaml.j2')
    rendered = template.render(name=name, labels=labels, replicas=replicas, envs=envs)

    yaml.safe_load(rendered)
    return rendered

def main():
    parser = argparse.ArgumentParser(description="Generate Kubernetes Deployment manifest.")
    parser.add_argument('--name', required=True, help='Deployment and container name')
    parser.add_argument('--labels', help='Labels filed')
    parser.add_argument('--replicas', type=int, help='Number of replicas (default: 3)')
    parser.add_argument('--envs', help='Comma-separated envs, e.g. ENV1=val1,ENV2=val2')
    args = parser.parse_args()

    name = args.name
    labels = args.labels
    replicas = args.replicas if args.replicas is not None else 3
    envs = parse_envs(args.envs)

    try:
        output = render_deployment(name, labels, replicas, envs)
        print(output)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
