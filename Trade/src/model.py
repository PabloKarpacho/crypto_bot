from pydantic import BaseModel, Field
from typing import Optional

class OrderRequest(BaseModel): 
    category: str = Field("spot", description="Product type")
    symbol: str = Field(None, description="Symbol name, like BTCUSDT, uppercase only")
    isLeverage: Optional[int] = Field(0, description="Whether to borrow. Valid for Unified spot only. 0(default): false then spot trading, 1: true then margin trading")
    side: str = Field(None, description="Buy, Sell")
    orderType: str = Field('Limit', description="Market, Limit")
    qty: str = Field(None, description="Order quantity")

    marketUnit: Optional[str] = Field(None, description="The unit for qty when create Spot market orders for UTA account. Currently, TP/SL and conditional orders are not supported.")
    price: Optional[str] = Field(None, description="Order price")
    triggerDirection: Optional[int] = Field(1, description="Conditional order param. Used to identify the expected direction of the conditional order.")
    orderFilter: Optional[str] = Field(None, description="If it is not passed, Order by default.")
    triggerPrice: Optional[str] = Field(None, description= "For spot, it is the TP/SL and Conditional order trigger price")
    triggerBy: Optional[str] = Field(None, description="Trigger price type, Conditional order param for Perps & Futures. LastPrice, IndexPrice, MarkPrice Valid for linear & inverse")
    orderIv: Optional[str] = Field(None, description="mplied volatility. option only. Pass the real value, e.g for 10%, 0.1 should be passed. orderIv has a higher priority when price is passed as well")
    timeInForce: Optional[str] = Field(None, description="Time in force")
    positionIdx: Optional[str] = Field(None, description="Used to identify positions in different position modes. Under hedge-mode, this param is required (USDT perps & Inverse contracts have hedge mode)")
    orderLinkId: Optional[str] = Field(None, description="	User customised order ID. A max of 36 characters. Combinations of numbers, letters (upper and lower cases), dashes, and underscores are supported.")

    takeProfit: Optional[str] = Field(None, description="Take profit price")
    stopLoss: Optional[str] = Field(None, description="Stop loss price")

    tpTriggerBy: Optional[str] = Field(None, description="The price type to trigger take profit. MarkPrice, IndexPrice, default: LastPrice. Valid for linear & inverse")
    slTriggerBy: Optional[str] = Field(None, description="The price type to trigger stop loss. MarkPrice, IndexPrice, default: LastPrice. Valid for linear & inverse")
    reduceOnly: Optional[bool] = Field(None, description="true means your position can only reduce in size if this order is triggered.")
    closeOnTrigger: Optional[bool] = Field(None, description="For a closing order. It can only reduce your position, not increase it. If the account has insufficient available balance when the closing order is triggered, then other active orders of similar contracts will be cancelled or reduced. It can be used to ensure your stop loss reduces your position regardless of current available margin.")
    smpType: Optional[str] = Field(None, description="Smp execution type.")
    mmp: Optional[bool] = Field(None, description="Market maker protection. option only. true means set the order as a market maker protection order.")
    tpslMode: Optional[str] = Field(None, description="TP/SL mode")

    tpLimitPrice: Optional[str] = Field(None, description="The limit order price when take profit price is triggered")
    slLimitPrice: Optional[str] = Field(None, description="The limit order price when stop loss price is triggered")

    tpOrderType: Optional[str] = Field(None, description="The order type when take profit is triggered")
    slOrderType: Optional[str] = Field(None, description="The order type when stop loss is triggered")

