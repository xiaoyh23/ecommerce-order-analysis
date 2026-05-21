from faker import Faker
import pandas as pd
import random

fake = Faker('zh_CN')

# ==================================================
# 1. 生成用户数据
# ==================================================

print("=" * 50)
print("生成用户数据")
print("=" * 50)

city_list = [

    '北京市',
    '上海市',
    '深圳市',
    '广州市',
    '杭州市',
    '成都市',
    '重庆市',
    '武汉市',
    '南京市',
    '西安市',
    # '苏州市',
    '郑州市',
    '长沙市',
    '青岛市',
    '天津市',
    # '宁波市',
    '合肥市',
    '南昌市',
    '贵阳市',
    '兰州市',
    '海口市',
    '呼和浩特市'
]

city_weights = [

    # 一线城市
    15, 15, 12, 12,

    # 新一线
    10, 9, 8, 7,

    # 二线
    6, 6, 6, 6, 6, 5, 5,

    # 三线
    4, 3, 2, 3, 1
]

users = []

for i in range(10000):

    users.append([
        i + 1,
        fake.user_name(),
        random.choice(['男', '女']),
        random.choices(
            city_list,
            weights=city_weights
        )[0],
        fake.date_time_between(
            start_date='-3y',
            end_date='now'
        )
    ])

df_users = pd.DataFrame(
    users,
    columns=[
        'user_id',
        'username',
        'gender',
        'city',
        'register_time'
    ]
)

print(df_users.head())

df_users.to_csv(
    'data/users.csv',
    index=False
)

print("users.csv 生成成功")


# ==================================================
# 2. 生成商品数据
# ==================================================

print("=" * 50)
print("生成商品数据")
print("=" * 50)

products = []

categories = [
    '手机',
    '电脑',
    '耳机',
    '家电',
    '服装',
    '食品'
]

for i in range(500):

    category = random.choice(categories)

    # 不同品类价格区间
    if category == '手机':

        price = round(
            random.uniform(3000, 15000),
            2
        )

    elif category == '电脑':

        price = round(
            random.uniform(4000, 20000),
            2
        )

    elif category == '耳机':

        price = round(
            random.uniform(100, 3000),
            2
        )

    elif category == '家电':

        price = round(
            random.uniform(500, 10000),
            2
        )

    elif category == '服装':

        price = round(
            random.uniform(50, 1000),
            2
        )

    else:

        price = round(
            random.uniform(10, 300),
            2
        )

    products.append([
        i + 1,
        f"{category}_{i+1}",
        category,
        price
    ])

df_products = pd.DataFrame(
    products,
    columns=[
        'product_id',
        'product_name',
        'category',
        'price'
    ]
)

print(df_products.head())

df_products.to_csv(
    'data/products.csv',
    index=False
)

print("products.csv 生成成功")


# ==================================================
# 3. 生成订单数据
# ==================================================

print("=" * 50)
print("生成订单数据")
print("=" * 50)

orders = []

order_items = []

order_status_list = [
    '已支付',
    '已完成',
    '已取消'
]

order_id = 1
item_id = 1

