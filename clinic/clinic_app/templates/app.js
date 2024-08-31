<script type="text/javascript"></script>


    (function(d, t) {
        var BASE_URL = "https://engage.myserviceagent.net";
        var g = d.createElement(t),
            s = d.getElementsByTagName(t)[0];
        g.src = BASE_URL + "/packs/js/sdk.js";
        g.defer = true;
        g.async = true;
        s.parentNode.insertBefore(g, s);
        g.onload = function() {
            window.chatwootSDK.run({
                websiteToken: 'YG8XGwuLBF1iqYPDbqcxivZb',
                baseUrl: BASE_URL
            })
        }
    })(document, "script");

    
    $(document).ready(function() {
        const $stickyElement = $('.bottom-sticky_ele');
        const $offsetElement = $('.bottom-sticky_offset');

        if ($stickyElement.length !== 0) {
            $(window).on('scroll', function() {
                const elementOffset = $offsetElement.offset().top - ($(window).height() / 1.2);
                const scrollTop = $(window).scrollTop();

                if (scrollTop >= elementOffset) {
                    $stickyElement.addClass('stick');
                } else {
                    $stickyElement.removeClass('stick');
                }
            });
        }
    });
    
    $(document).ready(function() {
        $('.password-toggle-btn').on('click', function() {
            let checkbox = $(this).find('input[type=checkbox]');
            let eyeIcon = $(this).find('i');
            checkbox.change(function() {
                if (checkbox.is(':checked')) {
                    eyeIcon.removeClass('tio-hidden').addClass('tio-invisible');
                } else {
                    eyeIcon.removeClass('tio-invisible').addClass('tio-hidden');
                }
            });
        })

    });

    
    $(document).ready(function() {
        if (window.location.hash === "#subscribe") {
            $('#subscribe').focus();
        }
    });

    
    toastr.options = {
        "closeButton": false,
        "debug": false,
        "newestOnTop": false,
        "progressBar": false,
        "positionClass": "toast-top-right",
        "preventDuplicates": false,
        "onclick": null,
        "showDuration": "300",
        "hideDuration": "1000",
        "timeOut": "5000",
        "extendedTimeOut": "1000",
        "showEasing": "swing",
        "hideEasing": "linear",
        "showMethod": "fadeIn",
        "hideMethod": "fadeOut"
    }

    
    function showLoginModal() {
        $('#login-alert-modal').modal('show');
    }

    function showPresciptionUpload() {
        $('#mobile_nav').addClass('hidden');
        $('#upload-prescription-modal').modal('show');
    }

    $('#prescription').on('change', function() {
        var selectedFile = $(this).prop('files')[0];
        $('.presciptionName').text(selectedFile?.name)
    });

    function addWishlist(product_id, modalId) {
        $.ajaxSetup({
            headers: {
                'X-CSRF-TOKEN': $('meta[name="_token"]').attr('content')
            }
        });
        $.ajax({
            url: "https://medplusnig.com/store-wishlist",
            method: 'POST',
            data: {
                product_id: product_id
            },
            success: function(data) {
                if (data.value == 1) {
                    $('.countWishlist').html(data.count);
                    $('.countWishlist-' + product_id).text(data.product_count);
                    $('.tooltip').html('');
                    $(`.wishlist_icon_${product_id}`).removeClass('fa fa-heart-o').addClass('fa fa-heart');
                    $('#add-wishlist-modal').modal('show');
                    $(`#${modalId}`).modal('show');
                } else if (data.value == 2) {
                    $('#remove-wishlist-modal').modal('show');
                    $('.countWishlist').html(data.count);
                    $('.countWishlist-' + product_id).text(data.product_count);
                    $(`.wishlist_icon_${product_id}`).removeClass('fa fa-heart').addClass('fa fa-heart-o');
                } else {
                    $('#login-alert-modal').modal('show');
                }
            }
        });
    }

    function removeWishlist(product_id, modalId) {
        $.ajaxSetup({
            headers: {
                'X-CSRF-TOKEN': $('meta[name="_token"]').attr('content')
            }
        });
        $.ajax({
            url: "https://medplusnig.com/delete-wishlist",
            method: 'POST',
            data: {
                id: product_id
            },
            beforeSend: function() {
                $('#loading').show();
            },
            success: function(data) {
                $(`#${modalId}`).modal('show');

                $('.countWishlist').html(parseInt($('.countWishlist').html()) - 1);
                $('#row_id' + product_id).hide();
                $('.tooltip').html('');
                if (parseInt($('.countWishlist').html()) % 15 === 0) {
                    if ($('#wishlist_paginated_page').val() == 1) {
                        $("#set-wish-list").empty().append(`
                        <center>
                            <h6 class="text-muted">
                                No data found.
                            </h6>
                        </center>
                    `);
                    } else {
                        let page_value = $('#wishlist_paginated_page').val();
                        window.location.href = 'https://medplusnig.com/wishlists?page=' + (page_value -
                            1);
                    }
                }
            },
            complete: function() {
                $('#loading').hide();
            },
        });


    }

    function quickView(product_id) {
        $.get({
            url: 'https://medplusnig.com/quick-view',
            dataType: 'json',
            data: {
                product_id: product_id
            },
            beforeSend: function() {
                $('#loading').show();
            },
            success: function(data) {
                console.log("success...")
                $('#quick-view').modal('show');
                $('#quick-view-modal').empty().html(data.view);
            },
            complete: function() {
                $('#loading').hide();
            },
        });
    }

    function addToCart(form_id = 'add-to-cart-form', redirect_to_checkout = false) {
        if (checkAddToCartValidity()) {
            $.ajaxSetup({
                headers: {
                    'X-CSRF-TOKEN': $('meta[name="_token"]').attr('content')
                }
            });
            $.post({
                url: 'https://medplusnig.com/cart/add',
                data: $('#' + form_id).serializeArray(),
                beforeSend: function() {
                    $('#loading').show();
                },
                success: function(response) {
                    console.log(response);
                    if (response.status == 1) {
                        updateNavCart();
                        toastr.success(response.message, {
                            CloseButton: true,
                            ProgressBar: true
                        });
                        $('.call-when-done').click();
                        if (redirect_to_checkout) {
                            location.href = "https://medplusnig.com/checkout-details";
                        }
                        return false;
                    } else if (response.status == 0) {
                        $('#outof-stock-modal-message').html(response.message);
                        $('#outof-stock-modal').modal('show');
                        return false;
                    }
                },
                complete: function() {
                    $('#loading').hide();

                }
            });
        } else {
            Swal.fire({
                type: 'info',
                title: 'Cart',
                text: 'Please choose all the options'
            });
        }
    }

    function buy_now() {
        addToCart('add-to-cart-form', true);
        /* location.href = "https://medplusnig.com/checkout-details"; */
    }

    function currency_change(currency_code) {
        $.ajaxSetup({
            headers: {
                'X-CSRF-TOKEN': $('meta[name="_token"]').attr('content')
            }
        });
        $.ajax({
            type: 'POST',
            url: 'https://medplusnig.com/currency',
            data: {
                currency_code: currency_code
            },
            success: function(data) {
                toastr.success('Currency changed to' + data.name);
                location.reload();
            }
        });
    }

    function removeFromCart(key) {
        $.post('https://medplusnig.com/cart/remove', {
            _token: 'OTQTE4iOouBPrNT2IPv3oyPGLzjibwEo5nixwzhP',
            key: key
        }, function(response) {
            $('#cod-for-cart').hide();
            updateNavCart();
            $('#cart-summary').empty().html(response.data);
            toastr.info('Item has been removed from cart', {
                CloseButton: true,
                ProgressBar: true
            });
            let segment_array = window.location.pathname.split('/');
            let segment = segment_array[segment_array.length - 1];
            if (segment === 'checkout-payment' || segment === 'checkout-details') {
                location.reload();
            }
        });
    }

    function updateNavCart() {
        $.post('https://medplusnig.com/cart/nav-cart-items', {
            _token: 'OTQTE4iOouBPrNT2IPv3oyPGLzjibwEo5nixwzhP'
        }, function(response) {
            $('#cart_items').html(response.data);
        });
    }
    /*new*/
    $("#add-to-cart-form").on("submit", function(e) {
        e.preventDefault();
    });

    /*new*/
    function cartQuantityInitialize() {
        $('.btn-number').click(function(e) {
            e.preventDefault();

            fieldName = $(this).attr('data-field');
            type = $(this).attr('data-type');
            productType = $(this).attr('product-type');
            var input = $("input[name='" + fieldName + "']");
            var currentVal = parseInt($('.input-number').val());
            // alert(currentVal);
            if (!isNaN(currentVal)) {
                // console.log(productType)
                if (type == 'minus') {

                    if (currentVal > $('.input-number').attr('min')) {
                        $('.input-number').val(currentVal - 1).change();
                    }
                    if (parseInt($('.input-number').val()) == $('.input-number').attr('min')) {
                        $(this).attr('disabled', true);
                    }

                } else if (type == 'plus') {
                    // alert('ok out of stock');
                    if (currentVal < $('.input-number').attr('max') || (productType === 'digital')) {
                        $('.input-number').val(currentVal + 1).change();
                    }

                    if ((parseInt(input.val()) == $('.input-number').attr('max')) && (productType ===
                            'physical')) {
                        $(this).attr('disabled', true);
                    }

                }
            } else {
                $('.input-number').val(0);
            }
        });

        $('.input-number').focusin(function() {
            $(this).data('oldValue', $(this).val());
        });

        $('.input-number').change(function() {
            productType = $(this).attr('product-type');
            minValue = parseInt($(this).attr('min'));
            maxValue = parseInt($(this).attr('max'));
            valueCurrent = parseInt($(this).val());
            var name = $(this).attr('name');
            if (valueCurrent >= minValue) {
                $(".btn-number[data-type='minus'][data-field='" + name + "']").removeAttr('disabled')
            } else {
                Swal.fire({
                    icon: 'error',
                    title: 'Cart',
                    text: 'Sorry the minimum order quantity does not match'
                });
                $(this).val($(this).data('oldValue'));
            }
            if (productType === 'digital' || valueCurrent <= maxValue) {
                $(".btn-number[data-type='plus'][data-field='" + name + "']").removeAttr('disabled')
            } else {
                Swal.fire({
                    icon: 'error',
                    title: 'Cart',
                    text: 'Sorry stock limit exceeded.'
                });
                $(this).val($(this).data('oldValue'));
            }


        });
        $(".input-number").keydown(function(e) {
            // Allow: backspace, delete, tab, escape, enter and .
            if (
                $.inArray(e.keyCode, [46, 8, 9, 27, 13, 190]) !== -1 ||
                // Allow: Ctrl+A
                (e.keyCode == 65 && e.ctrlKey === true) ||
                // Allow: home, end, left, right
                (e.keyCode >= 35 && e.keyCode <= 39)
            ) {
                // let it happen, don't do anything
                return;
            }
            // Ensure that it is a number and stop the keypress
            if (
                (e.shiftKey || e.keyCode < 48 || e.keyCode > 57) &&
                (e.keyCode < 96 || e.keyCode > 105)
            ) {
                e.preventDefault();
            }
        });
    }

    function updateQuantity(key, element) {
        $.post('https://medplusnig.com/cart/updateQuantity', {
            _token: 'OTQTE4iOouBPrNT2IPv3oyPGLzjibwEo5nixwzhP',
            key: key,
            quantity: element.value
        }, function(data) {
            updateNavCart();
            $('#cart-summary').empty().html(data);
        });
    }



    function updateCartQuantity(cart_id, product_id, action, event) {
        let remove_url = $("#remove_from_cart_url").data("url");
        let update_quantity_url = $("#update_quantity_url").data("url");
        let token = $('meta[name="_token"]').attr("content");
        let product_qyt =
            parseInt($(`.cartQuantity${cart_id}`).val()) + parseInt(action);
        let cart_quantity_of = $(`.cartQuantity${cart_id}`);
        let segment_array = window.location.pathname.split("/");
        let segment = segment_array[segment_array.length - 1];

        if (cart_quantity_of.val() == 0) {
            toastr.info($('.cannot_use_zero').data('text'), {
                CloseButton: true,
                ProgressBar: true,
            });
            cart_quantity_of.val(cart_quantity_of.data("min"));
        } else if (
            (cart_quantity_of.val() == cart_quantity_of.data("min") &&
                event == "minus")
        ) {
            $.post(
                remove_url, {
                    _token: token,
                    key: cart_id,
                },
                function(response) {
                    updateNavCart();
                    toastr.info(response.message, {
                        CloseButton: true,
                        ProgressBar: true,
                    });
                    if (
                        segment === "shop-cart" ||
                        segment === "checkout-payment" ||
                        segment === "checkout-details"
                    ) {
                        location.reload();
                    }
                }
            );
        } else {
            if (cart_quantity_of.val() < cart_quantity_of.data("min")) {
                let min_value = cart_quantity_of.data("min");
                toastr.error('Minimum order quantity cannot be less than ' + min_value);
                cart_quantity_of.val(min_value)
                updateCartQuantity(cart_id, product_id, action, event)
            } else {
                $(`.cartQuantity${cart_id}`).html(product_qyt);
                $.post(
                    update_quantity_url, {
                        _token: token,
                        key: cart_id,
                        product_id: product_id,
                        quantity: product_qyt,
                    },
                    function(response) {
                        if (response["status"] == 0) {
                            toastr.error(response["message"]);
                        } else {
                            toastr.success(response["message"]);
                        }
                        response["qty"] <= 1 ?
                            $(`.quantity__minus${cart_id}`).html(
                                '<i class="tio-delete-outlined text-danger fs-10"></i>'
                            ) :
                            $(`.quantity__minus${cart_id}`).html(
                                '<i class="tio-remove fs-10"></i>'
                            );

                        $(`.cartQuantity${cart_id}`).val(response["qty"]);
                        $(`.cartQuantity${cart_id}`).html(response["qty"]);
                        $(`.cart_quantity_multiply${cart_id}`).html(response["qty"]);
                        $(".cart_total_amount").html(response.total_price);
                        $(`.discount_price_of_${cart_id}`).html(
                            response["discount_price"]
                        );
                        $(`.quantity_price_of_${cart_id}`).html(
                            response["quantity_price"]
                        );
                        $(`.total_discount`).html(
                            response["total_discount_price"]
                        );
                        $(`.free_delivery_amount_need`).html(
                            response.free_delivery_status.amount_need
                        );
                        if (response.free_delivery_status.amount_need <= 0) {
                            $('.amount_fullfill').removeClass('d-none');
                            $('.amount_need_to_fullfill').addClass('d-none');
                        } else {
                            $('.amount_fullfill').addClass('d-none');
                            $('.amount_need_to_fullfill').removeClass('d-none');
                        }
                        const progressBar = document.querySelector('.progress-bar');
                        progressBar.style.width = response.free_delivery_status.percentage + '%';
                        if (response["qty"] == cart_quantity_of.data("min")) {
                            cart_quantity_of
                                .parent()
                                .find(".quantity__minus")
                                .html(
                                    '<i class="tio-delete-outlined text-danger fs-10"></i>'
                                );
                        } else {
                            cart_quantity_of
                                .parent()
                                .find(".quantity__minus")
                                .html('<i class="tio-remove fs-10"></i>');
                        }
                        if (
                            segment === "shop-cart" ||
                            segment === "checkout-payment" ||
                            segment === "checkout-details"
                        ) {
                            location.reload();
                        }
                    }
                );
            }
        }
    }
    $('#add-to-cart-form input').on('change', function() {
        getVariantPrice();
    });

    function getVariantPrice() {
        if ($('#add-to-cart-form input[name=quantity]').val() > 0 && checkAddToCartValidity()) {
            $.ajaxSetup({
                headers: {
                    'X-CSRF-TOKEN': $('meta[name="_token"]').attr('content')
                }
            });
            $.ajax({
                type: "POST",
                url: 'https://medplusnig.com/cart/variant_price',
                data: $('#add-to-cart-form').serializeArray(),
                success: function(data) {
                    $('#add-to-cart-form #chosen_price_div').removeClass('d-none');
                    $('#add-to-cart-form #chosen_price_div #chosen_price').html(data.price);
                    $('#chosen_price_mobile').html(data.price);
                    $('#set-tax-amount-mobile').html(data.tax);
                    $('#set-tax-amount').html(data.tax);
                    $('#set-discount-amount').html(data.discount);
                    $('#available-quantity').html(data.quantity);
                    $('.cart-qty-field').attr('max', data.quantity);
                }
            });
        }
    }

    function checkAddToCartValidity() {
        var names = {};
        $('#add-to-cart-form input:radio').each(function() { // find unique names
            names[$(this).attr('name')] = true;
        });
        var count = 0;
        $.each(names, function() { // then count them
            count++;
        });
        if ($('input:radio:checked').length == count) {
            return true;
        }
        return false;
    }

                $(document).ready(function() {
            $('#popup-modal').appendTo("body").modal('show');
        });
                
    $(".clickable").click(function() {
        window.location = $(this).find("a").attr("href");
        return false;
    });


    
    function couponCode() {
        $.ajaxSetup({
            headers: {
                'X-CSRF-TOKEN': $('meta[name="_token"]').attr('content')
            }
        });
        $.ajax({
            type: "POST",
            url: 'https://medplusnig.com/coupon/apply',
            data: $('#coupon-code-ajax').serializeArray(),
            success: function(data) {
                /* console.log(data);
                return false; */
                if (data.status == 1) {
                    let ms = data.messages;
                    ms.forEach(
                        function(m, index) {
                            toastr.success(m, index, {
                                CloseButton: true,
                                ProgressBar: true
                            });
                        }
                    );
                } else {
                    let ms = data.messages;
                    ms.forEach(
                        function(m, index) {
                            toastr.error(m, index, {
                                CloseButton: true,
                                ProgressBar: true
                            });
                        }
                    );
                }
                setInterval(function() {
                    location.reload();
                }, 2000);
            }
        });
    }

    jQuery(".search-bar-input").keyup(function() {
        $(".search-card").css("display", "block");
        let name = $(".search-bar-input").val();
        if (name.length > 0) {
            $.get({
                url: 'https://medplusnig.com/searched-products',
                dataType: 'json',
                data: {
                    name: name
                },
                beforeSend: function() {
                    $('#loading').show();
                },
                success: function(data) {
                    $('.search-result-box').empty().html(data.result)
                },
                complete: function() {
                    $('#loading').hide();
                },
            });
        } else {
            $('.search-result-box').empty();
        }
    });

    jQuery(".search-bar-input-mobile").keyup(function() {
        $(".search-card").css("display", "block");
        let name = $(".search-bar-input-mobile").val();
        if (name.length > 0) {
            $.get({
                url: 'https://medplusnig.com/searched-products',
                dataType: 'json',
                data: {
                    name: name
                },
                beforeSend: function() {
                    $('#loading').show();
                },
                success: function(data) {
                    $('.search-result-box').empty().html(data.result)
                },
                complete: function() {
                    $('#loading').hide();
                },
            });
        } else {
            $('.search-result-box').empty();
        }
    });

    jQuery(document).mouseup(function(e) {
        var container = $(".search-card");
        if (!container.is(e.target) && container.has(e.target).length === 0) {
            container.hide();
        }
    });

    function route_alert(route, message) {
        Swal.fire({
            title: 'Are you sure?',
            text: message,
            type: 'warning',
            showCancelButton: true,
            cancelButtonColor: 'default',
            confirmButtonColor: '#ff0077',
            cancelButtonText: 'No',
            confirmButtonText: 'Yes',
            reverseButtons: true
        }).then((result) => {
            if (result.value) {
                location.href = route;
            }
        })
    }

    function order_again(order_id) {
        $.ajaxSetup({
            headers: {
                "X-CSRF-TOKEN": $('meta[name="_token"]').attr("content"),
            },
        });
        $.ajax({
            type: "POST",
            url: $("#order_again_url").data("url"),
            data: {
                order_id,
            },
            beforeSend: function() {
                $('#loading').show();
            },
            success: function(response) {
                if (response.status === 1) {
                    updateNavCart();
                    toastr.success(response.message, {
                        CloseButton: true,
                        ProgressBar: true,
                        timeOut: 3000, // duration
                    });
                    location.href = response.redirect_url;
                    return false;
                } else if (response.status === 0) {
                    toastr.warning(response.message, {
                        CloseButton: true,
                        ProgressBar: true,
                        timeOut: 2000, // duration
                    });
                    return false;
                }
            },
            complete: function() {
                $('#loading').hide();
            },
        });
    }
    
    $('.filter-show-btn').on('click', function() {
        $('#shop-sidebar').toggleClass('show active');
    })
    $('.cz-sidebar-header .close').on('click', function() {
        $('#shop-sidebar').removeClass('show active');
    })
    $('.remove-address-by-modal').on('click', function() {
        let link = $(this).data('link');
        $('#remove-address-link').attr('href', link);
        $('#remove-address').modal('show');
    });

    
            let cookie_content = `
    <div class="cookie-section">
        <div class="container">
            <div class="d-flex flex-wrap align-items-center justify-content-between column-gap-4 row-gap-3">
                <div class="text-wrapper">
                    <h5 class="title">Your Privacy Matter</h5>
                    <div></div>
                </div>
                <div class="btn-wrapper">
                    <span class="text-white cursor-pointer" id="cookie-reject">No thanks</span>
                    <button class="btn btn-success cookie-accept" id="cookie-accept">Yes i Accept</button>
                </div>
            </div>
        </div>
    </div>
`;
    $(document).on('click', '#cookie-accept', function() {
        document.cookie = '6valley_cookie_consent=accepted; max-age=' + 60 * 60 * 24 * 30;
        $('#cookie-section').hide();
    });
    $(document).on('click', '#cookie-reject', function() {
        document.cookie = '6valley_cookie_consent=reject; max-age=' + 60 * 60 * 24;
        $('#cookie-section').hide();
    });

    $(document).ready(function() {
        if (document.cookie.indexOf("6valley_cookie_consent=accepted") !== -1) {
            $('#cookie-section').hide();
        } else {
            $('#cookie-section').html(cookie_content).show();
        }
    });
        
    
        $(document).ready(function() {
            const currentUrl = new URL(window.location.href);
            const referral_code_parameter = new URLSearchParams(currentUrl.search).get("referral_code");
            if (referral_code_parameter) {
                                        window.location.href = "https://medplusnig.com/customer/auth/sign-up?referral_code=" +
                        referral_code_parameter;
                                }
        });
    </script>

