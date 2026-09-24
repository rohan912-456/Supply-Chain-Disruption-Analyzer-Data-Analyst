Query 1: Top 10 Regions/Suppliers by Delay Frequency
SELECT 
    SUBSTRING_INDEX(OrderRegion, ',', 1) as Supplier_Region,
    COUNT(*) as Total_Orders,
    ROUND(AVG(DelayDays), 2) as Avg_Delay_Days,
    COUNT(CASE WHEN DelayDays > 0 THEN 1 END) as Late_Orders,
    ROUND((COUNT(CASE WHEN DelayDays > 0 THEN 1 END) / COUNT(*)) * 100, 1) as Late_Delivery_Percent
FROM supply_chain_orders
GROUP BY Supplier_Region
HAVING Total_Orders > 100
ORDER BY Avg_Delay_Days DESC
LIMIT 10;

Query 2: Average Delay by Shipping Mode (Delivery Status)
SELECT 
    DeliveryStatus,
    COUNT(*) as Order_Count,
    ROUND(AVG(DelayDays), 2) as Avg_Delay_Days,
    MIN(DelayDays) as Min_Delay,
    MAX(DelayDays) as Max_Delay,
    ROUND(STDDEV(DelayDays), 2) as Std_Deviation
FROM supply_chain_orders
WHERE DeliveryStatus IN ('Late delivery', 'Shipping on time', 'Advance shipping')
GROUP BY DeliveryStatus
ORDER BY Avg_Delay_Days DESC;

Query 3: Products with Highest Damage/Loss Rate
SELECT 
    ProductName,
    COUNT(*) as Total_Orders,
    ROUND(AVG(LossPercentage), 2) as Avg_Loss_Percent,
    ROUND(SUM(CostImpactOfDelay), 2) as Total_Cost_Impact,
    ROUND(SUM(CostImpactOfDelay) / SUM(OrderItemTotal) * 100, 2) as Impact_as_Percent_of_Sales
FROM supply_chain_orders
GROUP BY ProductName
HAVING Avg_Loss_Percent > 0
ORDER BY Total_Cost_Impact DESC
LIMIT 15;

Query 4: Monthly Order Volume & Delay Trend
SELECT 
    DATE_FORMAT(FormattedOrderDate, '%Y-%m-01') as Month,
    COUNT(*) as Total_Orders,
    ROUND(AVG(DelayDays), 2) as Avg_Delay_Days,
    ROUND(SUM(CostImpactOfDelay), 0) as Monthly_Loss
FROM supply_chain_orders
GROUP BY Month
ORDER BY Month ASC;