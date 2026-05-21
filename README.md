# 电商订单分析与可视化平台

基于 Python + MySQL + Power BI 构建的电商数据分析项目，通过模拟真实电商业务数据，完成订单分析、用户消费分析、城市消费能力分析、热门商品分析、用户复购分析等业务场景。

---

## 项目亮点

- 模拟真实电商业务数据，包含用户分层、城市消费能力、热门商品权重等业务逻辑
- 基于 SQL 完成用户复购率、城市消费、热门商品等核心业务分析
- 使用 Power BI 搭建交互式数据分析仪表盘
- 构建完整数据分析流程：数据生成 → 数据存储 → SQL分析 → BI可视化
- 通过数据建模模拟真实电商消费规律，提高项目业务真实性

---

## Power BI 可视化分析

### 总仪表盘

![Power BI Dashboard](result/dashboard.png)

### 城市消费地图分析

![City Sales Map](result/city_sales_map.png)

---

## Tech Stack

- Python
- Pandas
- Faker
- MySQL
- SQL
- Power BI
- Git

---

## 项目结构

```text
ecommerce_order_analysis/
│
├── data/
│   ├── users.csv
│   ├── products.csv
│   ├── orders.csv
│   └── order_items.csv
│
├── scripts/
│   └── generate_data.py
│
├── sql/
│   ├── create_tables.sql
│   └── analysis.sql
│
├── result/
│   ├── dashboard.png
│   ├── city_sales_map.png
│   ├── top_products.png
│   ├── month_sales.png
│   ├── active_hour.png
│   └── powerbi_dashboard.pbix
│
│
├── README.md
├── requirements.txt
└── .gitignore
```

---

## 数据建模逻辑

### 用户分层

- 44% 用户低频消费（10000以下）
- 45% 用户中频消费（10000-100000）
- 11% 用户高活跃消费（100000+）

### 城市消费能力

一线城市消费能力更高，通过 `price_multiplier` 模拟不同城市消费水平差异。

### 热门商品机制

通过权重抽样模拟头部商品效应，形成明显销量集中现象。

### 时间规律

模拟晚间消费高峰，18:00~23:00订单量明显增加。

---

## SQL Analysis

### 热门商品分析

```sql
SELECT
    p.product_name,
    SUM(oi.quantity) AS sales_qty
FROM order_items oi
JOIN products p
ON oi.product_id = p.product_id
GROUP BY p.product_name
ORDER BY sales_qty DESC
LIMIT 10;
```

### 用户复购分析

```sql
SELECT 
    COUNT(DISTINCT CASE WHEN finish_cnt > 1 THEN user_id END) AS repeat_users,
    COUNT(DISTINCT user_id) AS total_users,
    CONCAT(
        ROUND(
            COUNT(DISTINCT CASE WHEN finish_cnt > 1 THEN user_id END) 
            / COUNT(DISTINCT user_id) * 100,
            2
        ),
        '%'
    ) AS repurchase_rate
FROM (
    SELECT 
        user_id, 
        SUM(
            CASE 
                WHEN order_status = '已完成' THEN 1 
                ELSE 0 
            END
        ) AS finish_cnt
    FROM orders
    GROUP BY user_id
) user_order_summary;
```

### 城市消费分析

```sql
SELECT
    u.city,
    SUM(o.total_amount) AS total_sales
FROM orders o
JOIN users u
ON o.user_id = u.user_id
WHERE o.order_status != '已取消'
GROUP BY u.city
ORDER BY total_sales DESC;
```

### 用户活跃时间分析

```sql
SELECT
    HOUR(order_date) AS hour,
    COUNT(*) AS order_count
FROM orders
GROUP BY hour
ORDER BY hour;
```

---

## Power BI 指标体系

### KPI 指标

- Total Sales（总销售额）
- Total Orders（订单总数）
- Total Users（总用户数）
- Repurchase Rate（复购率）
- Per Order Value（每笔订单金额）

### 可视化分析

- 月度销售趋势分析
- 城市消费地图分析
- 用户订单状态分析
- 热门商品 TOP10 分析
- 用户活跃时间分析
- 用户消费层级分析

---

## 数据分析结论

- 一线城市（北京、上海）消费金额明显高于其他城市，存在明显城市消费层级差异
- 用户消费高峰主要集中在晚间时段（18:00~23:00）
- 热门商品销量远高于普通商品，存在明显头部商品集中现象
- 用户复购率约 44.5%，高活跃用户对整体 Total Sales 贡献较高
- 已完成订单占比最高，整体订单完成情况较稳定

---

## 项目成果

基于 Python + MySQL + Power BI 构建完整电商订单分析平台，实现从数据生成、数据存储、SQL分析到 BI 可视化的完整数据分析流程，并通过业务建模模拟真实电商消费场景。

```