<script type="module">
    import 'https://cdn.jsdelivr.net/gh/orestbida/cookieconsent@v3.0.0/dist/cookieconsent.umd.js';

    document.documentElement.classList.add('cc--darkmode');

    CookieConsent.run({
        categories: {
            necessary: {
                enabled: true,
                readOnly: true
            },
        },

        guiOptions: {
            consentModal: {
                layout: 'box',
                position: 'bottom right',
                flipButtons: false,
                equalWeightButtons: true,
            }
        },

        language: {
            default: 'en',
            translations: {
                en: {
                    consentModal: {
                        title: 'We use cookies',
                        description: '<p style="font-size:13px !important; line-height: 1.2">On this website we use third-party and first-party cookies to personalize its content, analyze its performance, improve security and serve ads relevant to your interests. By continuing the use of the website you consent to the use of cookies as described in our</p> <a style="color:#1D46F5; font-weight: 600; font-size:13px" href="/cookie-policy">Cookie policy</a>.',
                        closeIconLabel: "<h1>close</h1",
                    },
                }
            }
        }
    });

    
    /*========================
    04: Background Image
    ==========================*/
    var $bgImg = $("[data-bg-img]");
    $bgImg
        .css("background-image", function() {
            return 'url("' + $(this).data("bg-img") + '")';
        })
        .removeAttr("data-bg-img")
        .addClass("bg-img");

        
