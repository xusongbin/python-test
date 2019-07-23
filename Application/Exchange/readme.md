
###2019-7-24 00:34:13
##功能一：
	前提=>以下汇率自动转为CNY
	目的=>买卖BURST转为CNYT
	流程=>充值BHD到BITATM，智能收币BHD->BURST然后自动提现到QBTC，QBTC卖币BURST->CNYT，等待提现。
	费用=>BITATM提现BURST币最高手续费5个币，QBTC提现CNYT费率0.8%最低8块
	实现=>
		获取QBTC买单价格，该价格为在QBTC可以卖出的最低价格
		获取QBTC最新买单价格，该价格与最低价格之间的差值为利润空间
		预测QBTC最佳托底价格，定期更新托底单，需要考虑波动问题
		预测QBTC最佳卖点价格，低于一定范围不提交卖单
		统计BITATM账户BURST币余额>=2500个自动提现到QTBC
	驱动=>
		QBTC获取买卖深度
		QBTC获取最新成交价格
		BITATM获取账户余额
		BITATM自动提现到QBTC
	问题=>
		QBTC充值地址是否会变更