window.innerWidth < 768 &&
  [].slice
    .call(document.querySelectorAll("[data-bss-disabled-mobile]"))
    .forEach(function (e) {
      e.classList.remove("animated"),
        e.removeAttribute("data-bss-hover-animate"),
        e.removeAttribute("data-aos"),
        e.removeAttribute("data-bss-parallax-bg"),
        e.removeAttribute("data-bss-scroll-zoom");
    }),
  document.addEventListener("DOMContentLoaded", function () {}, !1);
