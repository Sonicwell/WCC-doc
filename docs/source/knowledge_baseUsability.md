## Knowledge Base Usability

> 1.当主节点宕机时，知识库页面应保持可用性。

**Step1:** 先使用`curl -XGET 'http://elastic01:9200/_cat/master?v'`查看当前主节点地址(也可使用`curl -XGET 'http://elastic01:9200/_cat/nodes?v&h=name,ip,role,master'`查看当前集群信息)。

上述命令中elastic01需要替换成当前可用的节点地址。

**Step2:** 在主节点服务器，执行`systemctl stop elasticsearch.service`停用ES服务。

**Step3:** 在知识库页面进行增删改查操作，系统应保持可用，自动连接新的主节点。


> 2.当ES集群所有数据节点和投票节点均宕机后再次启用时，知识库页面应自动恢复可用，无需重启任何服务。

**Step1:** 在所有ES服务器执行`systemctl stop elasticsearch.service`，停用ES服务。

**Step2:** 此时访问知识库页面，提示服务不可用。

**Step3:** 在所有ES服务器执行`systemctl start elasticsearch.service`，启用ES服务（或至少保证2个节点恢复，其中一台应为数据节点）。

**Step4:** 再次访问知识库页面，进行增删改查操作，系统应保持可用，自动连接新的主节点。
