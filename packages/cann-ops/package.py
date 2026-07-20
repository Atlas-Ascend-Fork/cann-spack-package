# ----------------------------------------------------------------------------
# Copyright (c) 2025 Huawei Technologies Co., Ltd.
# This program is free software, you can redistribute it and/or modify it under the terms and conditions of
# CANN Open Software License Agreement Version 2.0 (the "License").
# Please refer to the License for details. You may not use this file except in compliance with the License.
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY, OR FITNESS FOR A PARTICULAR PURPOSE.
# See LICENSE in the root of the software repository for the full text of the License.
# ----------------------------------------------------------------------------

import os
import subprocess
import stat
import platform
from spack.package import *

_OBS_URL = (
    "https://ascend-repo.obs.cn-east-2.myhuaweicloud.com/"
    "CANN/CANN%20{obs_code}/Ascend-cann-{soc}-ops_{version}_linux-{arch}.run"
)
_ARTIFACTORY_URL = (
    "https://ascend.devcloud.huaweicloud.com/artifactory/"
    "cann-run/software/{version}/{arch}/Ascend-cann-{soc}-ops_{version}_linux-{arch}.run"
)


class CannOps(Package):
    """CANN (Compute Architecture for Neural Networks) Operations Suite for Ascend AI processors"""

    homepage = "https://gitcode.com/cann"
    has_code = False

    variant('soc', default='910b', description='Target Platform (910b/A3/950/910/310p/310b)')

    _versions = {
        "8.5.0": {
            "url_template": _OBS_URL,
            "obs_code": "8.5.0",
        },
        "8.5.0-beta.1": {
            "url_template": _ARTIFACTORY_URL,
        },
        "9.0.0": {
            "url_template": _OBS_URL,
            "obs_code": "9.0.0",
        },
        "9.0.0-beta.1": {
            "url_template": _OBS_URL,
            "obs_code": "9.0.T2",
        },
        "9.0.0-beta.2": {
            "url_template": _OBS_URL,
            "obs_code": "9.0.T511",
        },
        "9.1.0-beta.1": {
            "url_template": _OBS_URL,
            "obs_code": "9.1.T1",
        },
        "9.1.0-beta.3": {
            "url_template": _OBS_URL,
            "obs_code": "9.1.T6",
        },
    }

    for ver in _versions:
        version(ver)
        depends_on(f"cann-toolkit@{ver}", when=f"@{ver}")

    phases = ['install']

    def install(self, spec, prefix):
        arch = platform.machine()
        soc = spec.variants["soc"].value
        version = str(self.version)
        ver_info = self._versions[version]

        url = ver_info["url_template"].format(
            version=version,
            arch=arch,
            soc=soc,
            obs_code=ver_info.get("obs_code", ""),
        )
        package_name = f"Ascend-cann-{soc}-ops_{version}_linux-{arch}.run"
        run_package = join_path(self.stage.source_path, package_name)
        subprocess.run(
            ['curl', '-k', '-L', '-o', run_package, url],
            capture_output=True,
            text=True,
            check=True
        )
        st = os.stat(run_package)
        os.chmod(run_package, st.st_mode | stat.S_IEXEC)
        mkdirp(prefix.share)
        with open(join_path(prefix.share, "install.log"), "w") as f:
            f.write(f"package: {package_name}\n")
            f.write(f"version: {version}\n")
            f.write(f"soc: {soc}\n")
            f.write(f"source: {url}\n")
        cann_toolkit_dir = self.spec['cann-toolkit'].prefix
        self.install_package(run_package, cann_toolkit_dir)

    def install_package(self, installer, dir_name):
        st = os.stat(installer)
        os.chmod(installer, st.st_mode | stat.S_IEXEC)
        bash = which("bash")
        bash(installer, f"--install-path={dir_name}", "--install", "--quiet")
