from quark.plugin_manager import factory

from quark_plugin_ghz.ghz import GHZ, QasmGHZCircuit

def register() -> None:
    """
    Register all modules exposed to quark by this plugin.
    For each module, add a line of the form:
        factory.register("module_name", Module)

    The "module_name" will later be used to refer to the module in the configuration file.
    """
    factory.register("GHZ", GHZ)
    factory.register("QasmGHZCircuit", QasmGHZCircuit)
