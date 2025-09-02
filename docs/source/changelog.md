## Version 3.7.0

**Date:** Building...

* IVR工作流BUG修复，提高可用性。与IVR语音菜单数据同步。  
* 增加对移动端WCALL APP的支持，提供PN支持。  
* OpenSIPs升级至3.4.13版本，解决内存崩溃风险。WCALL APP的SRTP，TLS适配。  
* 支持通话实时转写、话后转写、大屏监控实时转写通话内容。转接电话可见前面一通电话的沟通内容与总结。  
* 通话实时转写时提供知识话术自动推荐，通话结束后支持通话内容总结、分类。  
* AI资源的对接参数由client自行申请配置。目前已支持Azure、OpenAI、namitech资源。  
* #3583 Elasticsearch部署优化，预防单点故障。系统代码改进，增加知识库页面的可用性。  
* #3626 When editing a client with reseller privileges, call profiles from all resellers under the root are being displayed.  
* #3628 兼容更多SRTP加密协议  
* #3627 The session has timed out and the user is actually logged out, but the screen does not reflect this.  
* #3272 解决呼入到队列驻留后原通话录音听不了&内线主叫驻留时原通话录音未停止  
* #3589 调整统计流程里并发效率  
* #3453 内线通话盲转到外线时，外显示号码和外呼档案都使用发起转接的坐席的  
* #3533 坐席登录后，获取webrtc连接地址时，应过滤掉已暂停的节点。  
* #3512 Since SMS is not being used, I would like to hide the menu.  
* #3595 解决当BLF所订阅的分机拨打外线时，无法收到通知，呼吸灯呈绿色无变化  
* #3531 删除坐席后ivr转向列表中还是会显示已删除坐席    
* #3598 浏览器端的聊天界面也支持换行  
* #3608 解决振铃组失败转向目标为自己或包含原有振铃坐席时，可能造成redis坐席振铃数据残余的问题`:R:CALLS:AGENTS:RINGING:Z`  
* #3452 改进内线通话盲转振铃时第三方不显示振铃状态的问题  
* #3607 Specification changes for the User tab and Ratio tab in the Real-Time Monitor    
* #3329 Difference between Real-Time Monitor and Monitoring Numbers    
* #3428 The string WCCIM-Typing is sent with every key input.  
* #3410 增加DND接口, 坐席状态数据增加DND信息返回，便于电话插件与服务端DND状态同步显示。功能键开启关闭DND时发送坐席事件。  
* #3580 坐席仪表盘的排行榜，坐席头像不会正常显示  
* #3597 System > System Settings > Call Settings tab > How to configure the outgoing number (Tooltip adjustment)  
* #3579 知识库搜索，重复回车的时候会报错，搜索框显示不完全  
* #3456 After receiving an external call and the transfer destination answers via responsibility transfer, the UI on the original side remains in the "On Hold" state.  
* #3603 wcc-2421 过滤客户页面、联络客户页面、客户包的客户数据。  
* wcc-2416 编辑client时的profile不应返回无关信息  
* wcc-2442 删除reseller页面的created_by_id和created_by_username  
* wcc-2422 邮件服务器和短信档案数据精简  
* #3599 改进盲转到非坐席内线号码(如驻留号码)时，不再直接挂断而是进行盲转失败回呼  
* wcc-2419 账户/坐席页面返回的role信息精简  
* #3548 当建立一个自定义字段(必填类型)，更新流程里如果只更新部分字段数据，会导致更新失败  
* #3585 The error message displayed when a string is entered in the phone number input field on the call rejection list page is incorrect.  
* #3571 'New items that were not previously in the customer data are now appearing in black text.'  
* #3507 拨打外线超时、拨打分机超时、盲转振铃超时时长，这几个值如果设置成0，保存提示成功，但刷新后显示空白，实际生效的值还是之前设置的数  
* #3591 修复坐席与坐席之间聊天，系统提示显示问题  
* #3577 点击坐席面板上的知识库-个人知识后再切换到知识列表，只显示出来一个关键词，直接点击面板知识库或者顶部搜索知识库可以显示出多个关键词  
* #3515 About the package settings  
* #3573 In the ticket screen, the names of the items created as custom fields under the ticket categories are getting cut off.  
* #3521 The layout of the 'Reservation' panel on the dashboard is not displaying correctly.  
* #3567 将工单的类别改为无效状态，之前使用这个类别的工单编辑会报错  
* #3535 Change the campaign terminology  
* #3586 In the 'Call History', the disconnection reason is displayed as [DNC].  
* #3578 On the Tickets > Add/Edit Category screen, Pending' is written.  
* #3542 呼入IP控制不生效且无法输入多个地址，中继呼入IP改用grp=2表示。  
* #3561 多节点时，遇到通话和坐席当前通话不在一个节点时transfer使用原始DID做为被叫  
* #3520 Status message when an administrator sets a user as away.  
* #3525 自定义字段中字段类型为自定义并且支持多选时，在添加客户数据页面字段下拉框会多出一个空格  