function openTab(tabName) {
      // Hide all tab contents
      document.querySelectorAll(".tab-content").forEach((tab) => {
        tab.classList.add("hidden");
      });

      // Remove active class from all buttons
      document.querySelectorAll(".tab-button").forEach((button) => {
        button.classList.remove(
          "text-[#FF0077]",
          "border-b",
          "border-[#FF0077]"
        );
      });

      document.getElementById(tabName).classList.remove("hidden");
      document.getElementById(tabName).classList.add("block");
      // Show the current tab
      document
        .getElementById(tabName + "-category-tab")
        .classList.add("text-[#FF0077]", "border-b", "border-[#FF0077]");
      // Add active class to the current button
    }

    function toggleAccordion(sectionId) {
      const section = document.getElementById(sectionId);
      const button = document.querySelector(
        `[onclick="toggleAccordion('${sectionId}')"]`
      );

      if (section.classList.contains("hidden")) {
        // Hide all sections
        document
          .querySelectorAll(".accordion-content")
          .forEach((content) => {
            content.classList.add("hidden");
          });
        document.querySelectorAll(".accordion-button").forEach((button) => {
          button.classList.remove(
            "text-[#FF0077]",
            "border-b-2",
            "border-[#FF0077]"
          );
          button.classList.add("text-[#75869D]");
        });

        // Show the current section
        section.classList.remove("hidden");
        button.classList.add(
          "text-[#FF0077]",
          "border-b-2",
          "border-[#FF0077]"
        );
        button.classList.remove("text-[#75869D]");
      } else {
        // Hide the current section
        section.classList.add("hidden");
        button.classList.remove(
          "text-[#FF0077]",
          "border-b-2",
          "border-[#FF0077]"
        );
        button.classList.add("text-[#75869D]");
      }
    }
  document.addEventListener("DOMContentLoaded", () => {
          
        document
        .getElementById("drugs-category-tab")
        .addEventListener("click", () => openTab("drugs"));
  
          
        document
        .getElementById("non-drugs-category-tab")
        .addEventListener("click", () => openTab("non-drugs"));
  
          
    
    // Default open the first tab
    openTab("drugs");
  });
  
    $(document).ready(function() {
        // Initially hide all extra FAQs
        $('.extra-faq').hide();

        // Toggle visibility on button click
        $('#viewMoreBtn').on('click', function() {
            $('.extra-faq').toggle();

            // Toggle the button text
            if ($(this).text() === 'View More') {
                $(this).text('View Less');
            } else {
                $(this).text('View More');
            }
        });
    });
    /*--flash deal Progressbar --*/
    const countdownElement = document.querySelector('.cz-countdown');

    /*--flash deal Progressbar --*/
    function update_flash_deal_progress_bar(){
        const current_time_stamp = new Date().getTime();
        const start_date = new Date('').getTime();
        const countdownElement = document.querySelector('.cz-countdown');
        const get_end_time = countdownElement.getAttribute('data-countdown');
        const end_time = new Date(get_end_time).getTime();
        let time_progress = ((current_time_stamp - start_date) / (end_time - start_date))*100;
        const progress_bar = document.querySelector('.flash-deal-progress-bar');
        progress_bar.style.width = time_progress + '%';
    }
    if(countdownElement) {
        update_flash_deal_progress_bar();
        setInterval(update_flash_deal_progress_bar, 10000);
    }
    /*-- end flash deal Progressbar --*/
