# Local Password Manager

A local password manager, small but useful.

# 支持功能

- [x] 新增密码表
- [ ] 删除密码表（还有一点问题）

- [x] 新增密码
- [x] 删除单个或多个密码
- [x] 更新密码
- [x] 根据关键词查询密码
- [x] 切换密码表

# 功能介绍

**整体界面：**

<img src="./screenshots/window_1.png" alt="window_1" style="zoom:83%;" />

<img src="./screenshots/window_2.png" alt="window_2" style="zoom:83%;" />

## 新增密码表

![1](./screenshots/1.gif)

## 删除密码表

![2](./screenshots/2.gif)

## 新增密码

在空白处或者表格单元格右键选择`Add Row`弹出`新增密码`的窗口。

![3](./screenshots/3.gif)

## 删除密码

可以删除单行或者多行密码。

![4](./screenshots/4.gif)

## 更新密码

选中一个单元格，通过`F2`或`回车`键进入编辑。

![5](./screenshots/5.gif)

## 关键词查询

![6](./screenshots/6.gif)

## 切换密码表

可通过下拉菜单选择其他密码表，或者通过鼠标滚轮滑动实现无缝切换。

![7](./screenshots/7.gif)

## 清空单元格

![8](./screenshots/8.gif)

# 使用须知

如果是用源码，`python`版本最好在`3.7.3`附近，另外需要安装如下库：

* pycryptodome == 3.16.0
* loguru == 0.6.0
* PyQt5 == 5.15.9

# Todo

- [ ] 导入密码表
- [ ] 导出密码表
- [ ] 优化删除密码表的功能
- [ ] 支持生成随机账号和密码
- [ ] 打包源码到exe