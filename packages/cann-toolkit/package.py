# ----------------------------------------------------------------------------
# Copyright (c) 2026 Huawei Technologies Co., Ltd.
# This program is free software, you can redistribute it and/or modify it under the terms and conditions of
# CANN Open Software License Agreement Version 2.0 (the "License").
# Please refer to the License for details. You may not use this file except in compliance with the License.
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY, OR FITNESS FOR A PARTICULAR PURPOSE.
# See LICENSE in the root of the software repository for the full text of the License.
# ----------------------------------------------------------------------------

from spack_repo.builtin.build_systems.generic import Package
from spack.fetch_strategy import URLFetchStrategy
from spack.package import *
import os
import stat


class CannToolkit(Package):
    "CANN (Compute Architecture for Neural Networks) Toolkit for Ascend AI processors"
    
    homepage = "https://gitcode.com/cann"

    # 架构信息映射
    _versions = {
        "8.5.0-beta.1": {
            "x86_64": (
                "https://ascend.devcloud.huaweicloud.com/artifactory/"
                "cann-run/software/8.5.0-beta.1/x86_64/"
                "Ascend-cann-toolkit_8.5.0-beta.1_linux-x86_64.run",
                "a26f9e4639227e0e1d0ac6cf8d499e042fb6cfbe5cbf6bed95018bba7c049ead",
            ),
            "aarch64": (
                "https://ascend.devcloud.huaweicloud.com/artifactory/"
                "cann-run/software/8.5.0-beta.1/aarch64/"
                "Ascend-cann-toolkit_8.5.0-beta.1_linux-aarch64.run",
                "ee315d590beefa11f1f311e53e963b5fc71b4803c9ed3091c4f48d61ed3cbd3f",
            ),
        },
        "8.5.0": {
            "x86_64": (
                "https://ascend.devcloud.huaweicloud.com/artifactory/"
                "cann-run/software/8.5.0/x86_64/"
                "Ascend-cann-toolkit_8.5.0_linux-x86_64.run",
                "df23796269a136591f9f5cbde8b06b031fc67bb8dc9b3b5b1c97858a57a503b6",
            ),
            "aarch64": (
                "https://ascend.devcloud.huaweicloud.com/artifactory/"
                "cann-run/software/8.5.0/aarch64/"
                "Ascend-cann-toolkit_8.5.0_linux-aarch64.run",
                "7beec8c02700cba1eaca9e2e8decb0acf5b01337db7714a8c6b7536316e070e7",
            ),
        },
        "9.0.0-beta.1": {
            "x86_64": (
                "https://ascend.devcloud.huaweicloud.com/artifactory/"
                "cann-run/software/9.0.0-beta.1/x86_64/"
                "Ascend-cann-toolkit_9.0.0-beta.1_linux-x86_64.run",
                "6d4b92770761f3562758cd286d07d27f3323cd33aa44eb209c816790199cff4b",
            ),
            "aarch64": (
                "https://ascend.devcloud.huaweicloud.com/artifactory/"
                "cann-run/software/9.0.0-beta.1/aarch64/"
                "Ascend-cann-toolkit_9.0.0-beta.1_linux-aarch64.run",
                "50d5f124ebb357548a14d52591a2e23049ecb212f2a870db49f3d3da1a1b444b",
            ),
        },
        "9.0.0-beta.2": {
            "x86_64": (
                "https://ascend.devcloud.huaweicloud.com/artifactory/"
                "cann-run/software/9.0.0-beta.2/x86_64/"
                "Ascend-cann-toolkit_9.0.0-beta.2_linux-x86_64.run",
                "47d333ff57c2aeb1a7bde8c71c01a1533fa15a4a80c14d4622b0281428ef9363",
            ),
            "aarch64": (
                "https://ascend.devcloud.huaweicloud.com/artifactory/"
                "cann-run/software/9.0.0-beta.2/aarch64/"
                "Ascend-cann-toolkit_9.0.0-beta.2_linux-aarch64.run",
                "df2ecc234b4aab542d45e23457e4981a81d09ed7007164393b6f31a3919606b1",
            ),
        },
    }

    import platform
    arch = platform.machine()
    for ver, packages in _versions.items():
        pkg = packages.get(arch)
        if pkg:
            version(ver, url=pkg[0], sha256=pkg[1], expand=False)
    
    phases = ["install"]

    def install(self, spec, prefix):
        run_file = self.stage.archive_file
        
        chmod = which("chmod")
        chmod("+x", run_file)

        self.install_package(run_file, prefix)

    # cann-toolkit安装命令，如果安装用户和驱动安装用户不一致，请确保已将用户加入驱动安装用户组，例如usermod -aG 组名 用户名
    def install_package(self, installer, dir_name):
        st = os.stat(installer)
        os.chmod(installer, st.st_mode | stat.S_IEXEC)
        bash = which("bash")
        bash(installer, f"--install-path={dir_name}", "--full", "--force", "--quiet")

    def setup_run_environment(self, env):
        """设置运行时环境变量"""
        ascend_home_path = os.path.join(self.prefix, 'cann')
        
        # 设置基础环境变量
        env.set('ASCEND_HOME_PATH', ascend_home_path)
        env.set('ASCEND_TOOLKIT_HOME', ascend_home_path)
        env.set('TOOLCHAIN_HOME', os.path.join(ascend_home_path, 'toolkit'))
        env.set('ASCEND_AICPU_PATH', ascend_home_path)
        env.set('ASCEND_OPP_PATH', os.path.join(ascend_home_path, 'opp'))

        # 设置PATH
        paths = [
            os.path.join(ascend_home_path, 'bin'),
            os.path.join(ascend_home_path, 'tools/ccec_compiler/bin'),
            os.path.join(ascend_home_path, 'tools/profiler/bin'),
            os.path.join(ascend_home_path, 'tools/ascend_system_advisor/asys'),
            os.path.join(ascend_home_path, 'tools/show_kernel_debug_data'),
            os.path.join(ascend_home_path, 'tools/msobjdump'),
        ]
        for path in paths:
            env.prepend_path('PATH', path)

        # 设置LD_LIBRARY_PATH
        arch = os.uname().machine
        lib_paths = [
            os.path.join(ascend_home_path, 'lib64'),
            os.path.join(ascend_home_path, 'lib64/plugin/opskernel'),
            os.path.join(ascend_home_path, 'lib64/plugin/nnengine'),
            os.path.join(ascend_home_path, f'opp/built-in/op_impl/ai_core/tbe/op_host/lib/linux/{arch}'),
            os.path.join(ascend_home_path, 'tools/aml/lib64'),
            os.path.join(ascend_home_path, 'tools/aml/lib64/plugin'),
        ]
        for lib_path in lib_paths:
            env.prepend_path('LD_LIBRARY_PATH', lib_path)
        
        # 设置本地驱动库路径
        driver_lib_paths = [
            '/usr/local/Ascend/driver/lib64',
            '/usr/local/Ascend/driver/lib64/common', 
            '/usr/local/Ascend/driver/lib64/driver'
        ]
        for lib_path in driver_lib_paths:
            env.prepend_path('LD_LIBRARY_PATH', lib_path)

        # 设置PYTHONPATH
        python_paths = [
            os.path.join(ascend_home_path, 'python/site-packages'),
            os.path.join(ascend_home_path, 'opp/built-in/op_impl/ai_core/tbe'),
        ]
        for python_path in python_paths:
            env.prepend_path('PYTHONPATH', python_path)
            
        # 设置CMAKE_PREFIX_PATH 
        env.prepend_path('CMAKE_PREFIX_PATH', os.path.join(ascend_home_path, 'lib64/cmake'))
        env.prepend_path('CMAKE_PREFIX_PATH', os.path.join(ascend_home_path, 'toolkit/tools/tikicpulib/lib/cmake'))

    def setup_dependent_build_environment(self, env, dependent_spec):
        """为依赖此包的软件设置构建环境"""
        self.setup_run_environment(env)

    def setup_dependent_run_environment(self, env, dependent_spec):
        """为依赖此包的软件设置运行环境"""
        self.setup_run_environment(env)