$( document ).ready(function() {

    var clickable_menu_selector = '#portal-globalnav li:not(#portaltab-index_html) a';
    $(clickable_menu_selector).each(function(){
        $(this).click(function() {
            
            var activated = $(this).hasClass('activated');
            var menu_id = this.parentNode.id.replace('portaltab-', '');

            if (!activated) {
                $(clickable_menu_selector).each(function(){
                    $(this).removeClass('activated');
                    $(this).parent('li').removeClass('menu-activated');
                });
                $(this).addClass('activated');
                $(this).parent('li').addClass('menu-activated');

                $('ul.sf-menu').each(function(){
                    $(this).hide();
                });
                $('#portal-globalnav-cpskinmenu-' + menu_id).show();
            } else {
                $(this).removeClass('activated');
                $(this).parent('li').removeClass('menu-activated');
                $('#portal-globalnav-cpskinmenu-' + menu_id).hide();
            }
            return false;
        })
    });
});
