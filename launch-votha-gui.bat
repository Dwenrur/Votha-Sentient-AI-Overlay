@echo off
setlocal
pushd %~dp0
python -B -X faulthandler src\gui\votha_gui.py
popd
