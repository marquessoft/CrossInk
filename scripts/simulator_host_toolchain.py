"""
PlatformIO pre-build script: host toolchain settings for native simulator
environments.

C dialect:
  GCC 15+ defaults to -std=gnu23, where `bool`, `true`, and `false` are
  keywords. Third-party C sources in lib_deps (e.g. ricmoo/QRCode) still
  typedef their own bool for pre-C23 compilers, which C23 rejects. The
  ESP32 toolchains default to gnu17, so pinning the host C dialect to the
  same keeps lib C sources building everywhere. CFLAGS applies only to C
  compilation; C++ translation units use CCFLAGS and are unaffected.

Linux OpenSSL:
  The simulator's MD5Builder_linux.h hashes via OpenSSL's MD5_* API, so
  Linux links need libssl/libcrypto (macOS uses CommonCrypto instead and
  must not gain these flags).
"""

import sys

Import("env")  # noqa: F821 -- supplied by PlatformIO at script load

env.Append(CFLAGS=["-std=gnu17"])

if sys.platform.startswith("linux"):
    env.Append(LIBS=["ssl", "crypto"])
