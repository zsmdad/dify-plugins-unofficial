from typing import Any

from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError

import requests


class Cl2wmProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        """
        草料二维码鉴权
        https://user.cli.im/opendata?withNav=1
        """
        apikey = credentials.get('token')

        if not apikey:
            raise ToolProviderCredentialValidationError('apikey is required')
        try:
            url = 'https://open.cli.im/api/v1/qrcode/scan_url'

            data = {
                "url": "https://gstatic.clewm.net/caoliao-resource/250221/80bc7c_be831017.png"
            }

            headers = {
                'Authorization': f'Bearer {apikey}' 
            }

            response = requests.post(url, json=data, headers=headers)
            if response.status_code!= 200:
                raise ToolProviderCredentialValidationError('apikey is invalid')
            result = response.json()
            if result.get('code')!= 0:
                raise ToolProviderCredentialValidationError(result.get('msg'))
        except Exception as e:
            raise ToolProviderCredentialValidationError(str(e))
