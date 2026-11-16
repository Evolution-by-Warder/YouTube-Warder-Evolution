"""Opt-in Enigma2 main-menu registration without a real receiver runtime."""
import importlib.util
import sys
import types
import unittest
from pathlib import Path
from unittest.mock import patch

SRC = Path(__file__).resolve().parents[1] / "plugin/Plugins/Extensions/WarderYouTube"

class Descriptor:
    WHERE_PLUGINMENU = 3
    WHERE_MENU = 5
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class MainMenuRegistrationTests(unittest.TestCase):
    def test_visibility_is_strictly_opt_in_and_stable_plugin_menu_is_preserved(self):
        package = types.ModuleType("_warder_mainmenu_test")
        package.__path__ = [str(SRC)]
        plugin_descriptor = types.ModuleType("Plugins.Plugin")
        plugin_descriptor.PluginDescriptor = Descriptor
        plugins = types.ModuleType("Plugins")
        plugins.__path__ = []
        enigma = types.ModuleType("enigma")
        enigma.getDesktop = lambda number: None
        ui = types.ModuleType("_warder_mainmenu_test.ui")
        ui.WarderYouTubeHome = object
        locale = types.ModuleType("_warder_mainmenu_test.i18n")
        locale.tr = lambda msg: msg
        config = types.SimpleNamespace(plugins=types.SimpleNamespace(
            warderyoutube=types.SimpleNamespace(
                show_main_menu=types.SimpleNamespace(value=False))))
        component_config = types.ModuleType("Components.config")
        component_config.config = config
        components = types.ModuleType("Components")
        components.__path__ = []
        mocks = {
            "_warder_mainmenu_test": package,
            "_warder_mainmenu_test.ui": ui,
            "_warder_mainmenu_test.i18n": locale,
            "Plugins": plugins, "Plugins.Plugin": plugin_descriptor,
            "enigma": enigma, "Components": components,
            "Components.config": component_config
        }
        spec = importlib.util.spec_from_file_location(
            "_warder_mainmenu_test.plugin", SRC / "plugin.py")
        mod = importlib.util.module_from_spec(spec)
        with patch.dict(sys.modules, mocks):
            spec.loader.exec_module(mod)
            descriptors = mod.Plugins()
            self.assertEqual(len(descriptors), 2)
            self.assertEqual(descriptors[0].where, Descriptor.WHERE_PLUGINMENU)
            self.assertEqual(descriptors[1].where, Descriptor.WHERE_MENU)
            self.assertEqual(mod.main_menu("mainmenu"), [])
            self.assertEqual(mod.main_menu("system"), [])
            config.plugins.warderyoutube.show_main_menu.value = True
            shortcut = mod.main_menu("mainmenu")
            self.assertEqual(len(shortcut), 1)
            self.assertEqual(shortcut[0][0], "YouTube Warder Evolution")
            self.assertEqual(shortcut[0][2], "warder_youtube_mainmenu")
            config.plugins.warderyoutube.show_main_menu.value = False
            self.assertEqual(mod.main_menu("mainmenu"), [])


if __name__ == "__main__":
    unittest.main()
