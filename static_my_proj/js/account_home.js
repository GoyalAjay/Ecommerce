$(document).ready(function()
{
    $('#toTopBtn').click(function()
    {
        $("html, body").animate(
        {
            scrollTop: 0
        }, 1000);
        return false;
    });
});