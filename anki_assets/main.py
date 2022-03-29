# -*- coding: utf-8 -*-
"""The implementation of the Anki Assets plugin."""
import os
import os.path
import pathlib

from aqt import mw  # type: ignore

addon_path = os.path.dirname(__file__)


def addons_assets_directory() -> pathlib.Path:
    return pathlib.Path(addon_path) / 'assets'


def list_my_assets(dir: pathlib.Path) -> list[str]:
    return [f for f in os.listdir(dir) if f.startswith("_aa-")]


IMPORT_STATEMENTS = (
    '<link rel="stylesheet" href="_aa-style.css" class="anki-assets">\n'
    '<script src="_aa-mathjax-config.js" type="text/x-mathjax-config" class="anki-assets"></script>\n'
    '<script src="_aa-script.js" type="text/javascript" class="anki-assets"></script>\n'
)


def install_assets():
    codehighlighter_assets_dir = codehighlighter_assets_directory()
    my_assets = list_my_assets(codehighlighter_assets_dir)
    for asset in my_assets:
        mw.col.media.add_file(codehighlighter_assets_dir / asset)

    def append_import_statements(tmpl):
        return tmpl + '\n' + IMPORT_STATEMENTS

    for model in mw.col.models.all():
        for tmpl in model['tmpls']:
            tmpl['afmt'] = append_import_statements(tmpl['afmt'])
            tmpl['qfmt'] = append_import_statements(tmpl['qfmt'])
        mw.col.models.save(model)


def delete_assets():

    def delete_import_statements(tmpl):
        return re.sub('^<[^>]*class="[^"]*anki-assets[^"]*"[^>]*>[^\n]*\n',
                      "",
                      tmpl,
                      flags=re.MULTILINE)

    for model in mw.col.models.all():
        for tmpl in model['tmpls']:
            tmpl['afmt'] = delete_import_statements(tmpl['afmt']).strip()
            tmpl['qfmt'] = delete_import_statements(tmpl['qfmt']).strip()
        mw.col.models.save(model)

    my_assets = list_my_assets(anki_media_directory())
    mw.col.media.trash_files(my_assets)


def setup_menu():
    mw.form.menuTools.addSection("Anki Assets")
    mw.form.menuTools.addAction(
        aqt.qt.QAction("Configure Anki Assets", mw, triggered=install_assets))
    mw.form.menuTools.addAction(
        aqt.qt.QAction("Delete Anki Assets", mw, triggered=delete_assets))


setup_menu()
