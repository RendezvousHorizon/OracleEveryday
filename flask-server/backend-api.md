### 天天甲骨文服务端API

#### 1.注册和登录

**(1) 注册**

* url: ```http://ip_addr:port/auth/register?username=xxx&password=xxx```
* 参数：username和password
* method: POST
* 返回值：
    * 'success'--成功
  * 'Username is required'--失败，username为空
  * 'Password is required'--失败，password为空
  * 'User xxx is already registered'--失败，用户已被注册

```java
//Java Unirest的代码示例
Unirest.setTimeouts(0, 0);
HttpResponse<String> response = Unirest.post("http://127.0.0.1:5000/auth/register?username=xxx&password=xxx")
  .multiPartContent()
  .asString();
```



**(2)登录**

* url: ```http://ip_addr:port/auth/login?username=xxx&password=xxx```
* 参数：username和password
* method: POST
* 返回值：

  * 'success'--成功
  * 'Incorrect username or password.'--失败

**(3)登出**

* url: ```http://ip_addr:port/auth/logout```
* 参数：无
* method: GET
* 返回值：'success'

#### 2. 甲骨文识别

* url: ```http:ip_addr:port/oracle_recognition```

* 参数

  * image: 一张图片
  * method: GET
  * 返回值：
    * 一个长为4的json列表，每个元素为(name, image)二元组，name为预测出的候选汉字，image为此汉字对应甲骨文图片的base64编码。

  ```java
  // Java--Unirest的代码示例
  Unirest.setTimeouts(0, 0);
  HttpResponse<String> response = Unirest.get("http://127.0.0.1:5000/oracle_recognition")
    .field("image", new File("path/to/image"))
    .asString();
  ```

#### 3.甲骨文检索

* url: ```http:ip_addr:port/oracle_search```
* 参数
  * name：一个汉字字符
* method: GET
* 返回值
  * 成功时：一张图片(mimetype='image/jpeg')。
  * 失败时：404 not found

#### 4. 甲骨文识记

**(1)获取题目**

* 需要先登录

* url: ```http:ip_addr:port/question```

* 参数： 无

* method: GET

* 返回值
  * 一个json格式的题目列表，每个题目是一个字典，key为 (id, image, a, b, c, d), 其中a为正确答案。

     (id是题目id， 可以用来上传错题)。

**(2)上传错题**

* 需要先登录

* url: ```http:ip_addr:port/wrong_question```

* method: POST

* 参数：
  * 	question_id:错题的id

  (用户信息存储在http session的cookie中,请求时不需要显式指明)。

* 返回值

  * 上传成功: 'success'

**(3)设置每次的做题数**

* 需要先登录
* url: ```http:ip_addr:port/num_questions```
* method: GET, POST
* 参数: GET没有，POST有一个参数
  * num_questions: 用户单次做题数目。
* 返回值:
  * GET: int num_questions
  * POST: 'success'

**(3)设置下一次做题开始的题目id**

* 需要先登录
  * url: ```http:ip_addr:port/next_question_id```
* method: GET, POST
* 参数: GET没有，POST有一个参数
  * next_question_id: 下一次开始时的。
* 返回值:
  * GET: int next_question_id
  * POST: 'success'