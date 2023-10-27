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
* 株式会社hokan所属（今年はGoldスポンサーとしてブースも出しています）
* Python歴は12年くらい（主にDjango）
* Python Boot Camp、Shonan.py、GCPUG Shonanなどコミュニティ活動もしています
* 著書（共著）：『 `Python実践レシピ <https://gihyo.jp/book/2022/978-4-297-12576-9>`_ 』

.. revealjs-break::

「Python Boot Campの紹介 - あなたの街で開催しませんか？」というポスターセッションをやっています。
ぜひ遊びに来てください！

今日話したいこと
----------------

* Python 3.11の新機能Data Class Transforms（PEP 681）について解説

この発表を聞いて何を得られるか
------------------------------

* Data Class Transforms（PEP 681）登場以前にPythonに存在した問題を理解できる
* Data Class Transforms（PEP 681）によりどうやって前述の問題を解決するのか理解できる
* 上記2つを知ることで、Python 3.11以降がより堅牢なコードを書けることを理解できる

PEP 681を一言で説明すると
=========================

.. revealjs-break::

「データクラス風ライブラリ」の型チェックを強化する機能。

…だけじゃ分かりませんよね？
---------------------------

「データクラス風ライブラリ」は私の造語です。
先に「データクラス」について説明します。

そもそもデータクラスとは
------------------------

クラスに定義した型アノテーションを元に、 ``dataclasses.dataclass`` デコレーターによって属性を自動生成したクラス。

.. revealjs-code-block:: python

   from dataclasses import dataclass

   @dataclass
   class Book:
       # ↓型アノテーション
       title: str
       price: int

   book = Book(title="Python実践レシピ", price=2970)
   print(book.title, book.price)
   # price引数の型が間違っているので型チェッカーではエラーになる
   book = Book(
       title="Python実践レシピ",
       price="定価2,970円（本体2,700円＋税10%）",
   )
   print(book.title, book.price)

データクラスは型チェッカーを使って型チェックできる
--------------------------------------------------

.. figure:: pyright-dataclass_example.*
   :alt: pyrightの実行結果

   pyrightの実行結果

「データクラス風ライブラリ」とは
--------------------------------

データクラスではないけど、データクラスと似たような書き方でクラスを定義するライブラリ。

* `attrs <https://www.attrs.org/en/stable/>`_
* `Pydantic <https://docs.pydantic.dev/latest/>`_
* `SQLAlchemy <https://www.sqlalchemy.org/>`_
* `Django <https://docs.djangoproject.com/ja/4.2/>`_ 内蔵のO/Rマッパー

Djangoの例
----------

Djangoで前述のデータクラス ``Book`` を表現するとこうなる。

.. revealjs-code-block:: python

   from django.db import models

   class Book(models.Model):
       title = models.CharField(max_length=255)
       price = models.IntegerField()

PEP 681以前に存在したある問題
=============================

「データクラス風ライブラリ」の型チェックに何が不足しているのか？

この発表で使う簡易O/Rマッパー
-----------------------------

本物のライブラリだと説明が長くなるので、簡易O/Rマッパーを使います。

.. revealjs-code-block:: python

   """orm.py"""
   class Base:
       """リレーショナルデータベースとマッピングさせるクラスの基底クラス"""
       def __init__(self, **kwargs):
           # 具体的な処理内容は省略
           print("Baseクラスの初期化処理")

    class String:
        """文字列フィールド用のクラス"""
        pass

    class Integer:
        """整数フィールド用のクラス"""
        pass

.. revealjs-break::

.. revealjs-code-block:: python

   """使用例"""
   from orm import Base, String, Integer

   class Book(Base):
       """書籍を表すクラス"""
       title = String()
       price = Integer()

こんなコードを書くとどうなる？
------------------------------

最後に以下のコードを追加。

.. revealjs-code-block:: python

   book = Book(
       title="Python実践レシピ",
       # priceは整数型なのでこれは間違っている
       price="定価2,970円（本体2,700円＋税10%）",
   )

