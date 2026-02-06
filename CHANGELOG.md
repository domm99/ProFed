## [0.7.4](https://github.com/domm99/ProFed/compare/0.7.3...0.7.4) (2026-02-06)

### Bug Fixes

* fix dirichlet splitting, it was not working when targets were not tensors ([e34c652](https://github.com/domm99/ProFed/commit/e34c652024419a0ab7b63090a1377c00589d3a01))

### General maintenance

* update readme ([03f7aed](https://github.com/domm99/ProFed/commit/03f7aed606b24a94f79dede0c8f346489fafc93d))
* update readme ([741d176](https://github.com/domm99/ProFed/commit/741d1768d5ed482d6f7dd5e0dbcd1a9a0e1cb7e3))
* update readme ([c99a3fa](https://github.com/domm99/ProFed/commit/c99a3fab5b5403f77777adfa1b987d89d34831e9))

## [0.7.3](https://github.com/davidedomini/ProFed/compare/0.7.2...0.7.3) (2025-07-23)

### Bug Fixes

* fix partitioning when using datasets in which targets are lists but not tensors ([093127d](https://github.com/davidedomini/ProFed/commit/093127da03408959462883b5fa6a410002dc0278))

### General maintenance

* update readme ([6b40db7](https://github.com/davidedomini/ProFed/commit/6b40db7dc98766399f813c0741c97267d0c2a3c7))

## [0.7.2](https://github.com/davidedomini/ProFed/compare/0.7.1...0.7.2) (2025-07-01)

### Bug Fixes

* fix regression split to consider indices of the subset ([80b0387](https://github.com/davidedomini/ProFed/commit/80b03876b280180e605bb2620830b056db97b7f2))

## [0.7.1](https://github.com/davidedomini/ProFed/compare/0.7.0...0.7.1) (2025-07-01)

### Bug Fixes

* fix UTKFaceDataset import ([35a914e](https://github.com/davidedomini/ProFed/commit/35a914e18ff8186c732cda335489bad9a26cab62))

## [0.7.0](https://github.com/davidedomini/ProFed/compare/0.6.5...0.7.0) (2025-07-01)

### Features

* implement hard partitioning for UTKFaceDataset ([8c48dca](https://github.com/davidedomini/ProFed/commit/8c48dcaa309afa48d12512db20d430b28cb700c8))
* implement UTKFaceDataset ([c47c232](https://github.com/davidedomini/ProFed/commit/c47c232d5a8ef2200a307bdaa3b54aacb2c6a97a))

### Dependency updates

* **deps:** add datasets, fsspec, tensorflow-datasets dependecies ([130014a](https://github.com/davidedomini/ProFed/commit/130014add9a60217f93d40eca8b5d5ae15b53084))

## [0.6.5](https://github.com/davidedomini/ProFed/compare/0.6.4...0.6.5) (2025-06-17)

### Bug Fixes

* add seed when creating the environment ([b275736](https://github.com/davidedomini/ProFed/commit/b2757367e27c9c21a45b00f0e90a312f870cd7af))

## [0.6.4](https://github.com/davidedomini/ProFed/compare/0.6.3...0.6.4) (2025-06-17)

### Bug Fixes

* add indexes shuffling before splitting ([bde0833](https://github.com/davidedomini/ProFed/commit/bde083389a0880b176331d2a43608bce14530e99))

## [0.6.3](https://github.com/davidedomini/ProFed/compare/0.6.2...0.6.3) (2025-06-17)

### Dependency updates

* **deps:** add pytest ([1e95ee4](https://github.com/davidedomini/ProFed/commit/1e95ee424d9a92c420c96938094c6de283cf7222))

### Bug Fixes

* using complete dataset and not only train and validation, otherwise we get index out of bounds ([7217fc0](https://github.com/davidedomini/ProFed/commit/7217fc0fcd8befbfcc4b4210c4ace9596053ef52))

## [0.6.2](https://github.com/davidedomini/ProFed/compare/0.6.1...0.6.2) (2025-06-17)

### Bug Fixes

* add return in method to distribute data from regions to devices ([3893417](https://github.com/davidedomini/ProFed/commit/38934176e4d3f51349218bfead8acc82e73fef36))

## [0.6.1](https://github.com/davidedomini/ProFed/compare/0.6.0...0.6.1) (2025-06-17)

### Bug Fixes

* fix EMNIST test dataset name ([e589fd1](https://github.com/davidedomini/ProFed/commit/e589fd1782031ce657d083bb028b3459efae19a7))

## [0.6.0](https://github.com/davidedomini/ProFed/compare/0.5.0...0.6.0) (2025-06-09)

### Features

* new API, added concepts of Environment and Region ([90fab5d](https://github.com/davidedomini/ProFed/commit/90fab5dc13609e68422b0e3652609396182f96a5))

### General maintenance

* add python version file ([5ee7b22](https://github.com/davidedomini/ProFed/commit/5ee7b223b2109e3550150fc96d4ff4e77f32a809))

## [0.5.0](https://github.com/davidedomini/ProFed/compare/0.4.2...0.5.0) (2025-05-21)

### Features

* implement new devices to data mapping ([76b2807](https://github.com/davidedomini/ProFed/commit/76b2807864462a2de8662191aa32051b650a36d5))

## [0.4.2](https://github.com/davidedomini/ProFed/compare/0.4.1...0.4.2) (2025-05-21)

### Bug Fixes

* update torch and torchvision dependecies ([beadd61](https://github.com/davidedomini/ProFed/commit/beadd6153c3e69bd7d50fea0fe1720c1cd6c171e))

## [0.4.1](https://github.com/davidedomini/ProFed/compare/0.4.0...0.4.1) (2025-02-03)

### Bug Fixes

* fix partitioning method ([952b8c5](https://github.com/davidedomini/ProFed/commit/952b8c5d630e45ab1017e791fc0b24c78c01f7fb))

## [0.4.0](https://github.com/davidedomini/ProFed/compare/0.3.0...0.4.0) (2025-02-03)

### Features

* implement method to distribute data among clients ([1c69181](https://github.com/davidedomini/ProFed/commit/1c69181b7eb55034e19c354f60d2a35e8412f777))

## [0.3.0](https://github.com/davidedomini/ProFed/compare/0.2.0...0.3.0) (2025-01-27)

### Features

* add call to hard and iid partitionings ([c5fdfa0](https://github.com/davidedomini/ProFed/commit/c5fdfa0d37fb93f2c77678608d51a327a95a7f00))

## [0.2.0](https://github.com/davidedomini/ProFed/compare/0.1.0...0.2.0) (2025-01-27)

### Features

* define empty API fot data distribution among client devices ([15fb161](https://github.com/davidedomini/ProFed/commit/15fb1618f34ec9085b0672f65f8bc31be5052f5a))

## [0.1.0](https://github.com/davidedomini/ProFed/compare/v0.0.1...0.1.0) (2025-01-27)

### Features

* add empty download dataset method ([3bfd498](https://github.com/davidedomini/ProFed/commit/3bfd498214f899601b666f57743a44f2c838aa42))
* add empty hard non-iid mapping method ([befe084](https://github.com/davidedomini/ProFed/commit/befe084f9929eb8984916ea815f2438af0251009))
* add empty partition method ([96abb8f](https://github.com/davidedomini/ProFed/commit/96abb8fc63d6d52518dbb809b93988671ec2d126))
* add poetry build to workflow ([1d486c9](https://github.com/davidedomini/ProFed/commit/1d486c92a09c472bee4e1a81a0358b29984ed9ab))
* define the base API ([4438d00](https://github.com/davidedomini/ProFed/commit/4438d0012a651e41b949c6871e3ef41cb1788ad8))
* implement dataset download ([740a2f4](https://github.com/davidedomini/ProFed/commit/740a2f44e3dc627f98f5c607d9e0d59fdd874cb7))
* implement dirichlet ([2ca7b85](https://github.com/davidedomini/ProFed/commit/2ca7b85a22ea412611fd27e6ae5a9e5089ee2d42))
* implement hard and iid ([7226f66](https://github.com/davidedomini/ProFed/commit/7226f663641a22d2be1e302a897cb85e41a73fb5))
* implement train val split ([b52f385](https://github.com/davidedomini/ProFed/commit/b52f385d40ee36bb8b076064fc6a05b834a8cb41))

### Bug Fixes

* add where to take the version number ([d996e87](https://github.com/davidedomini/ProFed/commit/d996e87138d4904d2aa5120e5fd13ed8dadd7479))
* remove white space from ci ([09e1b84](https://github.com/davidedomini/ProFed/commit/09e1b8478c159a60265ff5d5b1300986d274f5b6))

### Build and continuous integration

* configure semantic release to automatically release on gh and pypi ([75e1452](https://github.com/davidedomini/ProFed/commit/75e14525089ca8e2497f31c7974efab238de3cd6))
* remove github user config commands ([8b4bba4](https://github.com/davidedomini/ProFed/commit/8b4bba494a78e03807db5cd9410c59d032d348da))
* remove poetry build ([afdd2e7](https://github.com/davidedomini/ProFed/commit/afdd2e738280e804a11303de0f2d824c1b2d9974))
* switch python 3.10 to 3.12 ([72b92d0](https://github.com/davidedomini/ProFed/commit/72b92d05efa7e23b0a8213a2502a21ae6d018e63))

### General maintenance

* add gitignore ([4b711e8](https://github.com/davidedomini/ProFed/commit/4b711e8d8d8452a971c84252ecf7adf8028b5cc4))
* add MIT license ([6b0c10f](https://github.com/davidedomini/ProFed/commit/6b0c10fab064f8faba0fcb4b30c068835059a858))
* better readme ([c3dbca7](https://github.com/davidedomini/ProFed/commit/c3dbca7b6a73059e7b476e697db12cc87ffb7c9f))
* update gitignore ([48e5e68](https://github.com/davidedomini/ProFed/commit/48e5e6881f78fec9a68d1b747a91a4cd3481ade2))

# Changelog
