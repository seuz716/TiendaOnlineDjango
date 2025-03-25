// scripts.js

// ✅ Configuración del widget flotante del carrito
document.addEventListener('DOMContentLoaded', () => {
    const cartWidget = document.getElementById('cart-widget');
    
    if (cartWidget) {
        cartWidget.addEventListener('click', () => {
            alert('¡Carrito abierto!');
            // Aquí podrías redirigir a la vista del carrito o abrir un modal
        });
    }
});

// ✅ Configuración de LightGallery para galería de productos
document.addEventListener('DOMContentLoaded', () => {
    const gallery = document.getElementById('product-gallery');

    if (gallery) {
        lightGallery(gallery, {
            thumbnail: true,
            animateThumb: false,
            showThumbByDefault: false,
        });
    }
});

// ✅ Ejemplo de uso de StimulusJS para interactividad ligera
import { Application } from "stimulus";
import HelloController from "./controllers/hello_controller";

const application = Application.start();
application.register("hello", HelloController);