型チェックではエラーにならない
------------------------------

.. figure:: pyright-books-1.*
   :alt: pyrightの実行結果

   pyrightの実行結果

なぜエラーにならないのか
------------------------

``Book.__init__`` には型情報がないので。

.. revealjs-code-block:: shell

   >>> from books import Book
   Baseクラスの初期化処理
   >>> help(Book.__init__)
   Help on function __init__ in module orm:

   __init__(self, **kwargs)
       Initialize self.  See help(type(self)) for accurate signature.
   (END)

データクラスなら型チェックができるが…
-------------------------------------

.. revealjs-code-block:: python

    from dataclasses import dataclass

    @dataclass
    class Book:
        title: str
        price: int

    book = Book(
        title="Python実践レシピ",
        # priceは整数型なのでこれは間違っている
        price="定価2,970円（本体2,700円＋税10%）",
    )

.. revealjs-break::

.. figure:: pyright-dataclass_books.*
   :alt: pyrightの実行結果

   pyrightの実行結果

O/Rマッパーとデータクラスの機能のいいとこ取りができないか？
-----------------------------------------------------------

ではこんな風に書けばいいのでは？
--------------------------------

.. revealjs-code-block:: python

    from dataclasses import dataclass

    from orm import Base

    # Baseクラスを継承したデータクラスを作る
    @dataclass
    class Book(Base):
        # Baseクラスで型アノテーションを元にフィールドを作る想定
        title: str
        price: int

    book = Book(
        title="Python実践レシピ",
        # priceは整数型なのでこれは間違っている
        price="定価2,970円（本体2,700円＋税10%）",
    )

一応型チェックはできる
----------------------

.. figure:: pyright-books2.*
   :alt: pyrightの実行結果

   pyrightの実行結果

``dataclass`` デコレーターが型ヒントを作ってくれるので、型チェックができる
--------------------------------------------------------------------------

.. revealjs-code-block:: shell

   >>> from books import Book
   Baseクラスの初期化処理
   >>> help(Book.__init__)
   Help on function __init__ in module hoge:

   __init__(self, title: str, price: int) -> None
       Initialize self.  See help(type(self)) for accurate signature.

``Base.__init__`` に定義されたコードが呼ばれなくなった
------------------------------------------------------

``Base.__init__`` に書いた処理が呼ばれない。

.. revealjs-code-block:: python

   class Base:
       """リレーショナルデータベースとマッピングさせるクラスの基底クラス"""
       def __init__(self, **kwargs):
           # 具体的な処理内容は省略
           print("Baseクラスの初期化処理")  # ←これが呼ばれない

.. revealjs-code-block:: shell

    $ python books2.py  # "Baseクラスの初期化処理"が表示されない

なぜ ``Base.__init__`` が呼ばれないのか
---------------------------------------

``dataclass`` デコレーターは ``__init__`` を上書きするので。

ライブラリによっては型ヒントの恩恵を受けるのは難しい場合もある
--------------------------------------------------------------

型チェッカー側でこのような問題をカバーしようとしているものもある。

Mypyのプラグイン機能
--------------------

例えばMypyはプラグインで機能を拡張できる。

.. revealjs-code-block:: toml

    # 設定ファイル（mypy.ini）にこんな形でプラグインを指定できる
   [mypy]
   plugins = /one/plugin.py, other.plugin

参考: https://mypy.readthedocs.io/en/stable/extending_mypy.html#configuring-mypy-to-use-plugins

プラグインにも問題がある
------------------------

ただし、プラグインは特定の型チェッカー専用。しかも、メンテナの負担が大きい。


PEP 681登場によって何が解決されるのか
=====================================

typingモジュールに `dataclass_transform <https://docs.python.org/3/library/typing.html#typing.dataclass_transform>`_ デコレーターが追加された。

dataclass_transformデコレーターの使用例
---------------------------------------

時間の都合上、今回は `1.` のみ紹介。

