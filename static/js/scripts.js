document.addEventListener('DOMContentLoaded', () => {
    initUXFeatures();
    initCart();                   // Inicializa el contador persistente del carrito
    initScrollTop();
    initDarkMode();
    initAutocomplete();
    initCategoryFilter();
    initRealTimeSearch();
    initLightGallery();

    // Nuevas mejoras de UX:
    initTooltips();                // Inicializa tooltips de Bootstrap
    initLazyLoadImages();          // Fuerza lazy load en imágenes sin el atributo
    initAutocompleteKeyboardNav(); // Mejora la navegación por teclado en el autocomplete
    initGlobalErrorHandler();      // Manejo global de errores

    // Sincroniza el contador entre pestañas
    window.addEventListener('storage', (e) => {
        if (e.key === 'cartCount') {
            updateCartCount(e.newValue);
        }
    });
});

/* Funciones originales (sin cambios importantes) */

/* Animaciones al hacer scroll */
function initUXFeatures() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
            }
        });
    }, { threshold: 0.1 });
    document.querySelectorAll('.card, footer, .navbar').forEach(el => observer.observe(el));
}

/* Dark Mode */
function initDarkMode() {
    const toggle = document.getElementById('darkModeToggle');
    const isDark = localStorage.getItem('darkMode') === 'true';
    if (isDark) document.body.classList.add('dark-mode');
    toggle.addEventListener('click', () => {
        document.body.classList.toggle('dark-mode');
        localStorage.setItem('darkMode', document.body.classList.contains('dark-mode'));
    });
}

/* Scroll to Top */
function initScrollTop() {
    const scrollButton = document.querySelector('.scroll-top');
    window.addEventListener('scroll', () => {
        scrollButton.classList.toggle('visible', window.scrollY > 300);
    });
    scrollButton.addEventListener('click', () => {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
}

/* Búsqueda en tiempo real con Autocomplete */
function initAutocomplete() {
    const searchInput = document.getElementById('globalSearch');
    const resultsContainer = document.getElementById('autocompleteResults');
    const debounce = (func, delay) => {
        let timeout;
        return (...args) => {
            clearTimeout(timeout);
            timeout = setTimeout(() => func(...args), delay);
        };
    };
    const performSearch = debounce(async (query) => {
        if (query.length < 2) {
            resultsContainer.style.display = 'none';
            return;
        }
        // Simulación de resultados:
        const fakeResults = [
            { nombre: "Producto 1", url: "/productos/1/" },
            { nombre: "Producto 2", url: "/productos/2/" },
            { nombre: "Producto 3", url: "/productos/3/" }
        ];
        resultsContainer.innerHTML = fakeResults
            .filter(item => item.nombre.toLowerCase().includes(query.toLowerCase()))
            .map(item => `<div class="autocomplete-item" tabindex="0" data-url="${item.url}">${item.nombre}</div>`)
            .join('');
        resultsContainer.style.display = 'block';
    }, 300);
    searchInput.addEventListener('input', (e) => {
        performSearch(e.target.value);
    });
    resultsContainer.addEventListener('click', (e) => {
        if (e.target.classList.contains('autocomplete-item')) {
            window.location.href = e.target.getAttribute('data-url');
        }
    });
    resultsContainer.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && e.target.classList.contains('autocomplete-item')) {
            window.location.href = e.target.getAttribute('data-url');
        }
    });
    document.addEventListener('click', (e) => {
        if (!resultsContainer.contains(e.target) && e.target !== searchInput) {
            resultsContainer.style.display = 'none';
        }
    });
}

/* Función simulada para manejo del carrito */
function initCart() {
    const cartCount = document.getElementById('cartCount');
    const savedCount = localStorage.getItem('cartCount');
    cartCount.textContent = savedCount !== null ? savedCount : '0';
}

/* Función para actualizar el contador del carrito y guardarlo en localStorage */
function updateCartCount(newCount) {
    const cartCount = document.getElementById('cartCount');
    cartCount.textContent = newCount;
    localStorage.setItem('cartCount', newCount);
}

