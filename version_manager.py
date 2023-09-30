import subprocess
import os


# 현재 스크립트 파일의 경로
script_dir = os.path.dirname(os.path.abspath(__file__))

# 파일 경로 설정
version_file = os.path.join(script_dir, 'version.txt')
commit_hash_file = os.path.join(script_dir, 'commit_hash.txt')



class VersionManager:
    def __init__(self, version_file, commit_hash_file):
        self.version_file = version_file
        self.commit_hash_file = commit_hash_file
        self.major_version, self.minor_version = self.load_version()
        self.commit_hash = self.load_commit_hash()

    def load_version(self):
        try:
            with open(self.version_file, 'r') as f:
                major, minor = map(int, f.read().strip().split('.'))
                return major, minor
        except FileNotFoundError:
            with open(self.version_file, 'w') as f:
                f.write("0.0")
            return 0, 0

        

    def save_version(self):
        with open(self.version_file, 'w') as f:
            f.write(f"{self.major_version}.{self.minor_version}")

    def load_commit_hash(self):
        try:
            with open(self.commit_hash_file, 'r') as f:
                return f.read().strip()
        except FileNotFoundError:
            with open(self.commit_hash_file,'w') as f: 
                pass 
            return ""

    def save_commit_hash(self, commit_hash):
        with open(self.commit_hash_file, 'w') as f:
            f.write(commit_hash)

    def increment_minor(self):
        self.minor_version += 1
        self.save_version()
    
    def decrement_minor(self):
        self.minor_version -= 1
        self.save_version()

    def check_commit(self):
        current_commit_hash = self.get_current_commit_hash()
        if current_commit_hash != self.commit_hash:
            self.commit_hash = current_commit_hash
            self.increment_minor()
            self.save_commit_hash(current_commit_hash)

    def get_current_commit_hash(self):
        result = subprocess.run(['git', 'rev-parse', 'HEAD'], capture_output=True, text=True)
        output = result.stdout.strip()
        return output
