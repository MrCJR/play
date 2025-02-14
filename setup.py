import os
import sys
import logging
import platform
import argparse
import shutil
from datetime import datetime
from PyInstaller.__main__ import run


class PackageConfig:
    """
    打包配置类
    包含所有打包相关的配置信息，方便集中管理和修改
    """

    # 基础配置信息
    MAIN_SCRIPT = 'main.py'  # 主程序入口文件
    RESOURCES_PATH = 'static'  # 静态资源目录
    OUTPUT_DIR = 'dist'  # 默认输出目录

    # 应用信息配置
    APP_NAME = 'play'  # 应用名称
    APP_VERSION = '1.0.1'  # 应用版本号

    # 图标文件配置
    ICONS = {
        'windows': 'static/icons/app.ico',  # Windows 图标
        'macos': 'static/icons/app.icns',  # macOS 图标
        'linux': 'static/icons/app.png'  # Linux 图标
    }

    # 必需的Python依赖模块
    REQUIRED_MODULES = [
        'PySide6',  # GUI框架
        'PyInstaller'  # 打包工具
    ]

    # 各操作系统特定的打包配置
    SYSTEM_CONFIGS = {
        'windows': {
            'name': 'Windows',# 系统名称，用于显示和日志记录
            'args': [
                '--onefile',  # 打包成单个文件
                '--noconsole',  # 不显示控制台窗口
                '--clean',  # 清理临时文件
                '--name={}'.format(APP_NAME),
                '--icon={}',  # 图标路径（运行时填充）
                '--version-file=version.txt'  # 版本信息文件
            ]
        },
        'macos': {
            'name': 'macOS',  # 系统名称，用于显示和日志记录
            'bundle_id': 'com.guofeng.play', # macOS应用的唯一标识符，格式：com.公司名.应用名
            'args': [
                '--windowed',             # 创建一个纯GUI应用，不显示终端窗口
                '--clean',                 # 在构建之前清理临时文件和缓存
                '--name={}'.format(APP_NAME),
                '--icon={}',               # macOS要求使用.icns格式的图标
                '--osx-bundle-identifier=com.guofeng.play',  # 设置macOS应用程序包的标识符，系统识别用，如更新和权限管理
                '--target-architecture=x86_64'      # 指定目标CPU架构 x86_64: Intel芯片
            ]
        },
        'linux': {
            'name': 'Linux', # 系统名称，用于显示和日志记录
            'args': [
                '--onefile',  # 打包成单个文件
                '--clean',  # 清理临时文件
                '--strip',  # 减小文件体积
                '--name={}'.format(APP_NAME),
                '--icon={}',  # 图标路径（运行时填充）
                '--runtime-tmpdir=.'  # 运行时临时目录
            ]
        }
    }


def setup_logging(debug=False):
    """
    配置日志系统

    Args:
        debug (bool): 是否启用调试模式

    Returns:
        logger: 配置好的日志记录器
    """
    # 创建日志目录
    log_dir = 'logs'
    os.makedirs(log_dir, exist_ok=True)

    # 生成日志文件名（包含时间戳）
    log_file = os.path.join(log_dir, f'package_{datetime.now():%Y%m%d_%H%M%S}.log')

    # 设置日志级别
    level = logging.DEBUG if debug else logging.INFO

    # 配置日志格式和处理器
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),  # 文件处理器
            logging.StreamHandler()  # 控制台处理器
        ]
    )
    return logging.getLogger(__name__)


def parse_arguments():
    """
    解析命令行参数

    Returns:
        argparse.Namespace: 解析后的命令行参数
    """
    parser = argparse.ArgumentParser(description='视频播放器打包工具')
    parser.add_argument('--os',
                        choices=['windows', 'linux', 'macos'],
                        help='目标操作系统')
    parser.add_argument('--debug',
                        action='store_true',
                        help='启用调试模式')
    parser.add_argument('--output-dir',
                        help='指定输出目录')
    return parser.parse_args()


def check_environment():
    """
    检查打包环境，确保满足所有必要条件

    Raises:
        RuntimeError: 当环境检查失败时抛出
    """
    logger = logging.getLogger(__name__)

    # 检查Python版本
    if sys.version_info < (3, 10):
        raise RuntimeError("需要 Python 3.10 或更高版本")
    logger.debug("Python 版本检查通过")

    # 检查必需的Python模块
    missing_modules = []
    for module in PackageConfig.REQUIRED_MODULES:
        try:
            __import__(module)
        except ImportError:
            missing_modules.append(module)

    if missing_modules:
        raise RuntimeError(f"缺少必要的依赖模块: {', '.join(missing_modules)}")
    logger.debug("依赖模块检查通过")

    # 检查资源目录
    if not os.path.exists(PackageConfig.RESOURCES_PATH):
        raise RuntimeError(f"资源目录不存在: {PackageConfig.RESOURCES_PATH}")
    logger.debug("资源目录检查通过")


