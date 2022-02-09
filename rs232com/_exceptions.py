#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
FileName:
--------------------------------------------------------------------------------
    _exceptions.py

Description:
--------------------------------------------------------------------------------
    独自例外エラー定義

History:
--------------------------------------------------------------------------------
    2022/02/01 作成

"""


class RS232comException(Exception):
    pass


class RS232comPortException(RS232comException):
    pass


class RS232comParameterException(RS232comException):
    pass


class RS232comValueException(RS232comException):
    pass


class RS232comArgumentException(RS232comException):
    pass


class RS232comOpneException(RS232comException):
    pass


class RS232comCloseException(RS232comException):
    pass


class RS232comSendException(RS232comException):
    pass
