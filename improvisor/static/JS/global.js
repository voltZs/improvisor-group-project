function scrollTo(element_id) {
    var element = document.getElementById(element_id);
    window.scroll({
        // 45px offset due to navigation bar etc.
        top: element.getBoundingClientRect().top + window.scrollY - 45,
        left: 0,
        behavior: 'smooth'
    });
}