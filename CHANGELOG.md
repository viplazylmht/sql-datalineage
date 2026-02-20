# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v0.0.16] - 2026-02-20
### :bug: Bug Fixes
- [`b83cfb6`](https://github.com/viplazylmht/sql-datalineage/commit/b83cfb60dda3e5f2f244279ab44b4b543af672c3) - **renderer**: correct method signature for get_node_id *(commit by [@AbhishekASLK](https://github.com/AbhishekASLK))*

### :zap: Performance Improvements
- [`0b20dae`](https://github.com/viplazylmht/sql-datalineage/commit/0b20dae290a32a1775cfa0e24fd46cd5bf6420a1) - **renderer**: improving mermaid render performance *(commit by [@viplazylmht](https://github.com/viplazylmht))*
- [`491daf2`](https://github.com/viplazylmht/sql-datalineage/commit/491daf27631810e4c0b66a0f29a05a59c77d7ddf) - **schema_retriever**: improving batching schema retriever performance *(commit by [@viplazylmht](https://github.com/viplazylmht))*

### :wrench: Chores
- [`794f299`](https://github.com/viplazylmht/sql-datalineage/commit/794f299f6fa239543e074c48cb8e4b023fd9b9cd) - **build**: switch type-checker from mypy to ty *(commit by [@viplazylmht](https://github.com/viplazylmht))*


## [v0.0.15] - 2025-09-02
### :sparkles: New Features
- [`9c121c0`](https://github.com/viplazylmht/sql-datalineage/commit/9c121c0d22b3542d5e00ff82bcdac89962db9b86) - add initial schema retriever and its sqlalchemy impl *(commit by [@viplazylmht](https://github.com/viplazylmht))*
- [`d964832`](https://github.com/viplazylmht/sql-datalineage/commit/d9648322583cce4d13d9ad1b1d1091b870909069) - **schema_retriever**: add static schema retriever and enhancing tests *(commit by [@viplazylmht](https://github.com/viplazylmht))*
- [`aebef37`](https://github.com/viplazylmht/sql-datalineage/commit/aebef377430575c5a4db901d234f3dcaa823780b) - **serializer**: support serialize and deserialize data using pickle *(commit by [@viplazylmht](https://github.com/viplazylmht))*
- [`1a63a87`](https://github.com/viplazylmht/sql-datalineage/commit/1a63a87190aa994bd0be75280ed883aea8047789) - **node**: add node_id, node upstreams, and change node to json format *(commit by [@viplazylmht](https://github.com/viplazylmht))*
- [`08ad07b`](https://github.com/viplazylmht/sql-datalineage/commit/08ad07b9ad8bcf7e892233f1f32daf59b526fce1) - abstract node with node type *(commit by [@viplazylmht](https://github.com/viplazylmht))*
- [`882c556`](https://github.com/viplazylmht/sql-datalineage/commit/882c55658fe63311d702413ecafdec23e4663559) - **visitor**: Add base node visitor *(commit by [@viplazylmht](https://github.com/viplazylmht))*
- [`a0440fb`](https://github.com/viplazylmht/sql-datalineage/commit/a0440fbb78e404686bde118f00c9c2a7f70bcc35) - **renderer**: mermaid renderer can render to html and support ipython *(commit by [@viplazylmht](https://github.com/viplazylmht))*

### :bug: Bug Fixes
- [`005cb0d`](https://github.com/viplazylmht/sql-datalineage/commit/005cb0d14b2628b8936a69dad57a082b15e2c9fb) - **test**: fix sqlalchemy test can not delete db file on windows *(commit by [@viplazylmht](https://github.com/viplazylmht))*
- [`b511291`](https://github.com/viplazylmht/sql-datalineage/commit/b51129166686150deec44c26906f205fe776f351) - **cli**: fix cli always require schema path *(commit by [@viplazylmht](https://github.com/viplazylmht))*
- [`b742682`](https://github.com/viplazylmht/sql-datalineage/commit/b74268259ca4c5149d388780b1b31da397a23868) - fix test serializer not run *(commit by [@viplazylmht](https://github.com/viplazylmht))*
- [`ef8fc84`](https://github.com/viplazylmht/sql-datalineage/commit/ef8fc846a2a5fb49366b163f36a64f05ce7c2e2f) - **lineage**: fix missmatch scope of the union in cte *(commit by [@viplazylmht](https://github.com/viplazylmht))*
- [`b3a7c82`](https://github.com/viplazylmht/sql-datalineage/commit/b3a7c82a15962a7356521076dfc0dcae3eb7047a) - **renderer**: fix mermaid render duplicate nodes *(commit by [@viplazylmht](https://github.com/viplazylmht))*

### :wrench: Chores
- [`239bcd7`](https://github.com/viplazylmht/sql-datalineage/commit/239bcd7c5819b6a1f3a7c4ffe1e3722ed0d778f6) - **renderer**: make mermaid more stable and testable *(commit by [@viplazylmht](https://github.com/viplazylmht))*
- [`0dbcd23`](https://github.com/viplazylmht/sql-datalineage/commit/0dbcd2389928531ca10b8902d0f894fa10c6581e) - **renderer**: make test lineage support mermaid output type *(commit by [@viplazylmht](https://github.com/viplazylmht))*
- [`e8ce2f9`](https://github.com/viplazylmht/sql-datalineage/commit/e8ce2f9d01798b0d0a3da1bfe9b411bcb8fe9c3e) - **renderer**: bump all dependencies version to newest *(commit by [@viplazylmht](https://github.com/viplazylmht))*
- [`bd192ac`](https://github.com/viplazylmht/sql-datalineage/commit/bd192acd7468a37fc0d368d9836a90a8948a11f7) - **docs**: update readme to correct mermaid usage *(commit by [@viplazylmht](https://github.com/viplazylmht))*
- [`ab7fb2b`](https://github.com/viplazylmht/sql-datalineage/commit/ab7fb2b2eb0f77fcb2f130e2c2517b55570bef48) - refine project ignore files *(commit by [@viplazylmht](https://github.com/viplazylmht))*


## [v0.0.14] - 2024-12-07
### :sparkles: New Features
- [`7b16533`](https://github.com/viplazylmht/sql-datalineage/commit/7b165334ec15af7a41086a7276eecbb8807143bc) - **build**: change build tools to uv, build backend to hatchling *(commit by [@viplazylmht](https://github.com/viplazylmht))*

### :bug: Bug Fixes
- [`d23fc8d`](https://github.com/viplazylmht/sql-datalineage/commit/d23fc8d46c2ceef5bfa5f0510dbf0b5db8998469) - **pyproject**: fix project urls issues *(commit by [@viplazylmht](https://github.com/viplazylmht))*


## [v0.0.13] - 2024-11-17
### :boom: BREAKING CHANGES
- due to [`6f5e0d1`](https://github.com/viplazylmht/sql-datalineage/commit/6f5e0d1ff80aa58692cc3c640133051471b8ee8e) - support merge statement *(commit by [@viplazylmht](https://github.com/viplazylmht))*:

  support merge statement


### :sparkles: New Features
- [`6f5e0d1`](https://github.com/viplazylmht/sql-datalineage/commit/6f5e0d1ff80aa58692cc3c640133051471b8ee8e) - support merge statement *(commit by [@viplazylmht](https://github.com/viplazylmht))*

### :white_check_mark: Tests
- [`59a3191`](https://github.com/viplazylmht/sql-datalineage/commit/59a3191850c42cbb56fcd7662b45e260d8475a1c) - add more test config for lineage test *(commit by [@viplazylmht](https://github.com/viplazylmht))*


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
[v0.0.13]: https://github.com/viplazylmht/sql-datalineage/compare/v0.0.12...v0.0.13
[v0.0.14]: https://github.com/viplazylmht/sql-datalineage/compare/v0.0.13...v0.0.14
[v0.0.15]: https://github.com/viplazylmht/sql-datalineage/compare/v0.0.14...v0.0.15
[v0.0.16]: https://github.com/viplazylmht/sql-datalineage/compare/v0.0.15...v0.0.16
