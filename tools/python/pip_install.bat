rem 2021/12/2 12:10

rem pip パッケージを一括でインストールします。

@echo off
set CURRENT_DIR=%~dp0

%CURRENT_DIR%..\..\ENV\Scripts\python.exe -m pip install -r %CURRENT_DIR%install_pip.list
