import csv
import json
from typing import Dict, Optional
import os
from pathlib import Path

class KaggleAPI:
    def __init__(self, accounts_list: Optional[list[dict]] = None):
        """初始化KaggleAPI类
        
        Args:
            accounts_list: 可选的账户列表，格式为[{"username": str, "key": str}, ...]
            如果不提供，则从CSV文件读取
        """
        self.accounts: Dict[str, dict] = {}
        
        if accounts_list:
            for account in accounts_list:
                self.accounts[account['key']] = {
                    'username': account['username'],
                    'password': account['key']
                }
        else:
            self.auth_csv_file = os.path.join(os.path.dirname(__file__), 'users-private.csv')
            if not os.path.exists(self.auth_csv_file):
                self.auth_csv_file = os.path.join(os.path.dirname(__file__), 'users.csv')
            self._load_accounts(self.auth_csv_file)

        self.kaggle_auth_file = os.path.join(str(Path.home()), '.kaggle', 'kaggle.json')
        self.kaggle_kernel_dir = os.path.join(str(Path.home()), 'kaggle', 'kernel')
        os.makedirs(self.kaggle_kernel_dir, exist_ok=True)
        self.kaggle_kernel_py_path = os.path.join(self.kaggle_kernel_dir, 'kernel.py')
    
    def _load_accounts(self, csv_path: str) -> None:
        try:
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    account_info = {
                        'username': row['username'],
                        'password': row['password']
                    }
                    self.accounts[str(row['key'])] = account_info
        except Exception as e:
            print(f"加载CSV文件时出错: {e}")
    
    def get_account(self, key: int) -> Optional[dict]:
        return self.accounts.get(str(key))
    
    def change_kaggle_user(self, key: int) -> None:
        account = self.get_account(key)
        if account:
            with open(self.kaggle_auth_file, 'w', encoding='utf-8') as f:
                json.dump(account, f)
        return account['username']
    
    def update_metadata(self, kernel_name: str, username: str, gpu: bool = False) -> None:
        kernel_metadata = {
            "id": f"{username}/{kernel_name}",
            "title": kernel_name,
            "code_file": self.kaggle_kernel_py_path,
            "language": "python",
            "kernel_type": "script",
            "is_private": "true",
            "enable_gpu": "true" if gpu else "false",
            "enable_tpu": "false",
            "enable_internet": "true",
            "dataset_sources": [],
            "competition_sources": [],
            "kernel_sources": [],
            "model_sources": []
        }
        with open(self.kaggle_kernel_metadata_path, 'w', encoding='utf-8') as f:
            json.dump(kernel_metadata, f)
        
        print(f'Metadata file {self.kaggle_kernel_metadata_path} created.')

    def update_kernel_script(self, file_path: str, new_key: int) -> None:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            if lines[0].startswith('KKK'):
                lines[0] = f"KKK={new_key}\n"
            else:
                raise ValueError('the first line of the kernel script file must be KKK = ...')
        with open(self.kaggle_kernel_py_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        print(f'Kernel script file {self.kaggle_kernel_py_path} updated.')
    
    def push_kernel(self, userkey: str, script_path: str, key: int, kernel_name: str, gpu: bool = False) -> None:
        username = self.change_kaggle_user(userkey)
        self.update_metadata(kernel_name, username, gpu)
        self.update_kernel_script(script_path, key)
        try:
            import subprocess
            result = subprocess.run(
                ['kaggle', 'kernels', 'push', '-p', self.kaggle_kernel_dir],
                capture_output=True,
                text=True,
                check=True
            )
            print(f"内核推送成功: {result.stdout}")
        except subprocess.CalledProcessError as e:
            print(f"推送内核时出错: {e.stderr}")
        except Exception as e:
            print(f"发生未知错误: {str(e)}")

    @property
    def account_count(self) -> int:
        return len(self.accounts)
    
    @property
    def accounts_keys(self) -> list[str]:
        return list(self.accounts)
