// Langkah alur berganti mengikuti posisi scroll di dalam section #alur (panel menempel/sticky).
// Klik langkah = scroll ke posisinya. Gerak minimal tetap berganti langkah, hanya animasi yang mati (lewat CSS).
(function () {
  var track = document.querySelector("[data-track]");
  if (!track) return;
  var tabs = track.querySelectorAll("[role=tab]"), scenes = track.querySelectorAll(".scene");
  var n = scenes.length, current = -1;
  function show(k) {
    if (k === current) return;
    current = k;
    tabs.forEach(function (t, i) { t.setAttribute("aria-selected", i === k ? "true" : "false"); });
    scenes.forEach(function (s, i) {
      s.classList.remove("on");
      s.setAttribute("aria-hidden", i === k ? "false" : "true");
      if (i === k) { void s.offsetWidth; s.classList.add("on"); } // reflow agar animasi adegan diulang
    });
  }
  function span() { return track.offsetHeight - window.innerHeight; }
  function onScroll() {
    var p = (window.scrollY - track.offsetTop) / Math.max(1, span());
    show(Math.min(n - 1, Math.max(0, Math.floor(p * n))));
  }
  tabs.forEach(function (t, i) {
    t.addEventListener("click", function () {
      window.scrollTo({ top: track.offsetTop + span() * (i + 0.5) / n, behavior: "smooth" });
      show(i);
    });
  });
  window.addEventListener("scroll", onScroll, { passive: true });
  window.addEventListener("resize", onScroll);
  onScroll();
})();
