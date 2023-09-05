# coding:utf-8
from PyQt5.QtCore import Qt
from qfluentwidgets import InfoBar, InfoBarPosition

from managers.config_manager import config
import markdown
import requests
import json

from ..card.messagebox2 import MessageBox2


def checkUpdate(self):
    try:
        url = "https://api.github.com/repos/moesnow/March7thAssistant/releases/latest"
        res = requests.get(url, timeout=3)
        if res.status_code != 200:
            return

        data = json.loads(res.text)
        version = data["tag_name"]
        content = data["body"]
        url = data["html_url"]
        for asset in data["assets"]:
            if "full" in asset["browser_download_url"]:
                continue
            else:
                assert_url = asset["browser_download_url"]
                assert_name = asset["name"].rsplit(".", 1)[0]
                break

        if version > config.version:
            # if True:
            w = MessageBox2(f"发现新版本：{config.version} ——> {version}\n更新日志", markdown.markdown(content), url, self.window())
            if w.exec():
                import tempfile
                import subprocess
                source_file = r".\scripts\update_March7thAssistant.bat"
                temp_dir = tempfile.gettempdir()
                destination_file = temp_dir + "\\update_March7thAssistant.bat"
                subprocess.run(['xcopy', source_file, temp_dir, '/Y'], shell=True, check=True)
                subprocess.run(['start', destination_file, assert_url, assert_name, '/Y'], shell=True, check=True)
        else:
            InfoBar.success(
                title=self.tr('当前是最新版本'),
                content="",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=1000,
                parent=self
            )
    except Exception as e:
        # print(e)
        InfoBar.warning(
            title=self.tr('检测更新失败'),
            content="",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=1000,
            parent=self
        )