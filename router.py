# coding:utf8
from handler import index, stock, sku

handlers = [
  (r'/', index.IndexHandler),
  # 库存api
  (r'/api/stock/list', stock.StockListHandler),  # GET
  (r'/api/stock/create', stock.StockCreateHandler),  # POST： 创建
  (r'/api/stock/(\d+)', stock.StockRetrieveHandler),  # GET: 获取信息
  (r'/api/stock/(\d+)', stock.StockUpdateHandler),  # POST 多处信息修改
  (r'/api/stock/delete/(\d+)', stock.StockDeleteHandler),  # POST:删除
  (r'/api/stock/status/update/(\d+)', stock.StockStatusUpdateHandler),  # POST：修改状态

  # SKU api
  (r'/api/sku/list', sku.SkuListHandler),  # GET
  (r'/api/sku/create', sku.SkuCreateHandler),  # POST： 创建
  (r'/api/sku/(\d+)', sku.SkuRetrieveHandler),  # GET: 获取信息
  (r'/api/sku/(\d+)', sku.SkuUpdateHandler),  # POST 多处信息修改
  (r'/api/sku/delete/(\d+)', sku.SkuDeleteHandler),  # POST:删除


  (r'/.*', index.IndexHandler),

]
