// // carousel essentials
// // var carousel = $(".carousel-inner")
// // var item = carousel.find("div[name='carousel']");
// // var count = item.find("input[name='counter']");

// // right scroll
// // var next = document.getElementById('right-scroll');
// // next.onclick = function()
// // {
// //     var container = document.getElementById('scroll');
// //     sideScroll(container, 'right', 25, 500, 10);
// // };
// // // left scroll
// // var prev = document.getElementById('left-scroll');
// // prev.onclick = function()
// // {
// //     var container = document.getElementById('scroll');
// //     sideScroll(container, 'left', 25, 500, 10);
// // };
// // // function for side scroll
// // function sideScroll(element, direction, speed, distance, step)
// // {
// //     scrollAmount = 0;
// //     var slideTimer = setInterval(function()
// //     {
// //         if(direction == 'left')
// //         {
// //             element.scrollLeft -= step;
// //         }
// //         else
// //         {
// //             element.scrollLeft += step;
// //         }
// //         scrollAmount += step;
// //         if(scrollAmount >= distance)
// //         {
// //             window.clearInterval(slideTimer);
// //         }
// //     }, speed)
// // };

// // for carousel
// // for (var i = 0; i < count.length; i++)
// // {
// //     if (count[i].value == 1)
// //     {
// //         $(item[i]).addClass('carousel-item active')
// //     }
// //     else
// //     {
// //         $(item[i]).addClass('carousel-item')
// //     }
// // }

// // duration of scroll animation
// var scrollDuration = 300;
// // paddles
// var leftPaddle = document.getElementsByClassName('left-paddle');
// var rightPaddle = document.getElementsByClassName('right-paddle');
// // get items dimensions
// var itemsLength = $('.item').length;
// var itemSize = $('.item').outerWidth(true);
// // get some relevant size for the paddle triggering point
// var paddleMargin = 20;

// // get wrapper width
// var getMenuWrapperSize = function()
// {
//     return $('.menu-wrapper').outerWidth();
// }
// var menuWrapperSize = getMenuWrapperSize();
// // the wrapper is responsive
// $(window).on('resize', function()
// {
//     menuWrapperSize = getMenuWrapperSize();
// });
// // size of the visible part of the menu is equal as the wrapper size 
// var menuVisibleSize = menuWrapperSize;

// // get total width of all menu items
// var getMenuSize = function()
// {
//     return itemsLength * itemSize;
// };
// var menuSize = getMenuSize();
// // get how much of menu is invisible
// var menuInvisibleSize = menuSize - menuWrapperSize;

// // get how much have we scrolled to the left
// var getMenuPosition = function()
// {
//     return $('.menu').scrollLeft();
// };

// // finally, what happens when we are actually scrolling the menu
// $('.menu').on('scroll', function()
// {

//     // get how much of menu is invisible
//     menuInvisibleSize = menuSize - menuWrapperSize;
//     // get how much have we scrolled so far
//     var menuPosition = getMenuPosition();

//     var menuEndOffset = menuInvisibleSize - paddleMargin;

//     // show & hide the paddles 
//     // depending on scroll position
//     if (menuPosition <= paddleMargin)
//     {
//         $(leftPaddle).addClass('hidden');
//         $(rightPaddle).removeClass('hidden');
//     } else if (menuPosition < menuEndOffset)
//     {
//         // show both paddles in the middle
//         $(leftPaddle).removeClass('hidden');
//         $(rightPaddle).removeClass('hidden');
//     } else if (menuPosition >= menuEndOffset)
//     {
//         $(leftPaddle).removeClass('hidden');
//         $(rightPaddle).addClass('hidden');
//     }

// });

// // scroll to left
// $(rightPaddle).on('click', function() {
//     $('.menu').animate( { scrollLeft: menuInvisibleSize}, scrollDuration);
// });

// // scroll to right
// $(leftPaddle).on('click', function() {
//     $('.menu').animate( { scrollLeft: '0' }, scrollDuration);
// });