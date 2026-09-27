-- Query 1: Top 10 Regions/Suppliers by Delay Frequency
SELECT 
    OrderRegion,
    COUNT(*) AS Total_Orders,
    AVG(DelayDays) AS Avg_Delay_Days
FROM supply_chain_orders
GROUP BY OrderRegion
ORDER BY Avg_Delay_Days DESC
LIMIT 10;

-- Query 2: Delay Metrics by Delivery Status
SELECT 
    DeliveryStatus,
    COUNT(*) AS Order_Count,
    AVG(DelayDays) AS Avg_Delay_Days
FROM supply_chain_orders
GROUP BY DeliveryStatus
ORDER BY Avg_Delay_Days DESC;

-- Query 3: Products with Highest Financial Loss Impact
SELECT 
    ProductName,
    COUNT(*) AS Total_Orders,
    AVG(LossPercentage) AS Avg_Loss_Percent,
    SUM(CostImpactOfDelay) AS Total_Cost_Impact
FROM supply_chain_orders
GROUP BY ProductName
ORDER BY Total_Cost_Impact DESC
LIMIT 15;

-- Query 4: Monthly Order Volume & Delay Trends
SELECT 
    YEAR(FormattedOrderDate) AS Order_Year,
    MONTH(FormattedOrderDate) AS Order_Month,
    COUNT(*) AS Total_Orders,
    AVG(DelayDays) AS Avg_Delay_Days,
    SUM(CostImpactOfDelay) AS Total_Loss
FROM supply_chain_orders
GROUP BY Order_Year, Order_Month
ORDER BY Order_Year ASC, Order_Month ASC;

-- Query 5: Supplier Risk Score Calculation
SELECT 
    OrderRegion AS Supplier_Region,
    COUNT(*) AS Total_Orders,
    AVG(DelayDays) AS Avg_Delay,
    AVG(LateDeliveryRisk) * 100 AS Late_Risk_Percent,
    AVG(LossPercentage) AS Avg_Loss_Percent,
    (AVG(DelayDays) / 10) * 0.4 + AVG(LateDeliveryRisk) * 0.4 + (AVG(LossPercentage) / 100) * 0.2 AS Risk_Score
FROM supply_chain_orders
GROUP BY OrderRegion
ORDER BY Risk_Score DESC;

-- Query 6: On-Time Delivery % by Global Market
SELECT 
    Market,
    COUNT(*) AS Total_Orders,
    SUM(IF(DelayDays <= 0, 1, 0)) AS OnTime_Orders,
    (SUM(IF(DelayDays <= 0, 1, 0)) / COUNT(*)) * 100 AS OnTime_Percent,
    AVG(OrderItemTotal) AS Avg_Order_Value,
    SUM(CostImpactOfDelay) AS Total_Delay_Cost
FROM supply_chain_orders
GROUP BY Market
ORDER BY OnTime_Percent ASC;

-- Query 7: High-Risk Supplier Drill-Down
SELECT 
    OrderRegion,
    Market,
    COUNT(*) AS Order_Count,
    AVG(DelayDays) AS Avg_Delay,
    AVG(LossPercentage) AS Avg_Loss_Percent,
    SUM(OrderItemTotal) AS Total_Order_Value,
    SUM(CostImpactOfDelay) AS Cost_Impact
FROM supply_chain_orders
GROUP BY OrderRegion, Market
HAVING Avg_Delay > 0.5
ORDER BY Avg_Delay DESC;