# Changelog

Every noteable change is logged here.

## v2.15.2 (2022-10-16)

### Chore

* convert nightly to all (63927dd0cea1)
* upgrade baw (08bc016d1a0f)
* upgrade requirements.txt (61ab9a154c09)

## v2.15.1 (2022-10-06)

### Chore

* root is not required (1bf8c1593991)
* upgrade requirements.txt (ad884e2ef454)

## v2.15.0 (2022-10-03)

### Chore

* add Jenkinsfile (eb1e7afc1181)

## v2.14.4

### Feature

* raise ValueError if invalid ProcessState is given (84e9a7b07185)

### Fix

* do not fail on invalid state (0507c24bebf4)

## v2.14.3

### Feature

* add documentid access (bdef13d7c658)

### Fix

* add missing deleted step (11d34456cec6)
* fix path check (a087d9069e05)

## v2.14.2

### Fix

* do not fail on missing job info (d1d57a764f33)
* do not convert invalid state (fc32be4c7cac)
* add missing pdf resource (19bd9dbce7da)
* skip todo documents correctly (07652ea5283f)
* align test data to internal data structure (8c91030596ab)
* remove duplicated logging (af3502119d31)

## v2.14.1

### Feature

* add done flag (797a945379ff)

## v2.14.0

### Feature

* add method to determine job name (54e17d376887)
* move load documents from viewo project (a2057bf5f409)

### Documentation

* adjust modules path (46aa127f1aee)

## v2.13.0

### Feature

* add option to write debug as pip compatible (8f41fb2ea5b0)
* run debug in sorted order (7d4f74cc7c68)

### Documentation

* Happy New Year! (acba4d904c22)

## v2.12.1

### Fix

* use optimized findings (7b6e6f24ddef)

## v2.12.0

### Feature

* add parameter to shrink published findings (55c279bc8662)
* add flag to control failing behavior (034a4b9d3521)

### Documentation

* fix file name (bcca46c4200a)

## v2.11.1

### Fix

* add NOT SUPPORTED to raw state converter (7aa2df8cffab)

## v2.11.0

### Feature

* add method to signal that document type is not supported (8fb5f8e0b6d6)

## v2.10.0

### Feature

* add method to remove long pending jobs (bce9f5e5ac4a)
* add method to publish run statistics (116953fe9934)
* add method to write debug information (354b1fc5f5ea)

## v2.9.3

### Feature

* add option to automatically detect if document is done (6345aefb047c)

## v2.9.2

### Fix

* determine state for raw jobinfo loader (e9588eb61207)

## v2.9.1

### Feature

* add optional done selector (ddff7fb6457f)

## v2.9.0

### Feature

* add method to load raw job information (d14144c2092e)
* add method to load load pdfinfo from documentid (bccc84927685)
* add parameter to remove password (24796fc0e9aa)
* add option to convert to json (dbf46d33d09f)
* add Jobs-List datatype (7d435ee72cb7)
* add optional done flag (ac46e966f724)

### Fix

* add missing renaming (fb70697743d6)

## v2.8.0

### Feature

* add method to update bookkeeping (73ff16ec4460)
* clarify job file name (0ef65f629d4c)
* change from json to yaml (2bf8036cc6d7)
* update done flag while publishing document (59554d3eed84)
* add method to write job info (496ad67c5e39)

## v2.7.0

### Feature

* add method to check if document is private (f844eb8971b1)

## v2.6.0

### Feature

* encrypt private user data (7594a7c4dbfc)

## v2.5.1

### Feature

* add argument to skip coping files (8b50e6a22321)

## v2.5.0

### Feature

* run abel to gather document information (de92491198f5)

## v2.4.1

### Feature

* add default file name (1b14fa77d562)

### Documentation

* make interface more explicit (63644ac8db13)

## v2.4.0

### Feature

* add method to load debug information (52f93815cc3a)

## v2.3.2

### Feature

* add flag to not fail on existing workspace folder (2e32d9b8f622)

### Documentation

* Happy New Year! (65fe069a584c)

## v2.3.1

### Feature

* add method to convert ProcessState to State (3b44a3d6f8ed)
* add option to return raw job representation (a7018810ba90)

## v2.3.0

### Feature

* add state parameter (fdf0706a16a4)
* move enum State from viewo project (7de64cf579b9)

## v2.2.2

### Fix

* skip non existing documents (f1fad7bfd338)

## v2.2.1

### Fix

* return invalid progress if file does not exists (cbe265a52f20)

## v2.2.0

### Feature

* add Error state to current (72a12fe78d0e)
* add method to check fail state and add fail state (25345a460167)

## v2.1.1

### Feature

* add inprogressed method (bba413b888c3)
* add deleted method (a53350277f50)

## v2.1.0

### Feature

* add progress step update method (30fc6581f040)
* add method to update progress and determine progress (8084a098edb2)

## v2.0.5

### Feature

