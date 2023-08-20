#######################################################################
型チェックを強化するPython 3.11の新機能Data Class Transforms（PEP 681）
#######################################################################
.. raw:: html

   <a rel="license" href="http://creativecommons.org/licenses/by/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/88x31.png" /></a><br /><small>This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International License</a>.</small>

はじめに
========

自己紹介
--------

* Ryuji Tsutsui @ryu22e
* 株式会社hokan所属
* Python歴は12年くらい（主にDjango）
* Python Boot Camp、Shonan.py GCPUG Shonanなどコミュニティ活動もしています
* 著書（共著）：『 `Python実践レシピ <https://gihyo.jp/book/2022/978-4-297-12576-9>`_ 』

今日話したいこと
----------------

* Python 3.11の新機能Data Class Transforms（PEP 681）について解説
* PEP 681はどのような問題を解決するのか

Data Class Transforms（PEP 681）をざっくり説明すると
====================================================

「データクラスと似た構造を持つクラスを扱うライブラリ」の型チェックを強化する機能

そもそもデータクラスとは
------------------------

クラスに定義した型アノテーションを元に、 ``dataclasses.dataclass`` デコレーターによって属性を自動生成したクラス

.. revealjs-code-block:: python

   from dataclasses import dataclass

   @dataclass
   class Book:
       title: str
       price: int

   b = Book(title="Python実践レシピ", price=2970)
   print(b.name, b.price)


「データクラスと似た構造を持つクラスを扱うライブラリ」とは
----------------------------------------------------------

* `attrs <https://www.attrs.org/en/stable/>`_
* `Pydantic <https://docs.pydantic.dev/latest/>`_
* O/Rマッパー（ `SQLAlchemy <https://www.sqlalchemy.org/>`_ 、 `Django <https://docs.djangoproject.com/ja/4.2/>`_ 内臓のO/Rマッパー ）

PEP 681以前に存在したある問題
=============================

PEP 681登場によって何が解決されるのか
=====================================

dataclass_transformデコレータの仕組みについて解説
=================================================

「データクラスと似た構造を持つクラスを扱うライブラリ」のPEP 681への対応状況
===========================================================================

