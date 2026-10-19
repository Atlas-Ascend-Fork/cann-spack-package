# CANN社区项目 Spack 包仓库

## 📦 概述

本仓库管理 CANN社区 维护的spack软件包集合（如cann-toolkit、cann-ops等），核心文件为Spack package 定义文件（`package.py`），需要搭配[spack包管理器](https://gitcode.com/GitHub_Trending/sp/spack)一起使用。
package.py文件描述CANN各开源组件的版本、依赖、构建打包指令等，方便通过spack包管理器统一安装CANN环境。

## 适用场景
* Spack 是一款专为高性能计算 (HPC) 和科学计算设计的灵活软件包管理器，支持依赖自动解析、下载、编译和安装，在本地构造复杂的软件栈，同时支持多版本并存，互不干扰。
* spack 通过绑定本仓库后，可以使用spack install命令快速安装CANN组件，并自动解析下载组件运行时需要的依赖软件，一键构造算子开发运行环境。具体操作步骤参考[快速开始](#🚀快速开始)


## 🏗️ 仓库结构

```
仓库根目录/
├── packages/               # 所有 package.py 文件
│   ├── cann-project1/           # 项目1的package定义
│   │   └── package.py
│   ├── cann-project2/           # 项目2的package定义
│   │   └── package.py
│   └── ...
├── repo.yaml            # Spack仓库配置
├── spack-repo-index.yaml
└── README.md
```

## 🚀快速开始

### 1. 添加本仓库到 Spack 包管理器中

```bash
# 克隆仓库
git clone --depth=1 https://gitcode.com/cann/cann-spack-package.git
spack repo add {仓库本地绝对路径}
```

也可以通过手动编辑文件 `~/.spack/repos.yaml`：

```yaml
repos:
  - {仓库本地绝对路径}
```

### 2. 查看可用软件包

```bash
spack list |grep cann-
```

### 3. 安装软件包（以cann-toolkit@8.5.0为例）

```bash

# 创建并进入环境
spack env create cann-env
spack env activate cann-env

# 安装最新版
spack add cann-toolkit
spack install 

# 安装特定版本
spack add cann-toolkit@8.5.0
spack install cann-toolkit

# 查看软件包信息
spack info cann-toolkit
```

## 📝 添加新包

### 1. 创建包定义

```bash
# 创建项目目录
mkdir -p packages/{项目名}
touch packages/{项目名}/package.py
```

### 2. 编写 package.py 模板

```python
from spack.package import *

class {项目名大驼峰命名法}(Package):
    """{项目简短描述}"""
    
    homepage = "{项目主页URL}"
    url = "{源码下载URL}"
    git = "{Git仓库URL}"
    

    # 版本定义
    version("main", branch="main")
    version("{版本号}", tag="{标签名}", sha256="{SHA256值}")
    
    # 依赖
    depends_on("{依赖包名}")
    depends_on("{依赖包名}@{版本范围}")
    depends_on("{依赖包名}+{变体}")
    
    # 变体选项
    variant("{变体名}", default=True, description="{变体描述}")
    
    # 构建阶段
    def setup_build_environment(self, env):
        pass
    
    def configure_args(self):
        args = []
        if "+{变体}" in self.spec:
            args.append("--enable-{功能}")
        return args
    
    def install(self, spec, prefix):
        # 安装逻辑
        configure("--prefix=" + prefix, *self.configure_args())
        make()
        make("install")
```

## ❓ 常见问题

### 安装失败怎么办？
- 查看详细日志：`spack install -v {包名}`
- 检查构建日志：`spack build-env {包名} bash`
- 确认依赖是否满足：`spack spec {包名}`

### 如何更新现有包？
直接编辑对应的 `package.py` 文件并提交 PR。

### spack常用命令
```bash
#查看当前环境列表：
spack env list

#创建环境：spack管理的环境之间互相隔离，以链接的形式与软件包关联
spack env create <env-name>

#启用环境：当前激活的环境字体为绿色，spack的命令以当前激活环境为准，与所处位置无关
spack env activate <env-name>

#查看当前环境中都引入了哪些软件包：如果不在特定环境中执行则为查看所有已安装的软件包
spack find                              #列出所有软件包
spack find -L                           #显示完整哈希
spack find <package-name>               #按包名过滤，不提供则为全部包
spack find --deps <package-name>        #显示该包的依赖树
spack find --explicit <package-name>    #显示手动安装的定级包 缩写：-e
spack find -p <package-name>            #显示完整安装路径
spack find -lv <package-name>           #显示完整哈希和变体信息

#向当前环境中添加软件包：
spack add <package-name>                #同样支持spec语法，指定版本，变体，编译器等

#从当前环境中移除软件包: spack不会删除软件包，只是移除当前环境与软件包之间的依赖
spack remove <package-name>

#卸载软件包：需要所有的spack环境都不依赖该软件包才可以由spack卸载，会卸载本地安装好的包，慎用
spack uninstall <package-name>

#删除某个spack环境：物理删除文件，慎用
spack env remove <env-name>

#取消激活当前环境：
spack env deactivate

#搜索spack支持的软件包
spack list <package-name>
spack list 'py-*'        #列出所有 Python 包
spack list -d 'mpi'      #在描述中搜索 mpi

#查看可用版本号
spack versions <package-name>

#清除spack构建缓存：
spack clean
spack clean -all   #将旧源码与旧构建记录及缓存全部清除，慎用

#查看当前软件包信息：查看该软件包所有支持的版本，spack默认倾向于最新版本
spack info <package-name>

#安装软件包，spack自动选择最新版本
spack install                                                   #安装当前环境中所有未安装的软件包
spack install <package-name>                                    #指定具体的软件包名
spack install <package-name>@1.12.0%gcc@11.4.0                  #spec语法，指定版本与编译器版本
spack install <package-name>+mpi+fortran ^openmpi@4.1           #spec语法，指定变体
spack install <package-name1> <package-name2> <package-name3>   #同时安装多个包
spack -k install                                                #安装时跳过安全认证，慎用
spack install --verbose                                         #输出详细构建日志，缩写：-v
spack install --no-checksum                                     #安装时跳过SHA256校验和验证，慎用

#具体化当前环境：spack的策略是默认倾向于重用已安装在本地的软件包，即使已有更高版本且满足依赖条件，除非本地包已不符合依赖条件
spack concretize

#从远端下载软件包源码到本地并注册为开发包：否则spack引用的远端文件会作为缓存临时文件，会被spack clean清除
spack develop <package-name>

#从本地代码开发目录注册开发包
git clone <git-path>  #克隆源码并进入目录
cd /package/path
spack develop --no-clone <package-name>   

#解析该软件包依赖信息：
spack spec <package-name>

# 如果git仓有更新，该命令可以根据repos.yaml中配置的远程仓库地址与分支进行同步更新
spack repo update <repo name>

#定位软件包安装位置：
spack location -i <package-name>

#查看编译器配置：
spack compilers                                                 #查看所有支持的编译器，同spack compiler list
spack compiler add /path/to/compiler/bin                        #手动添加编译器

#扫描并注册本机已安装软件为外部包
spack external find

#查看spack版本，验证安装：
spack --version

#编辑spack配置: 会自动打开vim
spack config edit config
spack config edit packages
```

## 🔗 相关链接

- [安全声明](SECURITY.md)
- [Spack 官方文档](https://spack.readthedocs.io/)
- [Spack 教程](https://spack-tutorial.readthedocs.io/)
- [社区网站](https://gitcode.com/cann)

---

