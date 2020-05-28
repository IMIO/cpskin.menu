$( document ).ready(function() {

    var clickable_menu_selector = '#portal-globalnav li:not(#portaltab-index_html) a';
    $(clickable_menu_selector).each(function(){
        var set_focus = function(element) {
          element.attr("tabindex", -1).focus();
          element.get(0).focus();
        };

        $(this).click(function() {
            var activated = $(this).hasClass('activated');
            var menu_id = this.parentNode.id.replace('portaltab-', '');
            var submenu_id = '#portal-globalnav-cpskinmenu-' + menu_id;

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
                $(submenu_id).show();
                set_focus($(submenu_id));
            } else {
                $(this).removeClass('activated');
                $(this).parent('li').removeClass('menu-activated');
                $(submenu_id).hide();
            }
            return false;
        })
    });

});
