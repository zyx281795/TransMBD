# TransMbD 失智监护辅助系统安装指南

本指南详细说明如何在本地环境中安装和部署 TransMbD 失智监护辅助系统，以便您可以进行演示和测试。

## 系统要求

- Python 3.9 或更高版本
- 至少 4GB 可用内存
- 至少 2GB 可用磁盘空间
- 支持的操作系统：Windows 10/11、macOS 10.15+、Ubuntu 20.04+

## 安装步骤

### 1. 克隆或下载项目

您可以通过以下方式获取项目代码：

```bash
# 使用 Git 克隆（如果您有项目仓库）
git clone https://github.com/your-username/transmbd-project.git
cd transmbd-project

# 或者下载并解压缩项目压缩包
# 然后进入项目目录
```

### 2. 使用自动安装脚本

为了简化安装过程，我们提供了自动安装脚本。根据您的操作系统选择相应的脚本：

#### Windows 用户

双击运行 `run_demo.bat` 文件或在命令提示符中运行：

```cmd
run_demo.bat
```

#### macOS/Linux 用户

在终端中运行：

```bash
chmod +x run_demo.sh  # 赋予脚本执行权限
./run_demo.sh
```

这些脚本将自动执行以下操作：
- 创建 Python 虚拟环境
- 安装所需依赖
- 设置数据库
- 创建演示管理员账户
- 加载演示数据
- 启动开发服务器

当脚本完成后，您可以通过浏览器访问 [http://127.0.0.1:8000](http://127.0.0.1:8000) 来使用系统。

### 3. 手动安装（如果自动脚本失败）

如果自动安装脚本失败，您可以按照以下步骤手动安装：

#### 3.1 创建和激活虚拟环境

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### 3.2 安装依赖

```bash
pip install -r requirements.txt
```

#### 3.3 初始化数据库

```bash
python manage.py migrate
```

#### 3.4 创建管理员账户

```bash
python manage.py createsuperuser
```
按照提示输入用户名、电子邮件和密码。

#### 3.5 启动开发服务器

```bash
python manage.py runserver
```

现在您可以通过浏览器访问 [http://127.0.0.1:8000](http://127.0.0.1:8000) 来使用系统。

#### 其他指令1

您可以通过以下命令验证数据库表是否已正确创建：
```bash
python manage.py dbshell

```

#### 其他指令2

```bash
python manage.py makemigrations core

```

系统应该会显示类似于以下内容的输出：
CopyMigrations for 'core':
  core/migrations/0001_initial.py
    - Create model Patient
    - Create model Conversation
    - Create model Message
    - Create model DementiaAssessment

## 登录信息

如果您使用自动安装脚本，系统将创建一个默认的管理员账户：

- 用户名：`admin`
- 密码：`admin`

出于安全考虑，在实际部署中应立即更改此默认密码。

## 使用说明

安装完成后，您可以通过以下两个主要界面使用系统：

1. **患者界面**：[http://127.0.0.1:8000/patient/](http://127.0.0.1:8000/patient/)
   - 提供对话交互功能，支持文本和模拟语音输入
   - 系统会根据对话内容生成评估结果

2. **照护人员界面**：[http://127.0.0.1:8000/caregiver/](http://127.0.0.1:8000/caregiver/)
   - 需要登录管理员账户
   - 提供患者管理、评估查看和数据分析功能

## 常见问题

1. **依赖项安装失败**
   
   如果某些依赖项安装失败，请尝试更新 pip：
   ```bash
   pip install --upgrade pip
   ```
   然后重新尝试安装依赖项。

2. **数据库迁移错误**
   
   如果遇到数据库迁移错误，请尝试删除数据库文件（db.sqlite3）并重新运行迁移：
   ```bash
   rm db.sqlite3  # 在 Windows 上使用 del db.sqlite3
   python manage.py migrate
   ```

3. **服务器启动失败**
   
   如果开发服务器无法启动，请检查端口 8000 是否被占用。您可以通过以下命令使用不同的端口：
   ```bash
   python manage.py runserver 8080
   ```
   然后访问 [http://127.0.0.1:8080](http://127.0.0.1:8080)。

## 更多帮助

如需进一步的帮助或遇到其他问题，请参阅项目文档或联系开发团队。