1. 自作の関数デコレーターに使う方法
2. 自作の基底クラスに使う方法
3. 自作のメタクラスに使う方法

.. revealjs-break::

まず、以下の ``my_orm.py`` を作成。

.. revealjs-code-block:: python

    from typing import TypeVar, dataclass_transform
    from orm import Integer, String

    T = TypeVar("T")

    @dataclass_transform()
    def create_model(cls: type[T]) -> type[T]:
        # クラスの型アノテーションを元にフィールドを追加
        for key, value in cls.__annotations__.items():
            if value is str:
                setattr(cls, key, String())
            elif value is int:
                setattr(cls, key, Integer())
        return cls

.. revealjs-break::

次に、以下のファイルを作成。

.. revealjs-code-block:: python

    from my_orm import create_model
    from orm import Base

    @create_model
    class Book(Base):
        title: str
        price: int

    book = Book(
        title="Python実践レシピ",
        # priceは整数型なのでこれは間違っている
        price="定価2,970円（本体2,700円＋税10%）",
    )

型チェックしてみると…
---------------------

データクラスと同じように型チェックが行われる。

.. figure:: pyright-pep681_books.*
   :alt: pyrightの実行結果

   pyrightの実行結果

dataclass_transformデコレーターの仕組みについて解説
===================================================

dataclass_transformデコレーターのソースコードはこうなっている
-------------------------------------------------------------

``dataclass_transform`` デコレーターはデコレート対象に ``__dataclass_transform__`` 属性を追加するだけ。

.. revealjs-code-block:: python

    def dataclass_transform(
        *,
        eq_default: bool = True,
        order_default: bool = False,
        kw_only_default: bool = False,
        field_specifiers: tuple[type[Any] | Callable[..., Any], ...] = (),
        **kwargs: Any,
    ) -> Callable[[T], T]:
        def decorator(cls_or_fn):
            cls_or_fn.__dataclass_transform__ = {
                "eq_default": eq_default,
                "order_default": order_default,
                "kw_only_default": kw_only_default,
                "field_specifiers": field_specifiers,
                "kwargs": kwargs,
            }
            return cls_or_fn
        return decorator

.. revealjs-break::

型チェッカーは ``__dataclass_transform__`` 属性を読み取ると、「このクラスはデータクラスではないがデータクラスのような型チェックを行ってほしい」というメッセージとして受け取る。

型チェッカーのPEP 681への対応状況
=================================

以下について調べた。

* Pyright(1.1.328)
* Mypy(1.6.1)
* Pyre(0.9.18)
* pytype(2023.9.27)

調べた結果
----------

2023年10月27日現在、公式ドキュメントでPEP 681対応を謳っているのはPyrightのみ。

Pyrightについて
---------------

以下公式ドキュメント「Type Checking Features」にPEP 681が載っている。

https://microsoft.github.io/pyright/#/features

Mypyについて
------------

このスライドに載せたサンプルコードで型チェックできることは確認したが、以下Issueの内容を読むと完全に対応したわけではなさそう。

https://github.com/python/mypy/issues/14293

Pyreについて
------------

0.9.11のリリースノートに"Basic support for PEP 681 (dataclass transforms)."と書いているが、実際に型チェックしてみるとエラーを検出してくれなかった（0.9.18で確認）。

https://github.com/facebook/pyre-check/releases/tag/v0.9.11

pytypeについて
--------------

Python 3.11対応自体がまだできていない。
Python 3.11対応は以下Issueで進めている。

https://github.com/google/pytype/issues/1308

PyrightはVS Codeから簡単に呼び出せる
------------------------------------

Pylanceという拡張をインストールすると、VS Codeから簡単にPyrightを呼び出せる。

.. revealjs-break::

.. figure:: vscode-and-pylance.*
   :alt: VS Code + Pylanceでエラーを表示できる

   VS Code + Pylanceでエラーを表示できる

「データクラス風ライブラリ」のPEP 681への対応状況
=================================================

