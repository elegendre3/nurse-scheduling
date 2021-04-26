#   -*- coding: utf-8 -*-
from pybuilder.core import use_plugin, init

use_plugin("python.core")
use_plugin("python.unittest")
use_plugin("python.flake8")
use_plugin("python.coverage")
use_plugin("python.distutils")
use_plugin("python.install_dependencies")


name = "nurse-scheduling"
default_task = "publish"
version = '0.0.dev1'


@init
def set_properties(project):
    project.depends_on('pulp')
