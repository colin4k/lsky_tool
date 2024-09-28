# lsky_tool
LSky 图床增强工具

## 说明
- 本工具主要用于清理LSky图床中冗余 的图片，判断的标准是该图片是否在 Obsidian 笔记中使用。
- 在使用本工具前需要先获取 LSky 的 token，然后在环境变量中设置
    - 命令行执行以下命令获取 LSky 的 token：
    ```bash
    curl "http://127.0.0.1:9080/api/v1/tokens"  -H 'Accept: application/json' -d 'email=[your email]&password=[your password]'
    ```
    其中 `[your email]` 和 `[your password]` 分别改成你的 LSky 用户的邮箱和密码
    - 将 token 写入环境变量
    以下是 MacOS 下 ZSH 的写法，其他操作系统自行修改。`[token]`部分修改成上面获取的 LSky 的 token。
    ```bash
    echo 'export LSKY_AUTHORIZATION=[token]'>>~/.zshrc
    ```
- 本工具主要使用 LSky 官方提供的 API 获取图片清单、查询图片的 Key，并利用 Key 调用 API 进行删除操作。
- 工具第一次执行时会自动在当前目录下生成 search_del_progress.json 文件用于记录当前进度，如程序中断再次启动时，会自动读取该文件中记录的页数。
- 由于删除过程中会导致页数发生变化，这个无法避免，因此建议在第一次处理完成后，可以删除 search_del_progress.json 文件或者修改其中记录的页数，然后重新执行。
