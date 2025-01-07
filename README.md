# Kaggle API 工具

这是一个用于管理多个Kaggle账户的API工具。支持两种方式初始化账户信息：通过CSV文件或直接传递账户列表。

## 安装

```bash
pip install -r requirements.txt
```

## 使用方法

### 1. CSV文件方式

修改`users.csv`文件，包含以下格式：
```csv
key,username,password,email
0,example_username0,example_password0,example_email0
1,example_username1,example_password1,example_email1
2,example_username2,example_password2,example_email2
```

使用示例：
```python
kaggle_api = KaggleAPI()
```

### 2. 直接传递账户列表

你可以直接传递账户列表：
```python
accounts = [
    {
        "username": "example_username0",
        "key": "example_password0"
    },
    {
        "username": "example_username1",
        "key": "example_password1"
    },
    {
        "username": "example_username2",
        "key": "example_password2"
    }
]

kaggle_api = KaggleAPI(accounts_list=accounts)
```

### 3. 推送内核到Kaggle

使用`push_kernel`函数可以将本地脚本推送到Kaggle作为新的内核：

```python
# 初始化API
kaggle_api = KaggleAPI()

# 推送内核
kaggle_api.push_kernel(
    userkey="0",                                # 用户键（第n个用户，以0开始计数）
    script_path="path/to/your/script.py",       # 本地脚本路径，脚本第一行必须以KKK=开头
    key=1,                                      # 新的key值，用于替换第一行中的KKK=
    kernel_name="my_kernel",                    # Kaggle内核名称，同名将会新增版本
    gpu=False                                   # 是否启用GPU（可选，默认False）
)
```

注意：
- 本地脚本的第一行必须以`KKK=`开头，用于标识key值
- 确保已安装并配置好kaggle命令行工具