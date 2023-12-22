import platform

def get_device_version():
    device = platform.system()  # 현재 실행 중인 기기의 운영체제를 가져옵니다.

    if device == 'Windows':
        return 'Windows 버전'
    elif device == 'Darwin':
        return 'MacOS 버전'
    elif device == 'Linux':
        return 'Linux 버전'
    else:
        return '기타 기기'

device_version = get_device_version()
print(device_version)
