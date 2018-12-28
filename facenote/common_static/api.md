## 1. 登录
### 1.1 功能描述
目前只支持微信登录
### 1.2 请求说明
> 请求方式：POST<br>
请求URL ：[www.skinrec.com:33333/login/test](#)

### 1.3 请求参数
| 字段 | 字段类型 | 字段说明             |
| ---- | -------- | -------------------- |
| code | string   | wx.login()->res.code |
### 1.4 返回结果
```json  
{
  "data": {
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwOi8vc2FsZS1hcGkuZGV2L2xvZ2luIiwiaWF0IjoxNDkxNTMyOTI4LCJleHAiOjE0OTIyNTI5MjgsIm5iZiI6MTQ5MTUzMjkyOCwianRpIjoiN1hCUXdwN1FHZmxUdHVVQiIsInV1aWQiOiI1MDZjYWY3MCJ9.FyyXagHtBfDBtMJZPV_hm2q6CVULpY63JPDGDHXc",
    "errcode": "0",
  },
}
```
### 1.5 备注
返回的token存在本地，之后所有的命令，或者需要鉴权的命令携带token在http头部，字段名skinrec_token,服务器会为此token保存一周的有效期，过期后以错误码形式返回，需重新login，可对用户透明，维护登录态的意义主要是因为小程序本身没有cookie，openid等敏感信息本地透明，所以需要第三方token维持登录态，后期如需权限角色或用户增多重构为jwt。

--------------

## ERRCODE
> **所有回包携带errcode字段，非0为业务级别error**

#### 系统级错误

---

| 错误代码 | 返回msg              | 详细描述       |
| -------- | -------------------- | -------------- |
| 400      | 系统错误，请稍候再试 | 请求参数有误   |
| 401      | 系统错误，请稍候再试 | 用户未登录     |
| 404      | 系统错误，请稍候再试 | 资源未找到     |
| 405      | 系统错误，请稍候再试 | 请求方法不支持 |
| 500      | 系统错误，请稍候再试 | 服务器错误     |

#### 业务级错误

---

| 错误代码 | 详细描述  |
| :------: | :-------- |
|    1     | token过期 |