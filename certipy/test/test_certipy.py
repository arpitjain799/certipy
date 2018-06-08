import os
import pytest
import shutil
from pathlib import Path
from tempfile import NamedTemporaryFile, TemporaryDirectory

from ..certipy import Certipy

def test_key_cert_pair_for_name():
    with TemporaryDirectory() as td:
        c = Certipy(store_dir=td)
        name = "foo"
        test_path = "{}/{}".format(td, name)
        cert_info = c.key_cert_pair_for_name(name)

        assert cert_info.dir_name == test_path

def test_store_add():
    with TemporaryDirectory() as td:
        c = Certipy(store_dir=td)
        name = "foo"
        cert_info = c.key_cert_pair_for_name(name)
        c.store_add(cert_info)

        assert name in c.certs

def test_store_get():
    with TemporaryDirectory() as td:
        c = Certipy(store_dir=td)
        name = "foo"
        cert_info = c.key_cert_pair_for_name(name)
        c.store_add(cert_info)

        loadedInfo = c.store_get(name)

        assert loadedInfo.key_file == "{}/{}.key".format(cert_info.dir_name, name)
        assert loadedInfo.cert_file == "{}/{}.crt".format(cert_info.dir_name, name)

def test_store_remove():
    with TemporaryDirectory() as td:
        c = Certipy(store_dir=td)
        name = "foo"
        cert_info = c.key_cert_pair_for_name(name)
        c.store_add(cert_info)
        cert_info = c.store_get(name)

        assert cert_info is not None

        c.store_remove(name)
        cert_info = c.store_get(name)

        assert cert_info is None

def test_store_save():
    with TemporaryDirectory() as td:
        c = Certipy(store_dir=td)
        name = "foo"
        cert_info = c.key_cert_pair_for_name(name)
        c.store_add(cert_info)
        c.store_save()

        assert os.stat("{}/store.json".format(td))

def test_store_load():
    with TemporaryDirectory() as td:
        c = Certipy(store_dir=td)
        name = "foo"
        cert_info = c.key_cert_pair_for_name(name)
        c.store_add(cert_info)
        c.store_save()
        c.store_load()

        loadedInfo = c.store_get(name)

        assert loadedInfo.key_file == "{}/{}.key".format(cert_info.dir_name, name)
        assert loadedInfo.cert_file == "{}/{}.crt".format(cert_info.dir_name, name)

def test_create_ca():
    with TemporaryDirectory() as td:
        c = Certipy(store_dir=td)
        name = "foo"
        cert_info = c.create_ca(name)

        assert os.stat(cert_info.key_file)
        assert os.stat(cert_info.cert_file)

def test_create_key_pair():
    with TemporaryDirectory() as td:
        c = Certipy(store_dir=td)
        name = "foo"
        ca_name = "bar"
        c.create_ca(ca_name)
        cert_info = c.create_signed_pair(name, ca_name)

        assert os.stat(cert_info.key_file)
        assert os.stat(cert_info.cert_file)
