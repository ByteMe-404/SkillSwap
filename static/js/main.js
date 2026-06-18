document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('.ss-alert[id^="flash-"]').forEach(function (el) {
    setTimeout(function () {
      el.style.transition = 'opacity .4s';
      el.style.opacity = '0';
      setTimeout(() => el.remove(), 200);
    }, 2000);
  });
});