<!-- Owl Carousel -->
<script src="https://medplusnig.com/public/assets/front-end/js/owl.carousel.min.js"></script>



    $('.flash-deal-slider').owlCarousel({
        loop: false,
        autoplay: true,
        center:false,
        margin: 10,
        nav: true,
        navText: ["<i class='czi-arrow-left'></i>", "<i class='czi-arrow-right'></i>"],
        dots: false,
        autoplayHoverPause: true,
        'ltr': false,
        // center: true,
        responsive: {
            //X-Small
            0: {
                items: 1.1
            },
            360: {
                items: 1.2
            },
            375: {
                items: 1.4
            },
            480: {
                items: 1.8
            },
            //Small
            576: {
                items: 2
            },
            //Medium
            768: {
                items: 3
            },
            //Large
            992: {
                items: 4
            },
            //Extra large
            1200: {
                items: 4
            },
        }
    })
    $('.flash-deal-slider-mobile').owlCarousel({
        loop: false,
        autoplay: true,
        center:true,
        margin: 10,
        nav: true,
        navText: ["<i class='czi-arrow-left'></i>", "<i class='czi-arrow-right'></i>"],
        dots: false,
        autoplayHoverPause: true,
        'ltr': false,
        // center: true,
        responsive: {
            //X-Small
            0: {
                items: 1.1
            },
            360: {
                items: 1.2
            },
            375: {
                items: 1.4
            },
            480: {
                items: 1.8
            },
            //Small
            576: {
                items: 2
            },
            //Medium
            768: {
                items: 3
            },
            //Large
            992: {
                items: 4
            },
            //Extra large
            1200: {
                items: 4
            },
        }
    })

    $('#web-feature-deal-slider').owlCarousel({
        loop: false,
        autoplay: true,
        margin: 20,
        nav: false,
        //navText: ["<i class='czi-arrow-left'></i>", "<i class='czi-arrow-right'></i>"],
        dots: false,
        autoplayHoverPause: true,
        'ltr': true,
        // center: true,
        responsive: {
            //X-Small
            0: {
                items: 1
            },
            360: {
                items: 1
            },
            375: {
                items: 1
            },
            540: {
                items: 2
            },
            //Small
            576: {
                items: 2
            },
            //Medium
            768: {
                items: 2
            },
            //Large
            992: {
                items: 2
            },
            //Extra large
            1200: {
                items: 2
            },
            //Extra extra large
            1400: {
                items: 2
            }
        }
    })

    $('.new-arrivals-product').owlCarousel({
        loop: true,
        autoplay: true,
        margin: 20,
        nav: true,
        navText: ["<i class='czi-arrow-left'></i>", "<i class='czi-arrow-right'></i>"],
        dots: false,
        autoplayHoverPause: true,
        'ltr': true,
        // center: true,
        responsive: {
            //X-Small
            0: {
                items: 1.1
            },
            360: {
                items: 1.2
            },
            375: {
                items: 1.4
            },
            540: {
                items: 2
            },
            //Small
            576: {
                items: 2
            },
            //Medium
            768: {
                items: 2
            },
            //Large
            992: {
                items: 2
            },
            //Extra large
            1200: {
                items: 4
            },
            //Extra extra large
            1400: {
                items: 4
            }
        }
    })

    $('.category-wise-product-slider').owlCarousel({
        loop: true,
        autoplay: true,
        margin: 20,
        nav: true,
        navText: ["<i class='czi-arrow-left'></i>", "<i class='czi-arrow-right'></i>"],
        dots: false,
        autoplayHoverPause: true,
        'ltr': true,
        responsive: {
            0: {
                items: 1.2
            },
            375: {
                items: 1.4
            },
            425: {
                items: 2
            },
            576: {
                items: 3
            },
            768: {
                items: 4
            },
            992: {
                items: 5
            },
            1200: {
                items: 6
            },
        }
    })

    // Faq

    $('.faq-div').click(function() {
        // First add 'hidden' class
        $('div.accordion-content').not('.hidden').addClass('hidden');

        // Then remove 'hidden' from the active one
        $(this).find('div.accordion-content').removeClass('hidden');
    });
    
    $('#featured_products_list').owlCarousel({
        loop: true,
        autoplay: true,
        margin: 20,
        nav: true,
        navText: ["<i class='czi-arrow-left'></i>", "<i class='czi-arrow-right'></i>"],
        dots: false,
        autoplayHoverPause: true,
        'ltr': false,
        // center: true,
        responsive: {
            //X-Small
            0: {
                items: 1
            },
            360: {
                items: 1
            },
            375: {
                items: 1
            },
            540: {
                items: 2
            },
            //Small
            576: {
                items: 2
            },
            //Medium
            768: {
                items: 3
            },
            //Large
            992: {
                items: 4
            },
            //Extra large
            1200: {
                items: 6
            },
        }
    });
    
    $('.hero-banner').owlCarousel({
        loop: true,
        autoplay: true,
        margin: 20,
        nav: true,
        navText: ["<i class='czi-arrow-left'></i>", "<i class='czi-arrow-right'></i>"],
        dots: true,
        autoplayHoverPause: true,
        // 'ltr': false,
        // center: true,
        items: 1
    });
    
    $('.category-slider').owlCarousel({
        loop: false,
        autoplay: false,
        margin: 20,
        nav: true,
        navText: ["<i class='czi-arrow-left'></i>", "<i class='czi-arrow-right'></i>"],
        dots: false,
        responsiveClass:true,
        responsive:{
            0:{
                items:1,
                nav:true
            },
            600:{
                items:2,
                nav:true
            },
            1000:{
                items:3,
                nav:true,
                loop:false
            },
            1300:{
                items:4,
                nav:true,
                loop:false
            }
        }
    });
    
    $('.brands-slider').owlCarousel({
        loop: false,
        autoplay: true,
        margin: 10,
        nav: false,
        'ltr': true,
        autoplayHoverPause: true,
        // center: true,
        responsive: {
            //X-Small
            0: {
                items: 4,
                dots: true,
            },
            360: {
                items: 5,
                dots: true,
            },
            //Small
            576: {
                items: 6,
                dots: false,
            },
            //Medium
            768: {
                items: 7,
                dots: false,
            },
            //Large
            992: {
                items: 9,
                dots: false,
            },
            //Extra large
            1200: {
                items: 11,
                dots: false,
            },
            //Extra extra large
            1400: {
                items: 12,
                dots: false,
            }
        }
    })

    
    $('#category-slider, #top-seller-slider').owlCarousel({
        loop: false,
        autoplay: true,
        margin: 20,
        nav: false,
        // navText: ["<i class='czi-arrow-left'></i>","<i class='czi-arrow-right'></i>"],
        dots: true,
        autoplayHoverPause: true,
        'ltr': true,
        // center: true,
        responsive: {
            //X-Small
            0: {
                items: 2
            },
            360: {
                items: 3
            },
            375: {
                items: 3
            },
            540: {
                items: 4
            },
            //Small
            576: {
                items: 5
            },
            //Medium
            768: {
                items: 6
            },
            //Large
            992: {
                items: 8
            },
            //Extra large
            1200: {
                items: 10
            },
            //Extra extra large
            1400: {
                items: 11
            }
        }
    })
    $('.categories--slider').owlCarousel({
        loop: false,
        autoplay: true,
        margin: 20,
        nav: false,
        // navText: ["<i class='czi-arrow-left'></i>","<i class='czi-arrow-right'></i>"],
        dots: false,
        autoplayHoverPause: true,
        'ltr': true,
        // center: true,
        responsive: {
            //X-Small
            0: {
                items: 3
            },
            360: {
                items: 3.2
            },
            375: {
                items: 3.5
            },
            540: {
                items: 4
            },
            //Small
            576: {
                items: 5
            },
            //Medium
            768: {
                items: 6
            },
            //Large
            992: {
                items: 8
            },
            //Extra large
            1200: {
                items: 10
            },
            //Extra extra large
            1400: {
                items: 11
            }
        }
    })
    
    // Others Store Slider
    const othersStore = $(".others-store-slider").owlCarousel({
        responsiveClass: true,
        nav: false,
        dots: false,
        loop: true,
        autoplay: true,
        autoplayTimeout: 5000,
        autoplayHoverPause: true,
        smartSpeed: 600,
        rtl: false,
        responsive: {
            0: {
                items: 1.3,
                margin: 10,
            },
            480: {
                items: 2,
                margin: 26,
            },
            768: {
                items: 2,
                margin: 26,
            },
            992: {
                items: 3,
                margin: 26,
            },
            1200: {
                items: 4,
                margin: 26,
            },
        },
    });
    $(".store-next").on("click", function () {
        othersStore.trigger("next.owl.carousel", [600]);
    });
    $(".store-prev").on("click", function () {
        othersStore.trigger("prev.owl.carousel", [600]);
    });
    
