#!/bin/bash
# 获取系统架构
ARCH=$(uname -m)
# 处理不同架构名称
case "$ARCH" in
    "x86_64") ARCH_TYPE="amd64" ;;
    "aarch64") ARCH_TYPE="arm64" ;;
    "armv7l") ARCH_TYPE="arm" ;;
    *) echo "未知架构: $ARCH"; exit 1 ;;
esac
# 生成文件名
FILE="mtb_$ARCH_TYPE"
# 删除文件重新下载保存更新，不需要可以注释！
#rm -r $FILE
# 检查文件是否存在
if [ ! -f "$PWD/$FILE" ]; then
    echo "文件 $FILE 不存在，正在下载..."
    # 下载文件
    URL="https://ghfast.top/https://raw.githubusercontent.com/Code-KKK/pycode/refs/heads/main/mt/$FILE"
    curl -sS -o "$PWD/$FILE" --create-dirs "$URL"
    # 下载失败处理
    if [ $? -ne 0 ]; then
        echo "下载失败，请检查 URL 是否正确: $URL"
        exit 1
    fi
    echo "下载完成。"
fi
# 赋予执行权限
chmod +x "$PWD/$FILE"
# 运行文件，并直接回显输出
echo "正在执行 $FILE..."
"$PWD/$FILE"