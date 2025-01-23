// Array to hold all photos, current index, token for continuation, and loading flag
let photos = [];
let currentIndex = 0;
let nextToken = null;
let isLoading = false;
let zoomLevel = 1;
let limit = 12;
let offset = 0;
let totalPhotos = 0;

/**
 * Function to calculate the limit of photos to load based on the current window size.
 * This allows dynamically changing the number of photos loaded depending on screen size.
 * @returns {number} The limit of photos to load.
 */
function calculateLimit() {
    const screenHeight = $(window).height();  // Высота окна
    const cardHeight = 250;  // Высота карточки
    const cardsPerRow = Math.floor($('#gallery').width() / 250);  // Number of cards in a row
    const rowsPerScreen = Math.ceil(screenHeight / cardHeight);  // Number of rows in a window
    return Math.max(cardsPerRow * rowsPerScreen * 3, 12);  // 10 images minimum
}

/**
 * Function to load photos from the server.
 * New photos are automatically loaded when the bottom of the page is reached.
 */
function loadPhotos() {
    if (isLoading) return;  // Если идет загрузка, не делаем запросы

    isLoading = true;
    $('#loading').show();

    $.getJSON('/api/photos', { limit: limit, offset: offset }, function (response) {
        const newPhotos = response.files;  // Get new photos
        if (newPhotos.length === 0) {
            $('#loading').text('No more images').fadeOut(2000);
            $(window).off('scroll', handleScroll);  // Turn off the scroll handler
            return;
        }

        totalPhotos = response.total
        let gallery = $('#gallery');
        newPhotos.forEach(photo => {
            // Add unique images only
            if (!photos.includes(photo)) {
                photos.push(photo);
                const card = `
                    <div class="col">
                        <div class="card">
                            <img src="/download/${photo}" alt="${photo}" data-bs-toggle="modal" 
                                 data-bs-target="#photoModal" data-index="${photos.length - 1}" loading="lazy">
                        </div>
                    </div>`;
                gallery.append(card);
            }
        });

        offset += limit;  // Increase an offset
        isLoading = false;  // Change the loading flag
        $('#loading').hide();
    }).fail(function () {
        $('#loading').text('Ошибка загрузки. Пожалуйста, попробуйте снова.').fadeOut(2000);
        isLoading = false;
    });
}

/**
 * Function to handle scrolling behavior.
 * Loads more photos when the user scrolls to the bottom of the page.
 */
function handleScroll() {
    const scrollTop = $(window).scrollTop();
    const windowHeight = $(window).height();
    const documentHeight = $(document).height();

    // If it's scrolled until the end, load new images
    if (scrollTop + windowHeight >= documentHeight - 100) {
        if (isLoading) return;
        loadPhotos();
    }
}

/**
 * Function to update the modal with the current photo and its counter.
 */
function updateModal() {
    if (currentIndex < 0 || currentIndex >= photos.length) {
        console.error("Invalid photo index");
        return;
    }
    const photo = photos[currentIndex];  // Get the current photo
    const src = `/download/${photo}`;  // Set the source for the photo
    $('#modalImage').attr('src', src);  // Update the modal image
    $('#photoCounter').text(`${currentIndex + 1} of ${totalPhotos}`);  // Update the photo counter
}

$(document).ready(function () {
    limit = calculateLimit();
    loadPhotos();  // Load the initial set of photos
    $(window).on('scroll', handleScroll);  // Listen for scroll events to load more photos

    // When a photo is clicked, show the modal with the clicked photo
    $('#gallery').on('click', 'img', function () {
        const index = $(this).data('index');
        if (index === undefined) {
            console.error("index not found for the clicked image");
            return;
        }
        currentIndex = index
        updateModal();  // Update the modal
        $('#photoModal').modal('show');  // Show the modal
    });

    // Switch to the previous photo in the modal
    $('#prevPhoto').click(function () {
        if (currentIndex > 0) {
            currentIndex--;
            updateModal();
        }
    });

    // Switch to the next photo in the modal
    $('#nextPhoto').click(function () {
        if (currentIndex < photos.length - 1) {
            currentIndex++;
            updateModal();
        } else if (!isLoading) {
            loadPhotos (() => {
                if (currentIndex < photos.length - 1) {
                    currentIndex++;
                    updateModal();
                }
            });
        }
    });

    // Download the current photo
    $('#downloadPhoto').click(function () {
        const photo = photos[currentIndex];  // Get the current photo
        const link = document.createElement('a');  // Create a link element
        link.href = `/download/${photo}`;  // Set the download URL
        link.download = photo;  // Set the download attribute to the photo's name
        link.click();  // Trigger the download
    });
});