document.addEventListener("DOMContentLoaded", () => {
    const nav_element = document.getElementById("mobile_nav")
    const close_btn = document.getElementById("close_btn")

    close_btn.addEventListener("click", ()=> {
        nav_element.classList.add("hidden")
    })
});

$(document).ready(function() {
    // Toggle the visibility of the next element with the class 'category-list'
    $('.open-category').on('click', function(e) {
        e.preventDefault(); // Prevent the default action
        e.stopPropagation(); // Stop the event from propagating to parent elements

        $(this).closest('.category-name').next('.category-list').toggleClass('hidden');
        $(this).toggleClass('-rotate-90');
    });
});

function myFunction() {
        $('#anouncement').slideUp(300);
    }
    $(".category-menu").find(".mega_menu").parents("li").addClass("has-sub-item").find("> a").append("<i class='czi-arrow-right'></i>");

    $('.category-menu-toggle-btn').on('click', function() {
        $('.megamenu-wrap').toggleClass('show')
    });

    $('.navbar-tool-icon-box').on('click', function() {
        $('.megamenu-wrap').removeClass('show')
    })

    $('#hamburger_menu').on('click', function() {
        $('#mobile_nav').removeClass('hidden')
    })

    // mega menu will remove when window reload
    $(window).on('scroll', function() {
        $('.megamenu-wrap').removeClass('show')
    });


