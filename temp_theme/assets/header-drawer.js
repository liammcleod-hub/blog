// Mobile Menu Scroll Fix
(function() {
  if (window.innerWidth >= 750) return;
  
  function fix() {
    var drawer = document.querySelector('.menu-drawer');
    if (drawer) {
      drawer.style.setProperty('--drawer-height', '85dvh');
      drawer.style.height = '85dvh';
    }
  }
  
  fix();
  setTimeout(fix, 200);
  
  var details = document.getElementById('Details-menu-drawer-container');
  if (details) {
    new MutationObserver(fix).observe(details, { attributes: true, attributeFilter: ['open', 'class'] });
  }
})();
