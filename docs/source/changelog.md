## Changelog

### Version 3.5.0

**Date:** April 23, 2025

* #3209 解决MySQL连接不释放问题  
* #3095 修复中继在未勾选启用注册时，无法控制注册状态  
* #3199 Customer Data Custom Items [Value Width][Column Width] are not reflected.  
* #3065 BSL队列无可用坐席溢出  
* #3165 about User Management > User List screen does not sort correctly.  
* #1020 销售漏斗页面顶部的客户包下拉框增加缓存功能，页面刷新即可重置。调整客户弹屏上销售漏斗按分值倒序显示。  
* #3176 Regarding the list of customers assigned to the group dialer.  
* #3140 邮件模版页面选择任务最多只能显示20个任务。  
* #1030 about After registering to "Weekly" in "Conditions".  
* #1014 about When creating a FAQ, I want it to appear as "expired".  
* #1043 about display of filtering condition.  
* #953 客户数据, 数据表中添加总呼叫次数列。  
* #1081 Search words change after call.  
* #1067 on customer page on “my profile“, if a call gets connected, page item move to the “customer > customers“ and the system goes slow.  
* #1016 页面数据列表搜索下拉框宽度自动适应  
* #3148 点击拨号盘然后点击tab，最后一次切换页面只能切换一半。  
* #3174 Customer > Customize field > tools > Fields Sort  
* #1027 about User Management > User List screen does not sort correctly  
* #935 调整时间插件兼容日文全半角输入法。  
* #3137 修复节点管理菜单偏移问题。  
* #1026 about The time in the "Last dial time" in the general tab is wrong.  
* #1029 about Call Profile > Replace Calling Number > When editing  
* #1427 20230705_KK_03 FAQ shows pending review counts for users without verification privileges.  
* #3126 在坐席事件页面，选择搜索条件之后，取消页面所有标题的显示，然后进行导出，会导致taskcc进程卡住。  
* #3156 You can operate the items of the authority you are using.  
* #3150 避免振铃组中设置重复号码时会同时呼叫相同的号码  
* #858 改进预拨号页面只显示启用状态的任务  
* #3117 当转接到外线时，不应该统计到外呼数量和时长相关  
* #3107 「Reseller」 The date, domain, and version displayed in the lower right corner of the screen does not change from the root name.  
* #3106 导入数据时会上传一个文件，但是这个导入任务被另一台机器执行了，就会导致提示错误，并且没有正确回更任务的结束状态.  
* #849 修复客户数据页面多一个客户标签参数，以及点击重置会增加客户标签参数问题   
* #3101 root级别如果建立两个一样名称的数据来源，登录代理商建立client时，会提示数据重复不能建立。  
* #3097 解决预拨号放音收号，被叫主动挂机时cdr未记录用户输入   
* #2938 解决内线咨询转状态及连续咨询转状态问题  
* #3083 修复当坐席的关联redis数据不存在时，删除坐席数据，会造成服务端异常报错.  
* #3070 客户数据批量上传时，如果自定义字段中有关联字段选项，上传后会显示undefined  
* #3051 修复凌晨1点执行的设置redis过期脚本，会将符合20开头6位或者8位的坐席或者坐席组相关的redis进行错误设置bug，导致36小时后不可用  
* #3066 saas dev:自定义字段选择号码，添加客户数据之后，再编辑，号码字段会限制只允许添加15位以内的数字，但是编辑后如果超出15位点击保存，不会显示参数错误，会显示号码重复的提示。  
* #3063 Bug in the lower right-hand corner when logging in to the WCC PRD environment as root  
* #3058 Questions about Group Dialer [Customer Response Time  
* #3057 通话记录页面，搜索框无效  
* #3056 Deleted from the “Maximum number of outgoing calls” setting item in the Campaign Details settings.  
* #3018 调慢网页网速后，todo的时间插件不会显示。如果填写了内容再删除，点击保存会有报错提示。  
* #1848 删除坐席增加释放该坐席的客户和客户预约所属坐席，修复坐席没有任务坐席组登陆后报错问题。  
* #3024 client呼叫，填写了两个内线号码，提示成功显示undefined  
* #2891 解决内线转外线再转内线失败  
* #2975 Large images do not reach the other party in messages    
* #3001 有节点离线时，保存中继会出现超时错误  
* #3020 The [Memo] of the survey is not displayed.  
* #2990 In the settings under “Roles and Permissions, Monitoring Management>Monitoring>Edit” in the settings under ‘Roles and Permissions’, This “Edit” seems to be unnecessary.  
* #2979 Client Adjustment of the wording of the display on the dashboard  
* #2968 Failure to transfer responsibility after park hold and release after outgoing call  
* #2963 client顶部添加多个工具，放大镜搜索的位置和下拉菜单会错位  
* #2941 工单状态建立后，选择的坐席组被删除后，会有一个空格  
* 支持wss客户端的re-invite hold  
* 登录接口返回值添加outboundProxy  
* 添加联系人更新接口返回新数据  
* 坐席-联系客户页面，搜索号码时，可以使用横杠搜索。  
* 多语言修正及补充。  
* 增加通话测试代码。  
* 修复节点保存时，服务端报错提示  
* 外部联系人姓名分类支持片假名  
* 添加驻留可用查询接口  
* 通讯录接口添加按日文排序  
