$(document).ready(function(){

    var stripeFormModule = $(".stipe-payment-form")
    var stripeModuleToken = stripeFormModule.attr("data-token")
    var stripeModuleNextUrl = stripeFormModule.attr("data-next-url")
    var stripeModuleBtnTitle = stripeFormModule.attr("data-btn-title") || "Add Card"

    var stripeTemplate = $.templates("#stripeTemplate")
    var stripeTemplateDataContext = {
        publishKey: stripeModuleToken,
        nextUrl: stripeModuleNextUrl,
        btnTitle: stripeModuleBtnTitle
    }

    var stripeTemplateHtml = stripeTemplate.render(stripeTemplateDataContext)
    stripeFormModule.html(stripeTemplateHtml)

    var paymentForm = $(".payment-form")
    if (paymentForm.length > 1)
    {
        alert("Only one payment form is allowed per page")
        paymentForm.css('display','none')
    }

    else if (paymentForm.length == 1)
    {
        var pubKey = paymentForm.attr("data-token");
        var nextUrl = paymentForm.attr("data-next-url")


        var stripe = Stripe(pubKey);
        var elements = stripe.elements();
        var style = {
            base: {
                color: "#32325d",
                fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
                fontSmoothing: "antialiased",
                fontSize: "16px",
                "::placeholder": {
                    color: "#aab7c4"
                }
            },
            invalid: {
                color: "#fa755a",
                iconColor: "#fa755a"
            }
        };

        var card = elements.create("card", { style: style });
        card.mount("#card-element");

        
        card.addEventListener('change', function(event)
        {
            var displayError = document.getElementsById('card-errors');
            if (event.error)
            {
                displayError.textContent = event.error.message;
            }
            else
            {
                displayError.textContent = '';
            }
        });

        // var form = document.getElementById("payment-form");
        // form.addEventListener('submit', function(event)
        // {
        //     event.preventDefault();
        //     //get the btn
        //     //new btn UI
        //     var loadTime = 1500
        //     var errorHtml = "<i class='fa fa-warning'></i>An error occured"
        //     var errorClasses = "btn btn-danger disabled my-3"
        //     var loadingHtml = "<i class='fa fa-spin fa-spinner'></i>Loding....."
        //     var loadingClasses = "btn btn-success disabled my-3"

        //     stripe.createToken(card).then(function(result)
        //     {
        //         if (result.error)
        //         {
        //             var errorElement = document.getElementsById('card-errors');
        //             errorElement.textContent = event.error.message;
        //         }
        //         else
        //         {
        //             stripeTokenHandler(nextUrl ,result.token)
        //         }
        //     });
        // });


        var form = $("#payment-form");
        var btnLoad = form.find(".btn-load");
        var btnLoadDefaultHtml = btnLoad.html();
        console.log(btnLoadDefaultHtml)
        var btnLoadDefaulClasses = btnLoad.attr("class");

        form.on('submit', function(event)
        {
            event.preventDefault();
            //get the btn
            var $this = $(this)
            var btnLoad = $this.find(".btn-load")
            btnLoad.blur()
            //Display new btn UI
            var loadTime = 1500
            var currentTimeout;
            var errorHtml = "<i class='fa fa-warning'></i>An error occured"
            var errorClasses = "btn btn-danger disabled my-3"
            var loadingHtml = "<i class='fa fa-spin fa-spinner'></i>&nbsp;Loading....."
            var loadingClasses = "btn btn-success disabled my-3"

            stripe.createToken(card).then(function(result)
            {
                if (result.error)
                {
                    var errorElement = $('#card-errors');
                    errorElement.textContent = event.error.message;
                    currentTimeout = displayBtnStatus(
                                        btnLoad, 
                                        errorHtml, 
                                        errorClasses, 
                                        1000, 
                                        currentTimeout)
                }
                else
                {
                    currentTimeout = displayBtnStatus(
                                        btnLoad, 
                                        loadingHtml, 
                                        loadingClasses, 
                                        2000, 
                                        currentTimeout)
                    stripeTokenHandler(nextUrl ,result.token)
                }
            });
        });

        function displayBtnStatus(element, newHtml, newClasses, loadTime, timeout)
        {
            if(!loadTime)
            {
                loadTime = 1500
            }
            element.html(newHtml)
            element.removeClass(btnLoadDefaulClasses)
            element.addClass(newClasses)
            return setTimeout(function()
            {
                element.html(btnLoadDefaultHtml)
                element.removeClass(newClasses)
                element.addClass(btnLoadDefaulClasses)
            }, loadTime)


        }

        function redirectToNext(nextPath, timeOut)
        {
            if(nextPath)
            {
                setTimeout(function()
                {
                    window.location.href = nextPath
                }, timeOut)
            }
        }

        function stripeTokenHandler(nextUrl, token)
        {
            var paymentMethodEndpoint = '/billing/payment-method/create/'
            var paymentFormMethod = paymentForm.attr("method")
            var data = {
                'token': token.id
            }
            $.ajax(
            {
                data: data,
                url: paymentMethodEndpoint,
                method: paymentFormMethod,
                success: function(data)
                {
                    var successMsg = data.message || "Success! Your card has been added."
                    card.clear()
                    if (nextUrl)
                    {
                        successMsg = successMsg + "<br/><br/><i class='fa fa-spin fa-spinner'></i>&nbsp;Redirecting...."
                    }
                    if ($.alert)
                    {
                        $.alert(successMsg)
                    }
                    else
                    {
                        alert(successMsg)
                    }
                    btnLoad.html(btnLoadDefaultHtml)
                    btnLoad.attr('class', btnLoadDefaulClasses)
                    redirectToNext(nextUrl, 2000)
                },
                error: function(error)
                {
                    console.log(error)
                    $.alert({title: "An error occured", content: "Please try adding your card again."})
                    btnLoad.html(btnLoadDefaultHtml)
                    btnLoad.attr('class', btnLoadDefaulClasses)
                }
            })
        }
    }
})