echo %1 %2 %3 %4
echo on

rem
rem Wrapper script to run Python scripts with indexed output files
rem 
rem usage:
rem
rem run_python python_script index outputfile... 
rem

set python_script=%1
set index=%2
set outputfiles=%3
set python_version=%4

set default_version=python

if "%python_version%"=="" set python_version=%default_version%

set python_zipfile=%python_version%.zip 

rem
rem unbundle the python distribution - self extracting .exe
rem

%python_zipfile% > NUL
del %python_zipfile%

rem
rem pick up the python DLLs and .exes
rem 

set path=%cd%\dlls;%path%


rem
rem run the Python script
rem 

python %python_script%

rem
rem rename output files to indexed names
rem

index %index% %outputfiles%

