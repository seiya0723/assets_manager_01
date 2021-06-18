from django import template

register = template.Library()


@register.inclusion_tag("bbs/table.html")
def generate_balance(topics):
    balances = []

    # TODO:ページネーション化させる時はこの時点でこれまでのページの残高を計算しておく
    total = 0

    for topic in topics:
        row = {}

        row["id"] = topic.id
        row["category"] = topic.category
        row["title"] = topic.title
        row["comment"] = topic.comment
        row["income"] = topic.income
        row["spending"] = topic.spending
        row["dt"] = topic.dt
        row["pay_dt"] = topic.pay_dt

        # total   = total + row["income"] - row["spending"]

        if row["spending"]:
            spending = int(row["spending"])
        else:
            spending = 0

        if row["income"]:
            income = int(row["income"])
        else:
            income = 0

        total = total + income - spending
        row["total"] = total

        balances.append(row)

    return {"balances": balances}