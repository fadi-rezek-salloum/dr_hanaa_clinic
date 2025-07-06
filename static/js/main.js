(function () {
	"use strict";

	window.onload = function () {
		window.setTimeout(fadeout, 500);

		// Initialize WOW.js safely
		if (typeof WOW !== "undefined") {
			new WOW().init();
		} else {
			console.warn("WOW.js is not loaded");
		}
	};

	function fadeout() {
		const preloader = document.querySelector(".preloader");
		if (preloader) {
			preloader.style.opacity = "0";
			preloader.style.display = "none";
		}
	}

	// Sticky Header and Scroll-to-Top
	window.onscroll = function () {
		const header_navbar = document.querySelector(".navbar-area");
		if (header_navbar) {
			const sticky = header_navbar.offsetTop;
			if (window.pageYOffset > sticky) {
				header_navbar.classList.add("sticky");
			} else {
				header_navbar.classList.remove("sticky");
			}
		}

		const backToTo = document.querySelector(".scroll-top");
		if (backToTo) {
			if (
				document.body.scrollTop > 50 ||
				document.documentElement.scrollTop > 50
			) {
				backToTo.style.display = "block";
			} else {
				backToTo.style.display = "none";
			}
		}
	};

	// Initialize Tiny Slider if available
	if (typeof tns === "function") {
		tns({
			container: ".slider-active",
			items: 1,
			slideBy: "page",
			autoplay: true,
			mouseDrag: true,
			gutter: 0,
			nav: true,
			controls: false,
			autoplayButtonOutput: false,
		});
	} else {
		console.warn("Tiny Slider is not available");
	}

	// Smooth Scroll
	const pageLinks = document.querySelectorAll(".page-scroll");

	pageLinks.forEach((elem) => {
		elem.addEventListener("click", (e) => {
			e.preventDefault();
			const target = document.querySelector(elem.getAttribute("href"));
			if (target) {
				target.scrollIntoView({
					behavior: "smooth",
				});
			}
		});
	});

	// Section active menu on scroll
	function onScroll() {
		const scrollPos =
			window.pageYOffset ||
			document.documentElement.scrollTop ||
			document.body.scrollTop;

		pageLinks.forEach((currLink) => {
			const val = currLink.getAttribute("href");
			const refElement = document.querySelector(val);
			const scrollTopMinus = scrollPos + 73;

			if (
				refElement &&
				refElement.offsetTop <= scrollTopMinus &&
				refElement.offsetTop + refElement.offsetHeight > scrollTopMinus
			) {
				pageLinks.forEach((link) => link.classList.remove("active"));
				currLink.classList.add("active");
			}
		});
	}
	document.addEventListener("scroll", onScroll);

	// Navbar toggler
	const navbarToggler = document.querySelector(".navbar-toggler");
	const navbarCollapse = document.querySelector(".navbar-collapse");

	if (navbarToggler && navbarCollapse) {
		pageLinks.forEach((e) =>
			e.addEventListener("click", () => {
				navbarToggler.classList.remove("active");
				navbarCollapse.classList.remove("show");
			})
		);

		navbarToggler.addEventListener("click", function () {
			navbarToggler.classList.toggle("active");
		});
	}
})();
