echo %1 %2 %3
echo on

rem
rem Wrapper script to run Python scripts with indexed input and output files
rem 
rem usage:
rem
rem run_python python_script index outputfile
rem

set python_script=%1
set index=%2
set outputfiles=%3

rem
rem extract stan environment
rem

mkdir stan_env
tar -xzf stan_env.tar.gz -C stan_env

rem
rem activate stan environment
rem

cd ./stan_env/Scripts
call activate
cd ../../

rem
rem run Python script
rem

python %python_script%

rem
rem deactivate stan environment
rem

cd ./stan_env/Scripts
call deactivate
cd ../../

rem
rem rename output files to indexed names
rem

index %index% %outputfiles%