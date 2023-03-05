# 网盘管理器
目前本工具仅适配Matlab 2021a，也可以在命令行直接运行Python脚本

## 1 介绍
本工具是一个统一接口的网盘管理器，借助Alist+Rclone组合方案绕过各家网盘的客户端界面，以类似本地盘符的方式访问网盘空间，相比Anyshare具有如下优点：

（1）无需安全口令二次认证。

（2）无需将网盘视频文件先下载到本地才能观看，可以直接在线播放视频。

（3）可以组合多家网盘灵活存储文件，空间不受限。

（4）大厂网盘的iOS移动端支持更加成熟。

**注意：安装本工具之后，将在工程根目录之下新建一个TempCache文件夹用于缓存网盘文件，请尽量将本Matlab工程部署在硬盘空间富裕的盘符中，以免受硬盘空间不足问题的困扰**

**注意：本工具支持联网更新，但是需要连接GitHub下载文件，请自行确认当前PC所处的网络环境可以正常访问GitHub**

调用第三方Golang库 - [Alist](https://github.com/alist-org/alist) + [Rclone](https://github.com/rclone/rclone)

## 2 系统环境配置工作

### 2.1 安装Python
为正常调用Python包，需要在当前PC中安装Python，具体步骤如下：

（1）根据当前所用Matlab版本选择支持的Python版本 - [版本对应表](https://www.mathworks.com/content/dam/mathworks/mathworks-dot-com/support/sysreq/files/python-compatibility.pdf)

（2）到Python官网下载页面选择下载上一步决定的版本 - [Python下载页面](https://www.python.org/downloads/)

（3）在当前PC中运行上一步下载的Python安装包，直至安装完成

（4）在Matlab命令行中运行如下指令，查看Python版本信息，如果与上一步运行的安装包匹配，则说明适配Matlab的Python安装成功
``` matlab
pyenv
```

### 2.2 安装Alist+Rclone库
本工具复用第三方Golang库Alist+Rclone，具体步骤如下：

（1）在Matlab中打开本工具对应的Project，在Matlab命令行中运行如下指令，或者在快捷方式面板中点击同名的图标按钮。
``` matlab
Script_manage_network_disk
```

（2）选择操作"安装网盘链接功能组件"，过程中按照提示完成WinFsp的安装。

## 3 使用方法
（1）在Matlab中打开本工具对应的Project，在Matlab命令行中运行如下指令，或者在快捷方式面板中点击同名的图标按钮。
``` matlab
Script_manage_network_disk
```

（2）选择执行操作"开启网盘链接"。

**注意：初次开启网盘链接之后需要额外按以下步骤完成初始化配置：**
>
> a）打开浏览器，在地址栏输入localhost:5244并回车，将弹出Alist登录界面，用户名admin，密码888888
>
> b）成功登录之后，点击页面下方的"管理"按钮进入管理界面，再点击左侧的"存储"选项卡切换到存储界面，再点击中间的"添加"按钮，参照[官方指导文档](https://alist.nn.ci/zh/)配置自己的网盘账号，可以添加多个网盘

（3）在资源浏览器中打开此电脑，可以看到新增了一个名为"alist_webdav"的网络盘符，打开它即可直接访问自己配置好的各个网盘空间，无需安装各厂家指定的客户端即可实现文件上传下载。
