$(document).ready(function()
{
  //Contact Form Handler
  var contactForm = $(".contact-form")
  var contactFormMethod = contactForm.attr("method")
  var contactFormEndpoint = contactForm.attr("action")
  
  function displaySubmitting(submitBtn, defaultText, doSubmit)
  {
    if(doSubmit)
    {
      submitBtn.addClass("disabled")
      submitBtn.html("<i class='fa fa-spin fa-spinner'></i> Sending...")
    }
    else
    {
      submitBtn.removeClass("disabled")
      submitBtn.html(defaultText)
    }
  }

  contactForm.submit(function(event)
  {
    event.preventDefault()

    var contactFormSubmitBtn = contactForm.find("[type='submit']")
    var contactFormSubmitBtnTxt = contactFormSubmitBtn.text()

    var contactFormData = contactForm.serialize()
    displaySubmitting(contactFormSubmitBtn, "", true)
    $.ajax(
    {
      method: contactFormMethod,
      url: contactFormEndpoint,
      data: contactFormData,
      success: function(data)
      {
        contactForm[0].reset()
        $.alert({
          title: "Success!",
          content: data.message,
          theme: "modern",
        })
        setTimeout(function()
        {
          displaySubmitting(contactFormSubmitBtn, contactFormSubmitBtnTxt, false)
        }, 500)
      },
      error: function(error)
      {
        console.log(error.responseJSON)
        var jsonData = error.responseJSON
        var msg = ""
        $.each(jsonData, function(key, value)
        {
          msg += key + " : " + value[0].message + "<br/>"
        })

        $.alert({
          title: "Oops!",
          content: msg,
          theme: "modern",
        })
        setTimeout(function()
        {
          displaySubmitting(contactFormSubmitBtn, contactFormSubmitBtnTxt, false)
        }, 500)
      }
    })
  })


  // Auto Search
  var searchForm = $(".search-form")
  var searchInput = searchForm.find("[name='q']")
  var typingTimer;
  var typingInterval = 1000 //2 seconds
  var searchBtn = searchForm.find("[type='submit']")

  searchInput.keyup(function(event)
  {
    //key released
    clearTimeout(typingTimer)
    typingTimer = setTimeout(performSearch, typingInterval)
  })

  searchInput.keydown(function(event)
  {
    //key pressed
    clearTimeout(typingTimer)
  })

  function displaySearching()
  {
    searchBtn.addClass("disabled")
    searchBtn.html("<i class='fa fa-spin fa-spinner'></i> Searching...")
  }

  function performSearch()
  {
    displaySearching()
    var query = searchInput.val()
    setTimeout(function()
    {
      window.location.href='/search/?q='+query
    }, 1000)
    
  }

  //Cart + Add Products
  var productForm = $(".form-product-ajax")

  function getOwnedProduct(productId, submitSpan)
  {
    var actionEndpoint = '/orders/endpoint/verify/ownership/';
    var httpMethod = 'GET';
    var data = {
      product_id: productId
    }
    var isOwner;
    $.ajax(
    {
      url: actionEndpoint,
      method: httpMethod,
      data: data,
      success: function(data)
      {
        if(data.owner)
        {
          isOwner = true
          submitSpan.html("<a class='btn btn-primary card-button' href='/library/'>In Library</a>")
        }
        else
        {
          isOwner = false
        }
      },
      error: function(error)
      {
        console.log(error)
      }
    })
    return isOwner;
  }

  $.each(productForm, function(index, object)
  {
    var $this = $(this)
    var isUser = $this.attr("data-user")
    var submitSpan = $this.find(".submit-span")
    var productInput = $this.find("[name='product_id']")
    var productId = productInput.attr("value")
    var productIsDigital = productInput.attr("data-is-digital")
    if(productIsDigital && isUser)
    {
      var isOwned=getOwnedProduct(productId, submitSpan);
    }
  });

  productForm.submit(function(event)
  {
      
    event.preventDefault();
    var thisForm = $(this)
    //var actionEndpoint = thisForm.attr("action");
    var actionEndpoint = thisForm.attr("data-endpoint");
    var httpMethod = thisForm.attr("method");
    var formData = thisForm.serialize();

    $.ajax(
    {
      url: actionEndpoint,
      method: httpMethod,
      data: formData,
      success: function(data)
      {
        var submitSpan = thisForm.find(".submit-span")
        if (data.added)
        {
          submitSpan.html("<button class='btn btn-danger card-button'>Remove</button>")
        }
        else
        {
          submitSpan.html("<button type='submit' class='btn btn-success card-button'>Add to cart</button>")
        }
        var navbarCount = $(".navbar-cart-count")
        navbarCount.text(data.cartItemCount)
        var curentPath = window.location.href

        if (curentPath.indexOf("cart") != -1)
        {
          refreshCart()
        }
      },
      error: function(errorData)
      {
        $.alert({
          title: "Oops!",
          content: "An error occurred",
          theme: "modern",
        })
      }
    })
  })

  function refreshCart()
  {
    console.log("in current cart")
    var cartTable = $(".cart-table")
    var cartBody = cartTable.find(".cart-body")
    //cartBody.html("<h1>Changed</h1>")
    var productRows = cartBody.find(".cart-products")
    var currentUrl = window.location.href

    var refreshCartUrl = '/api/cart/'
    var refreshCartMethod = "GET";
    var data = {};
    $.ajax(
    {
      url: refreshCartUrl,
      method: refreshCartMethod,
      data: data,
      success: function(data)
      {
        var hiddenCartItemRemoveForm = $(".cart-item-remove-form")
        if (data.products.length > 0)
        {
          productRows.html("")
          var productTitle = cartBody.find(".title")
          i = data.products.length
          $.each(data.products, function(index, value)
          {
            console.log(value)
            var newCartItemRemove = hiddenCartItemRemoveForm.clone()
            newCartItemRemove.css("display", "block")
            //newCartItemRemove.removeClass("hidden-class")
            newCartItemRemove.find(".cart-item-product-id").val(value.id)
            if (value.image != null)
            {
              cartBody.prepend("<tr><th scope=\'row\'><div class='my-3'>" + i + "</div></th><td><div class='p-0'><img src='/media/" + value.image + "' class='img-fuild mx-4' height='94px' width='94px'></div></td><td><a href='" + value.url + "'><b style='color:black; font-size:25px; text-decoration:none !important;'>" + value.name + "</b></a>" + newCartItemRemove.html() + "</td><td></td><td>" + value.price + "</td></tr>")
            }
            else
            {
              cartBody.prepend("<tr><th scope=\'row\'><div class='my-3'>" + i + "</div></th><td></td><td><a href='" + value.url + "'>" + value.name + "</a></td><td>" + value.price + "</td></tr>")
            }
            
            i --
          })
          
          cartBody.find(".cart-subtotal").text(data.subtotal)
          cartBody.find(".cart-total").text(data.total)
        }
        else
        {
          window.location.href = currentUrl
        }
      },
      error: function(errorData)
      {
        $.alert({
          title: "Oops!",
          content: "An error occurred",
          theme: "modern",
        })
      }
    })
  }
})