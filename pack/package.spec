# -*- mode: python -*-

app_path = 'src'

exe_name = 'eavatar'
hiddenimports = []

if sys.platform.startswith('win32'):
    exe_name = 'eavatar.exe'
    app_icon = os.path.join(app_path, 'media/eavatar.ico')
    ext_name = '.win'
elif sys.platform.startswith('linux'):
    ext_name = '.lin'
    run_strip = True
elif sys.platform.startswith('darwin'):
    ext_name = '.mac'
else:
    ext_name = ''

a = Analysis([os.path.join(app_path,'ava.py')],
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
          name=os.path.join('build', 'pyi.'+sys.platform, 'server', exe_name),
          debug=False,
          strip=False,
          upx=True,
          icon= os.path.join(app_path, 'media/eavatar.ico'),
          console=True )


coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               Tree(os.path.join(app_path, 'static'), 'static', excludes=['*.py']),
               Tree(os.path.join(app_path, 'cqlengine'), 'cqlengine', excludes=['*.py']),
               a.datas,
               strip=run_strip,
               upx=True,
               name=os.path.join('dist', 'eavatar'))

