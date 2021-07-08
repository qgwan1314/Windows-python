## 测试文档

### 接口描述

这是文档描述信息

### 请求说明

#### HTTP方法：POST

#### URL：/api/logins/phone_login

#### URL 参数

| 字段 | 必选 | 类型 | 说明 |
| ---- | ---- | ---- | ---- |
| 无   |      |      |      |

#### Header

| 参数            | 值               | 说明                  |
| --------------- | :--------------- | --------------------- |
| Content-Type    | application/json | 数据格式              |
| Accept-Language | zh-CN            | 系统语言：zh-CN 或 en |

#### 请求参数

| 字段     | 必选 | 类型 | 说明       |
| -------- | ---- | ---- | ---------- |
| tel_num  | 是   | int  | 手机号     |
| tel_code | 是   | int  | 手机验证码 |

#### 请求示例

```json
# POST /api/logins/phone_login

{

}
```

### 返回说明

#### 返回参数

| 字段              | 必选 | 类型       | 说明                                |
| ----------------- | ---- | ---------- | ----------------------------------- |
| code              | 是   | int        | 状态码                              |
| msg               | 是   | string     | 状态详情                            |

#### 返回示例

```json
{
   
    "code": 200,
    "msg": "OK"
}
```

### 异常说明

| 状态码（code） | 状态详情（msg）                                              | 说明         |
| -------------- | ------------------------------------------------------------ | ------------ |
| 400            | Parameter Error.                                             | 参数不正确   |
| 400            | JSON parse error - Expecting property name enclosed in double quotes: line 4 column 1 (char 57) | 数据格式错误 |
