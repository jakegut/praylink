$(document).ready(function(){
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

    $('.delete-prayer').click(function() {
        if(confirm("Do you want to delete this prayer?")){
            var prayerID = $(this).attr('prayerID');
            deletePrayer(prayerID)
        }
    });
    

    function deletePrayer(prayerID){
        $.ajax({
            type: "POST",
            url: "/admin/delete/" + prayerID,
            success: function(msg) {
                showBar(msg.message)
                $('.prayer-row-' + msg.prayer_id).remove()
            },
            error: function(request, status, error){
                showBar("Prayer did not delete successfully.")
            }
        })
    }

    var elem = document.querySelector('.masonry-grid');
    var $grid = $('.masonry-grid').masonry({
     // options
        itemSelector: 'none',
        columnWidth: 45,
        gutter: 5,
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

    var dialog = document.querySelector('dialog');
    if (! dialog.showModal) {
        dialogPolyfill.registerDialog(dialog);
    }
    dialog.querySelector('.report-button').addEventListener('click', function() {
        var prayerID = $("#prayer-text-report").attr("prayer-id")
        $.ajax({
            type: "POST",
            url: "/report/" + prayerID,
            success: function(msg) {
                showBar(msg.message);
            },
            error: function(request, status, error){
                showBar("Prayer was not reported successfully.");
            }
        });
        dialog.close();
    });
    dialog.querySelector('.close').addEventListener('click', function() {
        dialog.close();
    });

    imagesLoaded( '.masonry-grid', function() {
        msnry.options.itemSelector = '.masonry-grid-item'; // select proper items
        document.querySelector('.masonry-grid').classList.add('are-images-ready');
        var items = document.querySelectorAll('.masonry-grid-item');
        msnry.appended( items );
        msnry.layout();
    });

    $('.masonry-grid').infiniteScroll({
        append: '.masonry-grid-item',
        path: "a.js-infinite-navigation-l",
        debug: true,
        history: false,
        outlayer: msnry,
        status: '.page-load-status',
        elementScroll: '.mdl-layout__content'
    });

    // function showReportModal(element){
    //     console.log(element.getAttribute("prayer-id"))
    // }

    function attachReportClickEvent(){
        $(".report-prayer").unbind();
        $(".report-prayer").click(function (){
            console.log("clicked!")
            var prayerID = this.getAttribute("prayer-id");
            var prayerText = $("#prayer-" + prayerID).text();
            $("#prayer-text-report").text(prayerText);
            $("#prayer-text-report").attr("prayer-id", prayerID);
            dialog.showModal();
        });
    }

    function reportPrayer(element){
        
    }

    function attachPrayedForButtons(){
        $('.prayed-for-button').unbind();
        $('.prayed-for-button').click(function() {
            var prayerID = $(this).attr('prayerID');
            prayedFor(prayerID)
        });
    }

    function attachButtons(){
        attachReportClickEvent();
        attachPrayedForButtons();
    }

    attachButtons();

    $('.masonry-grid').on( 'append.infiniteScroll', function( event, response, path, items ) {
        attachButtons();
        componentHandler.upgradeAllRegistered();
        console.log("new stuff");
    });
      
    function showBar(message){
        var snackbarContainer = document.querySelector('#demo-toast-example');
        var data = {message: message};
        snackbarContainer.MaterialSnackbar.showSnackbar(data);
    }
});