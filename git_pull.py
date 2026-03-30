#!/usr/bin/env python3
"""
简单 Git 拉取脚本 - 支持多远程仓库选择，自动处理冲突和重试
"""

import os
import sys
import subprocess

def run_command(command, show_output=True):
    """执行命令并返回结果"""
    result = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True,
        encoding='utf-8',
        errors='ignore'
    )

    if show_output and result.stdout:
        print(result.stdout)

    if show_output and result.stderr and result.returncode != 0:
        print(f"错误: {result.stderr}")

    return result

def select_remote():
    """列出所有远程仓库，让用户选择，返回选中的远程名"""
    result = run_command("git remote", show_output=False)
    remotes = [r.strip() for r in result.stdout.strip().split('\n') if r.strip()]
    
    if not remotes:
        print("❌ 没有配置任何远程仓库")
        return None
    
    if len(remotes) == 1:
        print(f"使用唯一的远程仓库: {remotes[0]}")
        return remotes[0]
    
    print("\n检测到多个远程仓库：")
    for i, remote in enumerate(remotes, 1):
        print(f"  {i}) {remote}")
    
    while True:
        choice = input(f"请选择要拉取的远程 (1-{len(remotes)}): ").strip()
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(remotes):
                return remotes[idx]
            else:
                print(f"无效选择，请输入 1 到 {len(remotes)} 之间的数字")
        except ValueError:
            print("输入无效，请输入数字")

def retry_pull(remote, branch, max_retries=3):
    """重试拉取功能，处理冲突和临时问题"""
    retry_count = 0

    while retry_count < max_retries:
        if retry_count > 0:
            print(f"\n第 {retry_count + 1} 次重试拉取...")

        # 尝试拉取
        print(f"正在从远程 {remote} 分支 {branch} 拉取...")
        result = run_command(f"git pull {remote} {branch}", show_output=True)

        if result.returncode == 0:
            print("✅ 拉取成功!")
            return True

        # 拉取失败，询问用户如何处理
        print(f"\n❌ 拉取失败，错误信息: {result.stderr.strip()}")

        # 检查是否有冲突
        if "CONFLICT" in result.stderr or "merge conflict" in result.stderr:
            print("\n⚠️ 检测到合并冲突！")
            print("请手动解决冲突，然后执行 'git add' 和 'git commit' 完成合并。")
            print("你也可以选择：")
            print("  1) 放弃本次拉取（git merge --abort）")
            print("  2) 使用远程版本覆盖本地（git reset --hard {}/{}）".format(remote, branch))
            choice = input("\n请选择 (1/2): ").strip()
            if choice == '1':
                run_command("git merge --abort", show_output=False)
                print("已放弃拉取，本地工作区恢复原状。")
                return False
            elif choice == '2':
                confirm = input(f"⚠️ 这将丢弃所有本地未提交的更改，确定覆盖吗？(y/N): ").strip().lower()
                if confirm == 'y':
                    run_command(f"git reset --hard {remote}/{branch}")
                    print("本地已强制同步到远程版本。")
                    return True
                else:
                    return False
            else:
                print("无效选择，放弃拉取。")
                return False

        # 非冲突错误，重试或让用户选择
        if retry_count < max_retries - 1:
            print("\n请选择操作:")
            print("  1) 再次尝试拉取")
            print("  2) 强制拉取（丢弃本地更改，谨慎使用）")
            print("  3) 跳过本次拉取")

            choice = input("\n请选择 (1/2/3): ").strip()

            if choice == '1':
                retry_count += 1
                continue
            elif choice == '2':
                confirm = input("⚠️ 强制拉取将丢弃本地未提交的更改，确定继续吗？(y/N): ").strip().lower()
                if confirm == 'y':
                    force_result = run_command(f"git fetch {remote} && git reset --hard {remote}/{branch}")
                    if force_result.returncode == 0:
                        print("✅ 强制拉取成功，本地已同步到远程版本。")
                        return True
                    else:
                        print("❌ 强制拉取失败")
                return False
            elif choice == '3':
                print("跳过拉取")
                return False
            else:
                print("无效选择，跳过拉取")
                return False
        else:
            retry_count += 1

    print(f"\n⚠️ 经过 {max_retries} 次尝试后拉取仍然失败")
    print("请手动检查并解决以下问题:")
    print("  1. 检查网络连接")
    print("  2. 检查远程仓库是否存在且权限正确")
    print("  3. 使用 'git status' 查看本地状态")
    print("  4. 尝试 'git fetch' 单独拉取远程数据")
    return False

