# -*- mode: python -*-

app_path = 'src'

exe_name = 'launcher'
hiddenimports = ['depends_linux.py']

run_strip = True

a = Analysis([os.path.join(app_path,'launcher.py')],
             pathex=['src'],
             hiddenimports=hiddenimports,
             hookspath=None,
             runtime_hooks=None,
             excludes=['PyQt4', 'wx', 'django', 'Tkinter', 'gi.repository', 'objc', 'AppKit', 'Foundation'])

run_strip = False

pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.dependencies,
          exclude_binaries=True,
          name=os.path.join('build', 'pyi.'+sys.platform, 'app', exe_name),
          debug=False,
          strip=False,
          upx=True,
          icon= os.path.join(app_path, 'src/eavatar.ico'),
          console=True )


coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               Tree(os.path.join(app_path, 'cqlengine'), 'cqlengine', excludes=['*.py']),
               a.datas,
               strip=run_strip,
               upx=True,
               name=os.path.join('dist', 'app'))