class AmendOrderRequest(BaseModel): 
    category: str = Field("spot", description="Product type")
    symbol: str = Field(None, description="Symbol name, like BTCUSDT, uppercase only")
    orderId: Optional[str] = Field(None, description="Order ID. Either orderId or orderLinkId is required")
    orderLinkId: Optional[str] = Field(None, description="User customised order ID. Either orderId or orderLinkId is required")
    orderIv: Optional[str] = Field(None, description="Implied volatility. option only. Pass the real value, e.g for 10%, 0.1 should be passed")
    triggerPrice: Optional[str] = Field(None, description="For spot, it is the TP/SL and Conditional order trigger price")
    qty: Optional[str] = Field(None, description="Order quantity after modification. Do not pass it if not modify the qty")
    price: Optional[str] = Field(None, description="Order price after modification. Do not pass it if not modify the price") 
    tpslMode: Optional[str] = Field(None, description="TP/SL mode")
    takeProfit: Optional[str] = Field(None, description="Take profit price after modification. If pass '0', it means cancel the existing take profit of the order. Do not pass it if you do not want to modify the take profit. valid for spot(UTA), linear, inverse")
    stopLoss: Optional[str] = Field(None, description="Stop loss price after modification. If pass '0', it means cancel the existing stop loss of the order. Do not pass it if you do not want to modify the stop loss. valid for spot(UTA), linear, inverse")
    tpTriggerBy: Optional[str] = Field(None, description="The price type to trigger take profit. When set a take profit, this param is required if no initial value for the order")
    slTriggerBy: Optional[str] = Field(None, description="The price type to trigger stop loss. When set a take profit, this param is required if no initial value for the order")
    triggerBy: Optional[str] = Field(None, description="Trigger price type")
    tpLimitPrice: Optional[str] = Field(None, description="Limit order price when take profit is triggered. Only working when original order sets partial limit tp/sl. valid for spot(UTA), linear, inverse")
    slLimitPrice: Optional[str] = Field(None, description="Limit order price when stop loss is triggered. Only working when original order sets partial limit tp/sl. valid for spot(UTA), linear, inverse")

class CancelOrderRequest(BaseModel): 
    category: str = Field("spot", description="Product type")
    symbol: str = Field(None, description="Symbol name, like BTCUSDT, uppercase only")
    orderId: Optional[str] = Field(None, description="Order ID. Either orderId or orderLinkId is required")
    orderLinkId: Optional[str] = Field(None, description="User customised order ID. Either orderId or orderLinkId is required")
    orderFilter: Optional[str] = Field(None, description="Valid for spot only. Order,tpslOrder,StopOrder. If not passed, Order by default")

class GetOpenOrderRequest(BaseModel): 
    category: str = Field("spot", description="Product type")
    symbol: str = Field(None, description="Base coin, uppercase only")
    baseCoin: Optional[str] = Field(None, description="Symbol name, like BTCUSDT, uppercase only")
    settleCoin: Optional[str] = Field(None, description="Settle coin, uppercase only")
    orderId: Optional[str] = Field(None, description="Order ID. Either orderId or orderLinkId is required")
    orderLinkId: Optional[str] = Field(None, description="User customised order ID. Either orderId or orderLinkId is required")
    openOnly: Optional[int] = Field(None)
    orderFilter: Optional[str] = Field(None, description="Valid for spot only. Order,tpslOrder,StopOrder. If not passed, Order by default")
    limit: Optional[int] = Field(None, description="Limit for data size per page. [1, 50]. Default: 20")
    cursor: Optional[str] = Field(None, description="Cursor. Use the nextPageCursor token from the response to retrieve the next page of the result set")

class CancelAllOrderRequest(BaseModel): 
    category: str = Field("spot", description="Product type")
    symbol: str = Field(None, description="Base coin, uppercase only")
    baseCoin: Optional[str] = Field(None, description="Symbol name, like BTCUSDT, uppercase only")
    settleCoin: Optional[str] = Field(None, description="Settle coin, uppercase only")
    orderFilter: Optional[str] = Field(None, description="Valid for spot only. Order,tpslOrder,StopOrder. If not passed, Order by default")
    stopOrderType: Optional[str] = Field(None, description="Stop order type Stop")
    



