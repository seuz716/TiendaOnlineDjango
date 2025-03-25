/* scripts.js */
document.addEventListener('DOMContentLoaded', () => {
    initCartWidget();
    updateCartCount();
    initCategoryFilter();

    // Cargar LightGallery solo si existe la galería
    const gallery = document.getElementById('product-gallery');
    if (gallery) {
        import('https://cdnjs.cloudflare.com/ajax/libs/lightgallery-js/1.4.0/lightgallery.min.js')
            .then(module => module.default(gallery, {
                thumbnail: true,
                animateThumb: false,
                showThumbByDefault: false,
            }));
    }
});

async function updateCartCount() {
    try {
        const response = await fetch('/api/cart/count/');
        const data = await response.json();
        document.getElementById('cart-count').textContent = data.count;
        setTimeout(updateCartCount, 30000);
    } catch (error) {
        console.error('Error al actualizar el carrito:', error);
    }
}

function initCartWidget() {
    document.querySelectorAll('.add-to-cart').forEach(button => {
        button.addEventListener('click', async () => {
            const productId = button.getAttribute('data-id');
            try {
                const response = await fetch(`/api/cart/add/${productId}/`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                });
                if (response.ok) {
                    updateCartCount();
                }
            } catch (error) {
                console.error('Error al agregar al carrito:', error);
            }
        });
    });
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

// Búsqueda en tiempo real
document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('globalSearch');
    const productGrid = document.getElementById('productGrid');
    
    const debounce = (func, delay) => {
        let timeout;
        return (...args) => {
            clearTimeout(timeout);
            timeout = setTimeout(() => func.apply(this, args), delay);
        };
    };

    const performSearch = debounce(async (query) => {
        try {
            const response = await fetch(`/api/productos/?search=${encodeURIComponent(query)}`);
            const data = await response.json();
            
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
                            <!-- Botones de acción -->
                        </div>
                    </div>
                </div>
            `).join('');
        } catch (error) {
            console.error('Error en la búsqueda:', error);
        }
    }, 300);

    searchInput.addEventListener('input', (e) => {
        performSearch(e.target.value);
    });
});