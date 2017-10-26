
$(document).ready(function() {
    $("#id_amount").blur(function () {
        var payment_total = parse_decimal(this.value);
        var discount_rate = parse_decimal($('#id_discount_rate').val()).dividedBy(100);
        var discount = parse_decimal($('#id_discount').val());
        this.value = payment_total.toFixed(2);

        var balance = new BigNumber('0.00');
        $(".fee-row").each(function () {
            var month_amount = parse_decimal($('.fee-amount', this).text());

            // apply discount_rate
            if (!discount_rate.isZero()) {
                month_amount = month_amount.minus(discount_rate.times(month_amount));
                $('.fee-discount', this).text(month_amount.toFormat(2));
            } else {
                $('.fee-discount', this).text('');
            }

            var payment = payment_total.greaterThanOrEqualTo(month_amount) ? month_amount : payment_total;

            // apply discount
            var month_discount = new BigNumber('0.00');
            if (payment.lessThan(month_amount) && !discount.isZero()) {
                month_discount = discount.greaterThanOrEqualTo(month_amount.minus(payment)) ?
                    month_amount.minus(payment) : discount;
                month_amount = month_amount.minus(month_discount);
                discount = discount.minus(month_discount);
                $('.fee-discount', this).text(month_amount.toFormat(2));
            }

            // add classes to rows
            if (payment.equals(month_amount)) {
                $(this).addClass('table-success').removeClass('table-warning');
            } else if (payment.isZero() && month_discount.isZero()) {
                $(this).removeClass('table-success table-warning');
            } else {
                $(this).addClass('table-warning').removeClass('table-success');
                if (!discount_rate.isZero() || !month_discount.isZero()) {
                    $('.discount-row').addClass('bg-danger');
                } else {
                    $('.discount-row').removeClass('bg-danger');
                }
            }

            payment_total = payment_total.minus(payment);
            balance = balance.add(month_amount).minus(payment);

            $('.fee-balance', this).text(balance.toFormat(2));
            $('.fee-payment', this).text(payment.toFormat(2));
        });
        $('.fee-balance-total').text(balance.toFormat(2));
    });

    $("#id_discount_rate").blur(function () {
        var discount_rate = parse_decimal(this.value);
        this.value = discount_rate.toFixed(0);
        if (!discount_rate.isZero()) {
            $('#id_discount').val('');
        }
        $("#id_amount").blur();
    });

    $("#id_discount").blur(function () {
        var discount = parse_decimal(this.value);
        this.value = discount.toFixed(2);
        if (!discount.isZero()) {
            $('#id_discount_rate').val('');
        }
        $("#id_amount").blur();
    });

    $('#id_date').datepicker({dateFormat: "yy-mm-dd"});
});
