$(document).ready(function(){
    $('.prayed-for-button').click(function() {
        var prayerID = $(this).attr('prayerID');
        prayedFor(prayerID)
    });

    function prayedFor(prayer_id){
        $.ajax({
            type: "POST",
            url: "/prayed_for/" + prayer_id,
            success: function(msg) {
                $('.prayed-for-' + prayer_id).text("Prayed for: " + msg.prayer_count + " times")
            }
        });
      return false;
    }

    var elem = document.querySelector('.masonry-grid');
    var $grid = $('.masonry-grid').masonry({
     // options
        itemSelector: 'none',
        columnWidth: 50,
        fitWidth: true,
        stagger: 30,
        visibleStyle: {
            transform: 'translateY(0)',
            opacity: 1
        },
        hiddenStyle: {
            transform: 'translateY(100px)',
            opacity: 0,
        }
    });

    var msnry = $grid.data('masonry');

    imagesLoaded( '.masonry-grid', function() {
        msnry.options.itemSelector = '.masonry-grid-item'; // select proper items
        document.querySelector('.masonry-grid').classList.add('are-images-ready');
        var items = document.querySelectorAll('.masonry-grid-item');
        msnry.appended( items );
        msnry.layout()
    });

    $('.masonry-grid').infiniteScroll({
        append: '.masonry-grid-item',
        path: "a.js-infinite-navigation-l",
        debug: true,
        outlayer: msnry,
        status: '.page-load-status',
        elementScroll: '.mdl-layout__content'
    });
});