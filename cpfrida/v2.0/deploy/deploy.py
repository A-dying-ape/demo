# !/usr/bin/env python
# coding=utf-8
# @Time    : 2022/04/19
# @Author  : XQE
# @Software: PyCharm


import os
import re
import sys
import fire
import configparser
sys.path.append("../common")
from handle_template import FormatTemplate


class QuickBuildProject(object):
    """有望项目部署插件"""
    # 项目配置文件
    build_ini = "build.ini"

    def __init__(self, full=False):
        """初始化架构，并检测环境"""
        self.build_ini_obj = configparser.ConfigParser()
        self.build_ini_obj.read(self.build_ini, encoding='utf-8')
        # 项目目录
        self.project = self.build_ini_obj['project'].get("path")
        self._check_project()
        if full:
            # 工作空间相对路径
            self.workspaces = "../workspaces"
            # 监控相对路径
            self.monitor = "../workspaces/monitor"
            # 模板相对路径
            self.template = "template"
        else:
            # 工作空间绝对路径
            self.workspaces = os.path.join(self.project, "workspaces")
            # 监控绝对路径
            self.monitor = os.path.join(self.workspaces, "monitor")
            # 模板绝对路径
            self.template = os.path.join(os.path.join(self.project, "deploy"), "template")
        self.monitor_config = configparser.ConfigParser()
        self.monitor_config.read(os.path.join(self.monitor, "monitor_conf.ini"), encoding="utf-8")
        # 监控配置内容
        self.monitor_conf = {}
        self.handle_template = None

    def _check_project(self):
        """
        确保当前项目目录是否正常
        :return: None
        """
        if os.path.exists(self.project) is False:
            os.makedirs(self.project, exist_ok=True)
            print("创建项目目录: {}.".format(self.project))

    def _check_workspace(self, space_name):
        """
        检测当前项目下是否有该工作空间
        :param space_name: (string)工作空间
        :return: bool
        """
        workspace = [file for file in os.listdir(self.workspaces)]
        if os.path.isdir(os.path.join(self.workspaces, space_name)):
            return space_name in workspace
        return False

    def _check_file(self, space_name, filename):
        """
        检测该工作空间下是否有该文件
        :param space_name: (string)工作空间
        :param filename: None
        :return: bool
        """
        if self._check_workspace(space_name):
            workspace_path = os.path.join(self.workspaces, space_name)
            workspace = [file for file in os.listdir(workspace_path)]
            if os.path.isfile(os.path.join(workspace_path, filename)):
                return filename in workspace
            return False
        else:
            return False

    def _build_workspace(self, space_name):
        """
        创建工作空间
        :param space_name: (string)工作空间
        :return: None
        """
        if self._check_workspace(space_name):
            print("{}工作空间已存在.".format(space_name))
        else:
            os.mkdir(os.path.join(self.workspaces, space_name))

    def _delete_workspace(self, space_name):
        """
        删除工作空间
        :param space_name: (string)工作空间
        :return: None
        """
        if self._check_workspace(space_name):
            def del_files(path):
                for i in os.listdir(path):
                    cur_path = os.path.join(path, i)
                    if os.path.isdir(cur_path):
                        del_files(cur_path)
                        os.rmdir(cur_path)
                    else:
                        os.remove(cur_path)

            file_path = os.path.join(self.workspaces, space_name)
            del_files(file_path)
            os.rmdir(file_path)
        else:
            print("{}工作空间不存在.".format(space_name))

    def _build_config(self, space_name):
        """
        创建工作空间的配置文件
        :param space_name: (string)工作空间
        :return: None
        """
        if self._check_file(space_name, "config.py"):
            print("{}工作空间下已有config.py".format(space_name))
        else:
            if self._check_workspace(space_name):
                config = self.handle_template.format_template(space_name, "config_template")
                workspace = os.path.join(self.workspaces, space_name)
                with open(os.path.join(workspace, "config.py"), "w", encoding="utf-8") as f:
                    f.write(config)

    def _delete_config(self, space_name):
        """
        删除工作空间的配置文件
        :param space_name: (string)工作空间
        :return: None
        """
        if self._check_file(space_name, "config.py"):
            workspace = os.path.join(self.workspaces, space_name)
            config_path = os.path.join(workspace, "config.py")
            os.remove(config_path)
        else:
            print("{}工作空间不存在或工作空间下没有{}".format(space_name, "config.py"))

    def _build_sh(self, space_name):
        """
        创建linux下的工作空间启动脚本
        :param space_name: (string)工作空间
        :return: None
        """
        if self._check_file(space_name, space_name + ".sh"):
            print("{}工作空间下已有{}文件".format(space_name, space_name + ".sh"))
        else:
            if self._check_workspace(space_name):
                workspace = os.path.join(self.workspaces, space_name)
                bash = self.handle_template.format_template(space_name, "startwork_template")
                with open(os.path.join(workspace, space_name + ".sh"), "w", encoding="utf-8") as f:
                    f.write(bash)
            else:
                print("{}工作空间不存在.".format(space_name))

    def _delete_sh(self, space_name):
        """
        删除linux下的工作空间启动脚本
        :param space_name: (string)工作空间
        :return: None
        """
        if self._check_file(space_name, space_name + ".sh"):
            workspace = os.path.join(self.workspaces, space_name)
            config_path = os.path.join(workspace, space_name + ".sh")
            os.remove(config_path)
        else:
            print("{}工作空间不存在或工作空间下没有{}".format(space_name, space_name + ".sh"))

    def _build_workers(self, space_name):
        """
        创建工作者
        :param space_name: (string)工作空间
        :return: None
        """
        if self._check_file(space_name, space_name + ".py"):
            print("{}工作空间下已有{}文件".format(space_name, space_name + ".py"))
        else:
            if self._check_workspace(space_name):
                workspace = os.path.join(self.workspaces, space_name)
                with open("./template/workspace_template", "r") as f:
                    work = f.read()
                with open(os.path.join(workspace, space_name + ".py"), "w", encoding="utf-8") as f:
                    f.write(work)
            else:
                print("{}工作空间不存在.".format(space_name))

    def _delete_workers(self, space_name):
        """
        删除工作者
        :param space_name: (sting)工作空间
        :return: None
        """
        if self._check_file(space_name, space_name + ".py"):
            workspace = os.path.join(self.workspaces, space_name)
            config_path = os.path.join(workspace, space_name + ".py")
            os.remove(config_path)
        else:
            print("{}工作空间不存在或工作空间下没有{}".format(space_name, space_name + ".py"))

    def _build_uuid(self, space_name):
        """
        创建工作空间的UUID
        :param space_name: (string)工作空间
        :return: None
        """
        if self._check_file(space_name, "uuid"):
            print("{}工作空间下已有uuid".format(space_name))
        else:
            if self._check_workspace(space_name):
                workspace = os.path.join(self.workspaces, space_name)
                with open(os.path.join(workspace, "uuid"), "w", encoding="utf-8") as f1:
                    f1.write(self.build_ini_obj[space_name].get("uuid"))
            else:
                print("{}工作空间不存在.".format(space_name))

    def _delete_uuid(self, space_name):
        """
        删除工作空间的UUID
        :param space_name: (string)工作空间
        :return: None
        """
        if self._check_file(space_name, "uuid"):
            workspace = os.path.join(self.workspaces, space_name)
            config_path = os.path.join(workspace, "uuid")
            os.remove(config_path)
        else:
            print("{}工作空间下不存在或工作空间没有{}".format(space_name, "uuid"))

    def _build_monitor_config(self, space_name):
        if self._check_file(space_name, "monitor_conf.ini"):
            print("{}工作空间已有监控配置monitor_conf.ini".format(space_name))
        else:
            with open(os.path.join(self.monitor, "monitor_conf.ini"), "w", encoding="utf-8") as f:
                f.write("")
            self.monitor_config["config"] = {
                "reboot": self.build_ini_obj["monitor"]["reboot"]
            }
            self.monitor_config["devices"] = self.monitor_conf
            self.monitor_config.write(open(os.path.join(self.monitor, "monitor_conf.ini"), "w", encoding="utf-8"), space_around_delimiters=False)
            print("成功释放monitor_conf.ini")

    def _delete_monitor_config(self, space_name):
        if os.path.exists(os.path.join(self.monitor, "monitor_conf.ini")):
            config_path = os.path.join(self.monitor, "monitor_conf.ini")
            os.remove(config_path)
            print("成功收纳monitor_conf.ini")
        else:
            print("{}工作空间下不存在或工作空间没有{}".format(space_name, "monitor_conf.ini"))

    def receive_workspace(self, flag=False, space_name=None):
        """
        收纳当前项目下的所有工作空间
        :param flag: (bool)收纳的时候是否覆盖项目配置文件
        :param space_name: (string)工作空间，如果没有指定工作空间默认为None，操作所有工作空间
        :return: None
        """
        if space_name is None:
            workspace = [file for file in os.listdir(self.workspaces)]
            # 封装配置对象
            for i in workspace:
                if i in set(self.build_ini_obj.sections()[3:]):
                    self.build_ini_obj[i] = {}
                    config_dict = self.build_ini_obj[i]
                    try:
                        worker_path = os.path.join(self.workspaces, i)
                        with open(os.path.join(worker_path, "config.py"), "r", encoding="utf-8") as f1:
                            content1 = f1.read()
                            config_dict["timeout"] = re.search(r"timeout = (.*?)\n", content1).group(1).strip()
                            config_dict["frida_host"] = re.search(r"frida_host = r\"(.*?)\"\n", content1).group(1).strip()
                            config_dict["adb_host"] = re.search(r"adb_host = r\"(.*?)\"\n", content1).group(1).strip()
                            config_dict["app_name_en"] = re.search(r"app_name_en = r\"(.*?)\"\n", content1).group(1).strip()
                            config_dict["app_name_ch"] = re.search(r"app_name_ch = r\"(.*?)\"\n", content1).group(1).strip()
                            config_dict["app_ui"] = re.search(r"app_ui = r\"(.*?)\"\n", content1).group(1).strip()
                            config_dict["workspace"] = i
                            config_dict["hook_script"] = re.search(r"hook_script = os\.path\.join\(os\.path\.join\(project_path, \"hookscript\"\), r\"(.*?)\"\)\n", content1).group(1).strip()
                            config_dict["get_url"] = re.search(r"get_url = (.*?)\n", content1).group(1).strip()
                            config_dict["post_url"] = re.search(r"post_url = (.*?)\n", content1).group(1).strip()
                            config_dict["username"] = re.search(r"username = r\"(.*?)\"\n", content1).group(1).strip()
                            config_dict["inform_url"] = re.search(r"inform_url = r\"(.*?)\"\n", content1).group(1).strip()
                        with open(os.path.join(worker_path, "uuid"), "r", encoding="utf-8") as f2:
                            content2 = f2.read()
                            config_dict["uuid"] = content2.strip()
                        if flag:
                            self.build_ini_obj.write(open(self.build_ini, 'w', encoding='utf-8'), space_around_delimiters=False)
                    except Exception as e:
                        print("你已手动改过代码，请重新生成%s." % i)
                    self._delete_workspace(i)
                    print("收纳工作空间%s完成." % i)
                else:
                    print("%s不是工作空间，无法进行收纳." % i)
            self._delete_monitor_config("monitor")
            print("已完成所有工作空间收纳.")
        else:
            self.build_ini_obj[space_name] = {}
            config_dict = self.build_ini_obj[space_name]
            try:
                config_dict["section"] = space_name
                worker_path = os.path.join(self.workspaces, space_name)
                with open(os.path.join(worker_path, "config.py"), "r", encoding="utf-8") as f1:
                    content1 = f1.read()
                    config_dict["timeout"] = re.search(r"timeout = (.*?)\n", content1).group(1).strip()
                    config_dict["frida_host"] = re.search(r"frida_host = r\"(.*?)\"\n", content1).group(1).strip()
                    config_dict["adb_host"] = re.search(r"adb_host = r\"(.*?)\"\n", content1).group(1).strip()
                    config_dict["app_name_en"] = re.search(r"app_name_en = r\"(.*?)\"\n", content1).group(1).strip()
                    config_dict["app_name_ch"] = re.search(r"app_name_ch = r\"(.*?)\"\n", content1).group(1).strip()
                    config_dict["app_ui"] = re.search(r"app_ui = r\"(.*?)\"\n", content1).group(1).strip()
                    config_dict["workspace"] = space_name
                    config_dict["hook_script"] = re.search(r"hook_script = os\.path\.join\(os\.path\.join\(project_path, \"hookscript\"\), r\"(.*?)\"\)\n", content1).group(1).strip()
                    config_dict["get_url"] = re.search(r"get_url = (.*?)\n", content1).group(1).strip()
                    config_dict["post_url"] = re.search(r"post_url = (.*?)\n", content1).group(1).strip()
                    config_dict["username"] = re.search(r"username = r\"(.*?)\"\n", content1).group(1).strip()
                    config_dict["inform_url"] = re.search(r"inform_url = r\"(.*?)\"\n", content1).group(1).strip()
                with open(os.path.join(worker_path, "uuid"), "r", encoding="utf-8") as f2:
                    content2 = f2.read()
                    config_dict["uuid"] = content2.strip()
                if flag:
                    self.build_ini_obj.write(open(self.build_ini, 'w', encoding='utf-8'), space_around_delimiters=False)
            except Exception as e:
                print("你已手动改过代码，请重新生成%s." %space_name)
            self._delete_workspace(space_name)
            try:
                self.monitor_config.remove_option("devices", space_name)
                self.monitor_config.write(open(os.path.join(self.monitor, "monitor_conf.ini"), "w", encoding="utf-8"), space_around_delimiters=False)
            except Exception as e:
                print("monitor_conf.ini配置吗文件配置错误或者不存在.")
            print("收纳工作空间%s完成." % space_name)

    def release_workspace(self, space_name=None):
        """
        释放所有收纳的工作空间
        :param space_name: (string)空间名称，如果没有指定工作空间默认为None，操作所有工作空间
        :return: None
        """
        self.handle_template = FormatTemplate()
        if space_name is None:
            self._build_monitor_config(self.monitor)
            for i in self.build_ini_obj.sections()[3:]:
                try:
                    self._build_workspace(i)
                    self._build_config(i)
                    self._build_uuid(i)
                    self._build_sh(i)
                    self._build_workers(i)
                    self.monitor_config["devices"][i] = self.build_ini_obj[i].get("adb_host")
                    self.monitor_config.write(open(os.path.join(self.monitor, "monitor_conf.ini"), "w", encoding="utf-8"), space_around_delimiters=False)
                    print("释放工作空间%s完成." % i)
                except Exception as e:
                    self._delete_workspace(i)
                    print("释放工作空间%s失败: %s" % (i, e))
            print("已释放所有的工作空间.")
        else:
            try:
                self._build_workspace(space_name)
                self._build_config(space_name)
                self._build_uuid(space_name)
                self._build_sh(space_name)
                self._build_workers(space_name)
                if os.path.exists(os.path.join(self.monitor, "monitor_conf.ini")):
                    self.monitor_config["devices"][space_name] = self.build_ini_obj[space_name].get("frida_host")
                    self.monitor_config.write(open(os.path.join(self.monitor, "monitor_conf.ini"), "w", encoding="utf-8"), space_around_delimiters=False)
                else:
                    self._build_monitor_config(self.monitor)
                    self.monitor_config["devices"][space_name] = self.build_ini_obj[space_name].get("frida_host")
                    self.monitor_config.write(open(os.path.join(self.monitor, "monitor_conf.ini"), "w", encoding="utf-8"), space_around_delimiters=False)
                print("释放工作空间%s完成." % space_name)
            except Exception as e:
                self._delete_workspace(space_name)
                print("释放工作空间%s失败: %s" % (space_name, e))


if __name__ == '__main__':
    # fire.Fire(QuickBuildProject())
    QuickBuildProject().release_workspace()
    # QuickBuildProject().receive_workspace()
    # QuickBuildProject().release_workspace("comment4")
    # QuickBuildProject().receive_workspace(False, "comment4")