# Copyright (c) 2025 Science + Computing AG / Eviden SE (Atos Group)
#
# This file is part of the QUARK benchmarking framework.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#
# Contact: stefan-raimund.maschek@eviden.com


from quark.plugin_manager import factory

from quark_plugin_ghz.ghz import GHZ, GHZtoQasmCircuit

def register() -> None:
    """
    Register all modules exposed to quark by this plugin.
    For each module, add a line of the form:
        factory.register("module_name", Module)

    The "module_name" will later be used to refer to the module in the configuration file.
    """
    factory.register("GHZ", GHZ)
    factory.register("GHZtoQasmCircuit", GHZtoQasmCircuit)
