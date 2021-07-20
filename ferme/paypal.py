import sys

from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment


class PayPalClient:
    def __init__(self):
        self.client_id = "ARMN0sySxtSS7CfbJ19fxhfkMEoGvVSS8wSKiB2mo2MUujS3xGkNP6F2UPCe6t-BvKR5G0TbXBDEw4w7"
        self.client_secret = "EEoP0n9TN1xqM2y5WFAxQJG3gTYcK5_2PBRbDlTWw5v1DLdJf5skJgUGVOfZz_YV5DfOrCgcYQFvBz-s"
        self.environment = SandboxEnvironment(client_id=self.client_id, client_secret=self.client_secret)
        self.client = PayPalHttpClient(self.environment)