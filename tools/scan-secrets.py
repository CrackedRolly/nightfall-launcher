#!/usr/bin/env python3
"""Scan all Git history using an immutable, checksum-verified Gitleaks binary.

No license, repository write permission or artifact uploads are required.
"""
import hashlib,io,pathlib,subprocess,tarfile,tempfile,urllib.request
VERSION='8.24.2'
SHA256='fa0500f6b7e41d28791ebc680f5dd9899cd42b58629218a5f041efa899151a8e'
URL=f'https://github.com/gitleaks/gitleaks/releases/download/v{VERSION}/gitleaks_{VERSION}_linux_x64.tar.gz'
with urllib.request.urlopen(URL,timeout=60) as response:data=response.read()
assert hashlib.sha256(data).hexdigest()==SHA256,'Gitleaks download checksum mismatch'
with tempfile.TemporaryDirectory(prefix='nightfall-secrets-') as folder:
    binary=pathlib.Path(folder)/'gitleaks'
    with tarfile.open(fileobj=io.BytesIO(data)) as archive:
        member=archive.getmember('gitleaks')
        assert member.isfile(),'Unexpected scanner archive'
        binary.write_bytes(archive.extractfile(member).read())
    binary.chmod(0o700)
    subprocess.run([str(binary),'git','--redact=100','--no-banner','--log-opts=--all'],check=True)