* add todopath to bypass configo for testing purpose (7a1ff925b628)

### Documentation

* fix spelling error (2f8d0b1caeab)

## v2.0.4

## v2.0.3

## v2.0.2

## v2.0.1

## v2.0.0

### Feature

* add post init hook to verify data type (0eee941cb80d)
* use str to describe job index (c74677c92c1f)
* add owner parameter to todo creator (b31e29d81de6)
* add multiple owner (2ffd6fe1cd71)
* add owner parameter to filter loading (1f828c48b8cd)
* add job owner (493262aaa1ef)

## v1.4.1

### Fix

* fix level compare (fb0d9bb37e6c)

## v1.4.0

### Feature

* enable sink and source as equal folder (331eacf3c441)
* add option to control copying of optimized findings (41899024d43a)
* adjust logging policy (20bb96e7601c)

## v1.3.2

## v1.3.1

### Fix

* replace loader cause grouped loader expect optimized format (2722deaa889f)

## v1.3.0

### Feature

* publish optimized findings separately (90f4e121ec3d)
* add link to optimized finding path (e9b597ae6fac)

## v1.2.3

## v1.2.2

## v1.2.1

## v1.2.0

### Feature

* handle more cases of to delete a document (1d8348c6eeb6)
* add done flag to select result view type (bb74701de166)
* add method document to access document resource folder by id (129c8140269b)
* add constant to define width of random job id (e3d0f1537549)

## v1.1.1

## v1.1.0

### Feature

* return None if process does not exists (9e0bb9443888)

### Fix

* do not log that path does not exists (9b4986a6bb25)

## v1.0.4

## v1.0.3

## v1.0.2

## v1.0.1

## v1.0.0

### Feature

* add count of findings to publish step (f5b4e423c298)
* extend public API (7ff3fc3ea470)
* clarify code and drop support for simple status (f9ea27a233be)
* divide dumping and writing process of job information (e027dd0af474)

### Documentation

* update module description (dce0c4e6a984)

## v0.4.19

## v0.4.18

## v0.4.17

## v0.4.16

## v0.4.15

## v0.4.14

## v0.4.13

### Documentation

* add copyright header (b314d345f3d3)

## v0.4.12

## v0.4.11

## v0.4.10

### Feature

* log non existing todo (c650b2ce9360)

## v0.4.9

## v0.4.8

## v0.4.7

## v0.4.6

## v0.4.5

## v0.4.4

## v0.4.3

### Fix

* fix path to write `deleted` mark (52eebcb9d8af)

## v0.4.2

### Feature

* add method to skip removed extracted documents (bcd84017d0e7)

### Fix

* convert old style datatype to new FindingStatus (1ec9e8812c52)

### Documentation

* fix interface documentation (2d5f0238c7fa)

## v0.4.1

### Feature

* add method `delete` to set deleting folder flag (d109666b81bb)
* add data field password and hashlink (ca2db4455bde)

## v0.4.0

### Feature

* change result field from int to complex user progress datatype (621ca8155cf2)

## v0.3.16

## v0.3.15

## v0.3.14

## v0.3.13

## v0.3.12

## v0.3.11

## v0.3.10

## v0.3.9

## v0.3.8

## v0.3.7

## v0.3.6

## v0.3.5

## v0.3.4

## v0.3.3

### Fix

* add missing recursive flag (a2d910701439)

## v0.3.2

### Feature

* print assertion validation to ease debugging (d0f68f39b62d)

## v0.3.1

### Fix

* remove outdated resources from setup (b1e76198398a)

## v0.3.0

### Feature

* add methods to determine more paths (8ac183c7a458)
* support publish invalid pdf result (2f605eb8486b)
* add state machine to manage document live cycle (c7f3fb6937fc)
* override environment variables instead of creating all (3ba396c75ab9)

### Documentation

* add general doc structure (3f14c42ebd2a)

## v0.2.3

### Feature

* add support for file str path as file source (42867d25199e)

## v0.2.2

### Feature

* add parameter to define where todo folder is located (92cb1b60f47e)

## v0.2.1

## v0.2.0

### Feature

* extend job date with hour and second (3ebf4524a9c6)

## v0.1.13

### Documentation

* Happy New Year! (3f84a46a975e)

## v0.1.12

## v0.1.11

## v0.1.10

## v0.1.9

## v0.1.8

## v0.1.7

## v0.1.6

### Fix

* fix spelling error (63fb2276b407)

### Documentation

* extend basic readme (82c7924b89ef)

## v0.1.5

## v0.1.4

## v0.1.3

### Fix

* disable wrong pylint warnings (bbe933ee7530)

## v0.1.2

### Feature

* add method to count jobs which are ready (50d610e0d6bc)

## v0.1.1

### Feature

* add create_todo and todo_count from viewo (f3700e8461aa)

## v0.1.0

### Feature

* move job loader and scanner from viewo (b237ff130a65)

## v0.0.0 Initial release