def select_target_os():
    """
    交互式选择目标操作系统

    Returns:
        str: 选择的目标操作系统标识符
    """
    print("\n请选择目标操作系统：")
    options = {
        '1': 'windows',
        '2': 'linux',
        '3': 'macos'
    }

    # 显示选项
    for key, value in options.items():
        print(f"{key}. {PackageConfig.SYSTEM_CONFIGS[value]['name']}")

    # 获取用户输入
    while True:
        choice = input("\n请输入数字 (1/2/3): ").strip()
        if choice in options:
            return options[choice]
        print("错误：无效选项，请重新选择！")


def prepare_build_args(target_os, output_dir):
    """
    准备构建参数

    Args:
        target_os (str): 目标操作系统
        output_dir (str): 输出目录

    Returns:
        list: PyInstaller命令行参数列表
    """
    logger = logging.getLogger(__name__)

    # 获取系统特定配置
    system_config = PackageConfig.SYSTEM_CONFIGS[target_os]

    # 准备基础参数
    base_args = [
        PackageConfig.MAIN_SCRIPT,
        f'--distpath={output_dir}',
        # 根据操作系统使用不同的路径分隔符
        f'--add-data={PackageConfig.RESOURCES_PATH};resources' if target_os == 'windows'
        else f'--add-data={PackageConfig.RESOURCES_PATH}:resources',
        '--noconfirm'
    ]

    # 获取系统特定参数
    specific_args = system_config['args']

    # 设置图标路径
    icon_path = PackageConfig.ICONS[target_os]
    specific_args = [arg.format(icon_path) if '{}' in arg else arg for arg in specific_args]

    return base_args + specific_args


def post_build_tasks(target_os, output_dir):
    """
    执行打包后的处理任务

    Args:
        target_os (str): 目标操作系统
        output_dir (str): 输出目录

    Raises:
        Exception: 当后处理任务失败时抛出
    """
    logger = logging.getLogger(__name__)

    try:
        # 创建README文件
        readme_path = os.path.join(output_dir, 'README.txt')
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(f"{PackageConfig.APP_NAME} v{PackageConfig.APP_VERSION}\n")
            f.write("================================\n\n")
            f.write("安装说明：\n")
            f.write("1. 解压文件\n")
            f.write("2. 运行可执行文件\n\n")
            f.write("注意事项：\n")
            f.write("- 请确保资源文件完整\n")
            f.write("- 如遇问题请查看日志文件\n")

        # 为Linux创建.desktop文件
        if target_os == 'linux':
            desktop_path = os.path.join(output_dir, f"{PackageConfig.APP_NAME}.desktop")
            with open(desktop_path, 'w', encoding='utf-8') as f:
                f.write("[Desktop Entry]\n")
                f.write(f"Name={PackageConfig.APP_NAME}\n")
                f.write("Type=Application\n")
                f.write(f"Exec={PackageConfig.APP_NAME}\n")
                f.write(f"Icon={PackageConfig.ICONS['linux']}\n")
                f.write("Categories=AudioVideo;\n")

        # 创建压缩包
        archive_name = os.path.join(
            output_dir,
            f"{PackageConfig.APP_NAME}_{target_os}_{PackageConfig.APP_VERSION}"
        )
        shutil.make_archive(archive_name, 'zip', output_dir)
        logger.info(f"已创建压缩包: {archive_name}.zip")

    except Exception as e:
        logger.error(f"后处理任务失败: {str(e)}")
        raise


def main():
    """
    主函数，协调整个打包流程
    """
    # 解析命令行参数
    args = parse_arguments()

    # 设置日志系统
    logger = setup_logging(args.debug)
    logger.info("开始打包流程")

    try:
        # 环境检查
        check_environment()

        # 确定目标系统
        target_os = args.os or select_target_os()
        current_os = platform.system().lower()
        if target_os != current_os:
            logger.warning(f"警告：当前系统为 {current_os}，正在为 {target_os} 打包！")

        # 设置输出目录
        output_dir = args.output_dir or os.path.join(
            PackageConfig.OUTPUT_DIR,
            f"{target_os}_{datetime.now():%Y%m%d_%H%M%S}"
        )
        os.makedirs(output_dir, exist_ok=True)

        # 准备构建参数
        build_args = prepare_build_args(target_os, output_dir)
        logger.debug(f"构建参数: {build_args}")

        # 执行打包
        logger.info(f"开始为 {target_os} 构建应用...")
        run(build_args)

        # 执行后处理任务
        logger.info("执行后处理任务...")
        post_build_tasks(target_os, output_dir)

        logger.info(f"打包完成！输出目录: {output_dir}")

    except Exception as e:
        logger.error(f"打包失败: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    main()

