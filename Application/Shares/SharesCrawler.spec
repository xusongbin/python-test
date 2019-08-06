# -*- mode: python -*-

block_cipher = None


a = Analysis(['SharesCrawler.py'],
             pathex=['E:\\Development\\project\\python-test\\Shares'],
             binaries=[],
             datas=[('Stocks.ico', '.'), ('chromedriver.exe', '.'), ('szzs000001.xlsx', '.'), ('yh881155.xlsx', '.')],
             hiddenimports=['xlwings'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='SharesCrawler',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=False,
          console=False,
          icon='Stocks.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='SharesCrawler')
