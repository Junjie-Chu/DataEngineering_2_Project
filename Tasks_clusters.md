# Tasks

## 1 画流程图：
一台dashboard创建的虚拟机，+3台cloud init创建的虚拟机。（VM1：deploy server/raytune计算节点， VM2：production server，VM3：raytune计算节点）

## 2 每台机器的包依赖（ansible）：
VM1：deploysever：1 Lab2提供的包依赖 2 raytune 3 jupyternotebook 4 githook的自动化 5 python—sklearning，pip3
VM3：1 Lab2提供的包依赖 2 raytune 3 python—sklearning，pip3 
VM2：productionserver：1 Lab2提供的包依赖 

## 3 测试
使用lab2的example测试。

## 4 wait

## 5 现阶段的问题
a. 模型在development 里生成了，迁移到production里，用什么类去load模型。
b. 不同的模型需要在不同的containers里面跑，增大容错率
c. production能处理的请求数目，或者处理1000个请求所需要的时间，那么增加worker之后需要的时间是否会线性递减（scalability analysis）。 
d. 是否需要增加一个deployment node去测试development传输过来的模型是否有问题？ （已发邮件问老师）
