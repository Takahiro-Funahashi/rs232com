rem 2021/12/2 12:10

@echo off
set CURRENT_DIR=%~dp0
set DIST_PATH=%CURRENT_DIR%..\..\docs\pip_package\

md %DIST_PATH%

%CURRENT_DIR%..\..\ENV\Scripts\python.exe -V
%CURRENT_DIR%..\..\ENV\Scripts\python.exe -m pip list > %DIST_PATH%pip_list.txt
%CURRENT_DIR%..\..\ENV\Scripts\pip-licenses > %DIST_PATH%pip_licenses.txt
%CURRENT_DIR%..\..\ENV\Scripts\pipdeptree > %DIST_PATH%pip_tree.txt