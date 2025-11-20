import unittest
from generate_deployment import parse_envs, render_deployment

class TestDeploymentGen(unittest.TestCase):
    def test_parse_envs(self):
        self.assertEqual(parse_envs('FOO=bar,BAR=baz'), [
            {'name': 'FOO', 'value': 'bar'},
            {'name': 'BAR', 'value': 'baz'}
        ])
        self.assertEqual(parse_envs(''), None)
        self.assertEqual(parse_envs(None), None)

    def test_render_deployment_minimal(self):
        yaml_str = render_deployment('myapp', None, 3, None)
        self.assertIn('name: myapp', yaml_str)
        self.assertIn('replicas: 3', yaml_str)
        self.assertNotIn('labels:', yaml_str.split('metadata:')[1])

    def test_render_deployment_full(self):
        yaml_str = render_deployment('myapp', 'mylabel', 2, [
            {'name': 'FOO', 'value': 'bar'}
        ])
        self.assertIn('labels: mylabel', yaml_str)
        self.assertIn('replicas: 2', yaml_str)
        self.assertIn('name: FOO', yaml_str)
        self.assertIn('value: "bar"', yaml_str)

if __name__ == '__main__':
    unittest.main()
