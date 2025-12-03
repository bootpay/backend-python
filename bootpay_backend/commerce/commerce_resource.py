import requests
import base64
import json
import os
from typing import Optional, Dict, Any, List


class BootpayCommerceResource:
    """Commerce API 베이스 리소스 클래스"""

    API_ENTRYPOINTS = {
        'development': 'https://dev-api.bootapi.com/v1',
        'stage': 'https://stage-api.bootapi.com/v1',
        'production': 'https://api.bootapi.com/v1'
    }
    API_VERSION = '1.0.0'
    SDK_VERSION = '1.0.0'

    def __init__(self):
        self.mode = 'production'
        self._token: Optional[str] = None
        self._role = 'user'
        self.client_key: Optional[str] = None
        self.secret_key: Optional[str] = None
        self.timeout = 60

    def set_configuration(self, client_key: str, secret_key: str, mode: str = 'production'):
        """
        설정 정보 지정
        :param client_key: Commerce API 클라이언트 키
        :param secret_key: Commerce API 시크릿 키
        :param mode: 환경 ('development', 'stage', 'production')
        """
        self.client_key = client_key
        self.secret_key = secret_key
        self.mode = mode

    def set_token(self, token: str):
        """토큰 설정"""
        self._token = token

    def get_token(self) -> Optional[str]:
        """현재 토큰 반환"""
        return self._token

    def set_role(self, role: str):
        """Role 설정"""
        self._role = role

    def get_role(self) -> str:
        """현재 Role 반환"""
        return self._role

    def _get_basic_auth_header(self) -> str:
        """Basic Auth 헤더 생성"""
        if self.client_key and self.secret_key:
            credentials = f'{self.client_key}:{self.secret_key}'
            encoded = base64.b64encode(credentials.encode()).decode()
            return f'Basic {encoded}'
        return ''

    def _entrypoints(self, url: str) -> str:
        """엔트리포인트 URL 생성"""
        return '/'.join([self.API_ENTRYPOINTS[self.mode], url])

    def _get_headers(self, include_auth: bool = True) -> Dict[str, str]:
        """공통 헤더 생성"""
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Accept-Charset': 'utf-8',
            'BOOTPAY-SDK-VERSION': self.SDK_VERSION,
            'BOOTPAY-API-VERSION': self.API_VERSION,
            'BOOTPAY-SDK-TYPE': '302',
            'BOOTPAY-ROLE': self._role or 'user'
        }
        if include_auth and self._token:
            headers['Authorization'] = f'Bearer {self._token}'
        return headers

    def get(self, url: str, params: Optional[Dict] = None):
        """GET 요청"""
        response = requests.get(
            self._entrypoints(url),
            headers=self._get_headers(),
            params=params,
            timeout=self.timeout
        )
        return response.json()

    def post(self, url: str, data: Optional[Dict] = None):
        """POST 요청"""
        response = requests.post(
            self._entrypoints(url),
            headers=self._get_headers(),
            json=data,
            timeout=self.timeout
        )
        return response.json()

    def post_with_basic_auth(self, url: str, data: Optional[Dict] = None):
        """Basic Auth를 사용한 POST 요청"""
        headers = self._get_headers(include_auth=False)
        headers['Authorization'] = self._get_basic_auth_header()
        response = requests.post(
            self._entrypoints(url),
            headers=headers,
            json=data,
            timeout=self.timeout
        )
        return response.json()

    def post_multipart(self, url: str, data: Dict, image_paths: Optional[List[str]] = None):
        """
        Multipart/form-data POST 요청 (이미지 업로드 포함)
        :param url: 요청 URL
        :param data: 폼 데이터
        :param image_paths: 이미지 파일 경로 배열
        """
        headers = {
            'Accept': 'application/json',
            'Accept-Charset': 'utf-8',
            'BOOTPAY-SDK-VERSION': self.SDK_VERSION,
            'BOOTPAY-API-VERSION': self.API_VERSION,
            'BOOTPAY-SDK-TYPE': '302',
            'BOOTPAY-ROLE': self._role or 'user'
        }
        if self._token:
            headers['Authorization'] = f'Bearer {self._token}'

        # 폼 데이터 준비
        form_data = {}
        for key, value in data.items():
            if value is not None:
                if isinstance(value, (dict, list)):
                    form_data[key] = json.dumps(value)
                else:
                    form_data[key] = str(value)

        # 파일 준비
        files = []
        if image_paths:
            for image_path in image_paths:
                filename = os.path.basename(image_path)
                files.append(('images', (filename, open(image_path, 'rb'))))

        try:
            response = requests.post(
                self._entrypoints(url),
                headers=headers,
                data=form_data,
                files=files if files else None,
                timeout=self.timeout
            )
            return response.json()
        finally:
            # 파일 핸들 닫기
            for _, file_tuple in files:
                file_tuple[1].close()

    def put(self, url: str, data: Optional[Dict] = None):
        """PUT 요청"""
        response = requests.put(
            self._entrypoints(url),
            headers=self._get_headers(),
            json=data,
            timeout=self.timeout
        )
        return response.json()

    def delete(self, url: str, params: Optional[Dict] = None):
        """DELETE 요청"""
        response = requests.delete(
            self._entrypoints(url),
            headers=self._get_headers(),
            params=params,
            timeout=self.timeout
        )
        return response.json()
