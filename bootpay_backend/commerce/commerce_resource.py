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
        has_client_key = bool(self.client_key)
        has_secret_key = bool(self.secret_key)
        if not has_client_key and not has_secret_key:
            raise ValueError('Commerce API에는 client_key와 secret_key가 필요합니다.')
        if has_client_key != has_secret_key:
            missing = 'secret_key' if has_client_key else 'client_key'
            raise ValueError(f'{missing} 값이 비어있습니다. client_key와 secret_key는 함께 지정해야 합니다.')
        credentials = f'{self.client_key}:{self.secret_key}'
        encoded = base64.b64encode(credentials.encode()).decode()
        return f'Basic {encoded}'

    def _entrypoints(self, url: str) -> str:
        """엔트리포인트 URL 생성"""
        return '/'.join([self.API_ENTRYPOINTS[self.mode], url])

    def _get_headers(self, include_auth: bool = True, headers: Optional[Dict[str, str]] = None) -> Dict[str, str]:
        """
        공통 헤더 생성
        요청별로 지정된 헤더(headers)가 공통값을 덮어쓴다 —
        supervisor 전용 endpoint 의 BOOTPAY-ROLE 을 공통 계층이 덮어쓰지 않기 위함.
        """
        merged = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Accept-Charset': 'utf-8',
            'BOOTPAY-SDK-VERSION': self.SDK_VERSION,
            'BOOTPAY-API-VERSION': self.API_VERSION,
            'BOOTPAY-SDK-TYPE': '302',
            'BOOTPAY-ROLE': self._role or 'user'
        }
        if include_auth:
            basic_auth = self._get_basic_auth_header()
            if basic_auth:
                merged['Authorization'] = basic_auth
        if headers:
            merged.update(headers)
        return merged

    def get(self, url: str, params: Optional[Dict] = None, headers: Optional[Dict[str, str]] = None):
        """GET 요청"""
        response = requests.get(
            self._entrypoints(url),
            headers=self._get_headers(headers=headers),
            params=params,
            timeout=self.timeout
        )
        return response.json()

    def post(self, url: str, data: Optional[Dict] = None, headers: Optional[Dict[str, str]] = None):
        """POST 요청"""
        response = requests.post(
            self._entrypoints(url),
            headers=self._get_headers(headers=headers),
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

    def post_multipart(self, url: str, data: Dict, image_paths: Optional[List[str]] = None,
                       headers: Optional[Dict[str, str]] = None):
        """
        Multipart/form-data POST 요청 (이미지 업로드 포함)
        ⚠️ Content-Type 은 requests 가 생성한 값(boundary 포함)을 그대로 사용한다.
           직접 지정하면 boundary 가 사라져 본문이 서버에서 null 로 파싱된다.
        :param url: 요청 URL
        :param data: 폼 데이터
        :param image_paths: 이미지 파일 경로 배열
        :param headers: 요청별 추가 헤더 (공통값을 덮어쓴다)
        """
        request_headers = self._multipart_headers(headers)
        form_data = self._serialize_form_data(data)

        # 파일 준비
        # ⚠️ Rails 는 반복된 `images` 를 배열로 받지 않는다. images[0], images[1] ... 로 인덱싱해야 한다.
        files = []
        if image_paths:
            for index, image_path in enumerate(image_paths):
                filename = os.path.basename(image_path)
                files.append((f'images[{index}]', (filename, open(image_path, 'rb'))))

        try:
            response = requests.post(
                self._entrypoints(url),
                headers=request_headers,
                data=form_data,
                files=files if files else None,
                timeout=self.timeout
            )
            return response.json()
        finally:
            # 파일 핸들 닫기
            for _, file_tuple in files:
                file_tuple[1].close()

    def post_multipart_file(self, url: str, field: str, file: Any, data: Optional[Dict] = None,
                            headers: Optional[Dict[str, str]] = None):
        """
        단일 파일 필드 multipart/form-data POST 요청
        ⚠️ post_multipart 는 Rails 배열 규약(images[0], images[1] ...) 전용이다.
           알림톡 템플릿 이미지처럼 서버가 필드명을 정해 둔 단일 파일 업로드는 이 메서드를 쓴다.
           images[0] 으로 올리면 서버가 파일을 찾지 못한다.
        :param url: 요청 URL
        :param field: 파일 폼 필드명 (예: 'image')
        :param file: 파일 경로(str) 또는 이미 열린 파일 객체
        :param data: 함께 보낼 폼 데이터
        :param headers: 요청별 추가 헤더 (공통값을 덮어쓴다)
        """
        request_headers = self._multipart_headers(headers)
        form_data = self._serialize_form_data(data or {})

        # 경로를 받으면 여기서 열고 반드시 닫는다. 파일 객체를 받으면 호출자 소유이므로 닫지 않는다.
        opened = open(file, 'rb') if isinstance(file, str) else None
        handle = opened if opened is not None else file
        filename = os.path.basename(file if isinstance(file, str) else getattr(file, 'name', field))

        try:
            response = requests.post(
                self._entrypoints(url),
                headers=request_headers,
                data=form_data,
                files={field: (filename, handle)},
                timeout=self.timeout
            )
            return response.json()
        finally:
            if opened is not None:
                opened.close()

    def get_raw(self, url: str, params: Optional[Dict] = None, headers: Optional[Dict[str, str]] = None):
        """
        JSON 이 아닌 본문(CSV 등)을 파싱하지 않고 그대로 받는다.
        ⚠️ 공용 get 은 응답을 무조건 response.json() 으로 파싱하므로, CSV 를 돌려주는 endpoint
           (알림톡 템플릿 내보내기 format=csv)에서는 성공한 요청이 파싱 예외로 터진다.
           실제로는 200 이라 원인을 찾기 어려워서 원문 경로를 따로 둔다.
        :return: {'body': str, 'content_type': str, 'status': int}
        """
        # 원문 경로라 Accept 를 */* 로 낮춘다 (요청별로 지정했다면 그 값을 존중한다).
        request_headers = self._get_headers(headers={'Accept': '*/*', **(headers or {})})
        response = requests.get(
            self._entrypoints(url),
            headers=request_headers,
            params=params,
            timeout=self.timeout
        )
        return {
            'body': response.text,
            'content_type': response.headers.get('Content-Type', ''),
            'status': response.status_code
        }

    def _multipart_headers(self, headers: Optional[Dict[str, str]] = None) -> Dict[str, str]:
        """
        multipart 요청 공통 헤더
        ⚠️ Content-Type 은 넣지 않는다 — requests 가 생성한 값(boundary 포함)을 그대로 써야 한다.
           직접 지정하면 boundary 가 사라져 본문이 서버에서 null 로 파싱된다.
        """
        request_headers = {
            'Accept': 'application/json',
            'Accept-Charset': 'utf-8',
            'BOOTPAY-SDK-VERSION': self.SDK_VERSION,
            'BOOTPAY-API-VERSION': self.API_VERSION,
            'BOOTPAY-SDK-TYPE': '302',
            'BOOTPAY-ROLE': self._role or 'user'
        }
        basic_auth = self._get_basic_auth_header()
        if basic_auth:
            request_headers['Authorization'] = basic_auth
        if headers:
            request_headers.update(headers)
        return request_headers

    def _serialize_form_data(self, data: Dict) -> Dict[str, str]:
        """
        폼 데이터 직렬화
        ⚠️ bool 은 소문자 'true'/'false' 로 보낸다 — str(True) 의 'True'/'False' 는
           Rails 캐스팅 대상이 아니라서 "False" 가 true 로 해석되는 실위험이 있다.
        """
        form_data = {}
        for key, value in data.items():
            if value is not None:
                if isinstance(value, bool):
                    form_data[key] = 'true' if value else 'false'
                elif isinstance(value, (dict, list)):
                    form_data[key] = json.dumps(value)
                else:
                    form_data[key] = str(value)
        return form_data

    def put(self, url: str, data: Optional[Dict] = None, headers: Optional[Dict[str, str]] = None):
        """PUT 요청"""
        response = requests.put(
            self._entrypoints(url),
            headers=self._get_headers(headers=headers),
            json=data,
            timeout=self.timeout
        )
        return response.json()

    def delete(self, url: str, params: Optional[Dict] = None, headers: Optional[Dict[str, str]] = None,
               data: Optional[Dict] = None):
        """
        DELETE 요청
        :param data: 요청 body (JSON) — 대상 ID 를 query 가 아닌 body 로 보내는 endpoint 용
        """
        response = requests.delete(
            self._entrypoints(url),
            headers=self._get_headers(headers=headers),
            params=params,
            json=data,
            timeout=self.timeout
        )
        return response.json()