def pull_from_remote(remote):
    """从指定的远程仓库拉取，包含重试机制和冲突处理"""
    # 获取当前分支
    branch_result = run_command("git branch --show-current", show_output=False)
    branch = branch_result.stdout.strip()
    if not branch:
        print("⚠️ 无法确定当前分支，使用默认分支 'main'")
        branch = "main"

    print(f"当前分支: {branch}")

    # 检查本地是否有未提交的更改
    status_result = run_command("git status --porcelain", show_output=False)
    if status_result.stdout.strip():
        print("\n⚠️ 检测到本地有未提交的更改")
        print("请选择操作:")
        print("  1) 暂存更改后拉取 (git stash)")
        print("  2) 提交更改后再拉取")
        print("  3) 放弃本地更改，直接拉取 (git reset --hard)")
        print("  4) 取消拉取")
        choice = input("\n请选择 (1/2/3/4): ").strip()

        if choice == '1':
            run_command("git stash")
            print("本地更改已暂存。")
        elif choice == '2':
            print("请先使用 commit 脚本提交更改，或手动提交后再运行此脚本。")
            return False
        elif choice == '3':
            confirm = input("⚠️ 这将永久删除所有未提交的更改，确定吗？(y/N): ").strip().lower()
            if confirm == 'y':
                run_command("git reset --hard")
                print("本地未提交更改已丢弃。")
            else:
                return False
        elif choice == '4':
            print("取消拉取")
            return False
        else:
            print("无效选择，取消拉取")
            return False

    # 执行拉取（带重试机制）
    return retry_pull(remote, branch)

def run_simple_pull():
    """运行简单的 Git 拉取流程"""
    print("=" * 50)
    print("Git 拉取助手")
    print("=" * 50)

    # 1. 检查远程仓库
    print("\n1. 检查远程仓库...")
    remote_result = run_command("git remote -v", show_output=True)
    if not remote_result.stdout.strip():
        print("⚠️ 未配置远程仓库")
        add_remote = input("是否添加远程仓库? (y/N): ").strip().lower()
        if add_remote == 'y':
            url = input("请输入远程仓库URL: ").strip()
            name = input("请输入远程仓库名称 (默认为 origin): ").strip()
            if not name:
                name = "origin"
            if url:
                run_command(f"git remote add {name} {url}")
                print(f"✅ 远程仓库 {name} 已添加")
            else:
                print("❌ 未提供URL，退出")
                return
        else:
            return

    # 2. 获取远程分支信息
    print("\n2. 获取远程分支信息...")
    run_command("git fetch --all")

    # 3. 选择远程仓库（只选一次）
    remote = select_remote()
    if not remote:
        return

    # 4. 显示差异
    branch_result = run_command("git branch --show-current", show_output=False)
    branch = branch_result.stdout.strip()
    if not branch:
        branch = "main"

    print(f"\n当前分支: {branch}")
    print(f"对比远程: {remote}/{branch}")
    print("\n本地与远程的差异:")
    run_command(f"git log {branch}..{remote}/{branch} --oneline", show_output=True)

    # 5. 询问是否拉取
    print("\n3. 是否从远程拉取最新代码?")
    pull_choice = input("拉取? (y/N): ").strip().lower()

    if pull_choice == 'y':
        pull_from_remote(remote)   # 传入已选择的远程名
    else:
        print("跳过拉取")

    print("\n✅ 操作完成!")

def setup_encoding():
    """设置 Git 编码配置（避免中文乱码）"""
    print("正在设置 Git 编码配置...")
    configs = [
        ('core.quotepath', 'false'),
        ('i18n.commitencoding', 'utf-8'),
        ('i18n.logoutputencoding', 'utf-8'),
    ]
    for key, value in configs:
        run_command(f'git config --global {key} {value}', show_output=False)
    print("编码配置完成!")

def check_git_installed():
    """检查 Git 是否已安装"""
    result = run_command("git --version", show_output=False)
    return result.returncode == 0

if __name__ == "__main__":
    # 检查 Git 是否安装
    if not check_git_installed():
        print("❌ Git 未安装或不在 PATH 中")
        print("请先安装 Git: https://git-scm.com/")
        sys.exit(1)

    # 检查是否在 Git 仓库中
    if not os.path.exists(".git"):
        print("⚠️ 当前目录不是 Git 仓库")
        init_choice = input("是否初始化 Git 仓库? (y/N): ").strip().lower()
        if init_choice == 'y':
            run_command("git init")
            print("✅ Git 仓库已初始化，但还没有远程仓库，请手动配置。")
            sys.exit(0)
        else:
            print("请在 Git 仓库中运行此脚本")
            sys.exit(1)

    # 如果带有 --setup 参数，仅设置编码
    if len(sys.argv) > 1 and sys.argv[1] == '--setup':
        setup_encoding()
    else:
        run_simple_pull()