# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v0.0.12] - 2024-10-15
### :sparkles: New Features
- [`d711767`](https://github.com/viplazylmht/sql-datalineage/commit/d71176769eed9131e401fb6b3fddedc154582f2b) - support parse lineage for scalar subquery *(commit by [@viplazylmht](https://github.com/viplazylmht))*
- [`71de182`](https://github.com/viplazylmht/sql-datalineage/commit/71de182f7215fc573e70240ff6696c107658ec05) - add support for INSERT statement *(commit by [@viplazylmht](https://github.com/viplazylmht))*
- [`067dc4a`](https://github.com/viplazylmht/sql-datalineage/commit/067dc4a4fe808e1a9999488c97893f44236bf0c3) - add support for create statement *(commit by [@viplazylmht](https://github.com/viplazylmht))*


## [v0.0.11] - 2024-08-12
### :sparkles: New Features
- [`6f29b8c`](https://github.com/viplazylmht/sql-datalineage/commit/6f29b8c5b5116b15f9f1405c1d80fb7f41e94ebc) - **ci**: add yaml module to dev env *(commit by [@viplazylmht](https://github.com/viplazylmht))*
- [`38964e6`](https://github.com/viplazylmht/sql-datalineage/commit/38964e649f03af7db6aa790c905abef2d439819a) - **renderer**: force render method return str *(commit by [@viplazylmht](https://github.com/viplazylmht))*
- [`5bbfacd`](https://github.com/viplazylmht/sql-datalineage/commit/5bbfacd99a98ebd1ade3d3345340d7ab17eab8f6) - add support for union *(commit by [@viplazylmht](https://github.com/viplazylmht))*
- [`9f1befa`](https://github.com/viplazylmht/sql-datalineage/commit/9f1befa35c3d53098c4d5d51982f48644399f6ee) - support select statement without contains from *(commit by [@viplazylmht](https://github.com/viplazylmht))*


## [v0.0.10] - 2024-06-19
### :bug: Bug Fixes
- [`2bcde8f`](https://github.com/viplazylmht/sql-datalineage/commit/2bcde8f834a0d5c60d9b8ac1e4544526543e6664) - missmatch dialect when ensure schema and qualify *(commit by [@viplazylmht](https://github.com/viplazylmht))*


## [v0.0.9] - 2024-06-19
### :sparkles: New Features
- [`7b390cf`](https://github.com/viplazylmht/sql-datalineage/commit/7b390cf738a18770a84095fe9da147b5b4b20af9) - add support parse lineage with dialect *(commit by [@viplazylmht](https://github.com/viplazylmht))*


## [v0.0.8] - 2024-06-17
### :sparkles: New Features
- [`a1687bb`](https://github.com/viplazylmht/sql-datalineage/commit/a1687bb5c4415f7bebbce91e2c1e7675a6e43fdc) - allow to infer columns in table when schema not found *(commit by [@viplazylmht](https://github.com/viplazylmht))*


## [v0.0.7] - 2024-06-14
### :boom: BREAKING CHANGES
- due to [`7d125ae`](https://github.com/viplazylmht/sql-datalineage/commit/7d125ae072e1b618a467e65a4ae942b10125615c) - add workflow for publish package and update changelog *(commit by [@viplazylmht](https://github.com/viplazylmht))*:

  add workflow for publish package and update changelog


### :sparkles: New Features
- [`ec78ab6`](https://github.com/viplazylmht/sql-datalineage/commit/ec78ab6eca19a80d30fd45885c5fa59171bc0916) - **build**: dynamic versioning using setuptools-scm *(commit by [@viplazylmht](https://github.com/viplazylmht))*
- [`b2646b4`](https://github.com/viplazylmht/sql-datalineage/commit/b2646b4968509915280c610d50e707c638146162) - **ci**: add github action *(commit by [@viplazylmht](https://github.com/viplazylmht))*
- [`c119a99`](https://github.com/viplazylmht/sql-datalineage/commit/c119a99dacc8f63ea3949dadc861f7066efb9466) - **ci**: update ggithub action python package *(commit by [@viplazylmht](https://github.com/viplazylmht))*
- [`6bb2593`](https://github.com/viplazylmht/sql-datalineage/commit/6bb2593d73abc829b5193fa7ef6a354f857d4288) - add lineage cli and api *(commit by [@viplazylmht](https://github.com/viplazylmht))*
- [`7d125ae`](https://github.com/viplazylmht/sql-datalineage/commit/7d125ae072e1b618a467e65a4ae942b10125615c) - add workflow for publish package and update changelog *(commit by [@viplazylmht](https://github.com/viplazylmht))*

### :bug: Bug Fixes
- [`fa5bbae`](https://github.com/viplazylmht/sql-datalineage/commit/fa5bbaeeab67c2d39f2b4d6bd202fa0bb9738764) - add missing permission for github actions *(commit by [@viplazylmht](https://github.com/viplazylmht))*

[v0.0.7]: https://github.com/viplazylmht/sql-datalineage/compare/v0.0.1...v0.0.7
[v0.0.8]: https://github.com/viplazylmht/sql-datalineage/compare/v0.0.7...v0.0.8
[v0.0.9]: https://github.com/viplazylmht/sql-datalineage/compare/v0.0.8...v0.0.9
[v0.0.10]: https://github.com/viplazylmht/sql-datalineage/compare/v0.0.9...v0.0.10
[v0.0.11]: https://github.com/viplazylmht/sql-datalineage/compare/v0.0.10...v0.0.11
[v0.0.12]: https://github.com/viplazylmht/sql-datalineage/compare/v0.0.11...v0.0.12
