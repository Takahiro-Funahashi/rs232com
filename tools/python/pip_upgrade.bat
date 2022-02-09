rem 2022/02/04

rem pipを最新状態にアップグレードするバッチです。

@echo off
set CURRENT_DIR=%~dp0

%CURRENT_DIR%..\..\ENV\Scripts\python.exe -m pip install --upgrade pip
