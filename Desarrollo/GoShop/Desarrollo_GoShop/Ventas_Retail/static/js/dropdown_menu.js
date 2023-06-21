document.getElementById("icon-bars").addEventListener("click", open_menu);
document.getElementById("back_menu").addEventListener("click", close_menu);

const icon_bars = document.getElementById("icon-bars");
const nav_menu_mobile = document.getElementById("nav-menu-mobile");
const nav_menu_dropdown = document.getElementById("nav_menu__dropdown");
const back_menu = document.getElementById("back_menu");

function open_menu(){
    back_menu.style.display = "block";
    icon_bars.style.display = "none";
    nav_menu_dropdown.style.width = "30%";
    nav_menu_dropdown.style.right = "0px";
    nav_menu_mobile.style.display = "none";
}

function close_menu(){
    nav_menu_mobile.style.display = "flex";
    icon_bars.style.display = "flex";
    back_menu.style.display = "none";
    nav_menu_dropdown.style.right = "-30%";
}