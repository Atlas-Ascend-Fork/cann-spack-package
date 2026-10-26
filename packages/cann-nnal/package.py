# ----------------------------------------------------------------------------
# Copyright (c) 2026 Huawei Technologies Co., Ltd.
# This program is free software, you can redistribute it and/or modify it under the terms and conditions of
# CANN Open Software License Agreement Version 2.0 (the "License").
# Please refer to the License for details. You may not use this file except in compliance with the License.
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY, OR FITNESS FOR A PARTICULAR PURPOSE.
# See LICENSE in the root of the software repository for the full text of the License.
# ----------------------------------------------------------------------------

import os
import stat

from spack.package import *


class CannNnal(Package):
    "CANN (Compute Architecture for Neural Networks) NNAL Acceleration Library for Ascend AI processors"

    homepage = "https://gitcode.com/cann"

    _versions = {
        "8.5.0-beta.1": {
            "x86_64": (
                "https://ascend.devcloud.huaweicloud.com/artifactory/"
                "cann-run/software/8.5.0-beta.1/x86_64/"
                "Ascend-cann-nnal_8.5.0-beta.1_linux-x86_64.run",
                "b05bb9e39ce88d78fd1673d15970136012fdaa81e6fba3e1681d643b33adbe9b",
            ),
            "aarch64": (
                "https://ascend.devcloud.huaweicloud.com/artifactory/"
                "cann-run/software/8.5.0-beta.1/aarch64/"
                "Ascend-cann-nnal_8.5.0-beta.1_linux-aarch64.run",
                "75663f6e398d3fc7621f7b95775fa8770b32b638e32f4c29a0242e03764c942b",
            ),
        },
        "8.5.0": {
            "x86_64": (
                "https://ascend-repo.obs.cn-east-2.myhuaweicloud.com/"
                "CANN/CANN%208.5.0/"
                "Ascend-cann-nnal_8.5.0_linux-x86_64.run",
                "3ee0e170f00dcdcf72f9eeda75996a2e812878ac72cc6249371140af256b5d4f",
            ),
            "aarch64": (
                "https://ascend-repo.obs.cn-east-2.myhuaweicloud.com/"
                "CANN/CANN%208.5.0/"
                "Ascend-cann-nnal_8.5.0_linux-aarch64.run",
                "138e473bc17e6cdfa0a34121ad3b96f0abe230e1b7787dd0957459a368cb8d77",
            ),
        },
        "9.0.0": {
            "x86_64": (
                "https://ascend-repo.obs.cn-east-2.myhuaweicloud.com/"
                "CANN/CANN%209.0.0/"
                "Ascend-cann-nnal_9.0.0_linux-x86_64.run",
                "d02ff36b63a7809abde3aae0dbeb24c7f07105150ace15801e2df155d8a04499",
            ),
            "aarch64": (
                "https://ascend-repo.obs.cn-east-2.myhuaweicloud.com/"
                "CANN/CANN%209.0.0/"
                "Ascend-cann-nnal_9.0.0_linux-aarch64.run",
                "75b3c695bee3a193f0391c39ba64bacb41b9bc03e5f6725624ba02e245b4f668",
            ),
        },
        "9.0.0-beta.1": {
            "x86_64": (
                "https://ascend-repo.obs.cn-east-2.myhuaweicloud.com/"
                "CANN/CANN%209.0.T2/"
                "Ascend-cann-nnal_9.0.0-beta.1_linux-x86_64.run",
                "5417c255a93a7a336cba780026d570858301738a00c8c416da147b3f0a42564e",
            ),
            "aarch64": (
                "https://ascend-repo.obs.cn-east-2.myhuaweicloud.com/"
                "CANN/CANN%209.0.T2/"
                "Ascend-cann-nnal_9.0.0-beta.1_linux-aarch64.run",
                "877e8be1cb60925a8b83b3aedf52e31c0b37cb7a53d61dd0b5107fbd164e99e1",
            ),
        },
        "9.0.0-beta.2": {
            "x86_64": (
                "https://ascend-repo.obs.cn-east-2.myhuaweicloud.com/"
                "CANN/CANN%209.0.T511/"
                "Ascend-cann-nnal_9.0.0-beta.2_linux-x86_64.run",
                "284be866b2bb0ad5c7bb72c615a98c3baa72198f22f7b4ea13e2e52d9887d7ae",
            ),
            "aarch64": (
                "https://ascend-repo.obs.cn-east-2.myhuaweicloud.com/"
                "CANN/CANN%209.0.T511/"
                "Ascend-cann-nnal_9.0.0-beta.2_linux-aarch64.run",
                "426aba2949defd0080550724d892cf0a5157bf6b280fc3b38c7e177703bfa07f",
            ),
        },
        "9.1.0-beta.1": {
            "x86_64": (
                "https://ascend-repo.obs.cn-east-2.myhuaweicloud.com/"
                "CANN/CANN%209.1.T1/"
                "Ascend-cann-nnal_9.1.0-beta.1_linux-x86_64.run",
                "c70fbc56ac926e9e06c8ac4d495a1d7c5c6e631bd2033ed1c97ea36ccb10d10d",
            ),
            "aarch64": (
                "https://ascend-repo.obs.cn-east-2.myhuaweicloud.com/"
                "CANN/CANN%209.1.T1/"
                "Ascend-cann-nnal_9.1.0-beta.1_linux-aarch64.run",
                "82d70ac0fd07a915b1a04216c9dfa58921732939a15c16a532a2c14eaacc20cc",
            ),
        },
        "9.1.0-beta.3": {
            "x86_64": (
                "https://ascend-repo.obs.cn-east-2.myhuaweicloud.com/"
                "CANN/CANN%209.1.T6/"
                "Ascend-cann-nnal_9.1.0-beta.3_linux-x86_64.run",
                "4b10c7eb673224304add11bfb8d160cb070889ad20973e78709a3f6b89a75048",
            ),
            "aarch64": (
                "https://ascend-repo.obs.cn-east-2.myhuaweicloud.com/"
                "CANN/CANN%209.1.T6/"
                "Ascend-cann-nnal_9.1.0-beta.3_linux-aarch64.run",
                "39c0ef444f606aded6d7764e6d55d281da9973b107e281e525771f3ee5c5fb3e",
            ),
        },
        "9.1.0": {
            "x86_64": (
                "https://ascend-repo.obs.cn-east-2.myhuaweicloud.com/"
                "CANN/CANN%209.1.0/"
                "Ascend-cann-nnal_9.1.0_linux-x86_64.run",
                "1a743a0957a77a0624c2ecfdf689b5c5937a9097fda1e3b3e8e0191a7d11c694",
            ),
            "aarch64": (
                "https://ascend-repo.obs.cn-east-2.myhuaweicloud.com/"
                "CANN/CANN%209.1.0/"
                "Ascend-cann-nnal_9.1.0_linux-aarch64.run",
                "62a79f474280eecdc5a584d78036a2074ad740369150e9403f260655307d86e1",
            ),
        },
        "9.2.0": {
            "x86_64": (
                "https://ascend-repo.obs.cn-east-2.myhuaweicloud.com/"
                "CANN/CANN%209.2.0/"
                "Ascend-cann-nnal_9.2.0_linux-x86_64.run",
                "bcf7ff0d0a97b4c679e1823918e8d868e97304b0c131601a93b5d3b181010ea7",
            ),
            "aarch64": (
                "https://ascend-repo.obs.cn-east-2.myhuaweicloud.com/"
                "CANN/CANN%209.2.0/"
                "Ascend-cann-nnal_9.2.0_linux-aarch64.run",
                "2629f46054ad63c75d38d2273f9dbc64d65fc323201eb506f0becdfd67f13f57",
            ),
        },
    }

    import platform
    arch = platform.machine()
    for ver, packages in _versions.items():
        pkg = packages.get(arch)
        if pkg:
            kwargs = {"url": pkg[0], "expand": False}
            if pkg[1]:
                kwargs["sha256"] = pkg[1]
            version(ver, **kwargs)

    for v in _versions:
        depends_on(f"cann-toolkit@{v}", type=["build", "run"], when=f"@{v}")

    phases = ["install"]

    def install(self, spec, prefix):
        run_file = self.stage.archive_file

        chmod = which("chmod")
        chmod("+x", run_file)

        self.install_package(run_file, prefix)

    def install_package(self, installer, dir_name):
        st = os.stat(installer)
        os.chmod(installer, st.st_mode | stat.S_IEXEC)
        bash = which("bash")
        bash(installer, f"--install-path={dir_name}", "--install", "--quiet")

    def setup_run_environment(self, env):
        nnal_path = os.path.join(self.prefix, 'nnal')

        atb_home = os.path.join(nnal_path, "atb/latest/atb/cxx_abi_1")

        env.set("NNAL_HOME_PATH", str(nnal_path))
        env.set("ATB_HOME_PATH", atb_home)

        env.prepend_path("LD_LIBRARY_PATH",
                         os.path.join(atb_home, "lib"))

        env.set("ATB_STREAM_SYNC_EVERY_KERNEL_ENABLE", "0")
        env.set("ATB_STREAM_SYNC_EVERY_RUNNER_ENABLE", "0")
        env.set("ATB_STREAM_SYNC_EVERY_OPERATION_ENABLE", "0")
        env.set("ATB_OPSRUNNER_KERNEL_CACHE_LOCAL_COUNT", "1")
        env.set("ATB_OPSRUNNER_KERNEL_CACHE_GLOABL_COUNT", "5")
        env.set("ATB_WORKSPACE_MEM_ALLOC_ALG_TYPE", "1")
        env.set("ATB_COMPARE_TILING_EVERY_KERNEL", "0")
        env.set("ATB_SHARE_MEMORY_NAME_SUFFIX", "")
        env.set("ATB_MATMUL_SHUFFLE_K_ENABLE", "1")
        env.set("LCCL_DETERMINISTIC", "0")
        env.set("LCCL_PARALLEL", "0")

    def setup_dependent_build_environment(self, env, dependent_spec):
        self.setup_run_environment(env)

    def setup_dependent_run_environment(self, env, dependent_spec):
        self.setup_run_environment(env)
