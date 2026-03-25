# ----------------------------------------------------------------------------
# This program is free software, you can redistribute it and/or modify.
# Copyright (c) 2026 Huawei Technologies Co., Ltd.
# This file is a part of the CANN Open Software.
# Licensed under CANN Open Software License Agreement Version 2.0 (the "License").
# Please refer to the License for details. You may not use this file except in compliance with the License.
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY, OR FITNESS FOR A PARTICULAR PURPOSE.
# See LICENSE in the root of the software repository for the full text of the License.
# ----------------------------------------------------------------------------

import os
import stat
import glob
import subprocess
import platform

from spack_repo.builtin.build_systems.generic import Package
from spack.package import *


class CannOpsMath(Package):
    homepage = "https://gitcode.com"
    git = "https://gitcode.com/cann/ops-math.git"

    version("master", branch="master")
    version("9.0.0-beta.1", commit="928b614c209f777751389b694ecb2762a9df5b78")
    version("8.5.0", commit="f1a42c5381bbd33981877ad87751d242663c2ce6")
    version("8.5.0-beta.1", commit="5b2e7da1bb5004a3f2192f1fd91ee303b18e6744")

    # 依赖项
    with when('~runfile'):
        depends_on('python@3.7.0:', type='build')
        depends_on('gcc@7.3.0:', type='build')
        depends_on('cmake@3.16.0:', type='build')
        depends_on('pigz@2.4:', type='build')
        depends_on('dos2unix', type='build')
        depends_on('gawk', type='build')
        depends_on('py-pyyaml', type='build')
        depends_on('googletest@1.11.0', type='build')
        depends_on('py-pip', type='build')
        depends_on('py-setuptools', type='build')
        depends_on('py-wheel', type='build')
    for v in ["8.5.0-beta.1", "8.5.0", "9.0.0-beta.1"]:
        depends_on(f"cann-toolkit@{v}", type=['build', 'run'], when=f"@{v}")
    depends_on(f"cann-toolkit@9.0.0-beta.1", type=['build', 'run'], when="@master")

    variant('runfile', default=False, description='install from run file rather than build form source')
    variant('pkg', default=False, description='Build run package with kernel bin')
    variant('jit', default=False, description='Build run package without kernel bin')
    variant('soc', default="none", description='Compile for specified Ascend SoC (comma-separated for multiple)')
    variant('vendor_name', default="none", description='Specify custom operator package vendor name')
    variant('ops', default="none", description='Compile specified operators (comma-separated for multiple)')
    variant('j', default="8", description='Compile thread nums, default is 8, eg: -j8', multi=False)
    variant('O', default="none", description='Compile optimization options, support [O0 O1 O2 O3], eg:-O3')
    variant('debug', default=False, description='Build with debug mode')
    variant('experimental', default=False, description='Build experimental version')

    variant('opkernel', default=False, description='Build binary kernel')

    variant('u', default=False, description='Build and run all unit tests')
    variant('noexec', default=False, description='Only compile ut, do not execute')
    variant('cov', default=False, description='Enable code coverage for unit tests')
    variant('disable_asan', default=False, description='Disable ASAN (Address Sanitizer)')
    variant('ophost_test', default=False, description='Build and run ophost unit tests')
    variant('opapi_test', default=False, description='Build and run opapi unit tests')
    variant('opgraph_test', default=False, description='Build and run opgraph unit tests')
    variant('opkernel_test', default=False, description='Build and run opkernel unit tests')


    variant('valgrind', default=False, description='Run unit tests with valgrind (disables ASAN and noexec)')

    variant('ophost', default=False, description='Build ophost library')
    variant('opapi', default=False, description='Build opapi library')
    variant('opgraph', default=False, description='Build opgraph library')

    variant('genop', default="none", description='Gen Op Directory Options')
    variant('genop_aicpu', default="none", description='Gen Op Directory Options')
    variant('torch_extension', default=False, description='Gen Op Directory Options')

    variant("run_example", default=False, description="Enable run example mode")
    variant("example_name", default="none", description="Example operator name for run_example")
    variant("example_mode", default="none", description="Example mode (eager/graph) for run_example")
    variant("pkg_mode", default="none", description="Package mode for run_example")
    variant("example_vendor", default="none", description="Vendor name for run_example")

    phases = ['install']

    def build_args(self, spec):
        """生成build.sh的参数列表"""
        args = []

        j_value = spec.variants["j"].value
        if j_value != "8":
            args.append(f"-j{j_value}")
        
        o_value = spec.variants["O"].value
        if o_value != "none":
            args.append(f"-{o_value}")
        
        if spec.variants["u"].value:
            args.append("-u")

        if spec.variants["debug"].value:
            args.append("--debug")
        
        # 测试相关选项
        if spec.variants["cov"].value:
            args.append("--cov")
        if spec.variants["noexec"].value:
            args.append("--noexec")
        if spec.variants["disable_asan"].value:
            args.append("--disable_asan")
        if spec.variants["valgrind"].value:
            args.append("--valgrind")

        # 组件构建选项
        if spec.variants["ophost"].value:
            args.append("--ophost")
        if spec.variants["opapi"].value:
            args.append("--opapi")
        if spec.variants["opgraph"].value:
            args.append("--opgraph")
        if spec.variants["opkernel"].value:
            args.append("--opkernel")
        
        # 打包选项
        if spec.variants["pkg"].value:
            args.append("--pkg")
        if spec.variants["jit"].value:
            args.append("--jit")
        
        # 测试组件选项
        if spec.variants["ophost_test"].value:
            args.append("--ophost_test")
        if spec.variants["opapi_test"].value:
            args.append("--opapi_test")
        if spec.variants["opgraph_test"].value:
            args.append("--opgraph_test")
        if spec.variants["opkernel_test"].value:
            args.append("--opkernel_test")
        
        # 自定义算子选项
        ops_value = spec.variants["ops"].value
        if ops_value != "none":
            args.append(f"--ops={ops_value}")
        
        soc_value = spec.variants["soc"].value
        if soc_value != "none":
            args.append(f"--soc={soc_value}")
        
        vendor_value = spec.variants["vendor_name"].value
        if vendor_value != "none":
            args.append(f"--vendor_name={vendor_value}")
        
        if spec.variants["experimental"].value:
            args.append("--experimental")
        
        
        # 处理 run_example 特殊选项
        if spec.variants["run_example"].value:
            example_name = spec.variants["example_name"].value
            example_mode = spec.variants["example_mode"].value
            
            if not example_name or not example_mode:
                raise InstallError("run_example requires both example_name and example_mode to be specified")
            
            args.append("--run_example")
            args.append(example_name)
            args.append(example_mode)
            
            # 处理可选的 pkg_mode 和 vendor
            pkg_mode = spec.variants["pkg_mode"].value
            if pkg_mode != "none":
                args.append(pkg_mode)
                
                vendor_value = spec.variants["example_vendor"].value
                if vendor_value != "none":
                    args.append(f"--vendor_name={vendor_value}")
        
        # 生成选项
        genop_value = spec.variants["genop"].value
        if genop_value != "none":
            args.append(f"--genop={genop_value}")
        
        genop_aicpu_value = spec.variants["genop_aicpu"].value
        if genop_aicpu_value != "none":
            args.append(f"--genop_aicpu={genop_aicpu_value}")

        if spec.variants["torch_extension"].value:
            args.append("--torch_extension")
        
        return args

    def build(self, spec, prefix):
        # 构建脚本路径
        build_script = join_path(self.stage.source_path, "build.sh")

        # 生成构建参数
        build_args = self.build_args(spec)
        
        # 使脚本可执行
        chmod = which("chmod")
        chmod("+x", build_script)

        # 运行构建
        bash = which("bash")
        bash(build_script, *build_args)

    def install_with_package(self, spec, prefix):
        if str(self.version) == "master":
            raise InstallError(f"This version can't be installed by runfile, please install from source code, \
                               for example: spack add cann-ops-math@{self.version};spack install")
        arch = platform.machine()
        soc_value = spec.variants["soc"].value
        if soc_value == "ascend910b":
            npu_model = "910b"
        elif soc_value == "ascend910_93":
            npu_model = "A3"
        else:
            raise InstallError(f"{soc_value} soc cannot be installed with run package")

        package_name = f"cann-{npu_model}-ops-math_{self.version}_linux-{arch}.run"
        package_url = f"https://ascend.devcloud.huaweicloud.com/cann/run/software/{self.version}/{arch}/ops/{package_name}"
        print(f"Download run package from {package_url}")
        run_package = join_path(self.stage.source_path, package_name)
        result = subprocess.run(
            ['curl', '-k', '-L', '-o', run_package, package_url],
            capture_output=True,
            text=True,
            check=True
        )
        st = os.stat(run_package)
        os.chmod(run_package, st.st_mode | stat.S_IEXEC)
        mkdirp(prefix.share)
        # spack的install方法会将下载run包copy到{spack.prefix}/share目录下，便于后面的统一打包
        install(run_package, prefix.share)
        
        # 获取 cann-toolkit 的安装目录
        cann_toolkit_dir = self.spec['cann-toolkit'].prefix
        # 执行安装,将ops-math安装到cann/opp目录下
        print(f"Install {run_package} to {cann_toolkit_dir}")
        self.install_package(run_package, cann_toolkit_dir)
    
    def install(self, spec, prefix):
        if spec.satisfies('+runfile'):
            self.install_with_package(spec, prefix)
            return

        self.build(spec, prefix)
        # 1. 定义源文件路径
        run_file = join_path(
            self.stage.source_path,
            "build_out"
        )

        # 2. 创建 share 目录并复制 .run 文件
        mkdirp(prefix.share)
        install_tree(run_file, prefix.share)

        # 3. 设置可执行权限（确保可运行）
        run_files = glob.glob(join_path(prefix.share, "*.run"))

        if not run_files:
            raise InstallError("No .run files found in share directory")

        # 获取 cann-toolkit 的安装目录，将ops-math安装到cann/opp目录下
        cann_toolkit_dir = self.spec['cann-toolkit'].prefix

        for run_file in run_files:
            chmod = which("chmod")
            chmod("+x", run_file)
            # 4. 使用已复制的 .run 文件执行安装（推荐）
            self.install_package(run_file, cann_toolkit_dir)


    def install_package(self, installer, dir_name):
        st = os.stat(installer)
        os.chmod(installer, st.st_mode | stat.S_IEXEC)
        bash = which("bash")
        bash(installer, f"--install-path={dir_name}", "--full", "--quiet")
