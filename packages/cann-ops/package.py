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
import subprocess
import stat

class CannOps(Package):
    """CANN (Compute Architecture for Neural Networks) Operations Suite for Ascend AI processors"""

    homepage = "https://gitcode.com/cann"
    has_code = False

    version("8.5.0")
    version("8.5.0-beta.1")
    version("9.0.0-beta.1")

    variant('soc', default='ascend910b', description='Target Platform')

    for v in ["8.5.0", "8.5.0-beta.1", "9.0.0-beta.1"]:
        depends_on(f"cann-toolkit@{v}", when=f"@{v}")

    phases = ['install']

    def install(self, spec, prefix):
        import platform
        arch = platform.machine()
        soc_value = spec.variants["soc"].value
        version = str(self.version)

        match soc_value:
            case "ascend910b":
                soc = "910b"
            case "ascend910_93":
                if version == "8.5.0":
                    soc = "910_93"
                else:
                    soc = "A3"
            case _:
                raise InstallError(f"暂不支持该硬件型号: {soc_value}")

        url = f"https://ascend.devcloud.huaweicloud.com/artifactory/cann-run/software/{version}/{arch}/Ascend-cann-{soc}-ops_{version}_linux-{arch}.run"
        package_name = f"Ascend-cann-{soc}-ops_{version}_linux-{arch}.run"
        run_package = join_path(self.stage.source_path, package_name)
        result = subprocess.run(
            ['curl', '-k', '-L', '-o', run_package, url],
            capture_output=True,
            text=True,
            check=True
        )
        st = os.stat(run_package)
        os.chmod(run_package, st.st_mode | stat.S_IEXEC)
        mkdirp(prefix.share)
        install(run_package, prefix.share)
        cann_toolkit_dir = self.spec['cann-toolkit'].prefix
        self.install_package(run_package, cann_toolkit_dir)

    def install_package(self, installer, dir_name):
        st = os.stat(installer)
        os.chmod(installer, st.st_mode | stat.S_IEXEC)
        bash = which("bash")
        bash(installer, f"--install-path={dir_name}", "--install", "--quiet")