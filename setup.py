from setuptools import setup, find_packages

setup(
    name='gp_tools',  # 项目名称
    version='0.1.0',  # 项目版本
    author='Your Name',  # 作者姓名
    author_email='your_email@example.com',  # 作者邮箱
    description='一个机构对股票评级的数据查询工具',  # 项目简短描述
    long_description='该工具用于从新浪财经获取股票相关的机构评级数据，并可将数据存储到 MySQL 数据库中。',  # 项目详细描述
    url='https://github.com/your_username/gp_tools',  # 项目仓库地址
    packages=find_packages(),  # 自动发现项目中的所有包
    install_requires=[
        'mysql-connector-python',  # 连接 MySQL 数据库
        'requests',  # 发送 HTTP 请求
        'beautifulsoup4',  # 解析 HTML 内容
        'lxml'  # 解析 HTML 的解析器
    ],  # 项目依赖的第三方库
    entry_points={
        'console_scripts': [
            'gp_tools = gp_tools.main:main'  # 定义命令行入口，执行 `gp_tools` 命令会调用 main.py 中的 main 函数
        ]
    },  # 命令行入口
    classifiers=[
        'Development Status :: 3 - Alpha',  # 项目开发状态
        'Intended Audience :: Developers',  # 目标受众
        'License :: OSI Approved :: MIT License',  # 项目许可证
        'Programming Language :: Python :: 3',  # 支持的 Python 版本
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],  # 项目分类信息
)