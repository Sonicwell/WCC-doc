## Version 3.6.0

**Date:** July 22, 2025
      
* #3557 修复中继创建或编辑后，无法立即执行注册的问题。修复注册式中继修改注册服务器后，原服务器的mysql registrant数据未删除问题. 
* #3581 Regarding the mismatch between the number of FAQ batches and the number under review.
* #3582 修复我的报表页面汇总错误累积数字坐席组，未显示坐席组名称只显示坐席组号码问题
* #3564 The status setting for the Category of the ticket does not take effect even when set to [Disabled].
* #3558 解决驻留播报成功语音时话机进行了转接操作，造成原通话无法结束，少cdr，实时通话信息未清除   
* #3554 Unable to save the reservation    
* #3552 The 'Recording File Format' setting is not being applied correctly.    
* 移除对内网双网卡的处理    
* #2823 修改trunk Volume为0时,不执行设置,避免影响强插声音问题    
* #3540 The list in Customer Data > Customer Data > Call Results displays the default package after navigating to another screen or reloading the page.    
* #3539 When creating a role with the name 'All', it appears as 'Select All'      
* #3354#note_309265 将知识手动操作为审核中状态时需要同步更新右上角铃铛提示中的数据，坐席新增个人知识数据的时候client的知识库待审核数量也要跟着实时更新    
* #3207 客户包中-->索引字段中有英文字段不应该显示，应当删除。 修改日语模式下客户包页面 年龄显示为年齢, 改进创建client时，使用json文件进行创建schema    
* #3352 Regarding the character count for quality management entries，页面警告消息tooltip不消失问题。        
* #3322 #3320 坐席端客户预约中分配错位问题      
* #3465 预拨号页面盲转挂断问题,解决预拨号盲转和盲转回呼时通话记录实际主叫带星号的问题       
* #3160 从代码里移除微信相关的功能         
* #3497 排查改进发送统计的csv文件到指定地址功能    
* #3498 Bugs or issues occurring in the 'Tickets > Categories > Custom Fields' section.修复没有自定义字段时，不显示空排序的马赛克界面。  
* #3499 Filtering valid customers: Call results also include funnel 0 or below.    
* #3509 The item name Reseller - VoIP Settings > Incoming Number is not translated.    
* #3510 Change the wording of the tooltip for IP address restriction.  
* #3514 ‘Roles and permissions’ are not being displayed.    
* #3468 增加一个脚本用于排查客户号码绑定关系是否缺失    
* #3500 Issues when downloading from Reports > Users    
* #3496 统一客户数据、联络记录和客户弹屏上，销售漏斗和呼叫结果的文字显示    
* #3504 SW:工单--自定义字段中添加关联字段，坐席建立工单页面会报错    
* #3506 Change of the item "Quality Control Rate" under the "Quality Control" tab on the Campaign Settings screen.    
* #3505 Call history – Call type: Two-way call    
* #3502 "Tooltip for the Outbound Call Block List"    
* #3501 如果在产品中添加一个有效期，这个产品就不会在坐席订单--产品中正常显示，不添加有效期是正常的    
* #3493 The UI when editing a ticket in the customer information section.    
* #3488 客户数据页面客户的质检结果无法进行筛选      
* #3469 联系客户页面，切换一个客户包吗，在客户数据页面查看一个默认客户包的客户，客户不能正常弹屏    
* #3484 The translations of the items on the Quality Management screen are incorrect.    
* #3471 Inconsistent terminology: On the client screen, the headings in the customer data list mix the terms "date," "date and time," and "time."    
* #3312 内线通话被叫驻留后，取回时CDR显示的工号不对。内线通话主叫驻留和被叫驻留时CDR中dialedNum显示不一致，都改成显示驻留号码了。    
* #3436 client已被分配外显号码，坐席组里依然可以随便填写（同时修改呼入路由 did页面）    
* #3437 坐席组溢出转向到外线号码，CallerID不显示问题(系统偏好切回来之后不显示)    
* #3333 通话记录不记录按键情况    
* #3438 “此工单中的客户已删除”的提示在添加新客户时还会出现    
* #3449 ivr语音菜单-转向-输入问题    
* 坐席组超时溢出转向到外线，外显号码不生效    
* 内线通话，坐席分别咨询转接到外线，通话记录只有3条通话记录，且页面显示undefined,原因是转接流程替换callid_legb时未取到咨询通话的callid_legb    
* #3425 修改插件获取坐席数据接口,默认获取全部的坐席数据    
* #3434 增加浏览器插件所需接口，获取坐席的部门信息    
* #3450 增加对ruri中sips的支持    
* #3448 坐席明细 和 坐席组明细 报表，在统计信息的坐席组字段中显示为空    
* #3129 統計---坐席組會在周和月的統計中會被累計錯誤。    
* #3388 内线盲转+咨询，点击挂断，点击方页面不挂断，通话正常挂断。外呼号码支持加号，去除dial参数中的空格     
* #3389 中继的外呼路由允许+，中继的主叫号码替换应当允许+    
* #3420 修复agephone使用tcp+srtp会遇到一个488问题    
* #3310 坐席呼入到振铃组，主叫咨询转成功后，第三方驻留，被叫电话直接挂断等    
* #3341 坐席登录网页并处于话后状态下不应该接到呼入电话    
* #3362 坐席呼入振铃组，主叫坐席咨询转成功后，第三方坐席咨询转后挂机，页面显示异常    
* #3401 客户数据添加界面上, 数据标签下出现2个 客户标签字段    
* #3313 坐席拨打振铃组号码，驻留问题    
* #3392 DID中无法保存带+号的号码       
* #3356 Customer data: Call results unrelated to the package or campaign are displayed.    
* #3371 保存\更新客户资料中被设置为唯一键值的字段为空值情况    
* #3379 隐藏录音名称    
* #3345 The Real-Time Monitor and the Monitoring System use different colors for the same statuses. It would be better to standardize them.    
* #3346 FAQ tab cannot be closed    
* #3375 "Negative values can be entered and saved in the following fields, which are supposed to accept only integer values."    
* #3337 ivr使用的媒体文件，将文件内容更新为其他音频时，ivr使用的媒体文件不会被更新    
* #3152 振铃组全部振铃且坐席同时应答时记录应答坐席错误的问题 解决_rgSessionId 未保存的问题    
* #3373 后台任务中仅导入的用户可以下载该文件，其他用户点击下载则弹出提示错误    
* #3359 Unable to register customer data despite unregistered number    
* #3243 删除坐席组应删除绑定多余的数据    
* #3370 When assigning a call profile to a client, if a non-existent profile is manually entered and saved, a success message is displayed.    
* #3369 File Type "Hold Music" Changes to "Waiting Call Playlist" After Screen Transition Reproduction Steps:    
* #3348 Regarding the Expansion/Resizing of the Comment Input Area in Quality Management    
* #3323 中继使用下载模版导入时，不能正常导入（启用注册参数必须是boolean类型）    
* #3331 Error in English when adding to the outbound blocked list    
* #3365 坐席端创建今天到期的知识时与client创建今天到期的知识,筛选时显示状态不同    
* #3349 When editing a draft again, the expiration date displays the time    
* #3318 超长字段后台报错问题    
* #3361 修复客户1使用 phone1, 客户2使用phone1和phone2, 删除客户2后,客户1的号码绑定关系丢失问题， 客户1的号码绑定关系应该继续在    
* #3350 The display when removing a highlight in the customer information section appears unnatural.    
* #3351 The profile picture taken with the webcam appears stretched vertically.      
* #3357 Regarding the translation of "Real-time Monitor > Ratio"    
* #3252 外线在播放位置通告中，坐席接通，通话不会立刻接通，仍会播放完位置通告    
* #3253 队列位置播报，排队数据大于20时，数字无法播放    
* #3353 If the purpose of the Schedule       
* #3340 Notation on the call history screen    
* #3335 自定义字段 中 字段类型为自定义时，存在问题。    
* #3334 agent和client打开自定义字段页面,选择项目类型时,自定义字段的日语不同      
* #3321 Behavior of the Save Button in the Interaction History under Customer Data     
* #3324 On the push notification reference screen, the Save/Reset buttons are displayed    
* #3327 Mismatch in the Away values under Ratio in the Real-Time Monitor     
* #3301 When sending a large image in chat, unnecessary items from the history are also resent.    
* #3308 修复节点挂起问题    
* #3314 About the display of call history items    
* #3315 menus sidebar element has Chinese in it    
* #3317 User - Customer from Campaign    
* #3316 预拨号--客户接通等待时，客户电话处显示的是client的外显号码，任务--预拨号中选择放音收号时，预拨号页面一直显示坐席振铃进度条。    
* #3177 被咨询坐席在咨询转瞬间可能接到队列中等待客户的通话    
* #3305 坐席组汇总页面，计算、字段显示问题       
* #3300 The waiting call display on the user dashboard is not updated in real-time.    
* #3294 reseller页面返回列表信息时，公司字段返回了属于reseller_id的所有公司信息，应只返回属于它自己的公司信息    
* #3291 修复客户数据页面使用的弹屏函数，避免调用坐席端选择错误的客户包导致错误    
* #3289 增加一个升级脚本用于对默认库和client库里schemas增加dnc字段    
* #3279 The “Hide Contact Information” tooltip is incorrectly described.    
* #3149 The vertical position of items in “Roles and Privileges” and “Messages” is different from the actual menu.    
* #3270 client-质检页面排版问题 提示服务器错误    
* #3265 修复sapi里获取cdr接口参数验证    
* #3264 坐席--话机部署模版，点击预览会显示网络错误    
* #3247 client-问卷选项模板页面，选项搜索框不能搜索    
* 通过中继外呼默认不开启722,防止引起asterisk Inband DTMF is not supported on codec g722. Use RFC2833错误    
* #3236 修复Root用户实时监控报错    
* #3228 root-中继管理页面，费率类型搜索框无效    
* #3191 20230725_HS_01 Fill in number predictive input and dial pad layout collapse    
* 调整聊天获取坐席接口，使插件聊天可以获取到坐席登录状态    
* #3180 Collapse of header layout    
