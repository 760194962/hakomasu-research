# default.xex 笔记

- XEX2，零售加密（AES-128：用零售 XEX 密钥解出 secinfo+0x150 处的文件密钥，再对 0x3000 起的 PE 数据做 CBC、IV 为 0），basic 压缩（(数据长度, 补零长度) 列表）。工具：`tools/xex_decrypt.py`，需要自行提供密钥。
- 镜像基址 0x82000000，.text RVA 0xE0000（大小 0x3A9B44），.rdata 0x400，.data 0x490000。
- 存档标签字符串（VA）：`ACDT TAG` 0x8203023C，`IDOL TAG` 0x82031D94，`MAILDATA` 0x82031E28，`PRODUCER` 0x82032C0C，`PEVA TAG` 0x820338D0，`PROD TAG` 0x82033A80，`PTRP TAG` 0x82033B9C，`REP SUB ` 0x82033BCC，`SYSTEM  ` 0x82033F3C，`UNIT    ` 0x82035978，`UNIT TAG` 0x82035ED8，`WORLD   ` 0x82036328，`gamedata` 0x820046FC，`savedata` 0x820046F0。
- 各记录类的构造函数都调用 0x8222DC50(标签, 版本号) 注册，例如 PROD TAG 在 0x82239A18，UNIT 在 0x8224A298，UNIT TAG 在 0x8224E7D8。
- UNIT 的反序列化函数在 0x8224A580：依次读入 UNIT TAG、REPO、PEVA、一个 6 元素数组、SONG，再读一个 0x38 字节结构、0xC 字节和 0x10 字节。
- 默认名字（"ナムコエンジェル"、制作人名）不在 xex 里，应在游戏数据文件中。
- 配饰能力值在 xex 里找不到静态表。
- TU（`TU_1A461UH_000000S000000.0000000000087`）还没有分析。