/* Función para mostrar Toasts */
function showToast(message, type = 'success') {
    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-bg-${type} border-0`;
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">${message}</div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;
    document.querySelector('.toast-container').appendChild(toast);
    new bootstrap.Toast(toast).show();
}

/* Funciones adicionales originales */

/* LightGallery para productos */
function initLightGallery() {
    const gallery = document.getElementById('product-gallery');
    if (gallery) {
        import('https://cdnjs.cloudflare.com/ajax/libs/lightgallery-js/1.4.0/lightgallery.min.js')
            .then(module => module.default(gallery, {
                thumbnail: true,
                animateThumb: false,
                showThumbByDefault: false,
            }))
            .catch(error => console.error("Error al cargar LightGallery:", error));
    }
}

/* Filtro por Categoría */
function initCategoryFilter() {
    const filters = document.querySelectorAll('.category-filter');
    filters.forEach(filter => {
        filter.addEventListener('click', () => {
            const category = filter.getAttribute('data-category');
            window.location.href = `/productos/?category=${category}`;
        });
    });
}

/* Búsqueda en tiempo real (versión con API) */
function initRealTimeSearch() {
    const searchInput = document.getElementById('globalSearch');
    if (!searchInput) return;
    const debounce = (func, delay) => {
        let timeout;
        return (...args) => {
            clearTimeout(timeout);
            timeout = setTimeout(() => func(...args), delay);
        };
    };
    const performSearch = debounce(async (query) => {
        try {
            const response = await fetch(`/buscar/?search=${encodeURIComponent(query)}`);
            if (!response.ok) {
                throw new Error(`Error HTTP: ${response.status}`);
            }
            const data = await response.json();
            const productGrid = document.getElementById('productGrid');
            if (productGrid) {
                productGrid.innerHTML = data.results.map(product => `
                    <div class="col">
                        <div class="card h-100 shadow-sm">
                            <div class="ratio ratio-1x1">
                                <img src="${product.imagen}" 
                                     class="card-img-top object-fit-cover" 
                                     alt="${product.nombre}" loading="lazy">
                            </div>
                            <div class="card-body d-flex flex-column">
                                <h5 class="card-title fs-6">${product.nombre}</h5>
                                <p class="card-text fw-bold text-primary">$${product.precio}</p>
                            </div>
                        </div>
                    </div>
                `).join('');
            }
        } catch (error) {
            console.error('Error en la búsqueda:', error);
        }
    }, 300);
    searchInput.addEventListener('input', (e) => {
        performSearch(e.target.value);
    });
}

/* Nuevas funciones de mejoras UX (no modifican las existentes) */

/* Inicializar Tooltips de Bootstrap */
function initTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.forEach(tooltipTriggerEl => {
        new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/* Forzar Lazy Load en imágenes sin el atributo 'loading' */
function initLazyLoadImages() {
    const images = document.querySelectorAll('img:not([loading])');
    images.forEach(img => {
        img.setAttribute('loading', 'lazy');
    });
}

/* Mejora de navegación por teclado en Autocomplete */
function initAutocompleteKeyboardNav() {
    const searchInput = document.getElementById('globalSearch');
    const resultsContainer = document.getElementById('autocompleteResults');
    let currentFocus = -1;
    searchInput.addEventListener('keydown', function(e) {
        const items = resultsContainer.querySelectorAll('.autocomplete-item');
        if (!items.length) return;
        if (e.key === 'ArrowDown') {
            currentFocus++;
            addActive(items);
            e.preventDefault();
        } else if (e.key === 'ArrowUp') {
            currentFocus--;
            addActive(items);
            e.preventDefault();
        } else if (e.key === 'Enter') {
            if (currentFocus > -1 && items[currentFocus]) {
                items[currentFocus].click();
                e.preventDefault();
            }
        }
    });
    function addActive(items) {
        removeActive(items);
        if (currentFocus >= items.length) currentFocus = 0;
        if (currentFocus < 0) currentFocus = items.length - 1;
        items[currentFocus].classList.add('autocomplete-active');
    }
    function removeActive(items) {
        items.forEach(item => item.classList.remove('autocomplete-active'));
    }
}

/* Manejo global de errores para capturar excepciones no previstas */
function initGlobalErrorHandler() {
    window.addEventListener('error', (e) => {
        console.error('Error global capturado:', e.error);
        showToast('Ha ocurrido un error inesperado', 'danger');
    });
}