<script src="https://medplus.ng/app/jsx/jquery.marquee.min.js"></script>



$('.close-search-form-mobile').on('click', function(){
        $('.search-form-mobile').removeClass('active')
    })
    $('.open-search-form-mobile').on('click', function(){
        $('.search-form-mobile').addClass('active')
    });


$('.marqueex').marquee({
    speed: 5000,
gap: 50,
delayBeforeStart: 0,
direction: 'left',
duplicated: true,
pauseOnHover: true
});




 $('#processText').hide();

function customRequestOpen(){
    $('#customRequestCall').modal('show');
};

var pBag = "";
function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            $('#productImage').attr('src', e.target.result);
            //$('#base').val(e.target.result);
            pBag = e.target.result;
        };
        reader.readAsDataURL(input.files[0]);
    }
};

function submitCustomData(){


    var pImage = pBag;


    var name = $('#name').val();
    var email = $('#email').val();
    var phone = $('#phone').val();
    var product = $('#product').val();
    var quantity = $('#quantity').val();

    if(name == null || name == "" ){
        toastr.error("Requester Name is mandatory", { CloseButton: true, ProgressBar: true });
        $('#name').attr("style", "border-width: medium; border-color: pink;");
        return false
    }

    if(email == null || email == "" ){
        toastr.error("Requester Email is mandatory", { CloseButton: true, ProgressBar: true });
        $('#email').attr("style", "border-width: medium; border-color: pink;");
        return false
    }

    if(phone == null || phone == "" ){
        toastr.error("Mobile Number is mandatory", { CloseButton: true, ProgressBar: true });
        $('#phone').attr("style", "border-width: medium; border-color: pink;");
        return false
    }

    if(product == null || product == "" ){
        toastr.error("Product Name is mandatory", { CloseButton: true, ProgressBar: true });
        $('#product').attr("style", "border-width: medium; border-color: pink;");
        return false
    }

    if(quantity == null || quantity == "" ){
        toastr.error("Product Quantity is mandatory", { CloseButton: true, ProgressBar: true });
        $('#quantity').attr("style", "border-width: medium; border-color: pink;");
        return false
    }
    $('#submitCustomBtn').hide();
    $('#processText').show();

    const settings = {
        "async": true,
        "crossDomain": true,
        "url": "https://medplusnig.com/service/mother",
        "method": "POST",
        "headers": {
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "insomnia/2023.5.8"
        },
        "data": {
            "condition": "customRequest",
            "name_of_customer": $('#name').val(),
            "phone_no": $('#phone').val(),
            "email": $('#email').val(),
            "name_of_product": $('#product').val(),
            "quantity": $('#quantity').val(),
            "productImage": pImage,
            "status": "pending",
            "note": $('#note').val(),
        }
    };

    $.ajax(settings).done(function (answer){
        toastr.success("Sent Successfully", { CloseButton: true, ProgressBar: true })

        $('#submitCustomBtn').show();
        $('#processText').hide();

        $('#customRequestCall').modal('hide');
        $('#name').val('');
        $("#name").removeAttr("style", "border-width: medium; border-color: pink;");

        $('#phone').val('');
        $("#phone").removeAttr("style", "border-width: medium; border-color: pink;");

        $('#email').val('');
        $("#email").removeAttr("style", "border-width: medium; border-color: pink;");

        $('#note').val('');
        $("#note").removeAttr("style", "border-width: medium; border-color: pink;");

        $('#product').val('');
        $("#product").removeAttr("style", "border-width: medium; border-color: pink;");

        $('#quantity').val('');
        $("#quantity").removeAttr("style", "border-width: medium; border-color: pink;");

        $('#productImage').val('');
        $("#productImage").removeAttr("style", "border-width: medium; border-color: pink;");

        }).fail(function(jqXHR, textStatus, errorThrown) {

        console.error(JSON.stringify(jqXHR + " | " + textStatus + " | " + errorThrown))

        toastr.error("Sent failed! try again " + JSON.stringify(err), {
            CloseButton: true,
            ProgressBar: true
        });

        $('#processText').show();


        $('#submitCustomBtn').show();
        $('#processText').hide();


        $('#customRequestCall').modal('hide');
        $('#name').val('');
        $("#name").removeAttr("style", "border-width: medium; border-color: pink;");

        $('#phone').val('');
        $("#phone").removeAttr("style", "border-width: medium; border-color: pink;");

        $('#product').val('');
        $("#product").removeAttr("style", "border-width: medium; border-color: pink;");

        $('#quantity').val('');
        $("#quantity").removeAttr("style", "border-width: medium; border-color: pink;");

        $('#productImage').val('');
        $("#productImage").removeAttr("style", "border-width: medium; border-color: pink;");


    });

}