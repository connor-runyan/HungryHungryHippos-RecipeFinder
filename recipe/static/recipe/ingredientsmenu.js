'use strict'

$(document).ready(function() {
  let COLLAPSED_SRC = "http://icons.iconarchive.com/icons/awicons/vista-artistic/128/add-icon.png";
  let EXPANDED_SRC = "https://cdn1.iconfinder.com/data/icons/basic-ui-elements-color/700/07_minus-128.png";

  updateImage($(".update-on-expand"), COLLAPSED_SRC);

  $(".update-on-expand").on('show.bs.collapse', function() {
    updateImage($(this), EXPANDED_SRC);
  });

  $(".update-on-expand").on('hide.bs.collapse', function() {
    updateImage($(this), COLLAPSED_SRC);
  });

  function updateImage(div, src) {
    div.siblings().find(".update-image").attr("src", src);
  };
});
