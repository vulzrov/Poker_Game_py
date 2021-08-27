# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['E:\\香港大学\\第二学年\\python\\爬虫\\Poker_Game\\Poker_Game.py',
              'E:\香港大学\第二学年\python\爬虫\Poker_Game\class1.py'],
             pathex=['C:\\Users\\zhang\\Desktop\\Poker_Game'],
             binaries=[],
             datas=[],
             hiddenimports=[],
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
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='Poker_Game',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
