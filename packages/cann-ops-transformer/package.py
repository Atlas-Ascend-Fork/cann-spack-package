# ----------------------------------------------------------------------------
# Copyright (c) 2025 Huawei Technologies Co., Ltd.
# This program is free software, you can redistribute it and/or modify it under the terms and conditions of
# CANN Open Software License Agreement Version 2.0 (the "License").
# Please refer to the License for details. You may not use this file except in compliance with the License.
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY, OR FITNESS FOR A PARTICULAR PURPOSE.
# See LICENSE in the root of the software repository for the full text of the License.
# ----------------------------------------------------------------------------

from spack_repo.builtin.build_systems.generic import Package
from spack.package import *
import os
import stat
import glob
import subprocess
import platform

class CannOpsTransformer(Package):
    homepage = "https://gitcode.com"
    git = "https://gitcode.com/cann/ops-transformer.git"

    version("master", branch="master")
    version("8.5.0-beta.1", commit="05c401f9ddebdc9ebf008bb974f9ec1256e9e6f9")
    version("8.5.0", commit="d73f30f8d0e6ff899f2afe78b87a0510d40f7696")
    version("9.0.0-beta.1", commit="2e87a82ecf760e0a6d7d7e0981686768866ca799")
    version("9.0.0-beta.2", branch="9.0.0-beta.2")

    variant('runfile', default=False,
            description='install from run file rather than build form source')
    variant('pkg', default=False,
            description='Build package')

    variant('soc', default='none',
            description='Product name')

    variant('build_type', default='none',
            description='CMake build type')

    variant('optimization', default='none',
            description='Compilation optimization level')

    variant('experimental', default=False,
            description='Build experimental version')

    variant('asan', default=False,
            description='Enable Address Sanitizer')

    variant('coverage', default=False,
            description='Enable code coverage for unit tests')

    variant('custom_ops', default=False,
            description='Build custom operators')

    variant('jit', default=False,
            description='Build run package without kernel bin')

    variant('static', default=False,
            description='Build static library')

    variant('vendor_name', default='none',
            description='Vendor name for custom operators')

    variant('ops_list', default=' ',
            description='List of operators to compile (comma-separated)')

    variant('jobs', default='8',
            description='Number of parallel jobs for compilation')

    with when('~runfile'):
        depends_on('python@3.7.0:', type='build')
        depends_on('gcc@7.3.0:', type='build')
        depends_on('cmake@3.16.0:', type='build')
        depends_on('pigz@2.4:', type='build')
        depends_on('dos2unix', type='build')
        depends_on('gawk', type='build')
        depends_on('py-pyyaml', type='build')
        depends_on('py-numpy', type='build')
        depends_on('py-decorator', type='build')
        depends_on('py-sympy', type='build')
        depends_on('py-scipy', type='build')
        depends_on('py-attrs', type='build')
        depends_on('py-protobuf', type='build')
        depends_on('py-psutil', type='build')
    for v in ["8.5.0-beta.1", "8.5.0", "9.0.0-beta.1", "9.0.0-beta.2"]:
        depends_on(f"cann-toolkit@{v}", type=['build','run'], when=f"@{v}")
    depends_on(f"cann-toolkit@9.0.0-beta.2", type=['build', 'run'], when="@master")
    
    phases = ['install']

    def build_args(self, spec):
        """生成build.sh的参数列表"""
        args = []

        # 打包选项
        if spec.variants['pkg'].value:
            args.append('--pkg')

        if spec.variants['soc'].value != 'none':
            soc = spec.variants['soc'].value
            args.append(f'--soc={soc}')

        if spec.variants['experimental'].value:
            args.append('--experimental')

        if spec.variants['build_type'].value != 'none':
            build_type = spec.variants['build_type'].value
            args.append(f'--build-type={build_type}')

        if spec.variants['optimization'].value != 'none':
            optimization = spec.variants['optimization'].value
            args.append(f'-{optimization}')

        jobs = spec.variants['jobs'].value
        args.append(f'-j{jobs}')

        if not spec.variants['asan'].value:
            args.append('--disable_asan')

        if spec.variants['coverage'].value:
            args.append('--cov')

        if spec.variants['custom_ops'].value:
            args.append('--ops=' + spec.variants['ops_list'].value)
            args.append('--vendor_name=' + spec.variants['vendor_name'].value)

        if spec.variants['jit'].value:
            args.append('--jit')

        if spec.variants['static'].value:
            args.append('--static')

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
            raise InstallError(f"This version can't be installed by runfile, please install from source code, for example: spack add cann-ops-transformer@{self.version};spack install")
        arch = platform.machine()
        soc_value = spec.variants["soc"].value
        if soc_value == "ascend910b":
            npu_model = "910b"
        elif soc_value == "ascend910_93":
            npu_model = "A3"
        else:
            raise InstallError(f"{soc_value} soc cannot be installed with run package")

        package_name = f"cann-{npu_model}-ops-transformer_{self.version}_linux-{arch}.run"
        package_url= f"https://ascend.devcloud.huaweicloud.com/cann/run/software/{self.version}/{arch}/ops/{package_name}"
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
        # 执行安装,将ops-transformer安装到cann/opp目录下
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

        # 获取 cann-toolkit 的安装目录，将ops-transformer安装到cann/opp目录下
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