以下について調べた。

* attrs(23.1.0)
* Pydantic(2.4.2)
* SQLAlchemy(2.0.21)
* Django内蔵のO/Rマッパー(4.2.5)

調べた結果
----------

Django以外はPEP 681に対応している。

attrsについて
-------------

``attr.define`` デコレーターが ``dataclass_transform`` デコレーターに相当する機能を持つ。

.. revealjs-code-block:: python

   import attr

   @attr.define
   class Book:
       title: str
       price: int

Pydanticについて
----------------

``pydantic.BaseModel`` クラスが ``dataclass_transform`` デコレーターに相当する機能を持つ。

.. revealjs-code-block:: python

    from pydantic import BaseModel

    class Book(BaseModel):
        title: str
        price: int

SQLAlchemyについて
------------------

``dataclass_transform`` デコレーターに相当する機能を持つものは2つ。

1つ目は ``sqlalchemy.orm.MappedAsDataclass`` クラス。

.. revealjs-code-block:: python

    from sqlalchemy.orm import (DeclarativeBase, Mapped, MappedAsDataclass,
                                mapped_column)

    class Base(DeclarativeBase):
        pass

    class Book(MappedAsDataclass, Base):
        __tablename__ = "book"
        id: Mapped[int] = mapped_column(init=False, primary_key=True)
        title: Mapped[str]
        price: Mapped[int]

.. revealjs-break::

2つ目は ``registry.mapped_as_dataclass()`` デコレーター。

.. revealjs-code-block:: python

    from sqlalchemy.orm import Mapped, mapped_column, registry

    reg = registry()

    @reg.mapped_as_dataclass(unsafe_hash=True)
    class Book:
        __tablename__ = "book"

        id: Mapped[int] = mapped_column(init=False, primary_key=True)
        title: Mapped[str]
        price: Mapped[int]

.. revealjs-break::

また、attrsを使ったクラスをSQLAlchemy用のクラスにする機能がある。

.. revealjs-code-block:: python

    import attr
    from sqlalchemy import Column, Integer, String, Table
    from sqlalchemy.orm import Mapped, registry

    mapper_registry = registry()

    @attr.define(slots=False)
    class Book:
        id: Mapped[int] = attr.ib(init=False)
        title: Mapped[str]
        price: Mapped[int]
    # ↓まだ続きがある


.. revealjs-break::

型アノテーションとテーブル定義で似たような構造を二重管理することになるので少し面倒そう。

.. revealjs-code-block:: python

    # ↑前の続き
    book = Table(
        "book",
        mapper_registry.metadata,
        Column("id", Integer, autoincrement=True, primary_key=True),
        Column("title", String(50)),
        Column("price", Integer),
    )

    mapper_registry.map_imperatively(Book, book)


Django内蔵のO/Rマッパーについて
-------------------------------

`Issue Tracker <https://code.djangoproject.com/query>`_ と `Django Enhancement Proposals <https://github.com/django/deps>`_ (DEPs)、`メーリングリスト <https://groups.google.com/g/django-users?pli=1>`_ で「PEP 681」、「dataclass_transform」を検索してみたが、該当する情報は見当たらなかった。

まとめ
======

まとめ1
-------

* PEP 681登場以前、「データクラス風ライブラリ」では、初期化処理に関する型チェックを行うことができなかった
* PEP 681でこれらのライブラリでもデータクラスのような型チェックをできる

まとめ2
-------

* 2023年10月27日現在、PEP 681対応を謳っている型チェッカーはPyrightのみ。他の型チェッカーがんばれ！
* attrs、Pydantic、SQLAlchemyはPEP 681に対応している。Djangoも対応してほしい😢

ご清聴ありがとうございました
============================

.. figure:: thank-you-for-your-attention.*
   :alt: AIが考えた「Pythonの型ヒントにより安心してプログラミングを楽しむプログラマー」

   AIが考えた「Pythonの型ヒントにより安心してプログラミングを楽しむプログラマー」
