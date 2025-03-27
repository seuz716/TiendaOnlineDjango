/* scripts.js */
/* scripts.js */
document.addEventListener('DOMContentLoaded', () => {
    initCategoryFilter();
    initRealTimeSearch();
    initLightGallery();
});

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



function initCategoryFilter() {
    const filters = document.querySelectorAll('.category-filter');
    filters.forEach(filter => {
        filter.addEventListener('click', () => {
            const category = filter.getAttribute('data-category');
            window.location.href = `/productos/?category=${category}`;
        });
    });
}

function initRealTimeSearch() {
    const searchInput = document.getElementById('globalSearch');
    if (!searchInput) return;

    // Función debounce para limitar la cantidad de peticiones
    const debounce = (func, delay) => {
        let timeout;
        return (...args) => {
            clearTimeout(timeout);
            timeout = setTimeout(() => func(...args), delay);
        };
    };

    const performSearch = debounce(async (query) => {
        try {
            // Se usa la ruta /buscar/ definida en tus urls
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
                                     alt="${product.nombre}">
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
