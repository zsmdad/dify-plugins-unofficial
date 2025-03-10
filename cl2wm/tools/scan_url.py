from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

import requests

class Cl2wmTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        # yield self.create_json_message({
        #     "result": "Hello, world!"
        # })
        """
        草料二维码开放平台文档
        https://cli.im/open-api/intro/intro.html
        """
        qrcode_url = tool_parameters.get("qrcode_url").strip()
        apikey = self.runtime.credentials.get("token", None)
        print(f"qrcode_url: {qrcode_url}")

        if not qrcode_url:
            yield self.create_text_message("Qrcode URL is required.")
        if not apikey:
            yield self.create_text_message("API key is required.")

        url = 'https://open.cli.im/api/v1/qrcode/scan_url'
        data = {'url': qrcode_url}
        headers = {
            'Authorization': f'Bearer {apikey}',
            'Content-Type': 'application/json'
        }
        response = requests.post(url, json=data, headers=headers)

        if response.status_code == 200:
            result = response.json()
            code = result.get('code')
            if code == 0:
                content = result["data"]["content"]
                yield self.create_text_message(content)
            else:
                yield self.create_text_message(f"Failed to scan URL {url}. Code: {code}. Reason: {result.get('message')}")
        else:
            yield self.create_text_message(f"Failed to scan URL {url}. Reason: {response.text}")
