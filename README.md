# THE IDOLM@STER（Xbox 360）存档研究

对象：THE IDOLM@STER，Xbox 360 版，Title ID `4E4D07DB`。
目的：修改胜率、补全配饰，以及为真机（RGH）解锁成就准备存档。验证环境为 Xenia Canary 和 Horizon。

## 已确认

- **存档包与校验**：存档包是 STFS `CON `，里面的 `gamedata` 前 2 字节是 CRC-16/CCITT-FALSE（计算范围 0x10 到末尾）。可以原位写回存档包，再用 Horizon 做 Rehash + Resign。
- **试镜胜率**：制作人 PEVA 的 [0] 是试镜次数，[1] 是合格次数，把 [1] 改成等于 [0] 即为 100%。真机和模拟器都已验证。
- **战绩栏**：每个 Unit 只保留最近 5 场试镜，新的在前，旧的会被挤掉，不留痕迹。
- **制作人名**：UTF-16BE，最多 8 个字，存档里有两处（0x80、0xB460）。改名工具已写好，但改名后的存档还没进游戏测试过。
- **配饰/衣装**：ID 与部位、DLC 的对应已经和官方 12 期目录、攻略站核对过。存档容量 246 条，正好是全部有效 ID：配饰 189 件，衣装 57 件。补满后剩下的"？"是从未发行的预留格。
- **成就**：奖杯在存档里的位置和顺序已确认；成就在事件点发放，清空奖杯记录后会重新发放。10 个成就都在模拟器上拿到过。
- **Unit 槽**：可以整块复制到空槽，改偶像 ID 和名字后能正常列出、推进和存档；前提是把"Unit 数"（0x39D0D0）一起改。
- **default.xex**：已解密解压，存档标签字符串和部分读写函数已定位。

详细内容：

- [docs/gamedata-format.md](docs/gamedata-format.md)：偏移表、PEVA、偶像 ID、Unit 槽
- [docs/accessories.md](docs/accessories.md)：配饰/衣装 ID 表、DLC 核对、剩余"？"
- [docs/achievements.md](docs/achievements.md)：奖杯顺序和触发方式
- [docs/xex-notes.md](docs/xex-notes.md)：xex 解包与函数位置

## 未确认 / 未完成

- 一体化成就解锁存档 [saves/achievement-set](saves/achievement-set/) 还没有测试。
- 10アイドル、16ソング、4シーズン、真アイドルマスター 的确切触发节点没有记录。
- Unit 槽里周数、等级等推进字段没有逐个解出来。
- PEVA 部分下标的含义只是推测。
- TU 补丁没有分析。

## 工具

需要 Python 3；`xex_decrypt.py` 另外需要 `cryptography`。

```
python3 tools/gamedata.py info gamedata                    # 查看摘要
python3 tools/gamedata.py winrate100 gamedata out          # 胜率 100%（制作人和各 Unit）
python3 tools/gamedata.py rename gamedata out アイマス      # 改制作人名
python3 tools/gamedata.py fixcrc gamedata                  # 只重算 CRC
python3 tools/stfs_gamedata.py extract 存档包 gamedata      # 从真机存档包取出
python3 tools/stfs_gamedata.py inject 存档包 gamedata 输出包 # 原位写回，之后在 Horizon 里 Rehash + Resign
python3 tools/xex_decrypt.py default.xex default.pe --key <零售 XEX 密钥>
```

改存档前请先备份。本仓库不包含游戏本体文件和密钥。
