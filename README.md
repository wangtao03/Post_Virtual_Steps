# Post Virtual Steps 发送虚拟步数

利用 Github Actions 定时发送虚拟步数，以完成每日云端运动会达标

## 使用方法

### 1、fork 本仓库

### 2、设置用户 Token 和 设备信息

**依次点击 Settings → Secrets → Actions → New repository secret**

数据说明：

| Name      | Value                                                                           | 说明          |
|-----------|---------------------------------------------------------------------------------|-------------|
| USERS     | [{"name": "用户1", "token": "令牌1"},<br/>{"name": "用户2", "token": "令牌2"},<br/>...] | 存储用户令牌字典的数组 |
| BRAND     | vivo                                                                            | 设备厂商        |
| MODEL     | v2024A                                                                          | 设备型号        |
| VERSION   | Android10                                                                       | 系统版本        |
| DEVICE_ID | 4savkqbzn7hf59lt28do6gwpe1j3m0xi                                                | 设备序号        |

### 3、启用 Acitons
手动启用GitHub Actions，Star项目即可

每日8点、14点会自动运行一次

在Actions → All workflows → ... → build → Post Steps 查看结果。
