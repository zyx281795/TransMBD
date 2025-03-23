# TransMbD 失智监护辅助系统

## 项目简介

TransMbD（Transformer Mistral 7B based on Dementia）是一个基于大型语言模型的失智症监护辅助系统。该系统旨在利用人工智能技术辅助医护人员观察患者并判定失智症严重程度，同时通过对话引导的方式与患者交互，持续收集和分析文本数据以评估症状变化趋势。

## 功能特点

- **患者交互界面**：提供简洁友好的对话界面，支持文本和语音输入
- **照护人员仪表板**：展示患者状态评估和失智症严重程度预测结果
- **失智症进展预测**：基于患者输入的文本内容分析失智症症状变化趋势
- **引导式对话**：通过智能对话引导患者持续提供有价值的文本信息
- **数据可视化**：将预测结果以直观的图表形式展示

## 技术架构

- 前端：HTML, CSS, JavaScript, Bootstrap
- 后端：Django (Python)
- 模型：基于Mistral 7B的大型语言模型
- 数据存储：SQLite (开发环境)
- 可视化：Plotly, Matplotlib

## 快速开始

### 环境要求

- Python 3.9+
- pip package manager

### 安装步骤

1. 克隆项目仓库
   ```bash
   git clone https://github.com/your-username/transmbd-project.git
   cd transmbd-project
   ```

2. 创建虚拟环境并激活
   ```bash
   python -m venv venv
   source venv/bin/activate  # 在Windows上使用: venv\Scripts\activate
   ```

3. 安装依赖包
   ```bash
   pip install -r requirements.txt
   ```

4. 初始化数据库
   ```bash
   python manage.py migrate
   ```

5. 创建超级用户（可选）
   ```bash
   python manage.py createsuperuser
   ```

6. 启动开发服务器
   ```bash
   python manage.py runserver
   ```

7. 访问系统
   - 患者界面: http://127.0.0.1:8000/patient/
   - 照护人员仪表板: http://127.0.0.1:8000/caregiver/
   - 管理界面: http://127.0.0.1:8000/admin/

## 使用示例

### 患者界面

1. 访问患者界面
2. 通过文本框或语音输入功能与系统交互
3. 系统会根据输入内容生成回复，并引导继续对话

### 照护人员仪表板

1. 登录照护人员账户
2. 查看患者列表及其预测的失智症严重程度
3. 点击具体患者查看详细分析报告和历史对话记录
4. 导出数据进行进一步分析

## 项目团队

- 开发者：[您的姓名]
- 指导教授：[教授姓名]
- 合作单位：[失智症共同照护中心名称]

## 许可证

[指定项目许可证]
