import PyInstaller.config
PyInstaller.config.CONF['distpath'] = '.'

##############################################################################################################################


chessAnalysis = Analysis(['..\\chess\\main.py'],
                         pathex=[],
                         binaries=[],
                         datas=[('..\\chess\\resources\\*.*', '.')],
                         hiddenimports=[],
                         hookspath=[],
                         hooksconfig={},
                         runtime_hooks=[],
                         excludes=[],
                         win_no_prefer_redirects=False,
                         win_private_assemblies=False,
                         cipher=None,
                         noarchive=False)

chessPYZ = PYZ(chessAnalysis.pure, chessAnalysis.zipped_data, cipher=None)

chessEXE = EXE(chessPYZ,
               chessAnalysis.scripts,
               chessAnalysis.binaries,
               chessAnalysis.zipfiles,
               chessAnalysis.datas,
               [],
               name='chess',
               debug=False,
               bootloader_ignore_signals=False,
               strip=False,
               upx=True,
               upx_exclude=[],
               runtime_tmpdir=None,
               console=False,
               disable_windowed_traceback=False,
               target_arch=None,
               codesign_identity=None,
               entitlements_file=None,
               icon='..\\chess\\resources\\app.ico')

##############################################################################################################################


snakeAnalysis = Analysis(['..\\snake\\main.py'],
                         pathex=[],
                         binaries=[],
                         datas=[('..\\snake\\resources\\*.*', '.')],
                         hiddenimports=[],
                         hookspath=[],
                         hooksconfig={},
                         runtime_hooks=[],
                         excludes=[],
                         win_no_prefer_redirects=False,
                         win_private_assemblies=False,
                         cipher=None,
                         noarchive=False)

snakePYZ = PYZ(snakeAnalysis.pure, snakeAnalysis.zipped_data, cipher=None)

snakeEXE = EXE(snakePYZ,
               snakeAnalysis.scripts,
               snakeAnalysis.binaries,
               snakeAnalysis.zipfiles,
               snakeAnalysis.datas,
               [],
               name='snake',
               debug=False,
               bootloader_ignore_signals=False,
               strip=False,
               upx=True,
               upx_exclude=[],
               runtime_tmpdir=None,
               console=False,
               disable_windowed_traceback=False,
               target_arch=None,
               codesign_identity=None,
               entitlements_file=None,
               icon='..\\snake\\resources\\app.ico')


##############################################################################################################################


calculatorAnalysis = Analysis(['..\\calculator\\main.py'],
                              pathex=[],
                              binaries=[],
                              datas=[('..\\calculator\\resources\\*.*', '.'),
                                     ('..\\calculator\\resources\\theme\\forest-dark.tcl', 'theme'),
                                     ('..\\calculator\\resources\\theme\\forest-dark', 'theme\\forest-dark')],
                              hiddenimports=[],
                              hookspath=[],
                              hooksconfig={},
                              runtime_hooks=[],
                              excludes=[],
                              win_no_prefer_redirects=False,
                              win_private_assemblies=False,
                              cipher=None,
                              noarchive=False)

calculatorPYZ = PYZ(calculatorAnalysis.pure, calculatorAnalysis.zipped_data, cipher=None)

calculatorEXE = EXE(calculatorPYZ,
                    calculatorAnalysis.scripts,
                    calculatorAnalysis.binaries,
                    calculatorAnalysis.zipfiles,
                    calculatorAnalysis.datas,
                    [],
                    name='calculator',
                    debug=False,
                    bootloader_ignore_signals=False,
                    strip=False,
                    upx=True,
                    upx_exclude=[],
                    runtime_tmpdir=None,
                    console=False,
                    disable_windowed_traceback=False,
                    target_arch=None,
                    codesign_identity=None,
                    entitlements_file=None,
                    icon='..\\calculator\\resources\\app.ico')


##############################################################################################################################


currencyConverterAnalysis = Analysis(['..\\currency converter\\main.py'],
                                     pathex=[],
                                     binaries=[],
                                     datas=[('..\\currency converter\\resources\\*.*', '.'),
                                            ('..\\currency converter\\resources\\theme\\sun-valley.tcl', 'theme'),
                                            ('..\\currency converter\\resources\\theme\\sun-valley', 'theme\\sun-valley')],
                                     hiddenimports=[],
                                     hookspath=[],
                                     hooksconfig={},
                                     runtime_hooks=[],
                                     excludes=[],
                                     win_no_prefer_redirects=False,
                                     win_private_assemblies=False,
                                     cipher=None,
                                     noarchive=False)

currencyConverterPYZ = PYZ(currencyConverterAnalysis.pure, currencyConverterAnalysis.zipped_data, cipher=None)

currencyConverterEXE = EXE(currencyConverterPYZ,
                           currencyConverterAnalysis.scripts,
                           currencyConverterAnalysis.binaries,
                           currencyConverterAnalysis.zipfiles,
                           currencyConverterAnalysis.datas,
                           [],
                           name='currency converter',
                           debug=False,
                           bootloader_ignore_signals=False,
                           strip=False,
                           upx=True,
                           upx_exclude=[],
                           runtime_tmpdir=None,
                           console=False,
                           disable_windowed_traceback=False,
                           target_arch=None,
                           codesign_identity=None,
                           entitlements_file=None,
                           icon='..\\currency converter\\resources\\app.ico')
