#1.月销售额分析
SELECT
	DATE_FORMAT(order_date,'%Y-%m') AS month,
	SUM(total_amount) AS total_sales
FROM orders
WHERE order_status != '已取消'
GROUP BY month
ORDER BY month;

#2.热门商品分析
SELECT
	p.product_name,
	SUM(oi.quantity) AS sales_qty
FROM order_items oi
JOIN products p
ON oi.product_id = p.product_id
GROUP BY p.product_name
ORDER BY sales_qty DESC
LIMIT 10;

#3.用户复购分析

SELECT 
    -- 分子：统计下了 2 单及以上已完成订单的用户数
    COUNT(DISTINCT CASE WHEN finish_cnt > 1 THEN user_id END) AS repeat_users,
    
    -- 分母：总消费用户数
    COUNT(DISTINCT user_id) AS total_users,
    
    -- 复购率
    CONCAT(
    	ROUND(
        	COUNT(DISTINCT CASE WHEN finish_cnt > 1 THEN user_id END) / COUNT(DISTINCT user_id) * 100,
        	2
    	),
    	'%'
    ) AS repurchase_rate
FROM (
    SELECT 
        user_id, 
        -- 针对每个用户计算已完成订单数
        SUM(CASE WHEN order_status = '已完成' THEN 1 ELSE 0 END) AS finish_cnt
    FROM orders
    GROUP BY user_id
) user_order_summary;

#4.城市消费分析
SELECT
	u.city,
	SUM(o.total_amount) AS total_sales
FROM orders o
JOIN users u
ON o.user_id = u.user_id
WHERE o.order_status != '已取消'
GROUP BY u.city
ORDER BY total_sales DESC;

#5.用户活跃时间分析
SELECT
	HOUR(order_date) AS hour,
	COUNT(*) AS order_count
FROM orders
GROUP BY hour
ORDER BY hour;

#6.订单分析状态
SELECT
    order_status,
    COUNT(*) AS order_count,
    
    -- 计算当前状态占总订单的比例（占比）
    CONCAT(
        ROUND(
            COUNT(*) / SUM(COUNT(*)) OVER() * 100, 
            2
        ),
        '%'
    ) AS conversion_rate

FROM orders
GROUP BY order_status;

#用户表
-- CREATE TABLE users (
--     user_id INT PRIMARY KEY AUTO_INCREMENT,
--     username VARCHAR(50),
--     gender VARCHAR(10),
--     city VARCHAR(50),
--     register_time DATETIME
-- );

#商品表
-- CREATE TABLE products (
--     product_id INT PRIMARY KEY AUTO_INCREMENT,
--     product_name VARCHAR(100),
--     category VARCHAR(50),
--     price DECIMAL(10,2)
-- );


#订单表
-- CREATE TABLE orders (
--     order_id INT PRIMARY KEY AUTO_INCREMENT,
--     user_id INT,
--     order_date DATETIME,
--     total_amount DECIMAL(10,2),
--     order_status VARCHAR(20),
-- 
--     FOREIGN KEY (user_id)
--     REFERENCES users(user_id)
-- );


#订单详情表
-- CREATE TABLE order_items (
--     item_id INT PRIMARY KEY AUTO_INCREMENT,
--     order_id INT,
--     product_id INT,
--     quantity INT,
--     item_amount DECIMAL(10,2),
-- 
--     FOREIGN KEY (order_id)
--     REFERENCES orders(order_id),
-- 
--     FOREIGN KEY (product_id)
--     REFERENCES products(product_id)
-- );