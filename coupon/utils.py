
def calculate_coupon_discout_for_product(productQ, coupon):
    product_discount = 0
    if productQ and coupon and coupon.valid and (coupon.usage_limit - coupon.used) > 0:
        course = productQ.course
        testseries = productQ.testseries
        if productQ.type == "course" and course:
            product_categories_ids = [i['id'] for i in list(course.category.values('id'))]
            coupon_product_categories_ids = [i['id'] for i in list(coupon.course_category.values('id'))]
            coupon_product_ids = [i['id'] for i in list(coupon.courses.values('id'))]

        if productQ.type == "testseries" and testseries:
            product_categories_ids = [i['id'] for i in list(testseries.category.values('id'))]
            coupon_product_categories_ids = [i['id'] for i in list(coupon.testseries_category.values('id'))]
            coupon_product_ids = [i['id'] for i in list(coupon.testseries.values('id'))]

        # validate the coupon code
        exits = False
        if (productQ.type == "course" and course) or (productQ.type == "testseries" and testseries):
            for product_category_id in product_categories_ids:
                if product_category_id in coupon_product_categories_ids:
                    exits = True
                    break
            if not exits and testseries.id in coupon_product_ids:
                exits = True

        # if coupon exits
        if exits:
            price = productQ.total_amount
            product_discount = float(price) * float(coupon.value / 100) if coupon.method.lower() == 'percent' else float(coupon.value)
    return product_discount


def validate_coupon_code_with_cart(coupon, cart):
    coupon_total_discount = 0
    if coupon and cart and coupon.valid and (coupon.usage_limit - coupon.used) > 0:
        productQuantity = cart.product_quantity.all()
        for productQ in productQuantity:
            product_discount = calculate_coupon_discout_for_product(productQ, coupon)
            coupon_total_discount += product_discount
        return True, coupon_total_discount
    return False, coupon_total_discount
