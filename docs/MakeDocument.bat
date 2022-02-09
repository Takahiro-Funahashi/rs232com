rem 開発ドキュメントを生成するバッチ
rem /docs/build/html/index.html

rem 2021/05/20 新規作成

set CURRENT_DIR=%~dp0

rem %CURRENT_DIR%

sphinx-apidoc -f -P -o %CURRENT_DIR%source/_root_source_ %CURRENT_DIR%../rs232com/
%CURRENT_DIR%make html