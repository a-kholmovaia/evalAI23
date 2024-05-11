# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
    ('levels/level0/*', 'levels/level0/'),
    ('levels/level1/*', 'levels/level1/'),
    ('levels/level2/*', 'levels/level2/'),
    ('levels/level3/*', 'levels/level3/'),
    ('questions/questions/*', 'questions/questions/')
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

##### include mydir in distribution #######
def extra_datas(mydir):
    def rec_glob(p, files):
        import os
        import glob
        for d in glob.glob(p):
            if os.path.isfile(d):
                files.append(d)
            rec_glob("%s/*" % d, files)
    files = []
    rec_glob("%s/*" % mydir, files)
    extra_datas = []
    for f in files:
        extra_datas.append((f, f, 'DATA'))

    return extra_datas
###########################################

# append the 'data' dir
a.datas += extra_datas("evalAI23/img/")
a.datas += extra_datas("evalAI23/levels/level0/")
a.datas += extra_datas("evalAI23/levels/level0/enemy/")
a.datas += extra_datas("evalAI23/levels/level1")
a.datas += extra_datas("evalAI23/levels/level1/projectile/")
a.datas += extra_datas("evalAI23/levels/level1/wizard/")

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='AILabEval',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico',
)
