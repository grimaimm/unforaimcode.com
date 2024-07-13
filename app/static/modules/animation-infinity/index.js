const scrollers = document.querySelectorAll(".scroller");

if (!window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    addAnimation();
}

function addAnimation() {
    scrollers.forEach((scroller) => {
        scroller.setAttribute("data-animated", true);

        const scrollerInner = scroller.querySelector(".scroller__inner");
        const scrollerContent = Array.from(scrollerInner.children);

        // Clone semua item di dalam scroller dan tambahkan sebagai duplikat
        scrollerContent.forEach((item) => {
            const duplicatedItem = item.cloneNode(true);
            duplicatedItem.setAttribute("aria-hidden", true);
            scrollerInner.appendChild(duplicatedItem);
        });

        // Animasi scroller
        const animationDuration = getComputedStyle(scrollerInner).getPropertyValue('--_animation-duration') || '40s'; // Durasi animasi default jika variabel tidak ada
        const animationDirection = getComputedStyle(scroller).getPropertyValue('--_animation-direction') || 'forwards'; // Arah animasi default jika variabel tidak ada

        scrollerInner.style.animation = `scroll ${animationDuration} ${animationDirection} linear infinite`;
    });
}
