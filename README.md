# Setup Steps:
1. 运行build_venv.bat
     1. 安装python
     2. 安装pip插件
   
# Errors:
 1. 无法安装pip插件
    1. pip是否安装
        1. pip --version
        2. pip install -r requirements.txt
    2. requirements.txt内容
       1. 填写以下内容
         mysql-connector
         flask
         flaskwebgui
         jieba

         # dev
         black
         auto-py-to-exe
       2. 在../下运行cmd
       3. pip install -r requirements.txt
 2. 提示系统禁用(报错为"Activate.ps1 cannot be loaded because running scripts is disabled on this system.")
   1. 右键windows图标
   2. 选择"windows powershell(管理员)"
   3. 输入"set-executionpolicy remotesigned"
   4. 输入"y" enter
      
# Others:
1. 安装数据库
   1. 安装php工具(Phpstdy.exe)
      1. 双击sqlsetup.exe
      2. 一直下一步直到完成安装
      3. 点击右侧"软件管理"
      4. 安装"MySQL8.0.12"
   2. 导入数据库
      1. 运行data.py
      2. 完成数据库导入
                            
2. 修改配置文件确保虚拟环境正常运行
   1. 将整个文件夹复制到新的电脑
   2. 修改pyvenv.cfg文件内的home为你新电脑python的安装路径。
   3. 如果使用vscode，还需要修改vscode的配置文件launch.json，这样就可以在新的电脑上调试了。
   4. 修改程序目录下Scripts\activate文件（可以用记事本打开）
   VIRTUAL_ENV="D:\FlaskProgram\DEV\venv"改为你新电脑的位置
   5. 修改程序目录下Scripts\activate.bat文件（可以用记事本打开）
   6. set VIRTUAL_ENV=D:\FlaskProgram\DEV\改为你的位置
   7. 运行程序目录下Scripts\activate.bat文件，激活虚拟环境。

# Introducing
1. config.cfg
   1. 实例
      [config]
      data_mode = False
      dev_mode = False
      keep_login = True

      [Settings]
      acc = zsc
      port = 5000
   2. 讲解
      data_mode  数据库连接方式 True为在线数据库 False为本地数据库
      dave_mode  开发者模式     True为开启开发者 False为关闭开发者
      keep_login 保持登录       True为开启      False为关闭