for user_id in range(1, 10001):

    rand = random.random()

    # ==================================================
    # 用户消费分层
    # ==================================================

    # 70% 用户只下一单
    if rand < 0.7:

        order_count = 1

    # 20% 用户下 2~5 单
    elif rand < 0.9:

        order_count = random.randint(2, 5)

    # 10% 高活跃用户
    else:

        order_count = random.randint(6, 20)

    # ==================================================
    # 一个用户多个订单
    # ==================================================

    for _ in range(order_count):

        # ==================================================
        # 城市消费能力
        # ==================================================

        city = df_users.loc[
            df_users['user_id'] == user_id,
            'city'
        ].values[0]

        tier1_cities = [
            '北京',
            '上海',
            '深圳',
            '广州'
            
        ]

        # 一线城市消费能力更强
        if city in tier1_cities:

            price_multiplier = random.uniform(
                1.3,
                2.0
            )

        else:

            price_multiplier = random.uniform(
                0.8,
                1.2
            )

        # ==================================================
        # 时间规律（晚间订单更多）
        # ==================================================

        hour_weights = (
            [1] * 6 +     # 0-5
            [2] * 6 +     # 6-11
            [4] * 6 +     # 12-17
            [8] * 6       # 18-23
        )

        hour = random.choices(
            range(24),
            weights=hour_weights
        )[0]

        order_date = fake.date_time_between(
            start_date='-2y',
            end_date='now'
        )

        order_date = order_date.replace(
            hour=hour
        )

        # ==================================================
        # 订单状态
        # ==================================================

        order_status = random.choices(
            order_status_list,
            weights=[15, 55, 30]
        )[0]

        # ==================================================
        # 一个订单几个商品
        # ==================================================

        product_count = random.randint(1, 5)

        selected_products = []

        # ==================================================
    # 热门商品池（头部效应）
    # ==================================================

    hot_products = (
        [1]*15 +
        [2]*14 +
        [3]*13 +
        [4]*12 +
        [5]*11 +
        [6]*10 +
        [7]*9 +
        [8]*8 +
        [9]*7 +
        [10]*6
    )

    for _ in range(product_count):

        rand_product = random.random()

        # ==================================================
        # 热门商品逻辑（头部商品）
        # ==================================================

        if rand_product < 0.5:

            # 热门商品（销量不均匀）
            product_id = random.choice(hot_products)

        else:

            # 普通商品
            product_id = random.randint(11, 500)

        selected_products.append(product_id)

        # 去重
        selected_products = list(
            set(selected_products)
        )

        total_amount = 0

        # ==================================================
        # 订单详情
        # ==================================================

        for product_id in selected_products:

            product_info = df_products.loc[
                df_products['product_id'] == product_id
            ]

            product_price = product_info[
                'price'
            ].values[0]

            category = product_info[
                'category'
            ].values[0]

            # ==================================================
            # 品类销量差异
            # ==================================================

            # 食品销量高
            if category == '食品':

                quantity = random.randint(2, 6)

            # 服装中等
            elif category == '服装':

                quantity = random.randint(1, 3)

            # 手机销量低但金额高
            elif category == '手机':

                quantity = 1

            else:

                quantity = random.randint(1, 2)

            # ==================================================
            # 金额计算
            # ==================================================

            item_amount = round(
                product_price *
                quantity *
                price_multiplier,
                2
            )

            total_amount += item_amount

            order_items.append([
                item_id,
                order_id,
                product_id,
                quantity,
                item_amount
            ])

            item_id += 1

        # ==================================================
        # 已取消订单金额降低
        # ==================================================

        if order_status == '已取消':

            total_amount = round(
                total_amount * 0.1,
                2
            )

        orders.append([
            order_id,
            user_id,
            order_date,
            round(total_amount, 2),
            order_status
        ])

        order_id += 1


# ==================================================
# 4. 保存订单表
# ==================================================

df_orders = pd.DataFrame(
    orders,
    columns=[
        'order_id',
        'user_id',
        'order_date',
        'total_amount',
        'order_status'
    ]
)

print(df_orders.head())

df_orders.to_csv(
    'data/orders.csv',
    index=False
)

print("orders.csv 生成成功")


# ==================================================
# 5. 保存订单详情表
# ==================================================

df_order_items = pd.DataFrame(
    order_items,
    columns=[
        'item_id',
        'order_id',
        'product_id',
        'quantity',
        'item_amount'
    ]
)

print(df_order_items.head())

df_order_items.to_csv(
    'data/order_items.csv',
    index=False
)

print("order_items.csv 生成成功")


# ==================================================
# 6. 数据统计
# ==================================================

print("=" * 50)
print("数据统计")
print("=" * 50)

print(f"用户数: {len(df_users)}")
print(f"商品数: {len(df_products)}")
print(f"订单数: {len(df_orders)}")
print(f"订单详情数: {len(df_order_items)}")

print("\n订单状态分布：")
print(df_orders['order_status'].value_counts())

print("\n平均订单金额：")
print(round(
    df_orders['total_amount'].mean(),
    2
))

print("\nTOP10 热门商品：")

top_products = df_order_items[
    'product_id'
].value_counts().head(10)

print(top_products)