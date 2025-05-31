#!/bin/bash
#new Env('codek-美团币');
# 首次运行会在运行目录下创建mtconfig.ini配置文件，按格式填写：
# #mt_token = token#uuid 例如：mt_token = Agxxxxx@0000xxxxxxxx 必须
# #mtgsig_server = https://xxx.xxx.xxx/api/mtgsig 可空
# #mtgsig_token = xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx 必须
# #mtgsig_ip = x.x.x.x 可空 (优选cloudflare的IP)
# 一天运行2遍即可！青龙的自己定时1天2次 如：30 9,10 * * *
#pwd
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
rm -r $FILE
# 检查文件是否存在
# Github代理镜像，下载不动，或者出错自行替换！
# https://ghfast.top/
# https://gh-proxy.com/
# https://ghproxy.cfd/
# https://ghproxy.net/
# 
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