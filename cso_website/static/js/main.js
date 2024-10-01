// Get the navbar
var navbar = document.querySelector('.navbar');
var navbar_header = document.querySelector('.navbar-header');
// Get the offset position of the navbar
var sticky = navbar.offsetTop;
// Function to add/remove fixed class
function fixNavbar() {
  if (window.scrollY >= sticky) {
    navbar.classList.add('navbar-fixed');
  } else {
    navbar.classList.remove('navbar-fixed');
  }
}
// Call fixNavbar() when the page is scrolled
window.onscroll = function() {
  fixNavbar();
};
